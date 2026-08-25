import uuid
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentFileResponse, DocumentResponse, DocumentStatusResponse
from app.schemas.rag import FeedbackRequest
from app.services.document_service import (
    DocumentNotFoundError,
    DocumentNotReadyError,
    FileTooLargeError,
    UnsupportedFileTypeError,
    create_document,
    delete_document,
    ensure_document_ready,
    get_owned_document,
    get_thumbnail_key,
    get_viewable_pdf_key,
)
from app.services.storage_service import get_presigned_url
from app.services.usage_service import (
    FeedbackTargetNotFoundError,
    submit_feedback,
)
from app.workers.ingestion_worker import run_ingestion

router = APIRouter()


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    extraction_mode: Literal["pypdf", "mistral_ocr", "hybrid"] = Form("pypdf"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file_bytes = await file.read()
    try:
        document = await create_document(
            db,
            user_id=current_user.id,
            filename=file.filename,
            content_type=file.content_type,
            file_bytes=file_bytes,
            extraction_mode=extraction_mode,
        )
    except UnsupportedFileTypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "UNSUPPORTED_FILE_TYPE", "message": "Only PDF and PPTX files are supported"},
        )
    except FileTooLargeError:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail={"code": "FILE_TOO_LARGE", "message": "File exceeds the 50MB limit"},
        )

    background_tasks.add_task(run_ingestion, document.id)
    return document


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    documents = await db.scalars(
        select(Document).where(Document.user_id == current_user.id).order_by(Document.created_at.desc())
    )
    return documents.all()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_owned_document(db, document_id, current_user.id)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )


@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_document_status(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_owned_document(db, document_id, current_user.id)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )


@router.get("/{document_id}/file", response_model=DocumentFileResponse)
async def get_document_file(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        document = await get_owned_document(db, document_id, current_user.id)
        pdf_key = get_viewable_pdf_key(document)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )
    except DocumentNotReadyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DOCUMENT_NOT_READY", "message": "The PDF isn't ready yet — ingestion hasn't converted it"},
        )

    return DocumentFileResponse(url=get_presigned_url(pdf_key))


@router.get("/{document_id}/thumbnail", response_model=DocumentFileResponse)
async def get_document_thumbnail(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        document = await get_owned_document(db, document_id, current_user.id)
        ensure_document_ready(document)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )
    except DocumentNotReadyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "DOCUMENT_NOT_READY", "message": "The document isn't ready yet"},
        )

    return DocumentFileResponse(url=get_presigned_url(get_thumbnail_key(document)))


@router.post("/{document_id}/ask/{answer_id}/feedback", status_code=status.HTTP_204_NO_CONTENT)
async def submit_answer_feedback(
    document_id: uuid.UUID,
    answer_id: uuid.UUID,
    payload: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """5.6.12 — 👍/👎 + lý do tùy chọn cho 1 câu trả lời cụ thể (answer_id =
    ai_usage_log.id / MessageResponse.answer_id). Gửi lại cho cùng answer_id sẽ CẬP NHẬT ý kiến cũ,
    không tạo thêm bản ghi mới."""
    try:
        await submit_feedback(db, answer_id, current_user.id, is_positive=payload.is_positive, reason=payload.reason)
    except FeedbackTargetNotFoundError:
        # Cùng 404 dù answer_id không tồn tại hay thuộc user khác — không tiết
        # lộ sự khác biệt, tránh dò answer_id của người khác bằng thử-sai.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "ANSWER_NOT_FOUND", "message": "Answer not found"},
        )


@router.delete("/{document_id}")
async def delete_document_route(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_document(db, document_id, current_user.id)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DOCUMENT_NOT_FOUND", "message": "Document not found"},
        )
    return {}
