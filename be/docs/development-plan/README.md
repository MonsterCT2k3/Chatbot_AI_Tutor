# AI Tutor — Kế hoạch phát triển chi tiết

> Dựa trên `ai-tutor-implementation-guide.md` (kiến trúc đã chốt) và `schema.sql` (schema đã thiết kế). Mỗi phase là 1 file riêng trong thư mục này, làm tuần tự, mỗi phase có: mục tiêu, việc cần làm, file đụng tới, tiêu chí hoàn thành (Definition of Done).

## Nguyên tắc xuyên suốt dự án

Đây là dự án học sâu về AI — không chỉ để "chạy được". **Mọi phần đụng trực tiếp tới chất lượng và độ an toàn của AI** (ingestion/embedding ở [Phase 3](phase-3-ingestion.md), RAG core + nâng cao ở [Phase 5](phase-5-rag-orchestrator.md)/[5.5](phase-5.5-advanced-rag.md), guardrail + observability ở [Phase 5.6](phase-5.6-guardrails-observability.md), multi-turn ở [Phase 6](phase-6-chat-sessions.md), streaming ở [Phase 7](phase-7-streaming.md), citation ở [Phase 8](phase-8-citation-highlight.md)) đều triển khai ở mức chuyên nghiệp đầy đủ, có đo lường/kiểm chứng thật (xem nguyên tắc "đo trước, tối ưu sau" ở Phase 5.5) — không rút gọn kiểu "tạm bợ chạy được". Chất lượng câu trả lời (5.5) và an toàn hệ thống (5.6) là 2 trụ cột riêng biệt, cả 2 đều bắt buộc — 1 hệ thống RAG trả lời hay nhưng không có guardrail vẫn không phải hệ thống chuyên nghiệp.

Các phần hạ tầng thuần túy không trực tiếp quyết định chất lượng AI (auth, upload, vận hành...) vẫn áp dụng nguyên tắc "đủ dùng, không over-engineer" như đã làm có chủ đích ở JWT ([Phase 1.5](phase-1.5-jwt-hardening.md) có hẳn 1 bảng ghi lại những gì cố ý KHÔNG làm và lý do) — 2 nguyên tắc này không mâu thuẫn nhau, chỉ khác phạm vi áp dụng.

## Trạng thái hiện tại (2026-08-25)

**Backend: Phase 0 → Phase 8 hoàn thành.** Phase 6 session + multi-turn; Phase 7 SSE (status/token/citation/replace/done), xoá `/ask` hỏi (giữ feedback + `ask()` eval); Phase 8 citation UX (auto-jump, chip/viền trang, spike + wire `bbox`).

**Frontend ([Phase 9](phase-9-frontend.md)):** khung dựng sớm; đã nối session + SSE + citation/bbox. **DoD E2E lõi đã đạt.** Còn checklist dọn tùy chọn (đổi tên session UI, comment cũ, mock quota, sync doc) — xem file Phase 9.

**Ghi chú cũ vẫn đúng:** thumbnail trang 1 + CORS R2 đã xử lý lúc làm FE sớm.

Tiếp theo: dọn sót Phase 9 (nếu muốn đóng sạch) và/hoặc **[Phase 10 — Hardening](phase-10-hardening.md)**.

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
- [Phase 6 — Chat session CRUD + multi-turn](phase-6-chat-sessions.md) ✅ Hoàn thành
- [Phase 7 — Streaming (SSE)](phase-7-streaming.md) ✅ Hoàn thành
- [Phase 8 — Citation UX trên viewer (jump + overlay + bbox)](phase-8-citation-highlight.md) ✅ Hoàn thành
- [Phase 9 — Frontend (React)](phase-9-frontend.md) ✅ DoD E2E đạt — còn checklist dọn 9.1–9.4 (tuỳ chọn)
- [Phase 10 — Hardening & vận hành](phase-10-hardening.md) ← tiếp theo / song song dọn Phase 9

## Thứ tự khuyến nghị tóm tắt

```
Phase 0 (hạ tầng) → Phase 1 (auth) → Phase 2 (upload) → Phase 3 (ingestion, test riêng)
→ Phase 4 (viewer) → Phase 5 (RAG baseline, non-stream) → Phase 5.5 (RAG nâng cao, có đo lường)
→ Phase 5.6 (guardrail + observability) → Phase 6 (session CRUD + multi-turn) → Phase 7 (streaming)
→ Phase 8 (citation highlight) → Phase 9 (frontend) → Phase 10 (hardening)
```

**Lưu ý thứ tự Phase 6/7 đã đổi so với ban đầu** (session CRUD giờ đi TRƯỚC streaming, không phải sau) — lý do kỹ thuật cụ thể ghi ở đầu file [Phase 6](phase-6-chat-sessions.md).

**Lưu ý Phase 9 (frontend) đã làm sớm, không theo thứ tự trên.** Phần không phụ thuộc Phase 6/7/8 (auth, dashboard, viewer PDF, chat non-streaming) đã dựng và chạy thật; phần còn lại chờ backend tương ứng rồi nối vào. Đánh đổi đã chấp nhận: có giao diện thật để dùng và soi lỗi backend sớm hơn, đổi lại phải quay lại sửa frontend thêm 1 lượt sau mỗi phase 6/7/8. Thực tế cách này đã sinh lợi ngay: chính lúc dựng frontend mới lộ ra bucket R2 thiếu CORS và việc bắt trình duyệt tải cả file PDF chỉ để hiện ảnh bìa — hai thứ test bằng `curl` không thể phát hiện.

Mỗi phase nên merge/commit riêng, test bằng `curl`/Postman trước khi chuyển phase tiếp theo — đặc biệt Phase 3 (ingestion) nên test độc lập bằng script trước khi nối vào API, vì đây là phase dễ lỗi nhất (parser PDF/PPTX, LibreOffice, rate limit embedding API).
