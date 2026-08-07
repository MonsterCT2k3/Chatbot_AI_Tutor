# AI Tutor — Kế hoạch phát triển chi tiết

> Dựa trên `ai-tutor-implementation-guide.md` (kiến trúc đã chốt) và `schema.sql` (schema đã thiết kế). Tài liệu này chia nhỏ thành các phase có thể làm tuần tự, mỗi phase có: mục tiêu, việc cần làm, file đụng tới, tiêu chí hoàn thành (Definition of Done).
>
> Trạng thái hiện tại (2026-08-07): **Phase 0 hoàn thành.** Supabase Postgres + R2 + Alembic đã kết nối và verify thật. Chưa có auth, chưa có ingestion, chưa có RAG — đó là Phase 1 trở đi.

---

## Phase 0 — Hạ tầng & môi trường ✅ HOÀN THÀNH

**Mục tiêu:** có đủ tài khoản/kết nối để mọi phase sau chạy được thật, không chỉ chạy trên giấy.

- [x] Tạo project Supabase (free tier) → bật extension `vector` + `uuid-ossp` → chạy `schema.sql` trong SQL Editor (bật RLS, không viết policy — chỉ khoá đường PostgREST/anon key, backend vẫn dùng role `postgres` nên bypass RLS)
- [x] Lấy connection string — dùng **Transaction pooler (port 6543)**
- [x] Tạo bucket Cloudflare R2 (`ai-tutor-documents`) + API token → verify bằng upload/read/delete object thật qua `boto3`
- [x] ~~Lấy `ANTHROPIC_API_KEY`~~ — đã đổi sang dùng `gpt-4o-mini` (OpenAI), tái sử dụng `OPENAI_API_KEY` đã có sẵn, không cần thêm vendor mới
- [x] Sinh `JWT_SECRET` bằng `openssl rand -hex 32` → điền `.env`
- [x] Điền toàn bộ biến trong `be/.env` (đối chiếu với `app/config.py`)
- [x] `alembic init -t async migrations`, wire `env.py` dùng chung `app.database.engine` (không tạo engine riêng), `target_metadata = Base.metadata` (import `app.models` để đăng ký hết model)
- [x] Migration baseline (`338222d0bfcf`) — autogenerate không còn diff nhờ siết lại type trong ORM models cho khớp 100% với `schema.sql` (Text, TIMESTAMP(timezone=True), BigInteger, Index/CheckConstraint tường minh) → `alembic stamp head`

**Lưu ý quan trọng phát sinh khi làm:** Supabase transaction pooler (6543) không hỗ trợ prepared statements — asyncpg mặc định có dùng, gây lỗi `DuplicatePreparedStatementError`. Đã fix bằng `connect_args={"statement_cache_size": 0}` trong `create_async_engine` ở `app/database.py`. Nếu sau này đổi sang session pooler hay direct connection thì có thể bỏ dòng này, nhưng để nguyên cũng không hại gì.

**DoD:** ✅ `SELECT 1` qua `app.database.engine` chạy được, `alembic current` trả về `338222d0bfcf (head)`, R2 upload/read/delete pass.

---

## Phase 1 — Auth module

**Vì sao làm trước:** mọi route khác đều cần `current_user`, làm sau sẽ phải sửa lại toàn bộ router.

**Việc cần làm:**
- `app/schemas/auth.py`: `SignupRequest`, `LoginRequest`, `TokenResponse` (access_token, token_type)
- `app/services/auth_service.py`:
  - `hash_password` / `verify_password` (passlib bcrypt)
  - `create_access_token(user_id)` — JWT, hạn `JWT_EXPIRE_MINUTES`
  - `decode_access_token(token)` — raise nếu hết hạn/sai chữ ký
- `app/dependencies.py` (mới): `get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User` — dùng làm `Depends()` cho mọi route cần login
- `app/routers/auth.py`:
  - `POST /api/auth/signup` — check email trùng → hash password → insert `users` → trả JWT luôn (khỏi bắt login lại)
  - `POST /api/auth/login` — verify password → trả JWT
  - `POST /api/auth/logout` — MVP: stateless JWT nên chỉ cần frontend xóa token; nếu muốn revoke thật thì cần bảng `refresh_tokens` (chưa có trong schema hiện tại — thêm sau nếu cần)
- Đăng ký `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")`

**DoD:** `curl -X POST /api/auth/signup` → nhận JWT → gọi 1 route bảo vệ thử (tạm thời thêm `GET /api/auth/me`) → trả đúng user.

---

## Phase 2 — Document upload (chưa cần ingestion, chỉ upload + lưu metadata)

**Việc cần làm:**
- `app/schemas/document.py`: `DocumentResponse` (id, filename, status, page_count, created_at…)
- `app/services/storage_service.py`:
  - `upload_file(file_bytes, key) -> None` — dùng `boto3` client trỏ `R2_ENDPOINT_URL`
  - `get_presigned_url(key, expires_in=3600) -> str`
  - `delete_file(key)`
- `app/routers/documents.py`:
  - `POST /api/documents` — nhận `UploadFile`, validate `file_type` (pdf/pptx) bằng extension + content-type, tạo `storage_key = f"documents/{user_id}/{document_id}/original.{ext}"`, upload lên R2, insert record `documents(status='pending')`, trả `202` kèm `document_id`
  - `GET /api/documents` — list theo `user_id`, `order by created_at desc`
  - `GET /api/documents/{id}` — 404 nếu không thuộc user
  - `DELETE /api/documents/{id}` — xóa record (cascade xóa pages/chunks) + xóa file trên R2

**Lưu ý:** validate kích thước file (vd giới hạn 20–50MB) để tránh nuốt hết R2 free tier/timeout khi parse.

**DoD:** Upload 1 file PDF thật qua Postman/curl → thấy record trong bảng `documents` với `status=pending` và file thật xuất hiện trong R2 bucket.

---

## Phase 3 — Ingestion pipeline (phase nặng nhất, tách test riêng trước khi nối vào chat)

**Việc cần làm:**
- `app/services/ingestion_service.py`:
  - `parse_pdf(file_bytes) -> list[PageContent]` — dùng `pypdf` lấy text; dùng `pdf2image` render từng trang ra PNG
  - `parse_pptx(file_bytes) -> list[PageContent]` — dùng `python-pptx` lấy text từng slide; render ảnh cần LibreOffice headless (`soffice --headless --convert-to png`) vì `python-pptx` không tự render ảnh — cân nhắc cài LibreOffice trong Docker image
  - `chunk_page(text, max_tokens=~300) -> list[str]` — chunk theo đoạn/câu, giữ ngữ nghĩa
  - `embed_chunks(chunks: list[str]) -> list[list[float]]` — gọi OpenAI embeddings (`EMBEDDING_MODEL`), batch để tiết kiệm request
- `app/workers/ingestion_worker.py`:
  - `run_ingestion(document_id)`:
    1. update `status='parsing'`
    2. tải file từ R2 → parse theo `file_type`
    3. với mỗi trang: upload thumbnail lên R2 (`thumbnail_key`) → insert `document_pages`
    4. update `status='embedding'`
    5. chunk toàn bộ trang → gọi embedding → insert `document_chunks` (kèm `embedding`, `page_number`, `bbox` nếu có)
    6. update `status='ready'`, `page_count`
    7. bắt exception ở mọi bước → `status='failed'`, `error_message=str(e)`
- Nối vào `POST /api/documents`: sau khi insert record → `background_tasks.add_task(run_ingestion, document_id)`
- `GET /api/documents/{id}/status` — trả `{status, error_message}` để frontend poll (hoặc để dành SSE ở phase sau nếu muốn)

**Test riêng trước khi làm chat:** viết 1 script/test thủ công chạy `run_ingestion` trực tiếp với 1 file PDF mẫu có sẵn trong `app/data/slide/`, kiểm tra bằng SQL:
```sql
select status, page_count from documents where id = '...';
select count(*) from document_pages where document_id = '...';
select count(*) from document_chunks where document_id = '...';
```

**DoD:** upload 1 file thật → sau vài giây `status` tự chuyển `pending → parsing → embedding → ready`, có đủ pages + chunks + embedding không null.

---

## Phase 4 — Document viewer API

**Việc cần làm:**
- `GET /api/documents/{id}/pages/{n}` — lấy `thumbnail_key` từ `document_pages`, trả presigned URL (không proxy file qua backend)
- (tuỳ chọn) `GET /api/documents/{id}/pages` — list toàn bộ trang kèm presigned URL, để frontend load 1 lần thay vì gọi từng trang

**DoD:** gọi endpoint trả về URL, mở URL đó trên browser thấy đúng ảnh trang/slide.

---

## Phase 5 — RAG orchestrator (chưa streaming, test logic trước)

**Việc cần làm:**
- `app/services/rag_service.py`:
  - `similarity_search(document_id, query_embedding, k=6) -> list[DocumentChunk]` — query pgvector: `order by embedding <=> :query_embedding limit :k`, filter `document_id`
  - `build_prompt(chunks, question) -> str` — system prompt yêu cầu chỉ trả lời dựa trên context, kèm tag `[Trang X]` để model tự trích dẫn
  - `ask(document_id, question) -> AnswerResult` — embed câu hỏi → similarity search → build prompt → gọi OpenAI Chat Completions API (`openai` SDK, model `gpt-4o-mini`, `stream=False` ở phase này) → parse citation từ response (regex tìm `[Trang X]` khớp với `page_number` của chunk đã dùng)
- Endpoint tạm để test: `POST /api/sessions/{id}/messages` (non-streaming trước, trả JSON thường)

**DoD:** hỏi 1 câu về nội dung file đã ingest ở Phase 3 → nhận câu trả lời đúng, có trích dẫn số trang hợp lệ.

---

## Phase 6 — Chuyển sang streaming (SSE)

**Việc cần làm:**
- Đổi `rag_service.ask()` thành generator/async generator dùng `client.chat.completions.create(..., stream=True)` của OpenAI SDK
- `app/routers/messages.py`: trả `StreamingResponse(media_type="text/event-stream")`, emit theo đúng format đã chốt trong guide:
  ```
  event: token     { "delta": "..." }
  event: citation  { "page_number": 4, "chunk_id": "...", "snippet": "..." }
  event: done       { "message_id": "...", "citations": [...] }
  ```
- Khi `done`: lưu `chat_messages` (role=assistant, content=full text ghép từ các token) + insert `message_citations`

**DoD:** dùng `curl -N` hoặc EventSource test thấy token chảy từng phần, không đợi full response.

---

## Phase 7 — Chat session CRUD (multi-session)

**Việc cần làm:**
- `app/schemas/session.py`: `SessionCreate`, `SessionResponse`, `SessionUpdate`
- `app/routers/sessions.py`:
  - `POST /api/sessions` — tạo với `document_id` (+ `title` mặc định `"New chat"`)
  - `GET /api/sessions` — list theo user, `order by updated_at desc`
  - `GET /api/sessions/{id}` / `PATCH /api/sessions/{id}` (đổi `title`) / `DELETE /api/sessions/{id}`
  - `GET /api/sessions/{id}/messages` — phân trang (`limit`/`offset` hoặc cursor theo `created_at`)
- Nối `POST /api/sessions/{id}/messages` (Phase 5/6) vào đúng `session_id` thay vì thẳng `document_id` — lấy `document_id` từ session để search

**DoD:** tạo 2 session cho cùng 1 document → chat riêng từng session → lịch sử không lẫn nhau.

---

## Phase 8 — Citation resolver + frontend highlight

**Việc cần làm (backend phần còn lại):** đảm bảo mỗi `event: citation` trả đủ `page_number` để frontend gọi `highlightRegion(page_number)`. Nếu muốn highlight vùng cụ thể (không chỉ cả trang) thì cần bắt đầu điền cột `document_chunks.bbox` ở Phase 3 (hiện schema đã có sẵn cột này, MVP có thể bỏ qua và chỉ highlight nguyên trang).

**DoD:** trong lúc AI đang trả lời, panel trái tự cuộn/highlight đúng trang được trích dẫn — test bằng tay trên frontend thật (không chỉ test API).

---

## Phase 9 — Frontend (React, 2 panel)

**Việc cần làm (tổng quan, có thể tách plan riêng khi tới lúc):**
- Layout 2 cột: viewer trái (render ảnh trang từ `GET /pages/{n}`, có `highlightRegion(page)`), chat phải
- Trang login/signup, lưu JWT (localStorage hoặc httpOnly cookie nếu muốn an toàn hơn), gắn `Authorization: Bearer` cho mọi request qua `axios` interceptor
- Upload modal → poll `status` hoặc lắng nghe SSE cho tới khi `ready`
- Session sidebar (list, tạo mới, đổi tên, xóa)
- Khung chat: gửi câu hỏi → `EventSource`/`fetch` streaming → render token dần, khi nhận `citation` thì gọi `highlightRegion`

**DoD:** luồng end-to-end thật trên browser: đăng ký → đăng nhập → upload PDF → chờ ready → hỏi → thấy trả lời stream + trang tự highlight.

---

## Phase 10 — Hardening & vận hành

- [ ] Rate limit route `/api/sessions/{id}/messages` (tránh spam OpenAI API tốn tiền)
- [ ] Giới hạn dung lượng/số file upload mỗi user (free tier Supabase 500MB, R2 10GB)
- [ ] Log lỗi ingestion rõ ràng (`error_message`) để debug khi parser fail với PPTX lạ
- [ ] GitHub Action ping định kỳ (tránh Supabase free tier tự pause sau 7 ngày không request)
- [ ] Viết `alembic` migration chính thức thay vì chạy tay `schema.sql` (để version control schema)
- [ ] CORS: đổi `allow_origins=["*"]` thành domain thật trước khi public

---

## Thứ tự khuyến nghị tóm tắt

```
Phase 0 (hạ tầng) → Phase 1 (auth) → Phase 2 (upload) → Phase 3 (ingestion, test riêng)
→ Phase 4 (viewer) → Phase 5 (RAG non-stream) → Phase 6 (streaming)
→ Phase 7 (session CRUD) → Phase 8 (citation highlight) → Phase 9 (frontend) → Phase 10 (hardening)
```

Mỗi phase nên merge/commit riêng, test bằng `curl`/Postman trước khi chuyển phase tiếp theo — đặc biệt Phase 3 (ingestion) nên test độc lập bằng script trước khi nối vào API, vì đây là phase dễ lỗi nhất (parser PDF/PPTX, LibreOffice, rate limit embedding API).
