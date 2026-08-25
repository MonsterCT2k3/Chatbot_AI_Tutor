[← Back to overview](README.md)

## Phase 9 — Frontend (React)

**Rà lại 2026-08-25.** Phase này **đã dựng sớm** (2026-08-19 → 23), rồi nối tiếp qua Phase 6/7/8. Bản mô tả “còn chờ backend” phía dưới **lạc** — file này thay thế phần đó bằng trạng thái thật + checklist dọn sót.

---

### Mục tiêu (DoD gốc — đã đạt)

Luồng browser end-to-end:

**đăng ký / đăng nhập → upload PDF → chờ `ready` → hỏi trong session → thấy status/stream → citation nhảy trang + chỉ báo nguồn (chip/viền; có bbox thì tô vùng) → F5 còn lịch sử + 👍/👎.**

---

### Tech stack (thực tế)

React 18 + Vite 5 + React Router v7 + axios + `react-pdf` + `lucide-react`. CSS thuần + design tokens. Auth state: React Context. **Không** EventSource (chat = POST + JWT → `fetch` SSE).

**Layout:** 3 panel (sidebar tài liệu + viewer + chat) — khác bản kế hoạch 2 cột, theo mock HTML tự làm (`fe/src/mock_html_ui/`).

---

### Bản kế hoạch / ghi chú 2026-08-23 lệch chỗ nào

| Viết năm 2026-08-23 | Hiện tại (sau 6–8) |
|---|---|
| Chat `POST /documents/{id}/ask` | Session SSE `POST /sessions/{id}/messages?stream=1` (7.5); `/ask` hỏi đã xoá (7.6); feedback URL cũ giữ |
| Session sidebar mock | Session list / tạo / xoá + lịch sử trong chat header (Phase 6) |
| Chưa stream | SSE `status` → `token` (+ `citation` / `replace` / `done`); token = full câu tiếng Việt (chốt 7.1 — không typewriter) |
| Chỉ nhảy trang, chưa highlight vùng | 8.1 auto-jump + 8.2 chip/viền trang + 8.3b rect bbox (null → fallback trang) |
| `EventSource` trong mô tả gốc | **Không dùng** — đúng quyết định Phase 7 |

Giữ nguyên các quyết định đúng từ lúc dựng sớm:

- JWT `localStorage` + axios refresh 1 lần khi 401; `fetch` SSE tự refresh riêng (7.5).
- Nút chưa có backend → **disabled** + tooltip “Chưa hỗ trợ” (không giả hoạt động).
- Backend phát sinh lúc làm FE: `GET .../thumbnail` + CORS R2 (đã xử lý).

---

### Đã xong (không làm lại)

| Khu vực | Nội dung |
|---|---|
| Auth | Signup / signin / logout / me; interceptor envelope + refresh |
| Dashboard | List / upload / poll status / thumbnail / xoá |
| Workspace | Sidebar tài liệu (collapse), `SlideViewer` (zoom, phím, filmstrip), `ChatPanel` |
| Session | List theo document, tạo mới, chọn, xoá; `?session=`; `listMessages` F5 |
| Chat | SSE stream, status tiếng Việt, feedback 👍/👎 |
| Citation UX | Click + auto-jump; chip/viền trang; overlay rect khi có `bbox` |

---

### Còn sót — checklist dọn (không blocker lõi)

Làm khi muốn “đóng” Phase 9 gọn; có thể tách spec ngắn từng mục.

| # | Việc | Ghi chú |
|---|---|---|
| **[9.1](specification-for-phase-9/9.1-rename-session.md)** | UI **đổi tên session** (inline edit + `PATCH`) | **Xong** (review PASS) |
| **[9.2](specification-for-phase-9/9.2-stale-comments.md)** | Sửa comment / CSS header còn nói mock session, chat `/ask` | **Xong** (review PASS) |
| **[9.3](specification-for-phase-9/9.3-quota-label.md)** | Quota sidebar: giữ thanh + copy “mốc UI / chưa giới hạn tài khoản” | **Xong** (review PASS) |
| **9.4** | Cập nhật overview README / bảng phase | Đồng bộ “Phase 8/9 xong” (làm kèm lần rà này) |

**Ngoài phạm vi Phase 9** (giữ disabled trừ khi mở product/phase riêng):

- Google / SSO, quên mật khẩu  
- Đính kèm file / mic trong ô chat  
- “Layout trình chiếu”, “Tìm trong tài liệu” trên viewer  
- Stream chữ từng từ tiếng Việt  
- Backfill bbox mọi document cũ  

Vận hành / bảo mật deploy: xem [Phase 10](phase-10-hardening.md).

---

### DoD phase (chốt lại 2026-08-25)

- [x] E2E browser: auth → upload → ready → hỏi session SSE → citation UX (trang ± bbox) → F5 + feedback  
- [x] Không còn phụ thuộc “chờ Phase 6/7/8” cho các mục trên  
- [x] Checklist dọn 9.1–9.3 (9.4 README đã sync khi rà Phase 9)

Spec chi tiết: [`specification-for-phase-9/`](specification-for-phase-9/).

---

[← Previous: Phase 8](phase-8-citation-highlight.md) · [Back to overview](README.md) · [Next: Phase 10 — Hardening →](phase-10-hardening.md)
