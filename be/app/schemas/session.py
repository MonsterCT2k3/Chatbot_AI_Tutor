import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# Giới hạn độ dài title. Cột trong DB là Text (không giới hạn) — chặn ở tầng
# schema để 1 title dài vô tội vạ không lọt xuống DB rồi phá vỡ giao diện
# sidebar. 200 ký tự thoải mái cho cả tên tự đặt lẫn tên auto-sinh từ câu hỏi
# đầu tiên (~60 ký tự, xem mục ⑨ phase 6).
TITLE_MAX_LENGTH = 200


class SessionCreate(BaseModel):
    # str_strip_whitespace: "   " -> "" -> rớt min_length, thay vì lọt vào DB
    # thành 1 title trắng nhìn như bị lỗi.
    model_config = ConfigDict(str_strip_whitespace=True)

    document_id: uuid.UUID
    # None = để DB tự điền server_default "New chat".
    #
    # Bước 6.2 KHÔNG cần xử lý gì đặc biệt cho trường hợp None: đã kiểm chứng
    # bằng log SQL thật rằng SQLAlchemy tự BỎ HẲN cột ra khỏi câu INSERT khi
    # giá trị là None mà cột có server_default —
    #     INSERT INTO chat_sessions (user_id, document_id) VALUES ($1, $2)
    # — nên server_default áp dụng bình thường, không hề vi phạm NOT NULL.
    # Cứ truyền thẳng `title=payload.title` là đúng.
    title: str | None = Field(default=None, min_length=1, max_length=TITLE_MAX_LENGTH)


class SessionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # Bắt buộc, không phải optional: hiện chỉ có đúng 1 trường sửa được, nên
    # PATCH mà không truyền gì là request vô nghĩa — để required thì lỗi hiện
    # ra ngay ở 422 thay vì âm thầm không đổi gì.
    title: str = Field(min_length=1, max_length=TITLE_MAX_LENGTH)


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    # KHÔNG trả user_id: người gọi CHÍNH LÀ chủ session (mọi endpoint đều lọc
    # theo user_id, xem mục ① phase 6), nên trường này không thêm thông tin gì
    # mà lại lộ 1 id nội bộ ra ngoài. Giống DocumentResponse cũng không trả.
    document_id: uuid.UUID
    title: str
    created_at: datetime
    # Được "chạm" mỗi khi có tin nhắn mới (mục ④ phase 6) — đây là khoá sắp xếp
    # của GET /api/sessions, không phải chỉ là dấu thời gian trang trí.
    updated_at: datetime
