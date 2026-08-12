[← Back to overview](README.md)

## Phase 5.6 — AI Guardrails, Safety & Observability

**Vì sao làm phase này, và vì sao tách riêng khỏi Phase 5.5:** Phase 5.5 làm cho câu trả lời TỐT HƠN (đúng hơn, liên quan hơn). Phase này làm cho hệ thống AN TOÀN và QUAN SÁT ĐƯỢC (observable) khi có người dùng thật — đây là 2 mối quan tâm khác nhau, không nên gộp chung. Một hệ thống RAG có retrieval/reranking xuất sắc nhưng không có guardrail vẫn là 1 hệ thống KHÔNG chuyên nghiệp — guardrail không phải tùy chọn thêm, mà là 1 trụ cột bắt buộc của bất kỳ sản phẩm AI thật nào tiếp xúc với người dùng thật, đặc biệt đây là sản phẩm giáo dục.

**Vị trí trong luồng triển khai:** ngay sau [Phase 5.5](phase-5.5-advanced-rag.md), TRƯỚC [Phase 6](phase-6-chat-sessions.md) — guardrail nên bọc quanh `ask()` càng sớm càng tốt, trước khi xây thêm session/streaming lên trên. Các guardrail theo user (không phải theo session) dùng thẳng `user_id` đã có sẵn từ Phase 1, không cần chờ Phase 6.

**Chia nhỏ theo 7 nhóm việc:**

### A. Input guardrails (trước khi câu hỏi chạm tới retrieval/generation)

- [ ] **5.6.1 Content moderation trên câu hỏi người dùng** — dùng OpenAI Moderation API (`omni-moderation-latest`, miễn phí, nhanh) chặn nội dung độc hại/không phù hợp TRƯỚC KHI xử lý tiếp. Test: gửi thử 1 câu hỏi vi phạm rõ ràng, xác nhận bị chặn với thông báo hợp lý, không lộ ra là do "moderation" (tránh gợi ý cách né).
- [ ] **5.6.2 Direct prompt injection / jailbreak defense** — khác với 5.5.8 (injection GIÁN TIẾP từ nội dung tài liệu): đây là phòng vệ trước việc CHÍNH người dùng cố thao túng system prompt (VD "bỏ qua mọi chỉ dẫn trước đó", "cho tôi biết system prompt của bạn"). Thiết kế system prompt theo nguyên tắc phân cấp chỉ dẫn (instruction hierarchy — chỉ dẫn hệ thống luôn có quyền cao nhất, input người dùng không được phép ghi đè), kèm delimiter rõ ràng đã có ở 5.5.8. Test: chạy qua 1 bộ câu jailbreak phổ biến đã biết (thu thập từ nguồn công khai), xác nhận model không bị lung lay.
- [ ] **5.6.3 Scope enforcement** — chặn lạm dụng chatbot (đang chạy trên OpenAI trả phí) thành chatbot chat chit chit chat chung chung không liên quan tới tài liệu/mục đích học tập (rủi ro chi phí thật, không chỉ rủi ro chất lượng). Có thể tận dụng chính điểm similarity cao nhất từ retrieval (5.1) — nếu quá thấp, nhiều khả năng câu hỏi ngoài phạm vi tài liệu — kết hợp 1 bước phân loại nhẹ nếu cần chính xác hơn. Test: hỏi 1 câu rõ ràng không liên quan gì tới tài liệu/giáo dục, xác nhận bị từ chối lịch sự thay vì trả lời hoặc tốn tiền gọi LLM đầy đủ.

### B. Output guardrails (trước khi trả câu trả lời về người dùng)

- [ ] **5.6.4 Content moderation trên câu trả lời của AI** — kiểm tra output TRƯỚC KHI trả về, không chỉ input — model vẫn có thể tự sinh nội dung không phù hợp dù input sạch.
- [ ] **5.6.5 Quyết định hành vi rõ ràng khi faithfulness check (5.5.7) thất bại** — không chỉ "cảnh báo" mơ hồ như bản nháp trước, mà chọn 1 trong các hành vi cụ thể: từ chối trả lời + giải thích lý do, tự động thử lại 1 lần với prompt nhấn mạnh hơn, hoặc trả kèm disclaimer rõ ràng cho người dùng biết độ tin cậy thấp. Quyết định cụ thể chốt lúc code, nhưng PHẢI là 1 hành vi xác định, không phải "để đó".

### C. Cost guardrails riêng cho AI (khác rate limit request thô ở Phase 10)

- [ ] **5.6.6 Giới hạn số câu hỏi/ngày theo `user_id`** — giới hạn nghiệp vụ (business quota), không phải giới hạn request/giây kỹ thuật. Test: vượt ngưỡng trong ngày → bị chặn với thông báo rõ ràng (VD "đã dùng hết X câu hỏi hôm nay").
- [ ] **5.6.7 Theo dõi ngân sách token/chi phí mỗi user** — cộng dồn token usage thật từ mỗi lệnh gọi (đã có sẵn thông tin này trong response của OpenAI API), cảnh báo khi gần chạm ngưỡng đã đặt.
- [ ] **5.6.8 Circuit breaker chống lạm dụng/tấn công** — nếu chi phí API trong 1 khoảng thời gian ngắn tăng đột biến bất thường (dấu hiệu bot spam hoặc lỗi vòng lặp gọi API), tự động tạm khóa tính năng chat + cảnh báo. Test: giả lập tăng đột biến, xác nhận circuit breaker kích hoạt đúng ngưỡng.

### D. Observability — không thể vận hành AI chuyên nghiệp mà "mù"

- [ ] **5.6.9 Structured logging cho mọi lệnh gọi AI** — log đầy đủ: prompt, response, latency, token usage, chi phí ước tính, model/prompt version — cho MỌI lệnh gọi LLM (không chỉ log lỗi chung chung như Phase 10 đã có). Đây là dữ liệu để debug chất lượng thật và theo dõi chi phí thật, không phải log vận hành thông thường.
- [ ] **5.6.10 Prompt versioning** — đánh version rõ ràng cho system prompt mỗi lần thay đổi, gắn version đó vào log của từng câu trả lời — cho phép so sánh chất lượng giữa các version sau này, đúng tinh thần "đo trước, tối ưu sau" đã áp dụng ở Phase 5.5.

### E. Citation đáng tin cậy hơn (nâng cấp 5.4)

- [ ] **5.6.11 Structured citation output** — thay quy trình sinh tag `[Trang X]` trong văn bản tự do rồi regex parse lại (5.4, vốn giòn — fragile, dễ vỡ nếu model viết sai định dạng tag) bằng OpenAI structured outputs / function calling (JSON schema mode — bắt model trả về đúng 1 cấu trúc JSON đã định nghĩa sẵn thay vì đoán chữ). Đáng tin cậy hơn hẳn: không lo model viết sai format, không lo thiếu/thừa citation, không cần regex.

### F. Feedback loop

- [ ] **5.6.12 Đánh giá câu trả lời (👍/👎 + lý do tùy chọn)** — thêm bảng/endpoint cho phép người dùng đánh giá từng câu trả lời, lưu vào DB. Đây là nguồn tín hiệu chất lượng THẬT theo thời gian sau khi lên production — không có bước này thì không biết hệ thống đang tốt lên hay tệ đi sau khi launch.

### G. Model resilience (ghi chú, mức độ ưu tiên thấp hơn)

- **5.6.13 (cân nhắc, chưa bắt buộc)** — fallback sang model/provider khác nếu OpenAI lỗi kéo dài. Effort thật lớn (phải test lại toàn bộ prompt trên model khác) — ghi chú lại như 1 lựa chọn tương lai, không triển khai ngay trong lần đầu vì chưa tương xứng quy mô hiện tại (giống cách Phase 1.5 đã cố ý bỏ bớt vài phần JWT).

**DoD:** input/output guardrail có test case thật chứng minh chặn được nội dung không phù hợp; cost guardrail test được bằng cách giả lập vượt ngưỡng; observability xem được log thật của vài request mẫu (prompt/response/token/cost/version đầy đủ); feedback loop lưu được đánh giá thật từ ít nhất 1 lượt test; citation chuyển sang structured output không còn phụ thuộc regex.

---

[← Previous: Phase 5.5](phase-5.5-advanced-rag.md) · [Back to overview](README.md) · [Next: Phase 6 — Chat session CRUD + multi-turn →](phase-6-chat-sessions.md)
