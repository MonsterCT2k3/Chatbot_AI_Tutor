import json
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

_SKIP_PATHS = {"/docs", "/redoc", "/openapi.json", "/health"}


class ResponseEnvelopeMiddleware(BaseHTTPMiddleware):
    """Wraps every successful (status < 400) JSON response in the standard
    {success, message, data, error, requestId} envelope.
    Error responses are already enveloped by the handlers in app/exceptions.py —
    this middleware only adds requestId there via request.state."""

    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        response = await call_next(request)

        if request.url.path in _SKIP_PATHS or response.status_code >= 400:
            return response

        body = b"".join([chunk async for chunk in response.body_iterator])
        try:
            data = json.loads(body) if body else None
        except json.JSONDecodeError:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        envelope = {
            "success": True,
            "message": getattr(request.state, "message", "Request processed successfully"),
            "data": data,
            "error": None,
            "requestId": request.state.request_id,
        }
        headers = {k: v for k, v in response.headers.items() if k.lower() not in ("content-length", "content-type")}
        return JSONResponse(content=envelope, status_code=response.status_code, headers=headers)
