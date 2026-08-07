# AI Tutor — Implementation Guide

> Đưa file này cho Claude Code để triển khai dự án. Đây là bản tổng hợp toàn bộ quyết định kiến trúc đã chốt — bám sát nội dung này khi code, không tự ý đổi stack nếu không cần thiết.

## 1. Mục tiêu sản phẩm

Web app cho phép người dùng:
- Upload file PDF hoặc PowerPoint (PPTX)
- Xem tài liệu ở panel trái (viewer)
- Chat với AI ở panel phải — AI chỉ được trả lời dựa trên nội dung tài liệu đã upload (RAG, không bịa)
- Khi AI trích dẫn, tài liệu ở panel trái tự động cuộn tới và highlight đúng trang/slide được nhắc tới
- Hỗ trợ nhiều phiên chat (multi-session) cho cùng 1 tài liệu
- Streaming câu trả lời (không đợi full response mới hiển thị)

Giai đoạn hiện tại: **dự án cá nhân / MVP**, ưu tiên chạy được nhanh trên free tier, nhưng kiến trúc phải dễ mở rộng lên production sau này mà không cần viết lại.

---

## 2. Tech stack đã chốt

| Thành phần | Lựa chọn | Lý do |
|---|---|---|
| Backend | **FastAPI** (Python) | Toàn bộ business logic (auth, ingestion, RAG, streaming) nằm ở đây, không phụ thuộc BaaS |
| Database | **Supabase Postgres** (pgvector enabled) | SQL quan hệ (JOIN sessions/messages/chunks) + vector search cùng 1 chỗ, không cần vector DB riêng |
| File storage (PDF/PPTX gốc + thumbnail ảnh) | **Cloudflare R2** | Egress miễn phí vĩnh viễn — quan trọng vì viewer sẽ load lại file/thumbnail liên tục; 10GB free tier |
| Auth | **Tự viết trong FastAPI** (JWT + passlib/bcrypt) | KHÔNG dùng Supabase Auth, không dùng Supabase RLS — mọi kiểm soát quyền truy cập nằm trong code backend |
| LLM | OpenAI `gpt-4o-mini` | Model chính cho RAG + streaming response — cùng vendor với embedding, dùng chung 1 API key |
| Embedding model | OpenAI `text-embedding-3-small` hoặc tương đương (1536 chiều) | Đã fix cứng chiều vector trong schema; nếu đổi model sau này, thêm cột `embedding_v2`, không sửa cột cũ |
| Ingestion (giai đoạn MVP) | `BackgroundTasks` của FastAPI | Chưa cần Celery/Redis queue riêng — chỉ thêm khi có traffic thật |

### Quyết định quan trọng cần tuân thủ

1. **Không lưu file PDF/PPTX vào Postgres.** File luôn nằm ở R2, Postgres chỉ lưu `storage_key` (object key) trỏ tới file.
2. **Không dùng Supabase client SDK ở frontend để query trực tiếp DB.** Mọi request đi qua FastAPI — frontend chỉ gọi API của FastAPI, không gọi thẳng Supabase.
3. **Kết nối Postgres qua connection string chuẩn** (asyncpg/SQLAlchemy), dùng Supabase **Connection Pooler** (port 6543, transaction mode) thay vì port 5432 trực tiếp nếu số connection đồng thời tăng.
4. **R2 dùng `boto3`** (S3-compatible API), không cần SDK riêng của Cloudflare.

---

## 3. Kiến trúc tổng quan

```
Frontend (React)
   │  gọi API qua FastAPI (không gọi thẳng Supabase/R2)
   ▼
FastAPI Backend
   ├── Auth module          (JWT, đăng ký/đăng nhập)
   ├── Document Service     (upload → lưu R2, tạo record Postgres, enqueue ingestion)
   ├── Ingestion Worker      (parse PDF/PPTX → chunk → embed → lưu Postgres/pgvector)
   ├── Session Service       (CRUD chat sessions)
   ├── Message Service       (nhận câu hỏi, gọi RAG, stream response)
   └── RAG Orchestrator      (similarity search trong pgvector → build prompt → gọi OpenAI Chat API, stream)
   │
   ├──▶ Supabase Postgres (metadata, chunks, embeddings, sessions, messages, citations)
   └──▶ Cloudflare R2 (file gốc PDF/PPTX, thumbnail ảnh từng trang/slide)
```

**Luồng upload & ingestion:**
1. User upload file → FastAPI lưu file lên R2 → tạo record `documents` (status=`pending`) → trả về ngay `document_id` (202 Accepted) → enqueue background task.
2. Background task: tải file từ R2 → parse từng trang/slide → render thumbnail (LibreOffice headless cho PPTX, hoặc `pdf2image` cho PDF) → upload thumbnail lên R2 → chunk text → gọi embedding model → lưu `document_chunks` (kèm vector) → update status=`ready`.
3. Frontend poll `/api/documents/{id}/status` hoặc dùng SSE để biết khi nào tài liệu sẵn sàng chat.

**Luồng chat (RAG + streaming + citation highlight):**
1. User gửi câu hỏi trong 1 session gắn với `document_id` cụ thể.
2. FastAPI lưu user message → RAG Orchestrator similarity-search trong `document_chunks` (filter theo `document_id`) → lấy top-k chunk liên quan.
3. Build prompt: system prompt (chỉ được trả lời dựa trên context) + các chunk retrieved + câu hỏi → gọi OpenAI Chat Completions API (`gpt-4o-mini`) với `stream=true`.
4. Response stream về frontend qua SSE: event `token` (từng phần text) → event `citation` (page_number, chunk_id, snippet) → event `done` (lưu message + citations vào Postgres).
5. Frontend nhận event `citation` → gọi `highlightRegion(page_number)` trên document viewer để tự động cuộn/highlight đúng trang.

---

## 4. Database schema

Schema đầy đủ đã được thiết kế sẵn ở file `schema.sql` đi kèm — chạy trực tiếp trên Supabase SQL Editor. Tóm tắt các bảng:

| Bảng | Vai trò |
|---|---|
| `users` | Tài khoản, tự quản lý (không dùng `auth.users` của Supabase) |
| `documents` | Metadata tài liệu upload, trạng thái ingestion, trỏ tới R2 qua `storage_key` |
| `document_pages` | 1 row / trang hoặc slide — chứa text gốc + `thumbnail_key` (trỏ R2) |
| `document_chunks` | Đơn vị retrieval cho RAG — chứa `content` + `embedding` (pgvector) + `page_number` trong cùng 1 row |
| `chat_sessions` | Multi-session chat, gắn với `document_id` |
| `chat_messages` | Tin nhắn user/assistant |
| `message_citations` | Liên kết message → chunk/page cụ thể, dùng để driver việc highlight |

**Nguyên tắc mở rộng đã áp dụng trong schema (giữ nguyên khi code, đừng phá vỡ):**
- Cột `metadata jsonb` ở các bảng chính (documents, pages, sessions, messages) để thêm field mới không cần migration.
- `page_number` bị denormalize (lặp ở cả `document_pages` và `document_chunks`) có chủ đích — tránh JOIN thêm ở đường query nóng nhất (mỗi lần chat).
- Nếu đổi embedding model sau này → thêm cột `embedding_v2 vector(N)` mới, không sửa cột `embedding` hiện tại.
- Citation tách bảng riêng (không nhét vào `chat_messages`) vì 1 câu trả lời có thể trích nhiều trang cùng lúc.

---

## 5. API design (FastAPI routes)

### Auth
```
POST   /api/auth/signup
POST   /api/auth/login          → trả JWT
POST   /api/auth/logout
```

### Documents
```
POST   /api/documents                    multipart upload, trả document_id ngay (202)
GET    /api/documents                    list tài liệu của user
GET    /api/documents/{id}               metadata + status
GET    /api/documents/{id}/status        polling / hoặc SSE push
GET    /api/documents/{id}/pages/{n}     trả về ảnh trang/slide đã render (presigned URL từ R2)
DELETE /api/documents/{id}
```

### Chat Sessions
```
POST   /api/sessions             tạo session mới (document_id, title tùy chọn)
GET    /api/sessions             list session của user
GET    /api/sessions/{id}
PATCH  /api/sessions/{id}        đổi tên
DELETE /api/sessions/{id}
GET    /api/sessions/{id}/messages   lịch sử tin nhắn (phân trang)
```

### Messaging (streaming)
```
POST   /api/sessions/{id}/messages   gửi câu hỏi, response là SSE stream
```

**Event shape khi stream:**
```json
event: token
{ "delta": "Photosynthesis " }

event: citation
{ "page_number": 4, "chunk_id": "c-123", "snippet": "..." }

event: done
{ "message_id": "m-789", "citations": [ { "page_number": 4, "chunk_id": "c-123" } ] }
```

---

## 6. Cấu trúc thư mục backend đề xuất

```
app/
├── main.py                  # FastAPI app entrypoint
├── config.py                 # env vars (Supabase URL, R2 keys, OpenAI API key...)
├── database.py               # SQLAlchemy async engine + session
├── models/                   # SQLAlchemy ORM models (map với schema.sql)
│   ├── user.py
│   ├── document.py
│   ├── chunk.py
│   ├── session.py
│   └── message.py
├── schemas/                  # Pydantic request/response schemas
├── routers/
│   ├── auth.py
│   ├── documents.py
│   ├── sessions.py
│   └── messages.py
├── services/
│   ├── auth_service.py       # JWT, hash password
│   ├── storage_service.py    # boto3 wrapper cho R2 (upload/download/presigned URL)
│   ├── ingestion_service.py  # parse PDF/PPTX, chunk, embed
│   └── rag_service.py        # retrieval + prompt + gọi OpenAI Chat API + stream
└── workers/
    └── ingestion_worker.py   # background task xử lý ingestion
```

---

## 7. Biến môi trường cần có

```env
# Supabase Postgres
DATABASE_URL=postgresql+asyncpg://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Cloudflare R2 (S3-compatible)
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_ENDPOINT_URL=https://[account_id].r2.cloudflarestorage.com

# OpenAI (LLM gpt-4o-mini + embedding, dùng chung 1 key)
OPENAI_API_KEY=
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Auth
JWT_SECRET=
JWT_EXPIRE_MINUTES=
```

---

## 8. Thứ tự triển khai đề xuất (cho Claude Code)

1. Setup FastAPI project skeleton + kết nối Supabase Postgres (chạy `schema.sql` trên Supabase SQL Editor trước).
2. Auth module (signup/login/JWT) — cần trước vì mọi route khác đều yêu cầu user đã đăng nhập.
3. Document upload flow: FastAPI → R2 → tạo record `documents` (status=pending).
4. Ingestion worker: parse PDF/PPTX → chunk → embed → lưu `document_chunks` → update status=ready. Test kỹ bước này riêng trước khi làm chat.
5. Document viewer API: trả presigned URL cho thumbnail từng trang từ R2.
6. RAG orchestrator: similarity search trong pgvector + gọi OpenAI Chat API (chưa cần stream, test non-streaming trước).
7. Chuyển sang streaming (SSE) sau khi RAG chạy đúng.
8. Chat session CRUD (multi-session).
9. Citation resolver + frontend highlight logic — nối `event: citation` với `highlightRegion()` trên viewer.
10. Frontend: layout 2 panel (viewer trái, chat phải), upload modal, session sidebar.

---

## 9. Lưu ý vận hành (free tier)

- **Supabase free tier**: project tự pause sau 7 ngày không có API request — data không mất, chỉ cần vào dashboard resume, hoặc setup GitHub Action ping định kỳ để tránh bị pause.
- **500MB database storage** đủ cho vài trăm tài liệu ở quy mô cá nhân — không cần lo tối ưu sớm.
- **R2 free tier**: 10GB storage, egress miễn phí vĩnh viễn — phù hợp vì viewer load lại file/thumbnail liên tục.
- Không cần Redis/Celery ở giai đoạn này — chỉ thêm khi có traffic thật hoặc ingestion bắt đầu chậm với `BackgroundTasks`.
