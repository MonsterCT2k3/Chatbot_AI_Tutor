import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small. New model? add embedding_v2, don't change this.


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("document_pages.id", ondelete="CASCADE"), nullable=False)
    page_number: Mapped[int] = mapped_column(nullable=False)  # denormalized, avoids a join on the hot chat path

    chunk_index: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    token_count: Mapped[int | None]

    bbox: Mapped[dict | None] = mapped_column(JSONB)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))

    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
