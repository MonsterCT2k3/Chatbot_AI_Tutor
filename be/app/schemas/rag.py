import uuid

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class CitationResponse(BaseModel):
    page_number: int
    chunk_id: uuid.UUID
    snippet: str


class AskResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
