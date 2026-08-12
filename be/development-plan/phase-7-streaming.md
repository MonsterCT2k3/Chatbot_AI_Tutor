[← Back to overview](README.md)

## Phase 7 — Chuyển sang streaming (SSE)

**Đổi thứ tự so với bản kế hoạch cũ** — xem giải thích ở [Phase 6](phase-6-chat-sessions.md): phase này giờ được xây dựng SAU khi session CRUD đã có thật, nên bước "lưu `chat_messages` khi `done`" bên dưới giờ nối vào 1 `session_id` thật, không còn mơ hồ như bản kế hoạch cũ.

**Việc cần làm:**
- Đổi `rag_service.ask()` thành generator/async generator dùng `client.chat.completions.create(..., stream=True)` của OpenAI SDK. Lưu ý: bước `contextualize_question` (Phase 6) và retrieval (5.1, cộng thêm hybrid/rerank nếu đã làm Phase 5.5) phải chạy XONG TRƯỚC KHI bắt đầu stream — chỉ phần sinh câu trả lời cuối cùng mới stream được, vì cần có đủ context trước khi gọi model.
- `app/routers/messages.py`: `POST /api/sessions/{id}/messages` trả `StreamingResponse(media_type="text/event-stream")`, emit theo đúng format đã chốt trong guide:
  ```
  event: token     { "delta": "..." }
  event: citation  { "page_number": 4, "chunk_id": "...", "snippet": "..." }
  event: done       { "message_id": "...", "citations": [...] }
  ```
- Khi `done`: lưu `chat_messages` (role=assistant, content=full text ghép từ các token) + insert `message_citations` — `session_id` lúc này là session thật đã tồn tại từ Phase 6, không còn vấn đề khóa ngoại.
- Nếu Phase 5.5 đã làm grounding/faithfulness check (5.5.7): chạy bước này SAU khi stream xong toàn bộ câu trả lời (cần full text mới kiểm tra được), không chặn luồng stream.
- **Tương tác với output guardrail (5.6.4)** — kiểm duyệt nội dung (content moderation) cần TOÀN BỘ câu trả lời mới chạy được chính xác, nhưng streaming lại hiển thị token dần cho người dùng thấy NGAY — nghĩa là về mặt lý thuyết, người dùng có thể đã nhìn thấy 1 phần nội dung không phù hợp trước khi hệ thống kịp phát hiện ở cuối. Cần quyết định đánh đổi lúc code: chấp nhận rủi ro nhỏ này (input guardrail ở 5.6.1-5.6.3 đã lọc phần lớn trước khi vào), hay trì hoãn hiển thị vài trăm mili-giây để buffer và kiểm duyệt theo cụm token thay vì stream ngay lập tức (đánh đổi độ trễ lấy an toàn).

**DoD:** dùng `curl -N` hoặc EventSource test thấy token chảy từng phần, không đợi full response; sau khi `done`, `chat_messages`/`message_citations` được lưu đúng vào session thật.

---

[← Previous: Phase 6](phase-6-chat-sessions.md) · [Back to overview](README.md) · [Next: Phase 8 — Citation highlight →](phase-8-citation-highlight.md)
