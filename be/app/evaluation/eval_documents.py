import uuid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.services.document_service import create_document
from app.workers.ingestion_worker import run_ingestion

# Fixed dev/eval user (nam@gmail.com), reused across ad-hoc testing throughout
# this project — evaluation runs need a stable owner so documents can be
# ingested once and reused across every Phase 5.5 sub-step, instead of
# re-uploading on every run.
EVAL_USER_ID = uuid.UUID("f693e621-9dc5-4b1e-b117-fa024ab93619")

SLIDE_TEST_DIR = Path(__file__).resolve().parent.parent / "data" / "slide-test"


async def ensure_eval_documents(db: AsyncSession, only_filenames: set[str] | None = None) -> dict[str, uuid.UUID]:
    """Ingest app/data/slide-test/*.pdf under EVAL_USER_ID if not already ready,
    and return {filename: document_id}. Idempotent — safe to call before every
    evaluation run. Pass `only_filenames` to skip ingesting documents that
    aren't even part of the current run (e.g. when testing one file only)."""
    filenames = sorted(p.name for p in SLIDE_TEST_DIR.glob("*.pdf"))
    if only_filenames is not None:
        filenames = [f for f in filenames if f in only_filenames]
    document_ids: dict[str, uuid.UUID] = {}

    for filename in filenames:
        existing = await db.scalar(
            select(Document).where(
                Document.user_id == EVAL_USER_ID,
                Document.filename == filename,
                Document.status == "ready",
            )
        )
        if existing is not None:
            document_ids[filename] = existing.id
            continue

        file_bytes = (SLIDE_TEST_DIR / filename).read_bytes()
        document = await create_document(
            db, EVAL_USER_ID, filename, "application/pdf", file_bytes, extraction_mode="pypdf"
        )
        await run_ingestion(document.id)
        await db.refresh(document)
        if document.status != "ready":
            raise RuntimeError(f"ingestion failed for {filename}: {document.error_message}")
        document_ids[filename] = document.id

    return document_ids
