[← Kế hoạch Phase 7](../phase-7-streaming.md)

# Đặc tả kỹ thuật — Phase 7

Kế hoạch **trước khi code**. Khác `explain-logic/` (viết sau khi làm xong).

Bản Phase 7 gốc đã lạc so với `send_message` + structured citation + FE session — kế hoạch mới: [`../phase-7-streaming.md`](../phase-7-streaming.md).

| File | Bước | Trạng thái |
|---|---|---|
| [7.1-stream-structured.md](7.1-stream-structured.md) | Đo Groq structured stream; chốt cách token + citation | **A** (API `beta.stream`); UX gần B — không delta chữ Việt |
| [7.2-sse-middleware-status.md](7.2-sse-middleware-status.md) | Middleware không nuốt SSE; POST messages nhánh SSE + `status`; generation vẫn blocking | **Xong** — JSON mặc định; SSE `?stream=1` |
| [7.3-generate-beta-stream.md](7.3-generate-beta-stream.md) | `_generate_structured` = `beta.stream`; `ask_events`; `status: generating`; token vẫn full tiếng Việt | **Xong** |
| [7.4-judge-after-token.md](7.4-judge-after-token.md) | Judge/mod sau `token`; `replace` nếu đổi câu; save chỉ bản final | **Xong** |
| [7.5-sse-frontend.md](7.5-sse-frontend.md) | FE `fetch` SSE: status / token / citation / replace / done; không EventSource | **Xong** (review PASS) |
| [7.6-delete-ask.md](7.6-delete-ask.md) | Xoá `POST /documents/{id}/ask`; giữ feedback + `ask()` eval | **Xong** (review PASS) |
