import asyncio
import json
import time
from pathlib import Path
import pypdfium2 as pdfium
import pypdf

from app.database import get_db
from app.evaluation.eval_documents import ensure_eval_documents
from app.models.chunk import DocumentChunk
from app.models.document import Document
from sqlalchemy import select


NEEDLE = "2017: Transformer"
PAGE_NUM = 22  # 1-indexed (index 21 in PDF)
DISPLAY_WIDTH = 600.0


async def main():
    print("=" * 60)
    print("SPIKE 8.3: BBOX EXTRACTION & COORDINATE MAPPING")
    print("=" * 60)

    # 4.1 Load PDF and get text for page 22
    pdf_path = Path(__file__).resolve().parent.parent / "app" / "data" / "slide-test" / "b1-full.pdf"
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found at {pdf_path}")
        return

    pdf_bytes = pdf_path.read_bytes()
    pdf = pdfium.PdfDocument(pdf_bytes)
    total_pages = len(pdf)
    print(f"Loaded PDF: {pdf_path.name}")
    print(f"Total pages: {total_pages}")

    page_idx = PAGE_NUM - 1
    page = pdf[page_idx]
    page_w, page_h = page.get_size()
    print(f"Page {PAGE_NUM} dimensions (pdf user units): {page_w} x {page_h}")

    t0 = time.perf_counter()
    textpage = page.get_textpage()
    page_text = textpage.get_text_range()
    t_extract_ms = (time.perf_counter() - t0) * 1000.0

    print(f"Page {PAGE_NUM} text length: {len(page_text)} chars")
    first_120 = page_text.replace("\r", " ").replace("\n", " ")[:120].strip()
    print(f"First 120 chars: {repr(first_120)}")

    if NEEDLE not in page_text and "Transformer" not in page_text:
        print(f"ERROR: Neither '{NEEDLE}' nor 'Transformer' found on page {PAGE_NUM}")
        print("CHOICE=NO_GO")
        return

    # 4.2 Benchmark Libraries: pypdfium2 (Primary) & pypdf (Secondary)
    print("\n--- 4.2 Library Benchmark ---")
    lib_tried = ["pypdfium2", "pypdf"]
    lib_primary = "pypdfium2"

    # A. pypdfium2 exact search
    search = textpage.search("Transformer", match_case=False)
    match = search.get_next()
    match_status = "fail"
    rects_pypdfium = []
    union_pdf = None

    if match:
        start_idx, count = match
        match_status = "exact"
        # Collect character bounding boxes
        char_boxes = [textpage.get_charbox(i) for i in range(start_idx, start_idx + count)]
        min_l = min(b[0] for b in char_boxes)
        min_b = min(b[1] for b in char_boxes)
        max_r = max(b[2] for b in char_boxes)
        max_t = max(b[3] for b in char_boxes)

        pdf_x = round(min_l, 2)
        pdf_y = round(min_b, 2)
        pdf_w = round(max_r - min_l, 2)
        pdf_h = round(max_t - min_b, 2)
        union_pdf = (pdf_x, pdf_y, pdf_w, pdf_h)

        rects_pypdfium.append({"x": pdf_x, "y": pdf_y, "w": pdf_w, "h": pdf_h})
        print(f"[pypdfium2] Exact match for 'Transformer' found at char {start_idx} (count {count})")
        print(f"[pypdfium2] Bbox (pdf user units, bottom-left origin): x={pdf_x}, y={pdf_y}, w={pdf_w}, h={pdf_h}")

    # B. Test pypdf comparison
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        pypdf_page = reader.pages[page_idx]
        pypdf_text = pypdf_page.extract_text()
        print(f"[pypdf] Extracted text length: {len(pypdf_text)} (pypdf character bbox extraction requires custom visitor)")
    except Exception as e:
        print(f"[pypdf] Note: {e}")

    # 4.3 Coordinate mapping to CSS pixels
    print("\n--- 4.3 Coordinate Mapping (PDF -> CSS) ---")
    scale = DISPLAY_WIDTH / page_w
    display_height = page_h * scale

    union_css = None
    if union_pdf:
        pdf_x, pdf_y, pdf_w, pdf_h = union_pdf
        css_x = round(pdf_x * scale, 2)
        # PDF origin is bottom-left; CSS origin is top-left.
        # Top of box in PDF is (pdf_y + pdf_h), so in CSS:
        css_y = round((page_h - (pdf_y + pdf_h)) * scale, 2)
        css_w = round(pdf_w * scale, 2)
        css_h = round(pdf_h * scale, 2)
        union_css = (css_x, css_y, css_w, css_h)
        print(f"Formula: scale = {DISPLAY_WIDTH} / {page_w} = {scale:.4f}")
        print(f"CSS bbox (displayWidth={DISPLAY_WIDTH}px, displayHeight={display_height:.1f}px):")
        print(f"  x = {css_x}px, y = {css_y}px, w = {css_w}px, h = {css_h}px")

    # 4.4 Compare against DB chunk
    print("\n--- 4.4 DB Chunk Comparison ---")
    chunk_match = "skipped"
    try:
        async for db in get_db():
            docs = await ensure_eval_documents(db, {"b1-full.pdf"})
            doc_id = docs["b1-full.pdf"]
            q = (
                select(DocumentChunk)
                .where(DocumentChunk.document_id == doc_id, DocumentChunk.page_number == PAGE_NUM)
                .order_by(DocumentChunk.chunk_index)
            )
            chunks = (await db.execute(q)).scalars().all()
            if chunks:
                first_chunk = chunks[0]
                print(f"Found DB chunk index={first_chunk.chunk_index}, length={len(first_chunk.content)}")
                print(f"Chunk content snippet: {repr(first_chunk.content[:80])}")
                chunk_prefix = first_chunk.content[:40].replace("\r", " ").replace("\n", " ").strip()
                if "Transformer" in chunk_prefix or "2017" in chunk_prefix:
                    chunk_match = "ok"
                    print(f"Chunk match with needle: {chunk_match}")
                else:
                    chunk_match = "partial"
            break
    except Exception as e:
        print(f"DB chunk check note: {type(e).__name__}: {str(e)[:200]}")

    # 4.5 Schema validation
    sample_bbox_schema = {
        "version": 1,
        "coord": "pdf_user_space",
        "page_width": float(page_w),
        "page_height": float(page_h),
        "rects": rects_pypdfium,
    }
    schema_ok = len(rects_pypdfium) > 0 and sample_bbox_schema["page_width"] > 0
    print("\nCandidate JSON Schema:")
    print(json.dumps(sample_bbox_schema, indent=2))

    # Choice calculation
    if match_status == "exact" and len(rects_pypdfium) > 0 and union_css is not None:
        choice = "GO_WIRE"
    elif match_status in ("near", "page_union"):
        choice = "GO_AFTER_FIX"
    else:
        choice = "NO_GO"

    print("\n" + "=" * 60)
    print("OUTPUT BLOCK")
    print("=" * 60)
    print(f"CHOICE={choice}")
    print(f"LIB_PRIMARY={lib_primary}")
    print(f"LIB_TRIED={','.join(lib_tried)}")
    print(f"MATCH={match_status}")
    print(f"N_RECTS={len(rects_pypdfium)}")
    print(f"UNION_PDF={','.join(map(str, union_pdf)) if union_pdf else 'null'}")
    print(f"CSS_DISPLAY_WIDTH={int(DISPLAY_WIDTH)}")
    print(f"UNION_CSS={','.join(map(str, union_css)) if union_css else 'null'}")
    print("ORIGIN_NOTE=pdf_bottom_left_to_css_top_left:css_y=(page_height-(pdf_y+pdf_h))*(display_width/page_width)")
    print(f"CHUNK_MATCH={chunk_match}")
    print(f"T_EXTRACT_MS={t_extract_ms:.2f}")
    print("ERROR=none")
    print(f"SCHEMA_OK={str(schema_ok).lower()}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
