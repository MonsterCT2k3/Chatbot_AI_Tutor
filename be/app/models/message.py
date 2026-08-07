import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)

    role: Mapped[str] = mapped_column(nullable=False)  # 'user' | 'assistant'
    content: Mapped[str] = mapped_column(nullable=False)

    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))


class MessageCitation(Base):
    __tablename__ = "message_citations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=False)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="SET NULL"))

    page_number: Mapped[int] = mapped_column(nullable=False)
    snippet: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
