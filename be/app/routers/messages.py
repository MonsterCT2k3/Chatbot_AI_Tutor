from fastapi import APIRouter

router = APIRouter()

# POST /{session_id}/messages   send a question, response is an SSE stream
# events: token (delta text) -> citation (page_number, chunk_id, snippet) -> done (message_id, citations)
