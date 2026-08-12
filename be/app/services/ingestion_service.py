import asyncio
import re
import tempfile
from io import BytesIO
from pathlib import Path

import tiktoken
from mistralai.client import Mistral
from openai import AsyncOpenAI
from pypdf import PdfReader

from app.config import settings

_openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

_mistral_client = Mistral(api_key=settings.MISTRAL_API_KEY)


class PptxConversionError(Exception):
    pass

_IMAGE_ANALYSIS_PROMPT = (
    "Bạn là trợ lý AI chuyên phân tích tài liệu bài giảng giáo trình.\n"
    "Hãy phân tích bức ảnh này và chuyển đổi thành dạng Markdown theo cấu trúc:\n\n"
    "1. Nếu đây là **Biểu đồ, Sơ đồ kiến trúc, Quy trình, Timeline**:\n"
    "   - **Tên/Chủ đề sơ đồ**: ...\n"
    "   - **Các cột mốc / Thành phần chính**: (Mô tả chi tiết các bước, trục X/Y, các box và mũi tên)\n"
    "   - **Số liệu & Insight quan trọng**: (Liệt kê chính xác số liệu, mốc thời gian, tên công nghệ)\n"
    "   - **Ý nghĩa bài học**: (Tóm tắt 2-3 câu ngắn về bài học)\n\n"
    "2. Nếu đây là **Ảnh chụp chữ, Mã nguồn (Code) hoặc Bảng biểu**:\n"
    "   - Trích xuất 100% nội dung chữ/code ra dạng Markdown hoặc fenced code block ```python ... ```.\n\n"
    "3. Nếu đây là **Ảnh chân dung tác giả, Logo hoặc Ảnh trang trí không chứa thông tin kiến thức bài học**:\n"
    "   - Trả về ngắn gọn: `> 🖼️ *[Hình ảnh minh họa / Chân dung]*`\n\n"
    "Yêu cầu: Trả lời bằng tiếng Việt, súc tích, giữ nguyên các mốc số liệu chính xác để phục vụ cho RAG."
)


def extract_text_pypdf(pdf_bytes: bytes) -> list[tuple[int, str]]:
    reader = PdfReader(BytesIO(pdf_bytes))
    return [(page_number, page.extract_text() or "") for page_number, page in enumerate(reader.pages, start=1)]


async def retry_async(fn, max_retries: int = 5, backoff_factor: int = 2):
    # External API calls (Mistral) can fail transiently on network/SSL — retry
    # with exponential backoff instead of failing the whole document ingestion.
    for attempt in range(1, max_retries + 1):
        try:
            return await fn()
        except Exception:
            if attempt == max_retries:
                raise
            await asyncio.sleep(backoff_factor**attempt)


async def _describe_image_pixtral(image_base64: str, mime_type: str = "image/png") -> str:
    async def _call() -> str:
        response = await _mistral_client.chat.complete_async(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": _IMAGE_ANALYSIS_PROMPT},
                        {"type": "image_url", "image_url": f"data:{mime_type};base64,{image_base64}"},
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    return await retry_async(_call)


async def extract_text_mistral_ocr(document_url: str, pages: list[int] | None = None) -> list[tuple[int, str]]:
    async def _call():
        kwargs = {
            "model": "mistral-ocr-latest",
            "document": {"type": "document_url", "document_url": document_url},
            "include_image_base64": True,
        }
        if pages is not None:
            kwargs["pages"] = pages
        return await _mistral_client.ocr.process_async(**kwargs)

    response = await retry_async(_call)

    results = []
    for page in response.pages:
        text = page.markdown
        for image in page.images or []:
            description = await _describe_image_pixtral(image.image_base64.split(",")[-1])
            text = text.replace(f"![{image.id}]({image.id})", description, 1)
        results.append((page.index + 1, text))
    return results


async def extract_text_hybrid(pdf_bytes: bytes, document_url: str) -> list[tuple[int, str]]:
    baseline = extract_text_pypdf(pdf_bytes)

    reader = PdfReader(BytesIO(pdf_bytes))
    pages_with_images = [i for i, page in enumerate(reader.pages) if page.images]

    if not pages_with_images:
        return baseline

    ocr_results = await extract_text_mistral_ocr(document_url, pages=pages_with_images)
    ocr_by_page = dict(ocr_results)

    return [(page_number, ocr_by_page.get(page_number, text)) for page_number, text in baseline]


async def convert_pptx_to_pdf(pptx_bytes: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / "input.pptx"
        input_path.write_bytes(pptx_bytes)

        # Each conversion gets its own LibreOffice user profile — concurrent
        # `soffice` invocations sharing the default profile hit lock conflicts
        # ("soffice is already running") under real, overlapping ingestion load.
        profile_dir = tmp_path / "profile"
        process = await asyncio.create_subprocess_exec(
            "soffice",
            "--headless",
            f"-env:UserInstallation=file://{profile_dir}",
            "--convert-to",
            "pdf",
            "--outdir",
            str(tmp_path),
            str(input_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        output_path = tmp_path / "input.pdf"
        if process.returncode != 0 or not output_path.exists():
            raise PptxConversionError((stderr or stdout).decode(errors="replace"))

        return output_path.read_bytes()


def _greedy_group(parts: list[str], encoding: tiktoken.Encoding, max_tokens: int, joiner: str) -> list[str]:
    chunks: list[str] = []
    current_parts: list[str] = []
    current_tokens = 0

    for part in parts:
        part_tokens = len(encoding.encode(part))
        if current_parts and current_tokens + part_tokens > max_tokens:
            chunks.append(joiner.join(current_parts))
            current_parts = []
            current_tokens = 0
        current_parts.append(part)
        current_tokens += part_tokens

    if current_parts:
        chunks.append(joiner.join(current_parts))
    return chunks


def chunk_text(text: str, max_tokens: int = 300) -> list[str]:
    text = text.strip()
    if not text:
        return []

    encoding = tiktoken.encoding_for_model("text-embedding-3-small")
    paragraphs = [p.strip() for p in _PARAGRAPH_SPLIT_RE.split(text) if p.strip()]

    chunks: list[str] = []
    current_parts: list[str] = []
    current_tokens = 0

    for paragraph in paragraphs:
        paragraph_tokens = len(encoding.encode(paragraph))

        if paragraph_tokens > max_tokens:
            # A single paragraph alone exceeds the limit (rare) — flush whatever
            # was accumulating, then fall back to sentence-level splitting for
            # just this paragraph.
            if current_parts:
                chunks.append("\n\n".join(current_parts))
                current_parts = []
                current_tokens = 0

            sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(paragraph) if s.strip()]
            chunks.extend(_greedy_group(sentences, encoding, max_tokens, " "))
            continue

        if current_parts and current_tokens + paragraph_tokens > max_tokens:
            chunks.append("\n\n".join(current_parts))
            current_parts = []
            current_tokens = 0

        current_parts.append(paragraph)
        current_tokens += paragraph_tokens

    if current_parts:
        chunks.append("\n\n".join(current_parts))

    return chunks


async def embed_chunks(chunks: list[str]) -> list[list[float]]:
    if not chunks:
        return []

    async def _call():
        return await _openai_client.embeddings.create(model=settings.EMBEDDING_MODEL, input=chunks)

    response = await retry_async(_call)
    ordered = sorted(response.data, key=lambda item: item.index)
    return [item.embedding for item in ordered]
