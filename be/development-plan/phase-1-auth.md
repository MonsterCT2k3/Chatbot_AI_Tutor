[← Back to overview](README.md)

## Phase 1 — Auth module ✅ HOÀN THÀNH

**Vì sao làm trước:** mọi route khác đều cần `current_user`, làm sau sẽ phải sửa lại toàn bộ router.

**9 bước, làm và test từng bước trước khi qua bước tiếp theo:**

- [x] **1.1 Password hashing** — `hash_password`/`verify_password` trong `app/services/auth_service.py`. Ban đầu dùng `passlib[bcrypt]` theo kế hoạch nhưng **passlib không tương thích với bcrypt >=4** (thư viện passlib đã ngừng phát triển từ 2020) → đổi sang gọi thẳng package `bcrypt`, bỏ passlib khỏi `requirements.txt`.
- [x] **1.2 JWT create/decode** — `create_access_token(user_id)`, `decode_access_token(token)` trong `auth_service.py`. Test: token hợp lệ, token hết hạn, token sai chữ ký đều raise đúng.
- [x] **1.3 Pydantic schemas** — `app/schemas/auth.py`: `SignupRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`. Cần thêm `pydantic[email]` (package `email-validator`) cho `EmailStr`.
- [x] **1.4 `get_current_user` dependency** — `app/dependencies.py`: `OAuth2PasswordBearer` + `get_current_user(token, db) -> User`, raise 401 nếu token invalid/user không tồn tại.
- [x] **1.5 `POST /api/auth/signup`**
- [x] **1.6 `POST /api/auth/login`**
- [x] **1.7 `GET /api/auth/me`** — route bảo vệ, verify dependency hoạt động đúng.
- [x] **1.8 `POST /api/auth/logout`** — MVP stateless, chỉ cần token hợp lệ để gọi, không revoke gì server-side (token cũ vẫn dùng được tới khi hết hạn — đã verify đúng ý đồ thiết kế qua test).
- [x] **1.9 Test end-to-end toàn bộ luồng** — 10 cases (signup, duplicate signup, login đúng/sai, /me có/không/sai token, logout có/không token, xác nhận token còn sống sau logout) — tất cả PASS.

**Việc phát sinh ngoài 9 bước gốc (làm thêm trong Phase 1 vì cần thiết cho production-readiness):**
- **Chuẩn hoá response envelope toàn cục** — mọi response (thành công lẫn lỗi) đều có dạng `{success, message, data, error, requestId}` (`app/middleware.py` + `app/exceptions.py`), áp dụng tự động cho mọi route hiện tại và tương lai.
- **Tách logic nghiệp vụ khỏi router** — router chỉ lo HTTP (parse request, chọn status code), toàn bộ business logic + DB access nằm trong `auth_service.py` (mô hình gần giống Controller/Service của Spring, không có tầng Repository riêng vì `AsyncSession` của SQLAlchemy đã đóng vai trò đó).

**DoD:** ✅ Toàn bộ 9 bước + test end-to-end đều pass qua HTTP thật (không chỉ test nội bộ).

---

[← Previous: Phase 0](phase-0-infrastructure.md) · [Back to overview](README.md) · [Next: Phase 1.5 — JWT Hardening →](phase-1.5-jwt-hardening.md)
