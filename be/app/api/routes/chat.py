from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# This depends on a global dependency which we will inject from main.py
def get_rag_service():
    from app.main import rag_service
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG Service is not initialized")
    return rag_service

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, rag_service=Depends(get_rag_service)):
    try:
        answer_text, action, follow_ups = rag_service.ask(
            question=request.question,
            target_lesson=request.lesson
        )
        return ChatResponse(
            answer=answer_text,
            action_taken=action,
            follow_up_questions=follow_ups
        )
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
