import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.services.storage_service import delete_file, upload_file

ALLOWED_CONTENT_TYPES = {
    "pdf": "application/pdf",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50MB


class UnsupportedFileTypeError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass


async def create_document(
    db: AsyncSession,
    user_id: uuid.UUID,
    filename: str,
    content_type: str | None,
    file_bytes: bytes,
    extraction_mode: str = "pypdf",
) -> Document:
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    expected_content_type = ALLOWED_CONTENT_TYPES.get(extension)
    if expected_content_type is None or content_type != expected_content_type:
        raise UnsupportedFileTypeError()

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError()

    # Generate the id up front so the storage key and DB row always agree on it.
    document_id = uuid.uuid4()
    storage_key = f"documents/{user_id}/{document_id}/original.{extension}"

    await upload_file(file_bytes, storage_key, content_type=content_type)

    document = Document(
        id=document_id,
        user_id=user_id,
        filename=filename,
        file_type=extension,
        file_size_bytes=len(file_bytes),
        storage_key=storage_key,
        status="pending",
        metadata_={"extraction_mode": extraction_mode},
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


async def get_owned_document(db: AsyncSession, document_id: uuid.UUID, user_id: uuid.UUID) -> Document:
    # Filtering by id AND user_id in one query means "doesn't exist" and "exists
    # but belongs to someone else" both raise the same error — the router turns
    # this into a single indistinguishable 404 for both cases.
    document = await db.scalar(select(Document).where(Document.id == document_id, Document.user_id == user_id))
    if document is None:
        raise DocumentNotFoundError()
    return document


async def delete_document(db: AsyncSession, document_id: uuid.UUID, user_id: uuid.UUID) -> None:
    document = await get_owned_document(db, document_id, user_id)
    await delete_file(document.storage_key)
    await db.delete(document)
    await db.commit()
