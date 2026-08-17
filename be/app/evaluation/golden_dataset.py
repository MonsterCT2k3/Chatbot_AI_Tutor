import json
from dataclasses import dataclass
from pathlib import Path

GOLDEN_QA_DIR = Path(__file__).resolve().parent.parent / "data" / "golden-qa"


@dataclass
class GoldenQuestion:
    document_filename: str
    question: str
    expected_pages: list[int]
    expected_answer_summary: str


def load_golden_dataset(
    document_filename: str | None = None, limit: int | None = None, offset: int = 0
) -> list[GoldenQuestion]:
    """Load golden questions. `document_filename` restricts to one document's
    JSON file (e.g. "b1-full.pdf") instead of the whole combined set — every
    eval run costs real OpenAI API calls, so scoping down matters. `offset`
    skips the first N questions before applying `limit`, so a capped run can
    target a specific slice (e.g. the questions known to be hard) instead of
    always re-testing the same first N."""
    questions: list[GoldenQuestion] = []
    for json_path in sorted(GOLDEN_QA_DIR.glob("*.json")):
        filename = f"{json_path.stem}.pdf"
        if document_filename is not None and filename != document_filename:
            continue
        records = json.loads(json_path.read_text(encoding="utf-8"))
        for record in records:
            questions.append(
                GoldenQuestion(
                    document_filename=filename,
                    question=record["question"],
                    expected_pages=record["expected_pages"],
                    expected_answer_summary=record["expected_answer_summary"],
                )
            )

    if offset:
        questions = questions[offset:]
    if limit is not None:
        questions = questions[:limit]
    return questions
