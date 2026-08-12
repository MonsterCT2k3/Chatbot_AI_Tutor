[← Back to overview](README.md)

## Phase 4 — Document viewer API

**Quyết định kiến trúc đã chốt (bàn luận lại trước khi code Phase 3, xem [Phase 3](phase-3-ingestion.md)):** viewer hiển thị **thẳng file PDF** (dùng thư viện `PDF.js`/`react-pdf` ở frontend) thay vì ảnh PNG tĩnh từng trang. Lý do chốt: ảnh tĩnh không cho người dùng copy/select text trong tài liệu (mất khả năng "copy đúng câu để hỏi AI"), trong khi PDF.js vẫn giữ được:
- Text layer thật → copy/select được.
- Nhảy tới trang cụ thể (`page=4`) → phục vụ citation từ AI.
- Vẽ overlay highlight theo toạ độ (dùng `document_chunks.bbox`, xem [Phase 8](phase-8-citation-highlight.md)) → không mất khả năng highlight vùng cụ thể.

Nói cách khác: được cả 2 (copy text + highlight theo trang/vùng), không phải đánh đổi cái này lấy cái kia.

**Việc cần làm:**
- [x] `GET /api/documents/{id}/file` — trả presigned URL của file PDF để frontend load vào PDF.js. Dùng `storage_key` (PDF gốc) nếu `file_type='pdf'`, dùng `converted_pdf_key` nếu `file_type='pptx'` (file PPTX gốc không tự hiển thị được trên browser). PPTX chưa convert xong (`converted_pdf_key` còn `null`) → trả lỗi `409 DOCUMENT_NOT_READY` rõ ràng, không trả URL rác.
- Không cần endpoint theo từng trang nữa (`/pages/{n}` của bản kế hoạch trước đã bỏ) — PDF.js tải nguyên file 1 lần, tự xử lý phân trang/zoom ở client.

**Đã test thật (qua HTTP + tải thật presigned URL về, không chỉ kiểm tra response):**
- PDF thường: `/file` trả URL, tải URL đó về ra đúng file PDF thật (header `%PDF-`).
- PPTX chưa convert (`converted_pdf_key=null`): `/file` trả `409 DOCUMENT_NOT_READY`.
- PPTX đã convert xong: `/file` trả URL trỏ tới bản PDF đã convert, tải về đúng file PDF thật.
- Document không tồn tại → `404`. Không có token → `401`.

**DoD:** gọi endpoint trả về URL, mở URL đó trên browser thấy đúng file PDF (hoặc bản PDF đã convert từ PPTX); test PDF.js ở frontend có thể nhảy tới trang bất kỳ và select được text (phần PDF.js ở frontend chưa làm, thuộc phạm vi FE — backend đã sẵn sàng cung cấp URL đúng).

---

[← Previous: Phase 3](phase-3-ingestion.md) · [Back to overview](README.md) · [Next: Phase 5 — RAG orchestrator →](phase-5-rag-orchestrator.md)
