[← Back to overview](README.md)

## Phase 8 — Citation resolver + frontend highlight

**Việc cần làm (backend phần còn lại):** đảm bảo mỗi `event: citation` trả đủ `page_number` để frontend gọi PDF.js nhảy tới đúng trang (`highlightRegion(page_number)`, xem quyết định dùng PDF.js thay vì ảnh tĩnh ở [Phase 4](phase-4-viewer-api.md)). Nếu muốn highlight vùng cụ thể (không chỉ cả trang) thì cần bắt đầu điền cột `document_chunks.bbox` ở Phase 3 (hiện schema đã có sẵn cột này, MVP có thể bỏ qua và chỉ nhảy tới/nhấn mạnh cả trang).

**DoD:** trong lúc AI đang trả lời, panel trái tự cuộn/highlight đúng trang được trích dẫn — test bằng tay trên frontend thật (không chỉ test API).

---

[← Previous: Phase 7](phase-7-chat-sessions.md) · [Back to overview](README.md) · [Next: Phase 9 — Frontend →](phase-9-frontend.md)
