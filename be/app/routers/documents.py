import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    DocumentNotFoundError,
    FileTooLargeError,
    UnsupportedFileTypeError,
    create_document,
    delete_document,
    get_owned_document,
)

router = APIRouter()


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile,
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


# GET    /{id}/status      polling / SSE push
# GET    /{id}/pages/{n}   rendered page/slide image (presigned R2 URL)
