[← Back to overview](README.md)

## Phase 7 — Streaming (SSE)

**Rà lại 2026-08-25.** Bản gốc (kể cả cập nhật 2026-08-23) **không còn triển khai được như đã viết** — lệch code Phase 6 và FE. File này thay thế bản đó. Chi tiết kỹ thuật các bước cần chốt trước khi code: [`specification-for-phase-7/`](specification-for-phase-7/).

Thứ tự 6 → 7 vẫn đúng: lưu tin cần `session_id` thật. Điều kiện đó **đã có** (`send_message`, FE gọi `POST /sessions/{id}/messages`).

---

### Bản cũ lệch chỗ nào

| Bản gốc | Code / FE hiện tại | Nếu làm nguyên chữ |
|---|---|---|
| Đổi `ask()` thành generator `create(..., stream=True)` | `ask()` dùng `.parse(..., response_format=StructuredAnswer)` — citation lấy từ `page_number`, không regex. Eval gọi `ask()` không HTTP | Mất structured citation, hoặc phá eval |
| Router `app/routers/messages.py` | POST đang ở `sessions.py`, cùng URL FE đang dùng. `messages.py` chỉ còn comment | Đôi URL / hai chỗ lưu |
| `EventSource` | EventSource **chỉ GET**. Chat là POST + JWT | Không gắn được `Authorization`, không gửi body |
| Envelope JSON mọi response thành công | `ResponseEnvelopeMiddleware` **đọc hết body** rồi bọc `{success, data}` | SSE bị buffer thành 1 JSON, mất stream |
| Xoá `/ask` khi FE chuyển session | FE **đã** chuyển; 👍/👎 vẫn `/documents/{id}/ask/{answer_id}/feedback` | Xoá `/ask` được; **cấm** xoá feedback |
| Judge sau stream — đúng hướng | `score_faithfulness` đang **chặn** trước khi HTTP trả | Cần tách khỏi đường hiện token |
| Output moderation: để ngỏ buffer vs stream ngay | Chưa chốt | Làm 2 nhánh sẽ lệch |

Những chỗ bản 2026-08-23 **vẫn đúng, giữ:**

- Retrieval + contextualize **xong rồi mới** stream generation.
- Lúc `done`: **tái sử dụng** `save_assistant_message` / `touch_session` / `ai_usage_log_id` (6.4–6.6). Không viết lối lưu thứ hai.
- Judge cần full text → sau khi generation kết thúc.

---

### Hiện trạng (điểm xuất phát)

```
FE  POST /sessions/{id}/messages  →  JSON MessageResponse (chờ hết)
        send_message:
          history → save_user (T1) → contextualize → ask_for_user
          ask(): moderate gốc → embed/rerank → parse structured → judge → moderate ra
          save_assistant + citations + metadata
```

Cảm nhận chậm ~8–10s: phần lớn **trước** generation (moderate, embed, vector, rerank). Stream **không** làm đoạn đó thành 1–2s; nó cho (1) hiện trạng thái lúc retrieve, (2) chữ chảy trong ~1–2s generation.

---

### Quyết định chốt

| # | Chốt | Không làm |
|---|---|---|
| 1 | Giữ `ask()` **blocking** cho eval và `/ask` (nếu còn). Thêm đường stream riêng (`ask_stream` / `send_message_stream`). | Biến `ask()` thành generator duy nhất |
| 2 | Cùng URL `POST /api/sessions/{id}/messages`, **đổi sang SSE** (FE đổi theo). Không dual JSON+SSE trên một handler. | `EventSource`. Router mới trên `messages.py` |
| 3 | Middleware: **không** gom body nếu `Content-Type` là `text/event-stream` | Bọc envelope lên SSE |
| 4 | Event: `status` (retrieve) → `token` → `citation` → `done`; thêm `replace` khi judge/moderation thay câu đã hiện | Buffer vài trăm ms trước khi hiện chữ |
| 5 | Structured citation **không** quay lại regex. **7.1 đo** Groq `parse(..., stream=True)`. Không stream được → xem fallback ở spec 7.1, không đoán lúc implement generation | Hai lần generate (structured + stream text) |
| 6 | Judge + output moderation **sau** generation. Fail: event `replace` (câu từ chối hoặc bản retry). User có thể thấy bản chưa kiểm chứng trong vài giây — chấp nhận (input moderation đã chạy; tài liệu là slide bài giảng) | Chặn stream đến khi judge xong |
| 7 | Retry faithfulness: `replace`/xoá bản 1 rồi stream bản 2, hoặc `replace` một phát nếu không retry kịp. Chốt cụ thể ở 7.4 | Im lặng để bản ungrounded nằm trên UI |
| 8 | Xoá `POST /documents/{id}/ask`. **Giữ** feedback URL | Đổi id 👍/👎 |
| 9 | FE: `fetch` + đọc stream (ReadableStream), parse SSE thủ công | `EventSource` |

---

### Protocol SSE (nháp, khóa ở 7.2)

Mỗi event: `event: <tên>\ndata: <json>\n\n`

| event | Khi | data (ý) |
|---|---|---|
| `status` | Trước token | `contextualize` / `retrieving` / `generating` |
| `token` | Delta generation | `{ "delta": "..." }` |
| `citation` | Có page (cuối generation hoặc từng segment xong) | `{ "page_number", "chunk_id", "snippet" }` |
| `replace` | Judge/moderation/retry thay câu đã hiện | `{ "content": "..." }` |
| `done` | Đã `save_assistant_message` | `{ "message_id", "answer_id", "citations" }` |
| `error` | Quota 429 / breaker / lỗi giữa stream | `{ "code", "message" }` — user message 6.4 **đã** commit |

Lỗi **trước** stream (session 404, document chưa ready): HTTP status như hiện tại, không SSE.

---

### Chia bước

| Bước | Việc | Plan trước? | DoD gọn |
|---|---|---|---|
| **[7.1](specification-for-phase-7/7.1-stream-structured.md)** | Đo Groq structured stream. **Xong:** A = `beta.chat.completions.stream(..., response_format=StructuredAnswer)` + `parsed`. Delta là JSON một cục, không chữ Việt dần — 7.2/7.3 `status` lúc retrieve rồi `token`/`citation` khi parsed đủ. **Không** C (`create` + `json.loads`). | Spike xong | — |
| **[7.2](specification-for-phase-7/7.2-sse-middleware-status.md)** | Middleware không nuốt SSE. POST messages: JSON mặc định (FE giữ); SSE khi `Accept` / `?stream=1`. `status` + `ask_for_user` blocking + một `token` full. **Không** `beta.stream`. | Spec chi tiết | `curl` JSON vẫn envelope; `curl -N` có `status`/`done` |
| **[7.3](specification-for-phase-7/7.3-generate-beta-stream.md)** | `_generate_structured` dùng `beta.stream` (7.1 A). Tách `ask_events`: `retrieving` rồi `generating`. Token = `render_structured_answer`, không JSON thô. Judge vẫn trước token (7.4 mới `replace`). JSON FE không đổi. | Spec chi tiết | SSE có `generating`; JSON envelope vẫn chạy; `ask()` eval không vỡ |
| **[7.4](specification-for-phase-7/7.4-judge-after-token.md)** | `generated` rồi `token`; judge/retry/mod sau; một `replace` nếu câu đổi; DB/`done` = final. JSON FE vẫn chỉ thấy bản judge. Không FE. | Spec chi tiết | Grounded: không `replace`. Mock ungrounded: đúng 1 `replace`, không token lần 2 |
| **[7.5](specification-for-phase-7/7.5-sse-frontend.md)** | FE: `fetch` SSE (`?stream=1`), hiện `status`, append `delta`, citation, `replace`, `done`. Bỏ chờ JSON trên UI. Cấm `EventSource`. | Spec chi tiết | Hỏi một câu: thấy status rồi nội dung; F5 còn tin; 👍/👎 vẫn được |
| **[7.6](specification-for-phase-7/7.6-delete-ask.md)** | Xoá `POST /documents/{id}/ask`. Giữ feedback URL + `ask()` cho eval. | Spec chi tiết | curl `/ask` không còn 200 RAG; OpenAPI sạch; feedback 204; `ask()` smoke OK |

**Không** làm trong Phase 7: highlight bbox (8), parallel embed/moderation, gộp `commit` log (có thể làm phụ lục nhỏ trong 7.3 nếu đụng file, không bắt buộc).

---

### DoD phase

1. `curl -N` POST `/sessions/{id}/messages` thấy `status` rồi `token` (hoặc fallback đã ghi ở 7.1), kết thúc `done` có `message_id` + `answer_id`.
2. F5: lịch sử đủ câu + citation; 👍/👎 theo `answer_id`.
3. Follow-up 6.7 vẫn chạy (contextualize trước `generating`).
4. `ask()` blocking: eval không vỡ.
5. Middleware không biến SSE thành một JSON envelope.

---

[← Previous: Phase 6](phase-6-chat-sessions.md) · [Back to overview](README.md) · [Next: Phase 8 — Citation highlight →](phase-8-citation-highlight.md)
