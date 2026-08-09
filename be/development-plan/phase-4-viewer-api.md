[← Back to overview](README.md)

## Phase 4 — Document viewer API

**Quyết định kiến trúc đã chốt (bàn luận lại trước khi code Phase 3, xem [Phase 3](phase-3-ingestion.md)):** viewer hiển thị **thẳng file PDF** (dùng thư viện `PDF.js`/`react-pdf` ở frontend) thay vì ảnh PNG tĩnh từng trang. Lý do chốt: ảnh tĩnh không cho người dùng copy/select text trong tài liệu (mất khả năng "copy đúng câu để hỏi AI"), trong khi PDF.js vẫn giữ được:
- Text layer thật → copy/select được.
- Nhảy tới trang cụ thể (`page=4`) → phục vụ citation từ AI.
- Vẽ overlay highlight theo toạ độ (dùng `document_chunks.bbox`, xem [Phase 8](phase-8-citation-highlight.md)) → không mất khả năng highlight vùng cụ thể.

Nói cách khác: được cả 2 (copy text + highlight theo trang/vùng), không phải đánh đổi cái này lấy cái kia.

**Việc cần làm:**
- `GET /api/documents/{id}/file` — trả presigned URL của file PDF để frontend load vào PDF.js. Dùng `storage_key` (PDF gốc) nếu `file_type='pdf'`, dùng `converted_pdf_key` nếu `file_type='pptx'` (file PPTX gốc không tự hiển thị được trên browser).
- Không cần endpoint theo từng trang nữa (`/pages/{n}` của bản kế hoạch trước đã bỏ) — PDF.js tải nguyên file 1 lần, tự xử lý phân trang/zoom ở client.

**DoD:** gọi endpoint trả về URL, mở URL đó trên browser thấy đúng file PDF (hoặc bản PDF đã convert từ PPTX); test PDF.js ở frontend có thể nhảy tới trang bất kỳ và select được text.

---

[← Previous: Phase 3](phase-3-ingestion.md) · [Back to overview](README.md) · [Next: Phase 5 — RAG orchestrator →](phase-5-rag-orchestrator.md)
