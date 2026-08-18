[← Kế hoạch Phase 5.6](../../development-plan/phase-5.6-guardrails-observability.md) · [← Tất cả các phase](../README.md)

# Phase 5.6 — Guardrails, Safety & Observability: giải thích luồng code

Mỗi bước nhỏ (5.6.1, 5.6.2...) có 1 file riêng trong folder này — dữ liệu/code thật, ý nghĩa, tại sao cần bước đó, tại sao làm theo cách đó, test đã chạy, và bước đó nối vào đâu ở các bước sau. Cùng format đã dùng ở [Phase 5.5](../phase-5.5-advanced-rag/README.md).

## Các bước

- [x] [5.6.1 — Content moderation trên câu hỏi người dùng](5.6.1-input-content-moderation.md)
- [x] [5.6.2 — Direct prompt injection / jailbreak defense](5.6.2-direct-prompt-injection.md)
- [x] [5.6.3 — Scope enforcement (không đạt) + bug ivfflat index nghiêm trọng phát hiện giữa chừng](5.6.3-scope-enforcement.md)
- [x] [5.6.4 — Content moderation trên câu trả lời của AI](5.6.4-output-content-moderation.md)
- [x] [5.6.5 — Chốt hành vi khi faithfulness fail + đo ngưỡng 0.7 lần đầu](5.6.5-faithfulness-failure-behavior.md)
- [x] [5.6.6 — Giới hạn số câu hỏi/ngày theo user (+ bảng `ai_usage_log`)](5.6.6-daily-question-quota.md)
- [x] [5.6.7 — Theo dõi ngân sách token/chi phí mỗi user](5.6.7-token-cost-tracking.md)
- [x] [5.6.8 — Circuit breaker chống lạm dụng/tấn công (toàn hệ thống)](5.6.8-circuit-breaker.md)
- [x] [5.6.9 — Structured logging cho mọi lệnh gọi AI](5.6.9-structured-logging.md)
- [x] [5.6.10 — Prompt versioning: kỷ luật bump thật + so sánh chất lượng](5.6.10-prompt-versioning.md)
- [x] [5.6.11 — Structured citation output: bỏ regex, dùng JSON schema thật](5.6.11-structured-citation.md)
- [x] [5.6.12 — Feedback loop: 👍/👎 + lý do tùy chọn](5.6.12-feedback-loop.md)
