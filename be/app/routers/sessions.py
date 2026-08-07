from fastapi import APIRouter

router = APIRouter()

# POST   /               create a session (document_id, optional title)
# GET    /                list sessions for the current user
# GET    /{id}
# PATCH  /{id}             rename
# DELETE /{id}
# GET    /{id}/messages    paginated message history
