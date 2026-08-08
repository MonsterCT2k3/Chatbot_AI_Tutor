from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.exceptions import http_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.middleware import ResponseEnvelopeMiddleware
from app.routers import auth, documents, sessions, messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AI Tutor Backend is READY!")
    yield
    print("Shutting down AI Tutor Backend.")


app = FastAPI(
    title="AI Tutor API",
    description="Backend API for the AI Tutor Chat Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Setup CORS for the Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ResponseEnvelopeMiddleware)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(messages.router, prefix="/api/sessions", tags=["Messages"])


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
