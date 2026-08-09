[← Back to overview](README.md)

## Phase 5 — RAG orchestrator (chưa streaming, test logic trước)

**Việc cần làm:**
- `app/services/rag_service.py`:
  - `similarity_search(document_id, query_embedding, k=6) -> list[DocumentChunk]` — query pgvector: `order by embedding <=> :query_embedding limit :k`, filter `document_id`
  - `build_prompt(chunks, question) -> str` — system prompt yêu cầu chỉ trả lời dựa trên context, kèm tag `[Trang X]` để model tự trích dẫn
  - `ask(document_id, question) -> AnswerResult` — embed câu hỏi → similarity search → build prompt → gọi OpenAI Chat Completions API (`openai` SDK, model `gpt-4o-mini`, `stream=False` ở phase này) → parse citation từ response (regex tìm `[Trang X]` khớp với `page_number` của chunk đã dùng)
- Endpoint tạm để test: `POST /api/sessions/{id}/messages` (non-streaming trước, trả JSON thường)

**DoD:** hỏi 1 câu về nội dung file đã ingest ở Phase 3 → nhận câu trả lời đúng, có trích dẫn số trang hợp lệ.

---

[← Previous: Phase 4](phase-4-viewer-api.md) · [Back to overview](README.md) · [Next: Phase 6 — Streaming (SSE) →](phase-6-streaming.md)
