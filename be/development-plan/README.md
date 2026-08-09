# AI Tutor — Kế hoạch phát triển chi tiết

> Dựa trên `ai-tutor-implementation-guide.md` (kiến trúc đã chốt) và `schema.sql` (schema đã thiết kế). Mỗi phase là 1 file riêng trong thư mục này, làm tuần tự, mỗi phase có: mục tiêu, việc cần làm, file đụng tới, tiêu chí hoàn thành (Definition of Done).

## Trạng thái hiện tại (2026-08-08)

**Phase 0 + Phase 1 + Phase 1.5 + Phase 2 hoàn thành.** Supabase Postgres (Singapore) + R2 + Alembic đã kết nối và verify thật. Auth đầy đủ (signup/login/refresh/logout/me) với refresh token thu hồi được thật + rate limit `/login`, và document upload/list/get/delete — cả 2 đã test end-to-end với dữ liệu thật. Quay lại **Phase 3 (ingestion)** tiếp theo.

## Danh sách các phase

- [Phase 0 — Hạ tầng & môi trường](phase-0-infrastructure.md) ✅ Hoàn thành
- [Phase 1 — Auth module](phase-1-auth.md) ✅ Hoàn thành
- [Phase 1.5 — JWT Hardening](phase-1.5-jwt-hardening.md) ✅ Hoàn thành
- [Phase 2 — Document upload](phase-2-document-upload.md) ✅ Hoàn thành
- [Phase 3 — Ingestion pipeline](phase-3-ingestion.md) ⏳ Đang làm
- [Phase 4 — Document viewer API](phase-4-viewer-api.md)
- [Phase 5 — RAG orchestrator](phase-5-rag-orchestrator.md)
- [Phase 6 — Streaming (SSE)](phase-6-streaming.md)
- [Phase 7 — Chat session CRUD](phase-7-chat-sessions.md)
- [Phase 8 — Citation resolver + frontend highlight](phase-8-citation-highlight.md)
- [Phase 9 — Frontend (React, 2 panel)](phase-9-frontend.md)
- [Phase 10 — Hardening & vận hành](phase-10-hardening.md)

## Thứ tự khuyến nghị tóm tắt

```
Phase 0 (hạ tầng) → Phase 1 (auth) → Phase 2 (upload) → Phase 3 (ingestion, test riêng)
→ Phase 4 (viewer) → Phase 5 (RAG non-stream) → Phase 6 (streaming)
→ Phase 7 (session CRUD) → Phase 8 (citation highlight) → Phase 9 (frontend) → Phase 10 (hardening)
```

Mỗi phase nên merge/commit riêng, test bằng `curl`/Postman trước khi chuyển phase tiếp theo — đặc biệt Phase 3 (ingestion) nên test độc lập bằng script trước khi nối vào API, vì đây là phase dễ lỗi nhất (parser PDF/PPTX, LibreOffice, rate limit embedding API).
