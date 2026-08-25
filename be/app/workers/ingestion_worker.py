import logging
import uuid

from app.database import async_session
from app.models.chunk import DocumentChunk
from app.models.document import Document, DocumentPage
from app.services.document_service import get_thumbnail_key
from app.services.ingestion_service import (
    chunk_text,
    convert_pptx_to_pdf,
    embed_chunks,
    extract_chunk_bboxes,
    extract_text_hybrid,
    extract_text_mistral_ocr,
    extract_text_pypdf,
    render_first_page_thumbnail,
)
from app.services.storage_service import download_file, get_presigned_url, upload_file

logger = logging.getLogger(__name__)


async def run_ingestion(document_id: uuid.UUID) -> None:
    async with async_session() as db:
        document = await db.get(Document, document_id)
        if document is None:
            return

        try:
            document.status = "parsing"
            await db.commit()

            file_bytes = await download_file(document.storage_key)

            if document.file_type == "pptx":
                pdf_bytes = await convert_pptx_to_pdf(file_bytes)
                converted_key = f"documents/{document.user_id}/{document.id}/converted.pdf"
                await upload_file(pdf_bytes, converted_key, content_type="application/pdf")
                document.converted_pdf_key = converted_key
                await db.commit()
            else:
                pdf_bytes = file_bytes

            try:
                thumbnail_bytes = render_first_page_thumbnail(pdf_bytes)
                await upload_file(thumbnail_bytes, get_thumbnail_key(document), content_type="image/png")
            except Exception:
                # Thumbnail is a nice-to-have for the dashboard card, not required
                # for the document to be usable — never fail ingestion over it.
                logger.exception("Failed to render thumbnail for document %s", document.id)

            extraction_mode = document.metadata_.get("extraction_mode", "pypdf")

            if extraction_mode == "pypdf":
                pages = extract_text_pypdf(pdf_bytes)
            elif extraction_mode in ("mistral_ocr", "hybrid"):
                pdf_key = document.converted_pdf_key or document.storage_key
                document_url = get_presigned_url(pdf_key)
                if extraction_mode == "mistral_ocr":
                    pages = await extract_text_mistral_ocr(document_url)
                else:
                    pages = await extract_text_hybrid(pdf_bytes, document_url)
            else:
                raise ValueError(f"Unknown extraction_mode: {extraction_mode!r}")

            page_id_by_number: dict[int, uuid.UUID] = {}
            for page_number, text in pages:
                page = DocumentPage(document_id=document.id, page_number=page_number, raw_text=text)
                db.add(page)
                await db.flush()
                page_id_by_number[page_number] = page.id
            await db.commit()

            document.status = "embedding"
            await db.commit()

            chunk_rows: list[tuple[int, int, str]] = []
            for page_number, text in pages:
                for chunk_index, content in enumerate(chunk_text(text)):
                    chunk_rows.append((page_number, chunk_index, content))

            if chunk_rows:
                vectors = await embed_chunks([content for _, _, content in chunk_rows])
                try:
                    bboxes = extract_chunk_bboxes(pdf_bytes, chunk_rows)
                except Exception:
                    logger.exception("Failed to extract chunk bboxes for document %s", document.id)
                    bboxes = [None] * len(chunk_rows)

                for (page_number, chunk_index, content), vector, bbox in zip(chunk_rows, vectors, bboxes):
                    db.add(
                        DocumentChunk(
                            document_id=document.id,
                            page_id=page_id_by_number[page_number],
                            page_number=page_number,
                            chunk_index=chunk_index,
                            content=content,
                            embedding=vector,
                            bbox=bbox,
                        )
                    )
            await db.commit()

            document.status = "ready"
            document.page_count = len(pages)
            await db.commit()

        except Exception as e:
            await db.rollback()
            document = await db.get(Document, document_id)
            document.status = "failed"
            document.error_message = str(e)[:2000]
            await db.commit()
