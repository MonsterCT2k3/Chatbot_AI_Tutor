[← Kế hoạch Phase 6](../../development-plan/phase-6-chat-sessions.md) · [← Tất cả các phase](../README.md)

# Phase 6 — Chat session CRUD + multi-turn: giải thích luồng code

Mỗi bước nhỏ (6.1, 6.2...) có 1 file riêng trong folder này — dữ liệu/code thật, ý nghĩa, tại sao cần bước đó, tại sao làm theo cách đó, test đã chạy, và bước đó nối vào đâu ở các bước sau. Cùng format đã dùng ở [Phase 5.6](../phase-5.6-guardrails-observability/README.md).

**Bối cảnh phase này giải quyết vấn đề gì:** tới hết Phase 5.6, mỗi câu hỏi là một lượt ĐỘC LẬP — hỏi xong đóng trang là mất sạch, và hỏi nối tiếp kiểu *"giải thích rõ hơn phần đó"* thì retrieval gần như chắc chắn tìm sai chunk vì bản thân câu hỏi không mang đủ thông tin. Phase 6 xử lý cả hai: lưu hội thoại thật (phần 1) và làm cho AI hiểu được ngữ cảnh nhiều lượt (phần 2).

> **Kế hoạch của phase này đã được rà lại ngày 2026-08-23 trước khi code** — bản gốc viết trước khi Phase 5.6 tồn tại nên đã lạc hậu ở 6 điểm, 2 trong đó nghiêm trọng (gọi `ask()` thay vì `ask_for_user()` sẽ lọt qua toàn bộ guardrail; và không hề nhắc tới kiểm tra quyền sở hữu). Chi tiết ở mục "Cập nhật" đầu file [kế hoạch Phase 6](../../development-plan/phase-6-chat-sessions.md).

## Các bước

- [x] [6.1 — Schemas cho session và message](6.1-schemas.md)
- [ ] 6.2 — `get_owned_session` + CRUD endpoints
- [ ] 6.3 — `GET /{id}/messages`: phân trang cursor
- [ ] 6.4 — Lưu tin nhắn đúng thứ tự (commit riêng trước khi gọi LLM)
- [ ] 6.5 — `POST /api/sessions/{id}/messages` (non-streaming)
- [ ] 6.6 — Feedback tải lại được sau khi mở lại lịch sử
- [ ] 6.7 — `rag_service.contextualize_question`
- [ ] 6.8 — Giới hạn lịch sử đưa vào contextualize
- [ ] 6.9 — Test end-to-end
