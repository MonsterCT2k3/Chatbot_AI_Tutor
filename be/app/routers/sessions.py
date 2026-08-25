import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageListResponse, MessageResponse
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate
from app.services.document_service import DocumentNotFoundError, DocumentNotReadyError
from app.services.session_service import (
    SessionNotFoundError,
    create_session,
    delete_session,
    get_owned_session,
    list_messages,
    list_sessions,
    rename_session,
    send_message,
)
from app.services.usage_service import CircuitBreakerOpenError, QuotaExceededError

router = APIRouter()

# Cùng 1 phản hồi 404 cho MỌI trường hợp không truy cập được — dù session
# không tồn tại hay là của người khác. Xem get_owned_session để biết vì sao
# không được phân biệt 2 trường hợp này.
_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"code": "SESSION_NOT_FOUND", "message": "Session not found"},
)


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    payload: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_session(db, current_user.id, payload.document_id, payload.title)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )


@router.get("", response_model=list[SessionResponse])
async def list_chat_sessions(
    document_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await list_sessions(db, current_user.id, document_id)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_chat_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_owned_session(db, session_id, current_user.id)
    except SessionNotFoundError:
        raise _NOT_FOUND


@router.patch("/{session_id}", response_model=SessionResponse)
async def rename_chat_session(
    session_id: uuid.UUID,
    payload: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await rename_session(db, session_id, current_user.id, payload.title)
    except SessionNotFoundError:
        raise _NOT_FOUND


@router.post("/{session_id}/messages", response_model=MessageResponse)
async def post_chat_message(
    session_id: uuid.UUID,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        message, citations = await send_message(db, session_id, current_user.id, payload.question)
    except SessionNotFoundError:
        raise _NOT_FOUND
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )
    except DocumentNotReadyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DOCUMENT_NOT_READY", "message": "The document isn't fully ingested yet"},
        )
    except QuotaExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"code": "QUOTA_EXCEEDED", "message": str(e)},
        )
    except CircuitBreakerOpenError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "CIRCUIT_BREAKER_OPEN", "message": str(e)},
        )

    return MessageResponse.from_model(message, citations)


@router.get("/{session_id}/messages", response_model=MessageListResponse)
async def list_chat_messages(
    session_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    # Khai kiểu datetime để FastAPI tự phân tích ISO-8601 và tự trả 422 với
    # giá trị rác — không cần tự viết parser, và không có đường nào để một
    # cursor hỏng lọt xuống tầng truy vấn.
    before: datetime | None = Query(None, description="Cursor: lấy các tin nhắn CŨ HƠN mốc này"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        messages, citations, has_more = await list_messages(
            db, session_id, current_user.id, limit=limit, before=before
        )
    except SessionNotFoundError:
        raise _NOT_FOUND

    # Chỉ trả cursor khi THẬT SỰ còn trang cũ hơn. Trả vô điều kiện sẽ khiến
    # client bấm "xem thêm" rồi nhận về 1 trang rỗng.
    # messages đã TĂNG dần, nên phần tử [0] là cũ nhất trang này.
    #
    # Dùng hậu tố "Z" thay vì "+00:00": trong query string, dấu "+" mang nghĩa
    # DẤU CÁCH, nên cursor dạng "...+00:00" nối thẳng vào URL sẽ tới server
    # thành "... 00:00" và hỏng. Client đúng ra phải URL-encode, nhưng cursor
    # vốn là token client trả lại NGUYÊN XI — phát ra một giá trị vỡ khi dùng
    # theo cách tự nhiên nhất là tự đặt bẫy. "Z" là ISO-8601 hợp lệ và an toàn
    # với URL mà không cần encode. (Phát hiện khi test: trang thứ 2 trả 422.)
    next_cursor = None
    if has_more and messages:
        oldest = messages[0].created_at.astimezone(timezone.utc)
        next_cursor = oldest.isoformat().replace("+00:00", "Z")

    return MessageListResponse(
        messages=[MessageResponse.from_model(m, citations.get(m.id, ())) for m in messages],
        next_cursor=next_cursor,
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_session(db, session_id, current_user.id)
    except SessionNotFoundError:
        raise _NOT_FOUND
