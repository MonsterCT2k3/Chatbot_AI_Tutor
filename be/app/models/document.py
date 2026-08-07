import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    filename: Mapped[str] = mapped_column(nullable=False)
    file_type: Mapped[str] = mapped_column(nullable=False)  # 'pdf' | 'pptx'
    file_size_bytes: Mapped[int | None]

    storage_key: Mapped[str] = mapped_column(nullable=False)
    thumbnail_key: Mapped[str | None]

    page_count: Mapped[int | None]

    # pending -> parsing -> embedding -> ready | failed
    status: Mapped[str] = mapped_column(nullable=False, server_default="pending")
    error_message: Mapped[str | None]

    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("now()"))


class DocumentPage(Base):
    __tablename__ = "document_pages"
    __table_args__ = (UniqueConstraint("document_id", "page_number"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)

    page_number: Mapped[int] = mapped_column(nullable=False)
    raw_text: Mapped[str | None]
    thumbnail_key: Mapped[str | None]

    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default="{}")
