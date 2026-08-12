[← Kế hoạch Phase 5](../../development-plan/phase-5-rag-orchestrator.md) · [← Tất cả các phase](../README.md)

# Phase 5 — RAG orchestrator: giải thích luồng code

Mỗi bước nhỏ (5.1, 5.2, 5.3...) có 1 file riêng trong folder này — code thật, ý nghĩa, tại sao cần bước đó, tại sao code theo cách đó chứ không phải cách khác, test đã chạy, và bước đó nối vào đâu ở các bước sau.

## Các bước

- [x] [5.1 — `similarity_search`: tìm chunk liên quan nhất bằng pgvector](5.1-similarity-search.md)
- [x] [5.2 — `build_prompt`: dựng prompt yêu cầu trả lời có trích dẫn](5.2-build-prompt.md)
- [x] [5.3 — `ask`: orchestrate toàn bộ RAG (chưa streaming)](5.3-ask.md)
- [x] [5.4 — `parse_citations`: khớp trích dẫn với chunk thật](5.4-parse-citations.md)
- [x] [5.5 — Endpoint tạm `POST /api/documents/{document_id}/ask`](5.5-ask-endpoint.md)
- [x] [5.6 — Test edge case: RAG phải "biết mình không biết"](5.6-edge-cases.md)
