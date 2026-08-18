import uuid

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class CitationResponse(BaseModel):
    page_number: int
    chunk_id: uuid.UUID
    snippet: str


class AskResponse(BaseModel):
    # 5.6.12: client cần id này để gửi feedback về ĐÚNG câu trả lời — trước đó
    # AskResponse không lộ ra id nào cả, không có cách nào biết phải feedback
    # cho câu nào. Chính là AIUsageLog.id (== AnswerResult.call_group_id).
    answer_id: uuid.UUID
    answer: str
    citations: list[CitationResponse]


class FeedbackRequest(BaseModel):
    is_positive: bool
    reason: str | None = Field(default=None, max_length=2000)
