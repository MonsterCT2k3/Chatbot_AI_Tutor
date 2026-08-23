[← Kế hoạch Phase 6](../../development-plan/phase-6-chat-sessions.md) · [← Tất cả các phase](../README.md)

# Phase 6 — Chat session CRUD + multi-turn: giải thích luồng code

Mỗi bước nhỏ (6.1, 6.2...) có 1 file riêng trong folder này.

### Format "Quyết định & Đánh đổi" (áp dụng từ phase này)

Các phase trước ([3](../phase-3-ingestion/README.md) → [5.6](../phase-5.6-guardrails-observability/README.md)) dùng format cũ, trong đó phần chiếm nhiều chỗ nhất là **chép lại code** — thứ đã có sẵn trong repo, sẽ lạc hậu khi code đổi, và đọc nó là chế độ "thợ code". Từ Phase 6 đổi sang format lấy **quyết định** làm trung tâm, mỗi file trả lời đúng 7 câu hỏi của kỹ sư:

| Mục | Trả lời câu hỏi |
|---|---|
| **Vấn đề** | Bước này giải quyết chuyện gì, vì sao không bỏ qua được? |
| **Các ngã rẽ** | Có mấy đường đi? Chọn đường nào, **bỏ** đường nào, và vì sao? |
| **Luồng** | Dữ liệu chạy qua đâu (sơ đồ, không phải danh sách gạch đầu dòng)? |
| **Bất biến** | Điều gì phải **luôn đúng**, nếu sai thì mọi thứ bên dưới sai theo? |
| **Hỏng thì biểu hiện thế nào** | Lỗi **ồn ào** (có exception) hay **âm thầm** (dữ liệu sai, không báo gì)? |
| **Bằng chứng** | Lấy gì chứng minh là đúng, không phải "chạy thấy ổn"? |
| **Ràng buộc để lại** | Bước sau bị buộc phải theo cái gì? |

Không chép code vào tài liệu — chỉ link tới file thật. Mục tiêu là hiểu được **tổng thể và lý do**, không cần đọc từng dòng.

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
