# AI Tutor K3

Chatbot RAG cho phép sinh viên hỏi-đáp trực tiếp với AI dựa trên nội dung tài liệu/slide bài giảng (PDF/PPTX) đã tải lên — có trích dẫn trang chính xác, kiểm tra độ trung thực câu trả lời, và các lớp guardrail an toàn/chi phí.

- **Backend**: `be/` — FastAPI + Supabase Postgres (pgvector) + Cloudflare R2 + Groq/OpenAI
- **Frontend**: `fe/` — React 18 + Vite + React Router

Tài liệu chi tiết hơn: [`be/development-plan/README.md`](be/development-plan/README.md) (kế hoạch/trạng thái từng phase) và [`be/explain-logic/README.md`](be/explain-logic/README.md) (giải thích lý do/luồng code từng bước).

## Yêu cầu hệ thống

| | Phiên bản đã dùng |
|---|---|
| Python | 3.14 |
| Node.js | 22 |
| npm | 9+ |

Database (Supabase Postgres) và file storage (Cloudflare R2) đã được provision sẵn — không cần cài đặt gì thêm, chỉ cần đúng connection string trong `be/.env`.

## 1. Chạy Backend

```bash
cd be
source .venv/bin/activate          # nếu chưa có venv: python3.14 -m venv .venv
pip install -r requirements.txt    # chỉ cần khi requirements.txt vừa đổi

alembic upgrade head               # áp dụng migration DB mới nhất (an toàn, chạy lại nhiều lần không sao)

uvicorn app.main:app --reload --port 8000
```

Backend chạy tại `http://localhost:8000` — API docs tự sinh (Swagger UI) tại `http://localhost:8000/docs`, thử endpoint trực tiếp trên đó mà không cần Postman.

### Biến môi trường (`be/.env` — không commit, đã có sẵn trên máy này)

```
OPENAI_API_KEY=...       # embedding + moderation + judge chấm điểm
GROQ_API_KEY=...         # model sinh câu trả lời chính (miễn phí)
MISTRAL_API_KEY=...      # OCR cho PDF scan
DATABASE_URL=...         # Supabase Postgres (asyncpg connection string)
R2_ACCOUNT_ID=...        # Cloudflare R2 — lưu file PDF/PPTX gốc
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=...
R2_ENDPOINT_URL=...
JWT_SECRET=...           # ký access/refresh token
```

Thiếu bất kỳ key nào ở trên, phần liên quan sẽ lỗi lúc gọi (không lỗi ngay lúc khởi động, vì đọc bằng `pydantic-settings` với default rỗng).

## 2. Chạy Frontend

```bash
cd fe
npm install     # chỉ cần khi package.json vừa đổi
npm run dev
```

Frontend chạy tại `http://localhost:5173` — mặc định gọi backend ở `http://localhost:8000/api` (đổi bằng biến `VITE_API_BASE_URL` trong `fe/.env` nếu backend chạy port/host khác).

**Cần chạy backend TRƯỚC** — trang đăng nhập/đăng ký cần API thật để hoạt động, không có chế độ mock trong app.

## 3. Thử luồng cơ bản

1. Mở `http://localhost:5173/signup` → tạo tài khoản thật (lưu vào Supabase Postgres thật).
2. Tự động chuyển vào Dashboard (đang xây, xem trạng thái bên dưới).
3. Muốn thử API độc lập, không qua giao diện: mở `http://localhost:8000/docs`, thử `POST /api/documents` (upload PDF/PPTX) rồi `POST /api/documents/{id}/ask`.

## Trạng thái hiện tại

- **Backend**: Phase 0 → 5.6 hoàn thành (auth, ingestion, RAG nâng cao có đo lường thật, đầy đủ guardrail an toàn/chi phí/observability). Chi tiết: [`be/development-plan/README.md`](be/development-plan/README.md).
- **Frontend**: đang dựng lại từ đầu theo thiết kế trong `fe/src/mock_html_ui/` — đã xong `SignInPage`/`SignUpPage` (nối API thật), Dashboard và màn hỏi-đáp (workspace 3-panel) đang làm tiếp.
- Multi-turn/session (Phase 6), streaming (Phase 7) chưa làm — `/documents/{id}/ask` hiện là endpoint tạm, mỗi câu hỏi độc lập, không lưu lịch sử hội thoại.

## Gỡ lỗi thường gặp

- **`alembic upgrade head` báo lỗi kết nối** — kiểm tra `DATABASE_URL` trong `be/.env`, và mạng có ra được Supabase (Singapore) không.
- **Backend chạy nhưng gọi `/ask` lỗi/timeout** — khả năng cao do hết quota Groq free tier (đã gặp thật, xem `be/explain-logic/phase-5.6-guardrails-observability/5.6.5-faithfulness-failure-behavior.md`) — kiểm tra log server để rõ lỗi thật.
- **Lỗi CORS** — hiện `be/app/main.py` đang mở `allow_origins=["*"]` (cho phép mọi origin, có comment nhắc "In production, restrict this to the frontend URL") nên không nên gặp lỗi CORS lúc dev — nếu vẫn gặp, khả năng cao là backend chưa chạy chứ không phải do CORS.
