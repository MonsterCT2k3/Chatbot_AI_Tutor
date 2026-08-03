from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    lesson: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    action_taken: str # "[ANSWER]", "[WEB_SEARCH]", "[IRRELEVANT]"
    follow_up_questions: List[str] = []
