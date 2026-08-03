from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.api.routes import chat
from app.services.rag_service import RAGService
import app.main as current_module

# Global variable to hold the RAG service instance
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    global rag_service
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data")
    print("Loading AI Models and Vector DB into memory...")
    rag_service = RAGService(data_dir=data_dir)
    print("AI Tutor Backend is READY!")
    yield
    # Shutdown logic
    rag_service = None
    print("Shutting down AI Tutor Backend.")

app = FastAPI(
    title="AI Tutor API",
    description="Backend API for the AI Tutor Chat Application",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS for the Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
