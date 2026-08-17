from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Tutor API"

    # Supabase Postgres
    DATABASE_URL: str = ""

    # Cloudflare R2 (S3-compatible)
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = ""
    R2_ENDPOINT_URL: str = ""

    # OpenAI: chat model (RAG generation) + embedding model, share one key
    OPENAI_API_KEY: str = ""
    CHAT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Mistral: OCR (mistral-ocr-latest) + vision image description (pixtral-12b-2409)
    MISTRAL_API_KEY: str = ""

    # Groq: free-tier inference for open-weight models (OpenAI-compatible API).
    # Being trialed as the answer-generation model in ask() (Phase 5.5) — NOT
    # used for embeddings (Groq has no embedding model; embeddings stay on
    # OpenAI regardless, see EMBEDDING_DIM note in app/models/chunk.py).
    GROQ_API_KEY: str = ""
    # llama-3.3-70b-versatile bị Groq gỡ khỏi catalog (2026-08-17, xác nhận
    # thật qua GET /v1/models — 404 not_found) → chuyển sang openai/gpt-oss-120b
    # (model open-weight lớn nhất còn lại trong catalog hiện tại của Groq).
    GROQ_CHAT_MODEL: str = "openai/gpt-oss-120b"

    # Auth
    JWT_SECRET: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")


settings = Settings()
