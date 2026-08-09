[← Kế hoạch Phase 3](../../development-plan/phase-3-ingestion.md) · [← Tất cả các phase](../README.md)

# Phase 3 — Ingestion Pipeline: giải thích luồng code

Mỗi bước nhỏ (3.1, 3.2, 3.3...) có 1 file riêng trong folder này — code thật, ý nghĩa, tại sao cần bước đó, tại sao code theo cách đó chứ không phải cách khác, test đã chạy, và bước đó nối vào đâu ở các bước sau.

## Các bước

- [x] [3.1 — `extract_text_pypdf`: lấy text thuần từ PDF](3.1-extract-text-pypdf.md)
- [x] [3.2 — `_describe_image_pixtral`: mô tả 1 ảnh/diagram bằng Pixtral vision](3.2-describe-image-pixtral.md)
- [x] [3.3 — `extract_text_mistral_ocr`: OCR toàn bộ trang + làm giàu mô tả ảnh](3.3-extract-text-mistral-ocr.md)
- [x] [3.4 — `extract_text_hybrid`: pypdf + OCR chỉ trang có ảnh](3.4-extract-text-hybrid.md)
- [x] [3.5 — `convert_pptx_to_pdf`: convert PPTX sang PDF bằng LibreOffice](3.5-convert-pptx-to-pdf.md)
- [x] [3.6 — `chunk_text`: cắt nhỏ text theo token](3.6-chunk-text.md)
- [x] [3.7 — `embed_chunks`: gọi OpenAI embeddings](3.7-embed-chunks.md)
- [x] [3.8 — `run_ingestion`: orchestrate toàn bộ pipeline](3.8-run-ingestion.md)
- [x] [3.9 — Nối `run_ingestion` vào `POST /api/documents`](3.9-wire-upload-endpoint.md)
- [x] [3.10 — `GET /api/documents/{id}/status`](3.10-status-endpoint.md)
- [x] [3.11 — Test xử lý lỗi](3.11-error-handling-tests.md)
- [x] [3.12 — Test end-to-end đầy đủ cả 3 mode](3.12-e2e-test.md)
