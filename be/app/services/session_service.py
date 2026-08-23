import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import ChatSession
from app.services.document_service import DocumentNotFoundError, get_owned_document


class SessionNotFoundError(Exception):
    pass


async def get_owned_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> ChatSession:
    # Lọc theo id VÀ user_id trong CÙNG 1 query — bản sao chính xác của
    # document_service.get_owned_document. Nhờ vậy "session không tồn tại" và
    # "session của người khác" cùng ném 1 lỗi, router biến cả hai thành CÙNG
    # một 404: kẻ tấn công không thể dò xem session_id nào có thật bằng cách
    # thử hàng loạt UUID rồi so sánh mã lỗi trả về.
    session = await db.scalar(
        select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user_id)
    )
    if session is None:
        raise SessionNotFoundError()
    return session


async def create_session(
    db: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID, title: str | None = None
) -> ChatSession:
    # Phải kiểm tra tài liệu có thuộc về CHÍNH user này không, không chỉ là
    # "tài liệu có tồn tại không". Bỏ bước này thì user A tạo được session trỏ
    # vào tài liệu của user B, rồi chat với nội dung tài liệu đó — lỗ hổng đọc
    # trộm dữ liệu, dù mọi endpoint session phía sau đều kiểm tra quyền đúng.
    # Ném thẳng DocumentNotFoundError để router trả 404 giống hệt trường hợp
    # tài liệu không tồn tại (cùng lý do chống dò như trên).
    await get_owned_document(db, document_id, user_id)

    # title=None: SQLAlchemy tự bỏ cột khỏi INSERT vì cột có server_default
    # -> DB điền "New chat". Đã kiểm chứng bằng log SQL ở 6.1.
    session = ChatSession(user_id=user_id, document_id=document_id, title=title)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def list_sessions(
    db: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID | None = None
) -> list[ChatSession]:
    # Sắp theo updated_at: session vừa có tin nhắn mới phải nổi lên đầu. Điều
    # này CHỈ đúng nếu 6.5 chủ động "chạm" vào dòng session mỗi khi lưu tin
    # nhắn (mục ④ kế hoạch) — thêm dòng vào chat_messages KHÔNG tự làm
    # updated_at đổi, dù DB có trigger, vì trigger chỉ bắn khi chính dòng
    # session bị UPDATE.
    query = select(ChatSession).where(ChatSession.user_id == user_id)
    if document_id is not None:
        query = query.where(ChatSession.document_id == document_id)
    result = await db.scalars(query.order_by(ChatSession.updated_at.desc()))
    return list(result.all())


async def rename_session(
    db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID, title: str
) -> ChatSession:
    session = await get_owned_session(db, session_id, user_id)
    session.title = title
    await db.commit()
    await db.refresh(session)
    return session


async def delete_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> None:
    # Không cần tự xoá chat_messages/message_citations: FK của chúng đều là
    # ON DELETE CASCADE (đã kiểm chứng trên DB thật ở 6.1), Postgres tự dọn.
    session = await get_owned_session(db, session_id, user_id)
    await db.delete(session)
    await db.commit()
