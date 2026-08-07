from fastapi import APIRouter

router = APIRouter()

# POST   /               multipart upload, returns document_id immediately (202)
# GET    /                list documents for the current user
# GET    /{id}             metadata + status
# GET    /{id}/status      polling / SSE push
# GET    /{id}/pages/{n}   rendered page/slide image (presigned R2 URL)
# DELETE /{id}
