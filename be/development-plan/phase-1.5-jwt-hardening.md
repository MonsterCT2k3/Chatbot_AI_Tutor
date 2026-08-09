[← Back to overview](README.md)

## Phase 1.5 — JWT Hardening: Refresh Token + Revocation + Rate Limit ✅ HOÀN THÀNH

**Vì sao làm phase này (chen ngang, tạm dừng Phase 3):** đánh giá lại hệ thống JWT hiện tại phát hiện 2 lỗ hổng thật — access token sống 60 phút không refresh được (hết hạn phải đăng nhập lại từ đầu), và `logout` không thực sự thu hồi được gì (token cũ vẫn dùng được tới khi tự hết hạn). Đã cân nhắc bộ tính năng "JWT chuyên nghiệp" đầy đủ (rotation, `jti`, logout-all-devices, httpOnly cookie, secret rotation...) và **chủ động bỏ bớt** những phần không tương xứng với quy mô dự án cá nhân hiện tại — xem lý do từng phần trong bảng dưới, tránh over-engineering.

**Trong scope Phase này:**
1. Refresh token — lưu DB (hash), có thể thu hồi.
2. Access token rút ngắn còn 15 phút (an toàn hơn, vì giờ đã có refresh token lo phiên dài).
3. `POST /api/auth/refresh` — đổi refresh token lấy access token mới.
4. `logout` thu hồi thật — set `revoked=true` trong DB.
5. Rate limit `/login` — chặn brute-force đoán mật khẩu.

**Cố ý KHÔNG làm ở phase này (ghi chú lại lý do, không phải quên):**
| Bỏ qua | Lý do |
|---|---|
| Refresh token rotation + phát hiện đánh cắp | Thêm độ phức tạp thật (token family, xử lý race condition) để chống 1 kiểu tấn công cụ thể — chưa tương xứng quy mô hiện tại. |
| `jti` claim / thu hồi từng access token | Access token giờ chỉ sống 15 phút — tự giới hạn thiệt hại rồi, không cần cơ chế thu hồi riêng cho nó. |
| Endpoint "đăng xuất mọi thiết bị" | Thiết kế DB bên dưới (`refresh_tokens` theo `user_id`) đã đủ để thêm rẻ sau này (`revoke where user_id = X`) — chưa cần endpoint riêng ngay. |
| Refresh token qua httpOnly cookie | Cần frontend phối hợp (CORS credentials, SameSite) — chưa có frontend để test, sẽ làm khi tới phase frontend. |
| Secret rotation, thu hồi khi đổi mật khẩu | Chưa có tính năng đổi mật khẩu để nối vào; secret rotation không tương xứng quy mô hiện tại. |

**9 bước:**

- [x] **1.5.1 Schema: bảng `refresh_tokens`** — `id, user_id (FK cascade), token_hash, expires_at, revoked (bool, default false), created_at`. Model + Alembic migration (`77a6aaf62202`) thật, `schema.sql` đồng bộ (kèm sửa luôn phần `converted_pdf_key` bị sót từ Phase 3 trước đó).
- [x] **1.5.2 `auth_service`: tạo & verify refresh token** — `secrets.token_urlsafe(32)` + SHA-256. Test: happy path, sai token, hết hạn, đã revoke — cả 4 case PASS.
- [x] **1.5.3 Tách cấu hình thời hạn token** — `ACCESS_TOKEN_EXPIRE_MINUTES=15`, `REFRESH_TOKEN_EXPIRE_DAYS=30`. Verify token thật hết hạn đúng 15 phút.
- [x] **1.5.4 `signup`/`login` trả về cả 2 token** — verify mỗi lần đăng nhập tạo 1 row `refresh_tokens` riêng (2 lần login = 2 row độc lập, đúng ý đồ multi-session).
- [x] **1.5.5 `POST /api/auth/refresh`** — không rotate (theo quyết định phạm vi). Test: valid/garbage/revoked/expired đều đúng.
- [x] **1.5.6 `logout` thu hồi thật** — có thêm kiểm tra **ownership** (chỉ thu hồi được refresh token của chính mình) không có trong plan gốc — phát hiện lúc code: nếu không check, user A có thể truyền refresh token của user B (nếu đoán/biết được) để logout hộ người khác. Đã test riêng: cross-user attempt bị từ chối VÀ không làm hỏng token của nạn nhân.
- [x] **1.5.7 Rate limit `/login`** — `slowapi`, 5 lần/phút/IP, in-memory. **Lưu ý:** giới hạn per-process — nếu sau này chạy nhiều worker, hiệu lực thực tế = 5 × số worker; lúc đó mới cần chuyển sang Redis backend.
- [x] **1.5.8 Test các trường hợp lỗi** — expired/revoked/malformed/missing refresh token, xác nhận access token mới luôn ~15 phút — 5/5 case PASS.
- [x] **1.5.9 Test end-to-end đầy đủ** — 7/7 case PASS, xác nhận đúng hành vi: refresh token chết ngay sau logout, access token cũ vẫn sống tới khi tự hết hạn (chấp nhận được, tối đa 15 phút).

**DoD:** ✅ access token sống 15 phút, refresh token thu hồi được thật (test HTTP thật), `/login` có rate limit, không phá vỡ luồng auth cũ.

---

[← Previous: Phase 1](phase-1-auth.md) · [Back to overview](README.md) · [Next: Phase 2 — Document upload →](phase-2-document-upload.md)
