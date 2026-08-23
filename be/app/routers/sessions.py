import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate
from app.services.document_service import DocumentNotFoundError
from app.services.session_service import (
    SessionNotFoundError,
    create_session,
    delete_session,
    get_owned_session,
    list_sessions,
    rename_session,
)

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
