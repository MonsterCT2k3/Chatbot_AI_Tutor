"""One-off: generate thumbnails for documents that were ingested before
render_first_page_thumbnail existed in the pipeline (ingestion only runs
once, at upload time -- it never re-runs for already-'ready' documents,
so anything uploaded before this feature landed has no thumbnail.png on
R2 and will keep showing the fallback file-type icon on the dashboard).

Safe to re-run -- re-renders and overwrites thumbnail.png for every
'ready' document each time.

Run: python -m scripts.backfill_thumbnails
"""

import asyncio

from sqlalchemy import select

from app.database import async_session
from app.models.document import Document
from app.services.document_service import get_thumbnail_key, get_viewable_pdf_key
from app.services.ingestion_service import render_first_page_thumbnail
from app.services.storage_service import download_file, upload_file


async def main() -> None:
    async with async_session() as db:
        result = await db.execute(select(Document).where(Document.status == "ready"))
        documents = result.scalars().all()

    print(f"{len(documents)} ready document(s) to backfill")
    for document in documents:
        try:
            pdf_bytes = await download_file(get_viewable_pdf_key(document))
            thumbnail_bytes = render_first_page_thumbnail(pdf_bytes)
            await upload_file(thumbnail_bytes, get_thumbnail_key(document), content_type="image/png")
            print(f"  OK   {document.filename} ({document.id})")
        except Exception as e:
            print(f"  FAIL {document.filename} ({document.id}): {e}")


if __name__ == "__main__":
    asyncio.run(main())
