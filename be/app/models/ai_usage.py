import uuid
from datetime import datetime

from sqlalchemy import Boolean, Float, ForeignKey, Index, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AIUsageLog(Base):
    # Một dòng cho MỖI lượt gọi ask() — kể cả lượt bị guardrail chặn.
    #
    # Vì sao không đếm từ chat_messages: bảng đó gắn với chat_sessions (Phase 6,
    # chưa làm) và chỉ lưu hội thoại thành công — trong khi quota phải tính cả
    # những lượt bị chặn (nếu không, spam nội dung độc hại sẽ không tốn quota
    # nào của kẻ tấn công, dù mỗi lượt vẫn tốn tiền moderation/embedding thật).
    #
    # Vì sao lưu từng dòng thay vì 1 bộ đếm gộp theo ngày: 5.6.8 (circuit
    # breaker) cần biết mật độ request trong vài phút, không chỉ tổng cả ngày —
    # bộ đếm gộp sẽ không dựng lại được thông tin đó.
    __tablename__ = "ai_usage_log"
    __table_args__ = (
        # Đúng hình dạng truy vấn của 5.6.6 ("user X đã hỏi bao nhiêu lượt kể từ
        # đầu ngày") và 5.6.8 ("... trong 5 phút gần nhất") — cùng 1 index phục
        # vụ được cả 2 vì chỉ khác mốc thời gian.
        Index("idx_ai_usage_user_time", "user_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Nullable: giữ được dòng log kể cả sau khi người dùng xoá tài liệu (quota
    # đã tiêu thì không "hoàn lại" được), và ondelete=SET NULL thay vì CASCADE
    # để việc xoá tài liệu không làm mất lịch sử sử dụng.
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )

    # Kết quả của lượt gọi — đủ để trả lời "guardrail nào đang chặn nhiều nhất"
    # mà không cần lưu lại nội dung câu hỏi/câu trả lời (tránh lưu dữ liệu nhạy
    # cảm của người dùng khi chưa thực sự cần).
    blocked_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    grounded: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    faithfulness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    retried: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # 5.6.7 — tổng token (generation + judge, cả retry nếu có) và chi phí ƯỚC
    # TÍNH (USD) của riêng lượt gọi này. server_default='0' để migration thêm
    # cột không NULL trên dữ liệu cũ đã có (nếu bảng đã có dòng trước đó).
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    estimated_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class AICallLog(Base):
    # 5.6.9 — 1 dòng cho MỖI lệnh gọi LLM/moderation THẬT (không phải mỗi lượt
    # ask()) — khác hẳn AIUsageLog (1 dòng GỘP cho cả lượt, không có prompt/
    # response/latency). 1 câu hỏi có retry sẽ tạo ra 4 dòng ở đây (generation,
    # judge, generation lần 2, judge lần 2) nhưng chỉ 1 dòng ở ai_usage_log.
    #
    # Vì sao KHÔNG FK cứng về ai_usage_log: các dòng ở đây được ghi NGAY LÚC
    # từng lệnh gọi API xảy ra, TRƯỚC KHI ask() chạy xong và ask_for_user() tạo
    # ra dòng ai_usage_log tương ứng (dòng cha được tạo SAU, không phải trước)
    # — 1 FK constraint thật sẽ báo lỗi vì cha chưa tồn tại lúc con được insert.
    # Thay vào đó dùng call_group_id (UUID sinh ra ở đầu mỗi lần gọi ask(), và
    # được ask_for_user() TÁI SỬ DỤNG làm chính id của dòng ai_usage_log) làm
    # khoá liên kết MỀM — join được bằng application code khi cần, không ép
    # buộc toàn vẹn tham chiếu (referential integrity) ở tầng DB.
    __tablename__ = "ai_call_log"
    __table_args__ = (
        Index("idx_ai_call_group", "call_group_id"),
        Index("idx_ai_call_created", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    call_group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    # 'generation' | 'judge' | 'input_moderation' | 'output_moderation'
    call_type: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Nội dung THẬT — cắt bớt nếu quá dài (xem MAX_LOGGED_TEXT_LENGTH trong
    # usage_service.py) để tránh 1 context RAG dài (hàng nghìn ký tự) nhân bản
    # vào mọi dòng log của mọi câu hỏi, làm phình bảng vô ích cho mục đích debug.
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)

    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    estimated_cost_usd: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class AnswerFeedback(Base):
    # 5.6.12 — 👍/👎 + lý do tùy chọn, gắn vào ĐÚNG 1 câu trả lời cụ thể qua
    # ai_usage_log_id. Khác AICallLog: đây LÀ FK CỨNG thật — feedback chỉ có
    # thể được gửi SAU KHI người dùng đã nhận câu trả lời, tức dòng ai_usage_log
    # cha CHẮC CHẮN đã tồn tại từ trước (không có vấn đề "con ghi trước cha"
    # như AICallLog gặp phải trong lúc ask() còn đang chạy).
    __tablename__ = "answer_feedback"
    __table_args__ = (
        # 1 user chỉ có 1 ý kiến hiện tại cho 1 câu trả lời — gửi lại (đổi ý)
        # thì UPDATE tại chỗ, không cộng dồn thành nhiều dòng lịch sử (xem
        # usage_service.submit_feedback) — tránh đếm nhân đôi khi gộp thống kê.
        UniqueConstraint("ai_usage_log_id", "user_id", name="uq_answer_feedback_log_user"),
        Index("idx_answer_feedback_log", "ai_usage_log_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    ai_usage_log_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ai_usage_log.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    is_positive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
