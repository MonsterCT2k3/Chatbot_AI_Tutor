[← Back to overview](README.md)

## Phase 9 — Frontend (React)

**Việc cần làm (tổng quan, có thể tách plan riêng khi tới lúc):**
- Layout 2 cột: viewer trái dùng `PDF.js`/`react-pdf` load file PDF từ `GET /api/documents/{id}/file` (xem [Phase 4](phase-4-viewer-api.md) — quyết định dùng PDF.js thay vì ảnh tĩnh để vẫn copy/select text được), có `highlightRegion(page)`, chat phải
- Trang login/signup, lưu JWT (localStorage hoặc httpOnly cookie nếu muốn an toàn hơn), gắn `Authorization: Bearer` cho mọi request qua `axios` interceptor
- Upload modal → poll `status` hoặc lắng nghe SSE cho tới khi `ready`
- Session sidebar (list, tạo mới, đổi tên, xóa)
- Khung chat: gửi câu hỏi → `EventSource`/`fetch` streaming → render token dần, khi nhận `citation` thì gọi `highlightRegion`

**DoD:** luồng end-to-end thật trên browser: đăng ký → đăng nhập → upload PDF → chờ ready → hỏi → thấy trả lời stream + trang tự highlight.

---

### Cập nhật (2026-08-23) — đã làm sớm, ngoài thứ tự kế hoạch

Phase này được dựng trong khoảng 2026-08-19 → 23, **trước** Phase 6/7/8. Lý do: đã có sẵn thiết kế HTML tự làm cho các màn hình chính (`fe/src/mock_html_ui/`), và cần 1 giao diện thật để dùng + soi lỗi backend thay vì chỉ `curl`. Phần nào không phụ thuộc Phase 6/7/8 thì làm luôn, phần nào phụ thuộc thì để mock có ghi chú rõ trong code.

**Tech stack thực tế:** React 18 + Vite 5 + React Router v7 + axios + `react-pdf` + `lucide-react`. **Không dùng** CSS framework (dùng CSS thuần + custom properties làm design token) và **không dùng** thư viện state management (React Context là đủ cho quy mô này).

**Khác kế hoạch:** layout là **3 panel** (sidebar tài liệu + viewer + chat), không phải 2 cột như bản kế hoạch — theo đúng thiết kế đã tự làm.

**Đã xong, đã chạy thật trên browser:**

| Màn hình | Nội dung |
|---|---|
| Đăng nhập / Đăng ký | JWT lưu `localStorage`, axios interceptor gắn `Authorization` + **tự refresh token 1 lần** khi gặp 401 rồi gọi lại đúng request cũ |
| Dashboard | Danh sách tài liệu, upload + poll `status` tới khi `ready` (chỉ poll khi thật sự có tài liệu đang xử lý), **ảnh bìa trang 1 thật** |
| Workspace | Sidebar tài liệu (thu gọn được), **viewer PDF thật** (`react-pdf`: vừa khung, zoom, chuyển trang bằng nút rìa + phím ← →, dải thumbnail), **chat thật** gọi `/api/documents/{id}/ask` có trích dẫn bấm được để nhảy tới đúng trang + 👍/👎 |

**Còn thiếu — chờ backend tương ứng:**

| Phần | Chờ phase | Hiện đang |
|---|---|---|
| Sidebar session (list/tạo/đổi tên/xoá) + lịch sử chat lưu lại | [Phase 6](phase-6-chat-sessions.md) | mock tĩnh, có ghi chú trong `WorkspaceSidebar.jsx` |
| Hiển thị token dần khi AI trả lời | [Phase 7](phase-7-streaming.md) | chờ trả lời xong rồi hiện 1 lần |
| Highlight vùng cụ thể trong trang | [Phase 8](phase-8-citation-highlight.md) | chỉ nhảy tới đúng **trang** (`bbox` chưa được điền từ Phase 3) |

Ngoài ra các nút Google/SSO, quên mật khẩu, đính kèm file, ghi âm, "layout trình chiếu", "tìm trong tài liệu" đều **để disabled kèm tooltip "Chưa hỗ trợ"** — cố ý không giả vờ hoạt động, vì backend không có endpoint tương ứng.

**2 việc backend phát sinh, đã làm luôn trong lúc dựng frontend:**
- Thêm `GET /api/documents/{id}/thumbnail` + sinh sẵn ảnh trang 1 bằng `pypdfium2` ngay lúc ingest. Trước đó frontend phải tải cả file PDF (có file 20MB) chỉ để hiện 1 ảnh bìa nhỏ, và làm lại việc đó mỗi lần mở dashboard.
- **Bucket R2 thiếu CORS policy** → trình duyệt chặn tải PDF qua presigned URL. Điểm đáng rút kinh nghiệm: `curl` bỏ qua CORS nên test bằng API **không bao giờ lộ ra lỗi này** — chỉ khi có frontend thật mới thấy. Đã áp policy qua Cloudflare dashboard (API token hiện tại chỉ có quyền Object, không có quyền Admin để đặt CORS bằng script); giữ `scripts/setup_r2_cors.py` cho lần sau khi có token đủ quyền.

**DoD cập nhật:** phần "thấy trả lời stream + trang tự highlight" trong DoD gốc **chưa đạt và chưa thể đạt** ở phase này — nó phụ thuộc Phase 7/8. Sẽ chốt lại DoD gốc sau khi làm xong Phase 6/7/8 và nối frontend vào.

---

[← Previous: Phase 8](phase-8-citation-highlight.md) · [Back to overview](README.md) · [Next: Phase 10 — Hardening →](phase-10-hardening.md)
