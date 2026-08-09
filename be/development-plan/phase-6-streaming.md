[← Back to overview](README.md)

## Phase 6 — Chuyển sang streaming (SSE)

**Việc cần làm:**
- Đổi `rag_service.ask()` thành generator/async generator dùng `client.chat.completions.create(..., stream=True)` của OpenAI SDK
- `app/routers/messages.py`: trả `StreamingResponse(media_type="text/event-stream")`, emit theo đúng format đã chốt trong guide:
  ```
  event: token     { "delta": "..." }
  event: citation  { "page_number": 4, "chunk_id": "...", "snippet": "..." }
  event: done       { "message_id": "...", "citations": [...] }
  ```
- Khi `done`: lưu `chat_messages` (role=assistant, content=full text ghép từ các token) + insert `message_citations`

**DoD:** dùng `curl -N` hoặc EventSource test thấy token chảy từng phần, không đợi full response.

---

[← Previous: Phase 5](phase-5-rag-orchestrator.md) · [Back to overview](README.md) · [Next: Phase 7 — Chat session CRUD →](phase-7-chat-sessions.md)
