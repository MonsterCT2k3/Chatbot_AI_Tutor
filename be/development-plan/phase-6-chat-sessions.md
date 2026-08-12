[← Back to overview](README.md)

## Phase 6 — Chat session CRUD + multi-turn conversation awareness

**Đổi thứ tự so với bản kế hoạch cũ** (trước đây Phase 6 = streaming, Phase 7 = session CRUD) — phát hiện lúc rà lại kế hoạch: bước "lưu `chat_messages` khi `done`" (nguyên bản nằm trong phase streaming) cần 1 `session_id` THẬT đã tồn tại trong DB (khóa ngoại — foreign key — bắt buộc phải trỏ tới 1 row có thật), nhưng session CRUD lại được xếp làm SAU streaming trong bản cũ — thứ tự ngược, không triển khai đúng như đã viết được. Sửa lại: xây session CRUD thật trước (phase này), rồi mới thêm streaming lên trên nền session đã có thật ([Phase 7](phase-7-streaming.md)).

**Phần 1 — Session CRUD (multi-session):**
- `app/schemas/session.py`: `SessionCreate`, `SessionResponse`, `SessionUpdate`
- `app/routers/sessions.py`:
  - `POST /api/sessions` — tạo với `document_id` (+ `title` mặc định `"New chat"`)
  - `GET /api/sessions` — list theo user, `order by updated_at desc`
  - `GET /api/sessions/{id}` / `PATCH /api/sessions/{id}` (đổi `title`) / `DELETE /api/sessions/{id}`
  - `GET /api/sessions/{id}/messages` — phân trang (`limit`/`offset` hoặc cursor theo `created_at`)
- Nối `POST /api/sessions/{id}/messages` thật (non-streaming trước, giống Phase 5) vào đúng `session_id` — lấy `document_id` từ session để search, thay cho endpoint tạm `/api/documents/{document_id}/ask` của Phase 5 (endpoint tạm đó có thể xóa hoặc giữ song song cho việc test nhanh sau này).

**Phần 2 — Multi-turn conversation awareness (nâng cấp chất lượng AI, không phải CRUD thuần):**

Vấn đề thật: RAG ở Phase 5/5.5 chỉ xử lý được câu hỏi ĐỘC LẬP. Trong 1 cuộc chat tutoring thật, học viên liên tục hỏi nối tiếp mơ hồ ("còn phần 2 thì sao?", "giải thích lại đơn giản hơn", "nó hoạt động thế nào?") — nếu đưa thẳng câu hỏi này vào `similarity_search` (5.1), retrieval gần như chắc chắn sai vì câu hỏi không tự mang đủ thông tin để tìm đúng chunk.

- `rag_service.contextualize_question(history, question) -> str` — dùng 1 lệnh gọi LLM nhỏ (nhanh, rẻ — `gpt-4o-mini`) viết lại câu hỏi hiện tại thành 1 câu hỏi ĐỘC LẬP (standalone), lồng ghép ngữ cảnh cần thiết từ vài lượt hội thoại gần nhất. VD: lịch sử "Kiến trúc Transformer gồm encoder và decoder" + câu hỏi mới "phần đầu tiên hoạt động thế nào?" → viết lại thành "Encoder trong kiến trúc Transformer hoạt động thế nào?".
- Giới hạn số lượt lịch sử đưa vào (context window management — quản lý giới hạn độ dài ngữ cảnh đưa vào prompt, VD chỉ lấy 5 cặp hỏi-đáp gần nhất) để tránh prompt phình to vô hạn khi hội thoại kéo dài.
- Tối ưu chi phí: nếu đây là câu hỏi ĐẦU TIÊN của session (chưa có lịch sử) → dùng thẳng câu hỏi gốc, không gọi `contextualize_question` (tránh 1 lệnh gọi LLM thừa không cần thiết).
- Nối vào `ask()` (Phase 5): thêm tham số `session_id` (optional) — nếu có, lấy lịch sử gần nhất từ `chat_messages`, gọi `contextualize_question` trước khi embed/search; câu hỏi đã viết lại chỉ dùng để RETRIEVE, câu hỏi GỐC của người dùng vẫn được lưu nguyên vào `chat_messages` (không lưu bản viết lại, tránh gây nhầm lẫn khi xem lại lịch sử).

**Chia nhỏ thành các bước:**

- [ ] **6.1 Schemas** — `SessionCreate`, `SessionResponse`, `SessionUpdate`.
- [ ] **6.2 CRUD endpoints** — `POST`/`GET`/`GET {id}`/`PATCH {id}`/`DELETE {id}`.
- [ ] **6.3 `GET /{id}/messages`** — phân trang lịch sử hội thoại.
- [ ] **6.4 `POST /api/sessions/{id}/messages` thật (non-streaming)** — nối vào `rag_service.ask()`, lấy `document_id` từ session, lưu cả câu hỏi + câu trả lời vào `chat_messages`.
- [ ] **6.5 `rag_service.contextualize_question`** — viết lại câu hỏi dựa trên lịch sử gần nhất. Test: 1 kịch bản hỏi nối tiếp thật (hỏi về 1 khái niệm, rồi hỏi tiếp "nó là gì") → xác nhận retrieval ra đúng chunk nhờ câu hỏi đã viết lại, so với việc dùng thẳng câu hỏi gốc (retrieval sai).
- [ ] **6.6 Giới hạn lịch sử đưa vào contextualize** — chốt số lượt tối đa, test hội thoại dài không làm phình prompt vô kiểm soát. **Nâng cấp cân nhắc (không bắt buộc ngay):** thay vì chỉ CẮT BỎ các lượt cũ khi vượt ngưỡng, có thể TÓM TẮT (summarize) các lượt cũ thành 1 đoạn ngắn thay vì bỏ hẳn — giữ được ngữ cảnh dài hạn của cả buổi học mà không phình prompt vô hạn (kỹ thuật "conversation summarization", phổ biến ở các chat AI chuyên nghiệp có hội thoại dài).
- [ ] **6.7 Test end-to-end** — 2 session cùng 1 document → chat riêng từng session, lịch sử không lẫn nhau; test follow-up thật trong cùng 1 session ra câu trả lời đúng ngữ cảnh mà người dùng không cần lặp lại toàn bộ câu hỏi.

**DoD:** tạo 2 session cho cùng 1 document → chat riêng từng session → lịch sử không lẫn nhau; hỏi nối tiếp (follow-up) trong cùng session ra câu trả lời đúng ngữ cảnh nhờ `contextualize_question`, không cần người dùng tự lặp lại toàn bộ câu hỏi.

---

[← Previous: Phase 5.6](phase-5.6-guardrails-observability.md) · [Back to overview](README.md) · [Next: Phase 7 — Streaming (SSE) →](phase-7-streaming.md)
