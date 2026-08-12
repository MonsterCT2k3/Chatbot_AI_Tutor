import re
import uuid
from dataclasses import dataclass

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chunk import DocumentChunk
from app.services.ingestion_service import embed_chunks, retry_async

_openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def similarity_search(
    db: AsyncSession, document_id: uuid.UUID, query_embedding: list[float], k: int = 6
) -> list[DocumentChunk]:
    stmt = (
        select(DocumentChunk)
        .where(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(k)
    )
    result = await db.scalars(stmt)
    return list(result.all())


_SYSTEM_PROMPT = (
    "Bạn là một trợ lý AI tutor, chỉ trả lời dựa trên nội dung nằm trong thẻ <context> bên dưới.\n"
    "Quy tắc bắt buộc:\n"
    "1. CHỈ dùng thông tin có trong <context> để trả lời. Không tự bịa, không dùng kiến thức ngoài tài liệu.\n"
    '2. Nếu <context> không chứa thông tin để trả lời câu hỏi, hãy trả lời đúng câu: '
    '"Tôi không tìm thấy thông tin này trong tài liệu." Không đoán, không suy diễn thêm.\n'
    "3. Mỗi khi dùng thông tin từ <context>, trích dẫn ngay sau bằng định dạng [Trang X], với X là số trang thật của đoạn đó.\n"
    "4. Trả lời bằng tiếng Việt, rõ ràng, súc tích.\n"
)


def build_prompt(chunks: list[DocumentChunk], question: str) -> list[dict]:
    if chunks:
        context = "\n\n---\n\n".join(f"[Trang {chunk.page_number}]\n{chunk.content}" for chunk in chunks)
    else:
        context = "(không có nội dung liên quan nào được tìm thấy trong tài liệu)"

    user_prompt = f"<context>\n{context}\n</context>\n\n<question>\n{question}\n</question>"

    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


@dataclass
class AnswerResult:
    answer: str
    chunks: list[DocumentChunk]


async def ask(db: AsyncSession, document_id: uuid.UUID, question: str) -> AnswerResult:
    query_embedding = (await embed_chunks([question]))[0]
    chunks = await similarity_search(db, document_id, query_embedding)
    messages = build_prompt(chunks, question)

    async def _call():
        return await _openai_client.chat.completions.create(model=settings.CHAT_MODEL, messages=messages)

    response = await retry_async(_call)
    answer = response.choices[0].message.content
    return AnswerResult(answer=answer, chunks=chunks)


_CITATION_RE = re.compile(r"\[Trang (\d+)\]")


@dataclass
class Citation:
    page_number: int
    chunk_id: uuid.UUID
    snippet: str


def parse_citations(answer_text: str, chunks: list[DocumentChunk]) -> list[Citation]:
    # chunks is already ordered by relevance (ascending cosine distance, from
    # similarity_search) — first chunk seen per page is the most relevant one.
    chunk_by_page: dict[int, DocumentChunk] = {}
    for chunk in chunks:
        chunk_by_page.setdefault(chunk.page_number, chunk)

    citations: list[Citation] = []
    seen_pages: set[int] = set()
    for match in _CITATION_RE.finditer(answer_text):
        page_number = int(match.group(1))
        if page_number in seen_pages:
            continue

        chunk = chunk_by_page.get(page_number)
        if chunk is None:
            # Model cited a page that wasn't actually part of the retrieved
            # context — can't verify it, so don't surface it as a citation.
            continue

        seen_pages.add(page_number)
        citations.append(Citation(page_number=page_number, chunk_id=chunk.id, snippet=chunk.content[:200]))

    return citations
