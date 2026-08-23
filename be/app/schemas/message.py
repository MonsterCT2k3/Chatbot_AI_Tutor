import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Khoá trong ChatMessage.metadata (cột JSONB) lưu id của dòng ai_usage_log đã
# sinh ra câu trả lời này — xem mục ⑦ phase 6.
#
# Vì sao phải lưu: 👍/👎 gắn vào ai_usage_log.id (answer_feedback có FK CỨNG
# tới đó, và ai_usage_log mới là nơi nối với dữ liệu chi phí/chất lượng), chứ
# không gắn vào chat_messages.id. Nếu không lưu lại, thì sau khi tải lại lịch
# sử, client không còn cách nào biết phải gửi feedback cho id nào — người dùng
# chỉ đánh giá được câu trả lời vừa nhận trong phiên hiện tại, mở lại là mất.
#
# Đặt thành hằng số thay vì viết chuỗi trực tiếp ở 2 nơi (bên GHI ở 6.5 và bên
# ĐỌC ở 6.3) — gõ lệch 1 ký tự giữa 2 chỗ sẽ không có lỗi nào báo ra, chỉ là
# answer_id lặng lẽ luôn bằng None.
ANSWER_ID_METADATA_KEY = "ai_usage_log_id"


class MessageCreate(BaseModel):
    # Đặt tên `question` (không phải `content`) để KHỚP với AskRequest của
    # endpoint /api/documents/{id}/ask đang chạy — trong lúc 2 endpoint còn
    # sống song song (mục ⑧ phase 6), frontend chuyển sang endpoint mới mà
    # không phải đổi hình dạng body.
    #
    # Chưa đặt max_length, cũng để khớp AskRequest. Giới hạn độ dài câu hỏi là
    # việc nên làm ở CẢ HAI endpoint cùng lúc (Phase 10 — hardening), đặt lệch
    # nhau giữa 2 endpoint làm cùng 1 việc sẽ khó hiểu hơn là không đặt.
    question: str = Field(min_length=1)


class MessageCitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    page_number: int
    # KHÁC CitationResponse của /ask (ở đó cả 2 trường đều bắt buộc): bảng
    # message_citations cho phép NULL ở 2 cột này —
    #   - chunk_id: FK tới document_chunks với ondelete=SET NULL, nên nếu sau
    #     này có tính năng ingest lại tài liệu (xoá chunk cũ, tạo chunk mới),
    #     trích dẫn cũ vẫn còn nhưng mất con trỏ tới chunk.
    #   - snippet: nullable trong schema gốc.
    # Khai đúng theo DB thay vì bắt buộc, để 1 dòng dữ liệu hợp lệ không làm
    # nổ lỗi validation lúc đọc lịch sử.
    #
    # LƯU Ý cho phần frontend sau này: ChatPanel.jsx đang dùng `c.chunk_id` làm
    # React key và `c.snippet` làm tooltip — cả hai giờ có thể null khi đọc
    # lịch sử cũ, cần xử lý (dùng index làm key, tooltip có fallback).
    chunk_id: uuid.UUID | None = None
    snippet: str | None = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime

    # Chỉ có ở tin nhắn role="assistant", và chỉ khi đọc được từ metadata.
    # None với tin nhắn của người dùng, và với các câu trả lời được lưu trước
    # khi có cơ chế này -> client phải coi "không có answer_id" là bình thường
    # (ẩn nút 👍/👎) chứ không phải lỗi.
    answer_id: uuid.UUID | None = None
    citations: list[MessageCitationResponse] = Field(default_factory=list)

    @classmethod
    def from_model(cls, message, citations=()) -> "MessageResponse":
        """Dựng response từ ChatMessage + các MessageCitation của nó.

        Có hàm này để việc "answer_id nằm ở đâu trong metadata" chỉ được biết
        tại ĐÚNG 1 chỗ. Nếu để mỗi nơi tự đọc metadata thì hàm đọc (6.3) và
        hàm ghi (6.5) rất dễ trôi lệch nhau theo thời gian mà không có test
        nào bắt được.
        """
        raw = (message.metadata_ or {}).get(ANSWER_ID_METADATA_KEY)
        return cls(
            id=message.id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            answer_id=uuid.UUID(raw) if isinstance(raw, str) else raw,
            citations=[MessageCitationResponse.model_validate(c) for c in citations],
        )


class MessageListResponse(BaseModel):
    # Sắp xếp TĂNG DẦN theo created_at (cũ -> mới), tức đúng thứ tự cần hiển
    # thị. Truy vấn thì lại phải lấy GIẢM DẦN (mới nhất trước) để phân trang
    # lùi về quá khứ, nên bước 6.3 phải đảo lại danh sách trước khi trả về —
    # ghi rõ ở đây để 2 bên không hiểu khác nhau.
    messages: list[MessageResponse]

    # Con trỏ để lấy tiếp các tin nhắn CŨ HƠN (truyền lại qua ?before=).
    # None = đã tới đầu cuộc hội thoại, không còn gì cũ hơn.
    #
    # Giá trị là created_at (ISO-8601) của tin nhắn CŨ NHẤT trong trang này.
    # Cách này chỉ đúng khi created_at trong 1 session là DUY NHẤT và tăng dần
    # — đảm bảo bởi quy tắc ở mục ③ phase 6: commit tin nhắn người dùng TRƯỚC
    # khi gọi LLM, vì now() của Postgres đứng yên trong suốt 1 transaction nên
    # lưu cả cặp hỏi-đáp trong cùng transaction sẽ ra 2 mốc thời gian y hệt
    # nhau. Ai đó phá vỡ quy tắc đó thì phân trang sẽ nhảy/lặp tin nhắn.
    next_cursor: str | None = None
