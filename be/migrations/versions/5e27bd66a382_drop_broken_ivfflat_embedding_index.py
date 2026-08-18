"""drop broken ivfflat embedding index

Revision ID: 5e27bd66a382
Revises: 77a6aaf62202
Create Date: 2026-08-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e27bd66a382'
down_revision: Union[str, Sequence[str], None] = '77a6aaf62202'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # idx_chunks_embedding (ivfflat, lists=100) was tuned for "tens of
    # thousands of rows" (see old schema.sql comment) but document_chunks
    # currently has ~170 rows total. With that few rows spread across 100
    # lists, many clusters are empty/near-empty, and ivfflat's default
    # probes=1 means a query vector landing in an empty cluster returns
    # ZERO rows even when the table clearly has a relevant chunk — silent,
    # wrong retrieval. Verified for real: 6/43 golden-dataset questions on
    # a single document (113 chunks) returned 0 rows via the index while a
    # forced sequential scan found the correct chunk every time. At this
    # table size, a plain sequential scan is both fast and exact (no ANN
    # approximation) — drop the index rather than retune it; revisit only
    # once the table is large enough (thousands+ rows per document) that
    # ANN search is actually justified.
    op.drop_index('idx_chunks_embedding', table_name='document_chunks')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "CREATE INDEX idx_chunks_embedding ON document_chunks "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )
