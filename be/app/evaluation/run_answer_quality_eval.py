import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from openai import AsyncOpenAI

from app.config import settings
from app.database import async_session
from app.evaluation.answer_quality_metrics import score_correctness, score_faithfulness, score_relevance
from app.evaluation.eval_documents import ensure_eval_documents
from app.evaluation.golden_dataset import load_golden_dataset
from app.services.ingestion_service import retry_async
from app.services.rag_service import ask, format_context

RESULTS_DIR = Path(__file__).resolve().parent / "results"

# generation provider for ask() — independent of the judge, which always
# stays on OpenAI (score_faithfulness/relevance/correctness) so the same
# model is never grading its own answers.
_openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
GENERATION_PROVIDERS = {
    "groq": {},  # ask()'s own defaults — Groq client + GROQ_CHAT_MODEL
    "openai": {"client": _openai_client, "model": settings.CHAT_MODEL},
}


async def evaluate_one(document_id, question, generation_kwargs: dict) -> dict:
    async def _run_ask():
        async with async_session() as db:
            return await ask(db, document_id, question.question, **generation_kwargs)

    # retry_async covers transient DB/network blips too, not just OpenAI calls —
    # a long batch run (300+ sequential calls) is long enough to hit one.
    result = await retry_async(_run_ask)

    context = format_context(result.chunks)
    faithfulness = await score_faithfulness(result.answer, context)
    relevance = await score_relevance(question.question, result.answer)
    correctness = await score_correctness(result.answer, question.expected_answer_summary)

    return {
        "document": question.document_filename,
        "question": question.question,
        "expected_answer_summary": question.expected_answer_summary,
        "answer": result.answer,
        "faithfulness": faithfulness.score,
        "faithfulness_reasoning": faithfulness.reasoning,
        "relevance": relevance.score,
        "relevance_reasoning": relevance.reasoning,
        "correctness": correctness.score,
        "correctness_reasoning": correctness.reasoning,
    }


async def run(label: str, document: str | None = None, limit: int | None = None, provider: str = "groq") -> None:
    generation_kwargs = GENERATION_PROVIDERS[provider]

    questions = load_golden_dataset(document_filename=document, limit=limit)
    if not questions:
        print(f"No questions matched (document={document!r}, limit={limit!r}) — nothing to evaluate.")
        return

    needed_filenames = {q.document_filename for q in questions}
    async with async_session() as db:
        document_ids = await ensure_eval_documents(db, only_filenames=needed_filenames)

    records = []
    failures = []
    for i, question in enumerate(questions, start=1):
        document_id = document_ids[question.document_filename]
        try:
            record = await evaluate_one(document_id, question, generation_kwargs)
        except Exception as e:
            print(f"[{i}/{len(questions)}] FAILED: [{question.document_filename}] {question.question!r} — {e}")
            failures.append({"document": question.document_filename, "question": question.question, "error": str(e)})
            continue
        records.append(record)
        print(
            f"[{i}/{len(questions)}] [{question.document_filename}] "
            f"faithfulness={record['faithfulness']:.2f} relevance={record['relevance']:.2f} "
            f"correctness={record['correctness']:.2f}"
        )

    if not records:
        print("No successful evaluations — aborting without writing a snapshot.")
        return

    def avg(key: str) -> float:
        return sum(r[key] for r in records) / len(records)

    overall = {"faithfulness": avg("faithfulness"), "relevance": avg("relevance"), "correctness": avg("correctness")}

    print(f"\n=== Answer-quality evaluation: {label} ===")
    print(f"Questions evaluated: {len(records)}/{len(questions)} ({len(failures)} failed after retry)")
    print(f"Faithfulness (avg): {overall['faithfulness']:.3f}")
    print(f"Relevance (avg):    {overall['relevance']:.3f}")
    print(f"Correctness (avg):  {overall['correctness']:.3f}")

    low_scores = [r for r in records if min(r["faithfulness"], r["relevance"], r["correctness"]) < 0.7]
    print(f"\nLow-scoring answers (any metric < 0.7): {len(low_scores)}/{len(records)}")
    for r in low_scores:
        print(f"  [{r['document']}] {r['question']!r}")
        print(f"    answer: {r['answer'][:150]!r}")
        print(f"    faithfulness={r['faithfulness']:.2f} relevance={r['relevance']:.2f} correctness={r['correctness']:.2f}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": label,
        "num_questions": len(records),
        "failures": failures,
        "overall": overall,
        "per_question": records,
    }
    out_path = RESULTS_DIR / f"{label}.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSnapshot saved to {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run answer-quality evaluation (faithfulness/relevance/correctness).")
    parser.add_argument(
        "label", nargs="?", default="phase-5-answer-quality-baseline", help="Snapshot label, saved to results/{label}.json"
    )
    parser.add_argument("--document", default=None, help='Only test one document, e.g. "b1-full.pdf" (default: all)')
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of questions (a cheap smoke test)")
    parser.add_argument(
        "--provider",
        default="groq",
        choices=sorted(GENERATION_PROVIDERS),
        help="Which model generates the answers (judge always stays on OpenAI)",
    )
    args = parser.parse_args()

    asyncio.run(run(args.label, document=args.document, limit=args.limit, provider=args.provider))
