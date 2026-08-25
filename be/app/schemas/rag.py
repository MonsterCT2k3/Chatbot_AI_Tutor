from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    is_positive: bool
    reason: str | None = Field(default=None, max_length=2000)
