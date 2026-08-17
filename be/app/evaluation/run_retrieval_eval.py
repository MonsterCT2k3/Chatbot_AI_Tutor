import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from app.database import async_session
from app.evaluation.eval_documents import ensure_eval_documents
from app.evaluation.golden_dataset import load_golden_dataset
from app.evaluation.retrieval_metrics import (
    evaluate_question,
    evaluate_question_hybrid,
    evaluate_question_multiquery,
    evaluate_question_rerank,
    mean_reciprocal_rank,
    recall_at_k,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"
K = 6  # matches similarity_search's default k, i.e. what ask() actually retrieves in production

MODES = {
    "vector": evaluate_question,
    "hybrid": evaluate_question_hybrid,
    "rerank": evaluate_question_rerank,
    "multiquery": evaluate_question_multiquery,
}


async def run(
    label: str, mode: str = "vector", document: str | None = None, limit: int | None = None, offset: int = 0
) -> None:
    evaluate_fn = MODES[mode]

    questions = load_golden_dataset(document_filename=document, limit=limit, offset=offset)
    if not questions:
        print(f"No questions matched (document={document!r}, limit={limit!r}) — nothing to evaluate.")
        return

    needed_filenames = {q.document_filename for q in questions}
    async with async_session() as db:
        document_ids = await ensure_eval_documents(db, only_filenames=needed_filenames)

    results = []
    for question in questions:
        document_id = document_ids[question.document_filename]
        async with async_session() as db:
            results.append(await evaluate_fn(db, document_id, question, k=K))

    overall_recall = recall_at_k(results)
    overall_mrr = mean_reciprocal_rank(results)

    print(f"\n=== Retrieval evaluation: {label} (k={K}) ===")
    print(f"Questions evaluated: {len(results)}")
    print(f"Recall@{K}: {overall_recall:.3f}")
    print(f"MRR: {overall_mrr:.3f}")

    misses = [r for r in results if not r.hit]
    print(f"\nMisses ({len(misses)}/{len(results)} — expected page not found in top-{K}):")
    for r in misses:
        print(f"  [{r.question.document_filename}] {r.question.question!r}")
        print(f"    expected_pages={r.question.expected_pages} retrieved_pages={r.retrieved_pages}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": label,
        "k": K,
        "num_questions": len(results),
        "recall_at_k": overall_recall,
        "mrr": overall_mrr,
        "per_question": [
            {
                "document": r.question.document_filename,
                "question": r.question.question,
                "expected_pages": r.question.expected_pages,
                "retrieved_pages": r.retrieved_pages,
                "hit": r.hit,
                "rank": r.rank,
            }
            for r in results
        ],
    }
    out_path = RESULTS_DIR / f"{label}.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSnapshot saved to {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run retrieval evaluation (Recall@k, MRR) against the golden dataset.")
    parser.add_argument("label", nargs="?", default="phase-5-baseline", help="Snapshot label, saved to results/{label}.json")
    parser.add_argument("mode", nargs="?", default="vector", choices=sorted(MODES), help="Retrieval strategy to evaluate")
    parser.add_argument("--document", default=None, help='Only test one document, e.g. "b1-full.pdf" (default: all)')
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of questions (a cheap smoke test)")
    parser.add_argument("--offset", type=int, default=0, help="Skip the first N questions before applying --limit")
    args = parser.parse_args()

    asyncio.run(run(args.label, args.mode, document=args.document, limit=args.limit, offset=args.offset))
