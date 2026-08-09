import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _error_envelope(request: Request, *, message: str, code: str, details=None) -> dict:
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": {"code": code, "details": details},
        "requestId": getattr(request.state, "request_id", None),
    }


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    # Routers should raise HTTPException(detail={"code": ..., "message": ...}).
    # Fall back to a generic code for any HTTPException still using a plain string detail.
    if isinstance(exc.detail, dict) and "code" in exc.detail and "message" in exc.detail:
        code, message, details = exc.detail["code"], exc.detail["message"], exc.detail.get("details")
    else:
        code, message, details = "HTTP_ERROR", str(exc.detail), None
    body = _error_envelope(request, message=message, code=code, details=details)
    return JSONResponse(status_code=exc.status_code, content=body, headers=exc.headers)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    body = _error_envelope(request, message="Invalid request data", code="VALIDATION_ERROR", details=exc.errors())
    return JSONResponse(status_code=422, content=body)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    body = _error_envelope(
        request,
        message="Too many attempts. Please try again later.",
        code="RATE_LIMIT_EXCEEDED",
    )
    return JSONResponse(status_code=429, content=body)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    body = _error_envelope(request, message="An unexpected error occurred", code="INTERNAL_ERROR")
    return JSONResponse(status_code=500, content=body)
