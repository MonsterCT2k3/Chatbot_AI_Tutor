[← Back to overview](README.md)

## Phase 10 — Hardening & vận hành

- [ ] Rate limit route `/api/sessions/{id}/messages` (tránh spam OpenAI API tốn tiền)
- [ ] Giới hạn dung lượng/số file upload mỗi user (free tier Supabase 500MB, R2 10GB)
- [ ] Log lỗi ingestion rõ ràng (`error_message`) để debug khi parser fail với PPTX lạ
- [ ] GitHub Action ping định kỳ (tránh Supabase free tier tự pause sau 7 ngày không request)
- [ ] Viết `alembic` migration chính thức thay vì chạy tay `schema.sql` (để version control schema)
- [ ] CORS: đổi `allow_origins=["*"]` thành domain thật trước khi public

---

[← Previous: Phase 9](phase-9-frontend.md) · [Back to overview](README.md)
