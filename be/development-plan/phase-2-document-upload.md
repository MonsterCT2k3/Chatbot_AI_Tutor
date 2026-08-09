[← Back to overview](README.md)

## Phase 2 — Document upload ✅ HOÀN THÀNH

**9 bước, làm và test từng bước trước khi qua bước tiếp theo (giống Phase 1):**

- [x] **2.1 `storage_service.upload_file()`** — wrapper `boto3` upload lên R2. **Lưu ý quan trọng:** `boto3` là thư viện blocking (đồng bộ) — gọi trực tiếp trong route `async def` sẽ đứng hình toàn bộ event loop (mọi request khác cũng bị chặn). Đã bọc bằng `starlette.concurrency.run_in_threadpool`.
- [x] **2.2 `storage_service.get_presigned_url()`** — sinh URL tạm thời để đọc file mà không cần public bucket. Đây chỉ là ký (sign) cục bộ, không gọi mạng tới R2 → không cần `run_in_threadpool`. Đã verify bucket KHÔNG public (URL không ký bị từ chối 400).
- [x] **2.3 `storage_service.delete_file()`** — gọi mạng thật nên vẫn cần `run_in_threadpool`.
- [x] **2.4 `schemas/document.py`: `DocumentResponse`** — không lộ `storage_key`/`user_id`/`metadata` (giống nguyên tắc không lộ `hashed_password` ở Phase 1).
- [x] **2.5 `POST /api/documents`** — logic thật (validate + upload + insert) nằm trong `document_service.create_document()` (Service layer), không phải trong router. Thứ tự cố ý: upload R2 **trước**, insert DB **sau** — nếu upload lỗi thì không có row rác trong DB.
- [x] **2.6 `GET /api/documents`** — chỉ query đơn giản (lọc + sắp xếp), không có logic quyết định → để thẳng trong router, không tạo service function (giống bài học "get_user_by_id là thừa" ở Phase 1).
- [x] **2.7 `GET /api/documents/{id}`** — 404 giống hệt nhau (byte-for-byte, đã test) cho cả 2 trường hợp "không tồn tại" và "của người khác", tránh lộ thông tin.
- [x] **2.8 `DELETE /api/documents/{id}`** — tách `get_owned_document()` dùng chung cho cả 2.7 và 2.8 (khác với `get_user_by_id`: ở đây có ≥2 nơi gọi thật nên tách ra là hợp lý, không phải abstraction thừa).
- [x] **2.9 Test end-to-end** — 12 case, tất cả PASS, bao gồm test 2 user riêng biệt để xác nhận không lộ dữ liệu chéo.

**Lưu ý:** giới hạn file 50MB, check cả extension lẫn `content_type` trước khi chấp nhận.

**DoD:** ✅ Toàn bộ 9 bước pass qua HTTP thật (in-process test client gọi qua ASGI, tương đương HTTP thật), có test với PDF thật (`app/data/slide/b3.pdf`) upload lên R2 thật.

---

[← Previous: Phase 1.5](phase-1.5-jwt-hardening.md) · [Back to overview](README.md) · [Next: Phase 3 — Ingestion pipeline →](phase-3-ingestion.md)
