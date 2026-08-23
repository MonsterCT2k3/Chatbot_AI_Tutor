[← Back to overview](README.md)

## Phase 8 — Citation resolver + frontend highlight

**Việc cần làm (backend phần còn lại):** đảm bảo mỗi `event: citation` trả đủ `page_number` để frontend gọi PDF.js nhảy tới đúng trang (`highlightRegion(page_number)`, xem quyết định dùng PDF.js thay vì ảnh tĩnh ở [Phase 4](phase-4-viewer-api.md)). Nếu muốn highlight vùng cụ thể (không chỉ cả trang) thì cần bắt đầu điền cột `document_chunks.bbox` ở Phase 3 (hiện schema đã có sẵn cột này, chưa được điền — Phase 3 hiện tại chỉ nhảy tới/nhấn mạnh cả trang).

**Cân nhắc (chưa quyết định):** đây là 1 phần liên quan tới trải nghiệm hiển thị hơn là chất lượng lõi của AI (retrieval/generation) — có thể cân nhắc quay lại bổ sung `bbox` cho Phase 3 (cần 1 công cụ trích tọa độ chữ trong PDF, VD `pdfplumber`) nếu muốn trải nghiệm highlight chính xác tới từng đoạn thay vì cả trang. Sẽ bàn kỹ hơn khi tới phase này.

**DoD:** trong lúc AI đang trả lời, panel trái tự cuộn/highlight đúng trang được trích dẫn — test bằng tay trên frontend thật (không chỉ test API).

---

[← Previous: Phase 7](phase-7-streaming.md) · [Back to overview](README.md) · [Next: Phase 9 — Frontend →](phase-9-frontend.md)
