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

    # Voyage AI Rerank — ứng viên thay thế reranker local (cross-encoder chạy
    # CPU/GPU tại chỗ) nếu đo cho thấy chất lượng tiếng Việt tương đương/tốt hơn
    # VÀ latency+chi phí hợp lý cho việc deploy. CHƯA wire vào ask() — đang ở
    # giai đoạn đo so sánh, xem explain-logic/phase-5.5-advanced-rag/5.5.5.
    VOYAGE_API_KEY: str = ""
    VOYAGE_RERANK_MODEL: str = "rerank-2.5"

    # Jina AI Reranker — ứng viên thứ 2, cùng mục đích đo so sánh với Voyage/
    # local. Free tier RPM cao hơn hẳn Voyage (100 vs 3), thực dụng hơn để eval.
    JINA_API_KEY: str = ""
    JINA_RERANK_MODEL: str = "jina-reranker-v2-base-multilingual"

    # AI cost guardrails (5.6.6+) — giới hạn NGHIỆP VỤ theo user/ngày, khác với
    # rate limit request/giây thuần kỹ thuật ở Phase 10. Để trong settings để
    # đổi được bằng biến môi trường mà không phải sửa code/deploy lại.
    DAILY_QUESTION_LIMIT: int = 50
    # 5.6.7 — ngưỡng CẢNH BÁO (không chặn) theo $ thật/user/tháng. Đo THẬT qua
    # ask() production (b1-full.pdf, câu hỏi bình thường không retry): 2496
    # token, $0.000164/lượt — chỉ judge (OpenAI gpt-4o-mini) tốn phí, Groq đang
    # free tier ($0). Với DAILY_QUESTION_LIMIT=50 câu/ngày, worst case retry
    # gấp đôi mỗi câu, dùng hết quota mỗi ngày suốt 30 ngày: 50*30*0.000164*2 ≈
    # $0.49/tháng — đặt $2.00 (an toàn ~4x worst case thực đo) làm ngưỡng cảnh
    # báo mặc định.
    MONTHLY_COST_BUDGET_USD: float = 2.0
    # 5.6.8 — circuit breaker TOÀN HỆ THỐNG (không theo user), phát hiện tăng
    # đột biến trong cửa sổ ngắn. Chưa có traffic production thật để hiệu
    # chỉnh — đặt theo suy luận từ quy mô đã biết (DAILY_QUESTION_LIMIT, chi
    # phí đo thật ở 5.6.7), xem chi tiết lý luận trong usage_service.py.
    CIRCUIT_BREAKER_WINDOW_MINUTES: int = 5
    CIRCUIT_BREAKER_MAX_REQUESTS: int = 30
    CIRCUIT_BREAKER_MAX_COST_USD: float = 0.05

    # Auth
    JWT_SECRET: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")


settings = Settings()
