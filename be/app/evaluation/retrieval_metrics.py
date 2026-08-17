import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.evaluation.golden_dataset import GoldenQuestion
from app.models.chunk import DocumentChunk
from app.services.ingestion_service import embed_chunks
from app.services.rag_service import hybrid_search, multi_query_search, rerank_search, similarity_search


@dataclass
class RetrievalResult:
    question: GoldenQuestion
    retrieved_pages: list[int]
    hit: bool
    rank: int | None  # 1-indexed rank of the first expected page found, None if not found


def score_retrieval(question: GoldenQuestion, chunks: list[DocumentChunk]) -> RetrievalResult:
    retrieved_pages = [chunk.page_number for chunk in chunks]

    rank = None
    for position, page in enumerate(retrieved_pages, start=1):
        if page in question.expected_pages:
            rank = position
            break

    return RetrievalResult(question=question, retrieved_pages=retrieved_pages, hit=rank is not None, rank=rank)


async def evaluate_question(
    db: AsyncSession, document_id: uuid.UUID, question: GoldenQuestion, k: int
) -> RetrievalResult:
    query_embedding = (await embed_chunks([question.question]))[0]
    chunks = await similarity_search(db, document_id, query_embedding, k=k)
    return score_retrieval(question, chunks)


async def evaluate_question_hybrid(
    db: AsyncSession, document_id: uuid.UUID, question: GoldenQuestion, k: int
) -> RetrievalResult:
    query_embedding = (await embed_chunks([question.question]))[0]
    chunks = await hybrid_search(db, document_id, query_embedding, question.question, k=k)
    return score_retrieval(question, chunks)


async def evaluate_question_rerank(
    db: AsyncSession, document_id: uuid.UUID, question: GoldenQuestion, k: int
) -> RetrievalResult:
    query_embedding = (await embed_chunks([question.question]))[0]
    chunks = await rerank_search(db, document_id, query_embedding, question.question, k=k)
    return score_retrieval(question, chunks)


async def evaluate_question_multiquery(
    db: AsyncSession, document_id: uuid.UUID, question: GoldenQuestion, k: int
) -> RetrievalResult:
    # multi_query_search computes its own embeddings internally (one per
    # variant) — no single query_embedding to precompute here, unlike the
    # other strategies above.
    chunks = await multi_query_search(db, document_id, question.question, k=k)
    return score_retrieval(question, chunks)


def recall_at_k(results: list[RetrievalResult]) -> float:
    if not results:
        return 0.0
    return sum(1 for r in results if r.hit) / len(results)


def mean_reciprocal_rank(results: list[RetrievalResult]) -> float:
    if not results:
        return 0.0
    return sum((1 / r.rank) if r.rank else 0.0 for r in results) / len(results)
