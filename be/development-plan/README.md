# AI Tutor — Kế hoạch phát triển chi tiết

> Dựa trên `ai-tutor-implementation-guide.md` (kiến trúc đã chốt) và `schema.sql` (schema đã thiết kế). Mỗi phase là 1 file riêng trong thư mục này, làm tuần tự, mỗi phase có: mục tiêu, việc cần làm, file đụng tới, tiêu chí hoàn thành (Definition of Done).

## Nguyên tắc xuyên suốt dự án

Đây là dự án học sâu về AI — không chỉ để "chạy được". **Mọi phần đụng trực tiếp tới chất lượng và độ an toàn của AI** (ingestion/embedding ở [Phase 3](phase-3-ingestion.md), RAG core + nâng cao ở [Phase 5](phase-5-rag-orchestrator.md)/[5.5](phase-5.5-advanced-rag.md), guardrail + observability ở [Phase 5.6](phase-5.6-guardrails-observability.md), multi-turn ở [Phase 6](phase-6-chat-sessions.md), streaming ở [Phase 7](phase-7-streaming.md), citation ở [Phase 8](phase-8-citation-highlight.md)) đều triển khai ở mức chuyên nghiệp đầy đủ, có đo lường/kiểm chứng thật (xem nguyên tắc "đo trước, tối ưu sau" ở Phase 5.5) — không rút gọn kiểu "tạm bợ chạy được". Chất lượng câu trả lời (5.5) và an toàn hệ thống (5.6) là 2 trụ cột riêng biệt, cả 2 đều bắt buộc — 1 hệ thống RAG trả lời hay nhưng không có guardrail vẫn không phải hệ thống chuyên nghiệp.

Các phần hạ tầng thuần túy không trực tiếp quyết định chất lượng AI (auth, upload, vận hành...) vẫn áp dụng nguyên tắc "đủ dùng, không over-engineer" như đã làm có chủ đích ở JWT ([Phase 1.5](phase-1.5-jwt-hardening.md) có hẳn 1 bảng ghi lại những gì cố ý KHÔNG làm và lý do) — 2 nguyên tắc này không mâu thuẫn nhau, chỉ khác phạm vi áp dụng.

## Trạng thái hiện tại (2026-08-18)

**Phase 0 → Phase 5.6 hoàn thành.** Supabase Postgres (Singapore) + R2 + Alembic đã kết nối và verify thật. Auth đầy đủ (signup/login/refresh/logout/me) với refresh token thu hồi được thật + rate limit `/login`; document upload/list/get/delete/status/file — toàn bộ ingestion pipeline (pypdf/mistral_ocr/hybrid + PPTX→PDF) đã chạy end-to-end với dữ liệu thật. **Phase 5.5 (Advanced RAG)** đã xong toàn bộ 9 bước + 1 bước phát sinh, mỗi bước đều đo bằng dữ liệu thật trước khi quyết định đưa vào production hay không: **đã đưa vào `ask()`** — reranking (cross-encoder đa ngôn ngữ, cải thiện rõ trên tài liệu dài), chuyển sang Groq (miễn phí, chất lượng ngang OpenAI), grounding/faithfulness verification (guardrail thật, có retry + fallback an toàn), phòng vệ prompt injection gián tiếp; **đã thử nhưng KHÔNG đưa vào** (có số liệu chứng minh không đạt) — hybrid search, query transformation, semantic caching. **Phase 5.6 (Guardrails, Safety & Observability)** đã xong 12/12 mục bắt buộc: input/output moderation, phòng vệ jailbreak trực tiếp (2 vòng vá thật), scope enforcement (đo, không đạt), hành vi khi faithfulness fail, quota/budget/circuit breaker theo user và toàn hệ thống, structured logging + prompt versioning có enforcement tự động, structured citation (bỏ regex), feedback loop 👍/👎. Phát hiện phụ đáng chú ý: bug index ivfflat gây mất 14% kết quả retrieval (đã sửa), Groq đổi/gỡ model 2 lần giữa phiên (bằng chứng thật cho rủi ro single-provider). Tiếp theo: **Phase 6 (Chat session CRUD + multi-turn)**.

## Danh sách các phase

- [Phase 0 — Hạ tầng & môi trường](phase-0-infrastructure.md) ✅ Hoàn thành
- [Phase 1 — Auth module](phase-1-auth.md) ✅ Hoàn thành
- [Phase 1.5 — JWT Hardening](phase-1.5-jwt-hardening.md) ✅ Hoàn thành
- [Phase 2 — Document upload](phase-2-document-upload.md) ✅ Hoàn thành
- [Phase 3 — Ingestion pipeline](phase-3-ingestion.md) ✅ Hoàn thành
- [Phase 4 — Document viewer API](phase-4-viewer-api.md) ✅ Hoàn thành
- [Phase 5 — RAG orchestrator (baseline)](phase-5-rag-orchestrator.md) ✅ Hoàn thành
- [Phase 5.5 — Advanced RAG (retrieval quality, faithfulness & evaluation)](phase-5.5-advanced-rag.md) ✅ Hoàn thành
- [Phase 5.6 — Guardrails, Safety & Observability](phase-5.6-guardrails-observability.md) ✅ Hoàn thành
- [Phase 6 — Chat session CRUD + multi-turn](phase-6-chat-sessions.md)
- [Phase 7 — Streaming (SSE)](phase-7-streaming.md)
- [Phase 8 — Citation resolver + frontend highlight](phase-8-citation-highlight.md)
- [Phase 9 — Frontend (React, 2 panel)](phase-9-frontend.md)
- [Phase 10 — Hardening & vận hành](phase-10-hardening.md)

## Thứ tự khuyến nghị tóm tắt

```
Phase 0 (hạ tầng) → Phase 1 (auth) → Phase 2 (upload) → Phase 3 (ingestion, test riêng)
→ Phase 4 (viewer) → Phase 5 (RAG baseline, non-stream) → Phase 5.5 (RAG nâng cao, có đo lường)
→ Phase 5.6 (guardrail + observability) → Phase 6 (session CRUD + multi-turn) → Phase 7 (streaming)
→ Phase 8 (citation highlight) → Phase 9 (frontend) → Phase 10 (hardening)
```

**Lưu ý thứ tự Phase 6/7 đã đổi so với ban đầu** (session CRUD giờ đi TRƯỚC streaming, không phải sau) — lý do kỹ thuật cụ thể ghi ở đầu file [Phase 6](phase-6-chat-sessions.md).

Mỗi phase nên merge/commit riêng, test bằng `curl`/Postman trước khi chuyển phase tiếp theo — đặc biệt Phase 3 (ingestion) nên test độc lập bằng script trước khi nối vào API, vì đây là phase dễ lỗi nhất (parser PDF/PPTX, LibreOffice, rate limit embedding API).
