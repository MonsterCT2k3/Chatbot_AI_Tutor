# AI Tutor — Kế hoạch phát triển chi tiết

> Dựa trên `ai-tutor-implementation-guide.md` (kiến trúc đã chốt) và `schema.sql` (schema đã thiết kế). Tài liệu này chia nhỏ thành các phase có thể làm tuần tự, mỗi phase có: mục tiêu, việc cần làm, file đụng tới, tiêu chí hoàn thành (Definition of Done).
>
> Trạng thái hiện tại (2026-08-07): **Phase 0 + Phase 1 + Phase 2 hoàn thành.** Supabase Postgres (Singapore) + R2 + Alembic đã kết nối và verify thật. Auth (signup/login/me/logout) và document upload/list/get/delete chạy đầy đủ, đã test end-to-end với file PDF thật. Chưa có ingestion (parse/chunk/embed) hay RAG — đó là Phase 3 trở đi.

---

## Phase 0 — Hạ tầng & môi trường ✅ HOÀN THÀNH

**Mục tiêu:** có đủ tài khoản/kết nối để mọi phase sau chạy được thật, không chỉ chạy trên giấy.

- [x] Tạo project Supabase (free tier) → bật extension `vector` + `uuid-ossp` → chạy `schema.sql` trong SQL Editor (bật RLS, không viết policy — chỉ khoá đường PostgREST/anon key, backend vẫn dùng role `postgres` nên bypass RLS)
- [x] Lấy connection string — dùng **Transaction pooler (port 6543)**. ⚠️ Project ban đầu tạo ở Seoul (`ap-northeast-2`) — đo latency thấy quá chậm (cold connect ~2.2s, query ấm ~700ms) nên đã **tạo lại project mới ở Singapore (`ap-southeast-1`)** và chuyển hẳn sang (chạy lại `schema.sql`, `alembic stamp head`). Project Seoul cũ không còn dùng, có thể xoá.
- [x] Tạo bucket Cloudflare R2 (`ai-tutor-documents`) + API token → verify bằng upload/read/delete object thật qua `boto3`
- [x] ~~Lấy `ANTHROPIC_API_KEY`~~ — đã đổi sang dùng `gpt-4o-mini` (OpenAI), tái sử dụng `OPENAI_API_KEY` đã có sẵn, không cần thêm vendor mới
- [x] Sinh `JWT_SECRET` bằng `openssl rand -hex 32` → điền `.env`
- [x] Điền toàn bộ biến trong `be/.env` (đối chiếu với `app/config.py`)
- [x] `alembic init -t async migrations`, wire `env.py` dùng chung `app.database.engine` (không tạo engine riêng), `target_metadata = Base.metadata` (import `app.models` để đăng ký hết model)
- [x] Migration baseline (`338222d0bfcf`) — autogenerate không còn diff nhờ siết lại type trong ORM models cho khớp 100% với `schema.sql` (Text, TIMESTAMP(timezone=True), BigInteger, Index/CheckConstraint tường minh) → `alembic stamp head`

**Lưu ý quan trọng phát sinh khi làm:** Supabase transaction pooler (6543) không hỗ trợ prepared statements — asyncpg mặc định có dùng, gây lỗi `DuplicatePreparedStatementError`. Đã fix bằng `connect_args={"statement_cache_size": 0}` trong `create_async_engine` ở `app/database.py`. Nếu sau này đổi sang session pooler hay direct connection thì có thể bỏ dòng này, nhưng để nguyên cũng không hại gì.

**Lưu ý về performance:** Ban đầu có bật `pool_pre_ping=True` (khuyến nghị mặc định để tránh lỗi "connection đã chết") nhưng nó thêm 1 round-trip mạng phụ mỗi lần checkout connection — đo được làm chậm request gần gấp đôi (~700ms → ~300-400ms sau khi bỏ). Đã bỏ `pool_pre_ping` khỏi `app/database.py`. Đánh đổi: nếu Supabase tự đóng connection nhàn rỗi, request đó có thể lỗi 1 lần rồi các request sau tự ổn — chấp nhận được ở giai đoạn MVP.

**DoD:** ✅ `SELECT 1` qua `app.database.engine` chạy được, `alembic current` trả về `338222d0bfcf (head)`, R2 upload/read/delete pass.

---

## Phase 1 — Auth module ✅ HOÀN THÀNH

**Vì sao làm trước:** mọi route khác đều cần `current_user`, làm sau sẽ phải sửa lại toàn bộ router.

**9 bước, làm và test từng bước trước khi qua bước tiếp theo:**

- [x] **1.1 Password hashing** — `hash_password`/`verify_password` trong `app/services/auth_service.py`. Ban đầu dùng `passlib[bcrypt]` theo kế hoạch nhưng **passlib không tương thích với bcrypt >=4** (thư viện passlib đã ngừng phát triển từ 2020) → đổi sang gọi thẳng package `bcrypt`, bỏ passlib khỏi `requirements.txt`.
- [x] **1.2 JWT create/decode** — `create_access_token(user_id)`, `decode_access_token(token)` trong `auth_service.py`. Test: token hợp lệ, token hết hạn, token sai chữ ký đều raise đúng.
- [x] **1.3 Pydantic schemas** — `app/schemas/auth.py`: `SignupRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`. Cần thêm `pydantic[email]` (package `email-validator`) cho `EmailStr`.
- [x] **1.4 `get_current_user` dependency** — `app/dependencies.py`: `OAuth2PasswordBearer` + `get_current_user(token, db) -> User`, raise 401 nếu token invalid/user không tồn tại.
- [x] **1.5 `POST /api/auth/signup`**
- [x] **1.6 `POST /api/auth/login`**
- [x] **1.7 `GET /api/auth/me`** — route bảo vệ, verify dependency hoạt động đúng.
- [x] **1.8 `POST /api/auth/logout`** — MVP stateless, chỉ cần token hợp lệ để gọi, không revoke gì server-side (token cũ vẫn dùng được tới khi hết hạn — đã verify đúng ý đồ thiết kế qua test).
- [x] **1.9 Test end-to-end toàn bộ luồng** — 10 cases (signup, duplicate signup, login đúng/sai, /me có/không/sai token, logout có/không token, xác nhận token còn sống sau logout) — tất cả PASS.

**Việc phát sinh ngoài 9 bước gốc (làm thêm trong Phase 1 vì cần thiết cho production-readiness):**
- **Chuẩn hoá response envelope toàn cục** — mọi response (thành công lẫn lỗi) đều có dạng `{success, message, data, error, requestId}` (`app/middleware.py` + `app/exceptions.py`), áp dụng tự động cho mọi route hiện tại và tương lai.
- **Tách logic nghiệp vụ khỏi router** — router chỉ lo HTTP (parse request, chọn status code), toàn bộ business logic + DB access nằm trong `auth_service.py` (mô hình gần giống Controller/Service của Spring, không có tầng Repository riêng vì `AsyncSession` của SQLAlchemy đã đóng vai trò đó).

**DoD:** ✅ Toàn bộ 9 bước + test end-to-end đều pass qua HTTP thật (không chỉ test nội bộ).

---

## Phase 2 — Document upload ✅ HOÀN THÀNH

**9 bước, làm và test từng bước trước khi qua bước tiếp theo (giống Phase 1):**

- [x] **2.1 `storage_service.upload_file()`** — wrapper `boto3` upload lên R2. **Lưu ý quan trọng:** `boto3` là thư viện blocking (đồng bộ) — gọi trực tiếp trong route `async def` sẽ đứng hình toàn bộ event loop (mọi request khác cũng bị chặn). Đã bọc bằng `starlette.concurrency.run_in_threadpool`.
- [x] **2.2 `storage_service.get_presigned_url()`** — sinh URL tạm thời để đọc file mà không cần public bucket. Đây chỉ là ký (sign) cục bộ, không gọi mạng tới R2 → không cần `run_in_threadpool`. Đã verify bucket KHÔNG public (URL không ký bị từ chối 400).
- [x] **2.3 `storage_service.delete_file()`** — gọi mạng thật nên vẫn cần `run_in_threadpool`.
- [x] **2.4 `schemas/document.py`: `DocumentResponse`** — không lộ `storage_key`/`user_id`/`metadata` (giống nguyên tắc không lộ `hashed_password` ở Phase 1).
- [x] **2.5 `POST /api/documents`** — logic thật (validate + upload + insert) nằm trong `document_service.create_document()` (Service layer), không phải trong router. Thứ tự cố ý: upload R2 **trước**, insert DB **sau** — nếu upload lỗi thì không có row rác trong DB.
- [x] **2.6 `GET /api/documents`** — chỉ query đơn giản (lọc + sắp xếp), không có logic quyết định → để thẳng trong router, không tạo service function (giống bài học "get_user_by_id là thừa" ở Phase 1).
- [x] **2.7 `GET /api/documents/{id}`** — 404 giống hệt nhau (byte-for-byte, đã test) cho cả 2 trường hợp "không tồn tại" và "của người khác", tránh lộ thông tin.
- [x] **2.8 `DELETE /api/documents/{id}`** — tách `get_owned_document()` dùng chung cho cả 2.7 và 2.8 (khác với `get_user_by_id`: ở đây có ≥2 nơi gọi thật nên tách ra là hợp lý, không phải abstraction thừa).
- [x] **2.9 Test end-to-end** — 12 case, tất cả PASS, bao gồm test 2 user riêng biệt để xác nhận không lộ dữ liệu chéo.

**Lưu ý:** giới hạn file 50MB, check cả extension lẫn `content_type` trước khi chấp nhận.

**DoD:** ✅ Toàn bộ 9 bước pass qua HTTP thật (in-process test client gọi qua ASGI, tương đương HTTP thật), có test với PDF thật (`app/data/slide/b3.pdf`) upload lên R2 thật.

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
