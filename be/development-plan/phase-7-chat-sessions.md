[← Back to overview](README.md)

## Phase 7 — Chat session CRUD (multi-session)

**Việc cần làm:**
- `app/schemas/session.py`: `SessionCreate`, `SessionResponse`, `SessionUpdate`
- `app/routers/sessions.py`:
  - `POST /api/sessions` — tạo với `document_id` (+ `title` mặc định `"New chat"`)
  - `GET /api/sessions` — list theo user, `order by updated_at desc`
  - `GET /api/sessions/{id}` / `PATCH /api/sessions/{id}` (đổi `title`) / `DELETE /api/sessions/{id}`
  - `GET /api/sessions/{id}/messages` — phân trang (`limit`/`offset` hoặc cursor theo `created_at`)
- Nối `POST /api/sessions/{id}/messages` (Phase 5/6) vào đúng `session_id` thay vì thẳng `document_id` — lấy `document_id` từ session để search

**DoD:** tạo 2 session cho cùng 1 document → chat riêng từng session → lịch sử không lẫn nhau.

---

[← Previous: Phase 6](phase-6-streaming.md) · [Back to overview](README.md) · [Next: Phase 8 — Citation highlight →](phase-8-citation-highlight.md)
