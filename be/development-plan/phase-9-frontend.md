[← Back to overview](README.md)

## Phase 9 — Frontend (React, 2 panel)

**Việc cần làm (tổng quan, có thể tách plan riêng khi tới lúc):**
- Layout 2 cột: viewer trái dùng `PDF.js`/`react-pdf` load file PDF từ `GET /api/documents/{id}/file` (xem [Phase 4](phase-4-viewer-api.md) — quyết định dùng PDF.js thay vì ảnh tĩnh để vẫn copy/select text được), có `highlightRegion(page)`, chat phải
- Trang login/signup, lưu JWT (localStorage hoặc httpOnly cookie nếu muốn an toàn hơn), gắn `Authorization: Bearer` cho mọi request qua `axios` interceptor
- Upload modal → poll `status` hoặc lắng nghe SSE cho tới khi `ready`
- Session sidebar (list, tạo mới, đổi tên, xóa)
- Khung chat: gửi câu hỏi → `EventSource`/`fetch` streaming → render token dần, khi nhận `citation` thì gọi `highlightRegion`

**DoD:** luồng end-to-end thật trên browser: đăng ký → đăng nhập → upload PDF → chờ ready → hỏi → thấy trả lời stream + trang tự highlight.

---

[← Previous: Phase 8](phase-8-citation-highlight.md) · [Back to overview](README.md) · [Next: Phase 10 — Hardening →](phase-10-hardening.md)
