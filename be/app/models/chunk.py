import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Index, Text, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

EMBEDDING_DIM = 1536  # OpenAI text-embedding-3-small. New model? add embedding_v2, don't change this.


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        Index("idx_chunks_document", "document_id"),
        Index("idx_chunks_page", "page_id"),
        # KHÔNG có index ANN (ivfflat/HNSW) trên `embedding` — có chủ đích.
        # Từng có idx_chunks_embedding (ivfflat, lists=100) nhưng đã DROP ở
        # migration 5e27bd66a382: với bảng nhỏ (~170 dòng) thì 100 cụm là quá
        # nhiều, nhiều cụm rỗng, và probes=1 mặc định khiến truy vấn trả về 0
        # dòng cho ~14% câu hỏi thật dù dữ liệu vẫn ở đó. Sequential scan ở quy
        # mô này vừa nhanh vừa CHÍNH XÁC TUYỆT ĐỐI (không xấp xỉ). Nếu thêm lại
        # ở đây, `alembic revision --autogenerate` sẽ đề xuất tạo lại đúng cái
        # index đã gây lỗi. Xem explain-logic/phase-5.6-guardrails-observability/5.6.3.
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("document_pages.id", ondelete="CASCADE"), nullable=False)
    page_number: Mapped[int] = mapped_column(nullable=False)  # denormalized, avoids a join on the hot chat path

    chunk_index: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None]

    bbox: Mapped[dict | None] = mapped_column(JSONB)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
