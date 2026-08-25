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
    # Đặt tên `question` (không phải `content`) để khớp với trường câu hỏi đầu vào
    # của người dùng.
    question: str = Field(min_length=1)


class MessageCitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    page_number: int
    # Bảng message_citations cho phép NULL ở 2 cột này —
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
    bbox: dict | None = None


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
    def from_model(
        cls, message, citations=(), chunk_bboxes: dict[uuid.UUID, dict | None] | None = None
    ) -> "MessageResponse":
        """Dựng response từ ChatMessage + các MessageCitation của nó."""
        raw = (message.metadata_ or {}).get(ANSWER_ID_METADATA_KEY)
        citation_models: list[MessageCitationResponse] = []
        for c in citations:
            bbox = None
            if chunk_bboxes and getattr(c, "chunk_id", None):
                bbox = chunk_bboxes.get(c.chunk_id)
            elif hasattr(c, "bbox"):
                bbox = getattr(c, "bbox", None)

            citation_models.append(
                MessageCitationResponse(
                    page_number=c.page_number,
                    chunk_id=c.chunk_id,
                    snippet=c.snippet,
                    bbox=bbox,
                )
            )

        return cls(
            id=message.id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            answer_id=uuid.UUID(raw) if isinstance(raw, str) else raw,
            citations=citation_models,
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
