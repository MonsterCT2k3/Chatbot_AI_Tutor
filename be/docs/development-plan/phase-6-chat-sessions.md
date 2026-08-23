[← Back to overview](README.md)

## Phase 6 — Chat session CRUD + multi-turn conversation awareness

**Đổi thứ tự so với bản kế hoạch cũ** (trước đây Phase 6 = streaming, Phase 7 = session CRUD) — phát hiện lúc rà lại kế hoạch: bước "lưu `chat_messages` khi `done`" (nguyên bản nằm trong phase streaming) cần 1 `session_id` THẬT đã tồn tại trong DB (khóa ngoại — foreign key — bắt buộc phải trỏ tới 1 row có thật), nhưng session CRUD lại được xếp làm SAU streaming trong bản cũ — thứ tự ngược, không triển khai đúng như đã viết được. Sửa lại: xây session CRUD thật trước (phase này), rồi mới thêm streaming lên trên nền session đã có thật ([Phase 7](phase-7-streaming.md)).

---

### Cập nhật (2026-08-23) — rà lại plan trước khi code

Bản plan này được viết TRƯỚC khi [Phase 5.6](phase-5.6-guardrails-observability.md) tồn tại. Rà lại lần nữa, đối chiếu với code + DB thật, phát hiện 6 chỗ lạc hậu hoặc thiếu — **2 chỗ đầu là nghiêm trọng** (một cái vô hiệu hoá toàn bộ lớp guardrail vừa xây, một cái là lỗ hổng phân quyền), **2 chỗ tiếp theo thuộc loại lỗi âm thầm** (code chạy không báo lỗi nhưng dữ liệu sai/thiếu):

| # | Vấn đề của bản cũ | Đã sửa ở đâu |
|---|---|---|
| 1 | Bước 6.4 ghi "nối vào `rag_service.ask()`" — sẽ **bỏ qua quota theo user (5.6.6), circuit breaker (5.6.8) và ghi log usage (5.6.9)**. Docstring của `ask_for_user()` ghi rõ *"ĐÂY là hàm endpoint thật phải gọi"*. | Phần 1 mục ⑤, bước 6.5 |
| 2 | Không nhắc gì tới **kiểm tra quyền sở hữu** cho 6 endpoint thao tác trên session của user, trong khi codebase đã có pattern cố ý (`get_owned_document`). | Phần 1 mục ①, bước 6.2 |
| 3 | `GET /api/sessions` sắp xếp `order by updated_at desc`, nhưng **không có gì cập nhật `updated_at`** khi có tin nhắn mới → danh sách hoá ra sắp theo thời điểm *tạo*. | Phần 1 mục ④, bước 6.5 |
| 4 | Không lưu `message_citations` ở phase này (mãi Phase 7 mới nhắc) → suốt Phase 6, tải lại lịch sử **mất sạch trích dẫn**, dù bảng/model đã có sẵn. | Phần 1 mục ⑥, bước 6.5 |
| 5 | Không nói FE gửi 👍/👎 bằng id nào sau khi có `chat_messages.id` (hiện `answer_id` = `ai_usage_log.id`, có FK cứng ở `answer_feedback`). | Phần 1 mục ⑦, bước 6.6 |
| 6 | Nhiều quyết định bỏ lửng: phân trang "offset **hoặc** cursor", endpoint `/ask` cũ "xoá **hoặc** giữ", `contextualize_question` lỗi thì sao, và không có auto-đặt tên session (sidebar sẽ toàn `"New chat"`). | Phần 1 mục ②③⑧, Phần 2 |

---

**Phần 1 — Session CRUD (multi-session):**

- `app/schemas/session.py`: `SessionCreate`, `SessionResponse`, `SessionUpdate`; `app/schemas/message.py`: `MessageCreate`, `MessageResponse`, `MessageListResponse`.

- ① **Quyền sở hữu — làm trước mọi endpoint.** Thêm `session_service.get_owned_session(db, session_id, user_id)` **soi gương đúng `document_service.get_owned_document`**: lọc theo `id` AND `user_id` trong CÙNG 1 query, để "session không tồn tại" và "session của người khác" đều ném cùng `SessionNotFoundError` → router trả **404 giống hệt nhau**, không tiết lộ sự khác biệt (chống dò `session_id` của người khác bằng thử-sai). MỌI endpoint dưới đây đều phải đi qua hàm này. Tạo session cũng phải kiểm tra `document_id` thuộc về chính user đó (`get_owned_document`) — nếu không, user A tạo được session trỏ vào tài liệu của user B rồi chat với nội dung tài liệu đó.

- `app/routers/sessions.py`:
  - `POST /api/sessions` — tạo với `document_id` (+ `title` tuỳ chọn, mặc định `"New chat"`).
  - `GET /api/sessions` — list theo user, `order by updated_at desc`. Hỗ trợ lọc `?document_id=` (FE cần: sidebar chỉ hiện các cuộc trao đổi của đúng tài liệu đang mở).
  - `GET /api/sessions/{id}` / `PATCH /api/sessions/{id}` (đổi `title`) / `DELETE /api/sessions/{id}`.
  - `GET /api/sessions/{id}/messages` — lịch sử hội thoại, có phân trang.

- ② **CHỐT: phân trang dùng cursor (keyset), không dùng offset.** Trả về `limit` tin nhắn MỚI NHẤT (`order by created_at desc`), kèm `next_cursor`; muốn xem cũ hơn thì truyền `?before=<cursor>`. Lý do chọn cursor: chat là danh sách **đang được ghi thêm liên tục** — nếu dùng `offset` mà giữa lúc người dùng cuộn lên lại có tin nhắn mới chèn vào, mọi tin nhắn sẽ bị dịch 1 nấc và người dùng thấy tin nhắn lặp/nhảy cóc. Cursor không có vấn đề này vì nó neo vào 1 mốc cố định.

- ③ **CẢNH BÁO — `now()` của Postgres CỐ ĐỊNH trong 1 transaction** (đã kiểm chứng trực tiếp trên DB thật: gọi `now()` hai lần cách nhau 0.3s trong cùng transaction ra **giá trị giống hệt**; `clock_timestamp()` mới tăng thật). `chat_messages.created_at` đang dùng `server_default=now()`, nên **nếu lưu câu hỏi và câu trả lời trong CÙNG 1 transaction thì cả hai có `created_at` y hệt nhau** → `order by created_at` không xác định được cái nào trước, lịch sử có thể hiện câu trả lời TRƯỚC câu hỏi, và cursor phân trang (mục ②) cũng gãy theo.

  **Cách xử lý (không cần migration):** lưu + **commit tin nhắn của người dùng TRƯỚC** khi gọi LLM, rồi lưu câu trả lời ở transaction sau → `created_at` chắc chắn tăng dần. Cách này còn được thêm 1 lợi ích: nếu việc sinh câu trả lời lỗi giữa chừng, câu hỏi của người dùng KHÔNG bị mất.

- ④ **`updated_at` phải được "chạm" khi có tin nhắn mới.** DB đã có trigger `trg_sessions_updated_at` (BEFORE UPDATE trên `chat_sessions`) — nhưng trigger chỉ chạy khi **chính dòng session bị UPDATE**; thêm dòng vào `chat_messages` KHÔNG đụng tới nó. Vậy nên khi lưu tin nhắn, phải chủ động UPDATE dòng session (đặt `title` nếu đang auto-đặt tên, hoặc chỉ cần `touch` để trigger chạy). Không làm bước này thì `order by updated_at desc` ở `GET /api/sessions` thực chất chỉ đang sắp theo thời điểm TẠO session — sai âm thầm, không có lỗi nào báo ra.

- ⑤ **`POST /api/sessions/{id}/messages` (non-streaming trước, giống Phase 5)** — lấy `document_id` từ session để search.

  **BẮT BUỘC gọi `rag_service.ask_for_user()`, KHÔNG gọi thẳng `ask()`.** `ask()` chỉ lo chất lượng/an toàn câu trả lời và không biết user là ai; toàn bộ **quota theo user (5.6.6), circuit breaker toàn hệ thống (5.6.8) và ghi `ai_usage_log` (5.6.9)** nằm ở `ask_for_user()`. Gọi nhầm `ask()` sẽ khiến endpoint thật của Phase 6 lọt qua toàn bộ lớp guardrail vừa xây ở 5.6 mà không có dấu hiệu gì báo lỗi. Router phải bắt và ánh xạ `QuotaExceededError` → 429 và `CircuitBreakerOpenError` → 503, **giống hệt** cách `POST /api/documents/{id}/ask` đang làm.

- ⑥ **Lưu `message_citations` NGAY ở phase này, không đợi Phase 7.** Sau khi có `AnswerResult`, insert 1 dòng `chat_messages` (role=assistant) + N dòng `message_citations` (`page_number`, `chunk_id`, `snippet`). Bảng và model đã có sẵn từ Phase 0. Không làm bước này thì `GET /{id}/messages` trả về lịch sử **không có trích dẫn** — mà trích dẫn chính là điểm mạnh cốt lõi của sản phẩm, và FE đã dựng sẵn UI trích dẫn bấm được để nhảy tới đúng trang.

- ⑦ **CHỐT: 👍/👎 vẫn gắn vào `ai_usage_log.id`, và lưu id đó vào `chat_messages.metadata`.** Hiện `answer_id` mà FE gửi feedback = `AnswerResult.call_group_id` = `ai_usage_log.id`, và `answer_feedback` có **FK cứng** trỏ tới `ai_usage_log_id`. Sau phase này mỗi câu trả lời có thêm `chat_messages.id` — hai định danh cho cùng một khái niệm.

  Quyết định: **không đổi** cơ chế feedback (giữ FK cứng đang chạy tốt, và `ai_usage_log` mới là nơi gắn với dữ liệu quan sát chi phí/chất lượng), nhưng khi lưu tin nhắn assistant thì **ghi kèm `ai_usage_log_id` vào cột `chat_messages.metadata`** (cột JSONB đã có sẵn, không cần migration). Nhờ vậy `GET /{id}/messages` trả kèm được `answer_id` cho từng câu trả lời cũ → tải lại trang vẫn bấm 👍/👎 được, và khôi phục được trạng thái đã bấm trước đó.

- ⑧ **CHỐT: endpoint cũ `POST /api/documents/{id}/ask` GIỮ NGUYÊN trong Phase 6**, đánh dấu deprecated trong mô tả OpenAPI. Lý do: FE hiện đang chạy trên nó, xoá ngay sẽ làm hỏng app đang dùng được. Xoá ở [Phase 7](phase-7-streaming.md) sau khi FE đã chuyển hẳn sang session API. Giữ song song cũng tiện cho việc test nhanh RAG mà không phải tạo session.

- ⑨ **Auto-đặt tên session.** Tạo session xong thì `title = "New chat"`; khi lưu tin nhắn ĐẦU TIÊN của người dùng, nếu title vẫn đang là mặc định thì đặt lại thành **~60 ký tự đầu của câu hỏi đó** (cắt theo ranh giới từ). Không làm bước này thì sidebar "Thảo luận học tập" sẽ hiện toàn `"New chat"` — không phân biệt được cuộc nào với cuộc nào. Cố tình KHÔNG dùng LLM để đặt tên: tốn thêm 1 lệnh gọi cho mỗi session mà giá trị tăng thêm rất ít so với việc cắt câu hỏi. (Để ngỏ nâng cấp sau nếu thấy tên cắt thô quá.)

**Phần 2 — Multi-turn conversation awareness (nâng cấp chất lượng AI, không phải CRUD thuần):**

Vấn đề thật: RAG ở Phase 5/5.5 chỉ xử lý được câu hỏi ĐỘC LẬP. Trong 1 cuộc chat tutoring thật, học viên liên tục hỏi nối tiếp mơ hồ ("còn phần 2 thì sao?", "giải thích lại đơn giản hơn", "nó hoạt động thế nào?") — nếu đưa thẳng câu hỏi này vào `similarity_search` (5.1), retrieval gần như chắc chắn sai vì câu hỏi không tự mang đủ thông tin để tìm đúng chunk.

- `rag_service.contextualize_question(history, question) -> str` — dùng 1 lệnh gọi LLM nhỏ (nhanh, rẻ — `gpt-4o-mini`) viết lại câu hỏi hiện tại thành 1 câu hỏi ĐỘC LẬP (standalone), lồng ghép ngữ cảnh cần thiết từ vài lượt hội thoại gần nhất. VD: lịch sử "Kiến trúc Transformer gồm encoder và decoder" + câu hỏi mới "phần đầu tiên hoạt động thế nào?" → viết lại thành "Encoder trong kiến trúc Transformer hoạt động thế nào?".
- Giới hạn số lượt lịch sử đưa vào (context window management — quản lý giới hạn độ dài ngữ cảnh đưa vào prompt, VD chỉ lấy 5 cặp hỏi-đáp gần nhất) để tránh prompt phình to vô hạn khi hội thoại kéo dài.
- Tối ưu chi phí: nếu đây là câu hỏi ĐẦU TIÊN của session (chưa có lịch sử) → dùng thẳng câu hỏi gốc, không gọi `contextualize_question` (tránh 1 lệnh gọi LLM thừa không cần thiết).
- Nối vào `ask()` (Phase 5): thêm tham số `session_id` (optional) — nếu có, lấy lịch sử gần nhất từ `chat_messages`, gọi `contextualize_question` trước khi embed/search; câu hỏi đã viết lại chỉ dùng để RETRIEVE, câu hỏi GỐC của người dùng vẫn được lưu nguyên vào `chat_messages` (không lưu bản viết lại, tránh gây nhầm lẫn khi xem lại lịch sử).
- **Hỏng thì làm gì (bản cũ không nói):** `contextualize_question` là bước LÀM TỐT THÊM, không phải bước bắt buộc — nếu lệnh gọi LLM này lỗi hoặc quá hạn, **fallback về dùng thẳng câu hỏi gốc** rồi đi tiếp, KHÔNG để cả request chết theo. Ghi lại qua `ai_call_log` (5.6.9) để đếm được tần suất hỏng. Cũng nên đặt timeout riêng ngắn cho nó: nó nằm trên đường đi của MỌI câu hỏi nối tiếp, nên chậm ở đây là người dùng cảm nhận trực tiếp.
- **Cũng ghi log lệnh gọi này** qua `log_ai_call(call_type="contextualize", ...)` với cùng `call_group_id` của lượt hỏi — nếu không, phần chi phí/độ trễ của nó sẽ vô hình trong observability vừa xây ở 5.6.

**Chia nhỏ thành các bước:**

- [ ] **6.1 Schemas** — `SessionCreate`, `SessionResponse`, `SessionUpdate`, `MessageResponse`, `MessageListResponse` (kèm `next_cursor`). `MessageResponse` phải có `answer_id` (đọc từ `metadata`) và `citations` — xem mục ⑥⑦.
- [ ] **6.2 `get_owned_session` + CRUD endpoints** — soi gương `get_owned_document` (404 không phân biệt), kiểm tra cả quyền sở hữu `document_id` lúc tạo. Test: user B gọi vào session của user A → 404, KHÔNG phải 403 (403 sẽ vô tình xác nhận session đó có tồn tại).
- [ ] **6.3 `GET /{id}/messages`** — phân trang cursor theo `created_at desc` (mục ②). Test: chèn thêm tin nhắn mới giữa 2 lần gọi phân trang → không có tin nhắn nào bị lặp hay bị nhảy cóc.
- [ ] **6.4 Lưu tin nhắn đúng thứ tự** — commit tin nhắn người dùng TRƯỚC khi gọi LLM (mục ③). Test: lưu 1 cặp hỏi-đáp rồi đọc lại → `created_at` của câu hỏi **thực sự nhỏ hơn** của câu trả lời (không bằng nhau).
- [ ] **6.5 `POST /api/sessions/{id}/messages` (non-streaming)** — gọi `ask_for_user()` (mục ⑤), lưu `chat_messages` + `message_citations` (mục ⑥), "chạm" `updated_at` của session (mục ④), auto-đặt tên ở tin nhắn đầu (mục ⑨). Test: sau khi chat, `GET /api/sessions` đưa session vừa chat lên ĐẦU danh sách; vượt quota → 429; đọc lại lịch sử thấy đủ trích dẫn.
- [ ] **6.6 Feedback tải lại được** — ghi `ai_usage_log_id` vào `chat_messages.metadata`, `GET /{id}/messages` trả kèm `answer_id` (mục ⑦). Test: chat → 👍 → tải lại lịch sử → vẫn gửi feedback được cho đúng câu trả lời cũ.
- [ ] **6.7 `rag_service.contextualize_question`** — viết lại câu hỏi dựa trên lịch sử gần nhất, có fallback khi lỗi, có ghi `ai_call_log`. Test: 1 kịch bản hỏi nối tiếp thật (hỏi về 1 khái niệm, rồi hỏi tiếp "nó là gì") → xác nhận retrieval ra đúng chunk nhờ câu hỏi đã viết lại, so với việc dùng thẳng câu hỏi gốc (retrieval sai).
- [ ] **6.8 Giới hạn lịch sử đưa vào contextualize** — chốt số lượt tối đa, test hội thoại dài không làm phình prompt vô kiểm soát. **Nâng cấp cân nhắc (không bắt buộc ngay):** thay vì chỉ CẮT BỎ các lượt cũ khi vượt ngưỡng, có thể TÓM TẮT (summarize) các lượt cũ thành 1 đoạn ngắn thay vì bỏ hẳn — giữ được ngữ cảnh dài hạn của cả buổi học mà không phình prompt vô hạn (kỹ thuật "conversation summarization", phổ biến ở các chat AI chuyên nghiệp có hội thoại dài).
- [ ] **6.9 Test end-to-end** — 2 session cùng 1 document → chat riêng từng session, lịch sử không lẫn nhau; test follow-up thật trong cùng 1 session ra câu trả lời đúng ngữ cảnh mà người dùng không cần lặp lại toàn bộ câu hỏi.

> **Lưu ý về chi phí test:** các bước 6.7–6.9 gọi LLM thật. Giữ đúng nguyên tắc đã thống nhất — test bằng vài kịch bản hỏi nối tiếp cụ thể, KHÔNG chạy lại toàn bộ golden dataset cho mỗi lần sửa.

**DoD:**
1. Tạo 2 session cho cùng 1 document → chat riêng từng session → lịch sử không lẫn nhau.
2. Hỏi nối tiếp (follow-up) trong cùng session ra câu trả lời đúng ngữ cảnh nhờ `contextualize_question`, không cần người dùng tự lặp lại toàn bộ câu hỏi.
3. User khác gọi vào session không phải của mình → 404 (không phải 403).
4. Sau khi chat, session vừa dùng nằm ĐẦU `GET /api/sessions`.
5. Tải lại lịch sử vẫn thấy đủ trích dẫn và vẫn gửi 👍/👎 được cho câu trả lời cũ.
6. Vượt quota → 429; circuit breaker mở → 503 (chứng minh endpoint mới KHÔNG lọt qua guardrail 5.6).

---

[← Previous: Phase 5.6](phase-5.6-guardrails-observability.md) · [Back to overview](README.md) · [Next: Phase 7 — Streaming (SSE) →](phase-7-streaming.md)
