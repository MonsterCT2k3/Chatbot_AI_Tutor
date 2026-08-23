[← Back to overview](README.md)

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

[← Back to overview](README.md) · [Next: Phase 1 — Auth module →](phase-1-auth.md)
