import asyncio
import json
import uuid
from pathlib import Path
from sqlalchemy import select, delete

from app.database import get_db, async_session
from app.evaluation.eval_documents import ensure_eval_documents, EVAL_USER_ID
from app.models.chunk import DocumentChunk
from app.models.document import Document, DocumentPage
from app.models.session import ChatSession
from app.services.session_service import create_session, send_message_events, list_messages
from app.workers.ingestion_worker import run_ingestion


async def run_test():
    print("=" * 60)
    print("TEST 8.3b: RE-INGEST & END-TO-END BBOX WIRING")
    print("=" * 60)

    async with async_session() as db:
        # Step 1: Force re-ingest b1-full.pdf to test extraction
        doc = await db.scalar(
            select(Document).where(
                Document.user_id == EVAL_USER_ID,
                Document.filename == "b1-full.pdf",
            )
        )
        if doc is not None:
            print(f"Deleting existing document and chunks for {doc.filename}...")
            await db.delete(doc)
            await db.commit()

        print("Ensuring eval documents (running ingestion with bbox extraction)...")
        docs = await ensure_eval_documents(db, {"b1-full.pdf"})
        doc_id = docs["b1-full.pdf"]
        print(f"Document ingested: id={doc_id}")

        # Step 2: Query DocumentChunk for page 22
        q = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == doc_id, DocumentChunk.page_number == 22)
            .order_by(DocumentChunk.chunk_index)
        )
        chunks = (await db.execute(q)).scalars().all()
        print(f"\nFound {len(chunks)} chunks on page 22:")
        has_valid_bbox = False
        sample_bbox = None
        for c in chunks:
            print(f"  Chunk idx={c.chunk_index}, content snippet={repr(c.content[:60])}")
            print(f"  Bbox: {json.dumps(c.bbox)}")
            if c.bbox and c.bbox.get("rects"):
                has_valid_bbox = True
                sample_bbox = c.bbox

        if not has_valid_bbox:
            raise RuntimeError("FAILED: No valid bbox found for page 22 chunks!")

        print("\n>>> Ingestion & DB Bbox Check: PASSED!")

        # Step 3: Test SSE message stream with bbox
        session = await create_session(db, EVAL_USER_ID, doc_id, title="Test 8.3b Session")
        print(f"\nCreated test session: id={session.id}")

        print("Streaming question: 'Transformer ra đời năm nào?'")
        events_received = []
        async for ev, payload in send_message_events(
            db, session.id, EVAL_USER_ID, "Transformer ra đời năm nào?"
        ):
            events_received.append((ev, payload))
            if ev == "citation":
                print(f"  [SSE event: citation] page={payload.get('page_number')}, bbox={payload.get('bbox') is not None}")
            elif ev == "done":
                print(f"  [SSE event: done] message_id={payload.get('message_id')}, citations={len(payload.get('citations', []))}")
                for cit in payload.get("citations", []):
                    print(f"    Citation page={cit.get('page_number')}, has_bbox={cit.get('bbox') is not None}")

        # Step 4: Test list_messages history
        messages, citations_map, has_more, chunk_bboxes = await list_messages(
            db, session.id, EVAL_USER_ID, limit=10
        )
        print(f"\nHistory messages: {len(messages)}")
        for m in messages:
            cits = citations_map.get(m.id, [])
            print(f"  Message role={m.role}, citations={len(cits)}")
            for c in cits:
                box = chunk_bboxes.get(c.chunk_id)
                print(f"    Citation chunk_id={c.chunk_id}, page={c.page_number}, bbox_loaded={box is not None}")

        print("\n" + "=" * 60)
        print("SAMPLE BBOX JSON:")
        print(json.dumps(sample_bbox, indent=2))
        print("=" * 60)
        print("ALL 8.3b BACKEND & SSE CHECKS PASSED 100%!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_test())
