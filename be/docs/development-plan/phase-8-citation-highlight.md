[← Back to overview](README.md)

## Phase 8 — Citation UX trên viewer (jump trang + overlay nhẹ)

**Rà lại 2026-08-25.** Bản gốc ngắn và **lạc** so với code sau Phase 5.6–7 + FE workspace. File này thay thế bản đó. Spec chi tiết: [`specification-for-phase-8/`](specification-for-phase-8/).

---

### Bản cũ lệch chỗ nào

| Bản gốc | Code / FE hiện tại | Nếu làm nguyên chữ |
|---|---|---|
| “Đảm bảo `event: citation` có `page_number`” (việc BE còn lại) | Đã có từ **5.6.11** + SSE 7.2–7.4: `page_number`, `chunk_id`, `snippet`. `citations_from_structured_answer` map segment → chunk | Làm lại “resolver” BE vô ích / đụng RAG |
| `highlightRegion(page_number)` như API viewer chưa có | `ChatPanel` **đã** `setPageNumber(c.page_number)` khi bấm badge; `SlideViewer` (`react-pdf`) nhảy trang | Coi jump-on-click là Phase 8 → trùng việc đã xong |
| Để ngỏ bbox / “có thể quay Phase 3” | Cột `document_chunks.bbox` **tồn tại**, **không chỗ nào ghi** trong ingestion | Phase 8 bị treo vì quyết định ingestion nặng |
| DoD: “lúc AI trả lời, panel trái tự cuộn/highlight” | SSE đã gửi `citation` giữa stream; FE **chưa** auto-jump / chưa overlay | Đúng phần UX còn thiếu — nhưng bản cũ không tách khỏi bbox |

Những chỗ **vẫn đúng, giữ hướng:**

- Viewer = PDF thật (`react-pdf` / PDF.js), không ảnh PNG từng trang ([Phase 4](phase-4-viewer-api.md)).
- Highlight **vùng chữ theo bbox** là hướng nâng cao hợp lý — nhưng **không** là DoD bắt buộc của Phase 8 lần này (đã chốt với người review: trang + overlay nhẹ).

---

### Hiện trạng (điểm xuất phát)

```
BE   citation SSE / MessageResponse.citations
       = { page_number, chunk_id, snippet }   # không có bbox

FE   click badge  → setPageNumber(page)      # ĐÃ CÓ
     SSE onCitation → chỉ push vào bubble    # chưa đụng viewer
     SlideViewer    → đổi trang, không overlay nguồn
```

`LessonWorkspacePage` đã chia sẻ `pageNumber` / `setPageNumber` giữa `ChatPanel` và `SlideViewer`.

---

### Quyết định chốt

| # | Chốt | Không làm |
|---|---|---|
| 1 | Phase 8 là **UX citation ↔ viewer**, chủ yếu **FE**. Không viết lại RAG / structured citation. | “Citation resolver” service BE mới |
| 2 | **Auto-jump trang** khi nhận citation của lượt trả lời đang stream (citation **đầu tiên** có `page_number`). Click badge giữ như hiện tại. | Đợi user bấm mới nhảy (chỉ polish click) |
| 3 | **Overlay nhẹ cấp trang** khi trang đang xem ∈ trang đang được cite (viền / wash / chip “Nguồn · Trang N” trên viewer). Không cần toạ độ chữ. | Bắt buộc `pdfplumber` + điền `bbox` trong DoD 8 |
| 4 | Nhiều citation: auto-jump **một lần** theo citation đầu; badge khác vẫn click để đổi trang + cập nhật overlay. | Auto-jump lần lượt mọi trang (nhảy loạn) |
| 5 | `replace` với `citations: []` (refusal): **xoá** highlight state. Input-mod chỉ token từ chối: không bật overlay. | Giữ glow trang cũ sau refusal |
| 6 | F5 / đổi session: **không** bắt buộc auto-jump theo tin cũ. Click badge trên lịch sử vẫn nhảy + overlay. | Sync URL `?page=` bắt buộc trong 8 |
| 7 | Protocol citation **giữ** `{ page_number, chunk_id, snippet }`. Không bắt BE thêm field cho 8 core. | Đổi shape SSE / phá FE 7.5 |
| 8 | **Bbox vùng chunk = phụ lục / phase sau** (ghi ở cuối file). Chỉ mở khi overlay trang ổn và có quyết định ingest lại / backfill. | Nhét bbox vào cùng PR với 8.1 |

---

### Chia bước

| Bước | Việc | Plan trước? | DoD gọn |
|---|---|---|---|
| **[8.1](specification-for-phase-8/8.1-auto-jump-highlight-state.md)** | FE: state `highlightedPage` + `revealCitationPage`; citation đầu SSE auto-jump; click badge cùng path; clear khi refusal/đổi session. Overlay CSS = 8.2. | Spec chi tiết | Hỏi grounded: viewer **tự** sang đúng trang khi có citation, không cần bấm |
| **[8.2](specification-for-phase-8/8.2-page-overlay.md)** | Overlay nhẹ: viền/glow + chip `Nguồn · Trang N` khi `highlightedPage === pageNumber`. Clear đã có ở 8.1. Kiểm tra desktop + viewport hẹp. | Spec chi tiết | Thấy rõ trang đang là “nguồn”; rời trang / refusal thì chỉ báo tắt |
| **[8.3](specification-for-phase-8/8.3-bbox-spike.md)** | Spike bbox: đo extract toạ độ chữ trên PDF eval, chốt schema `document_chunks.bbox` + công thức PDF→PDF.js; **CHOICE** GO_WIRE / NO_GO / GO_AFTER_FIX. | **Xong** — `GO_WIRE` | Stdout `CHOICE=`; Kết quả đo có schema + UNION rect |
| **[8.3b](specification-for-phase-8/8.3b-bbox-wire.md)** | Wire: ingest ghi `bbox` (pypdfium2) → citation/SSE/listMessages optional → FE overlay rect; null → giữ 8.2. | Spec chi tiết | Re-ingest eval có bbox; UI thấy ô tô vùng; doc cũ không crash |

Không tách “resolver BE” thành bước. Nếu sau này citation thiếu `chunk_id` trên lịch sử cũ (SET NULL) — overlay trang vẫn chạy nhờ `page_number`.

---

### DoD phase

1. Trong một câu trả lời grounded qua SSE: khi event `citation` tới, panel PDF **đổi sang đúng `page_number`** (không cần click).
2. Trang đó có **chỉ báo visual** (overlay/chip) phân biệt với trang thường.
3. Click badge citation khác → đổi trang + chỉ báo theo đúng trang đó.
4. Refusal / `replace` citations `[]` → không còn chỉ báo nguồn (hoặc tắt ngay).
5. F5: lịch sử + click badge vẫn nhảy trang như Phase 6/7; không regress SSE/chat.
6. **Không** yêu cầu `bbox` khác null; không đổi contract RAG.

Test bằng tay trên FE thật (bắt buộc) + có thể smoke script nhỏ set state — không đủ nếu chỉ test API.

---

### Bbox vùng chữ — 8.3 → 8.3b

DoD **8.1–8.2** (jump + overlay trang) **không** phụ thuộc bbox.

- **[8.3](specification-for-phase-8/8.3-bbox-spike.md)** spike — **xong**, `CHOICE=GO_WIRE` (`pypdfium2`, schema `pdf_user_space`).
- **[8.3b](specification-for-phase-8/8.3b-bbox-wire.md)** wire ingest + citation/SSE + overlay rect FE (fallback trang khi `bbox` null).

---

[← Previous: Phase 7](phase-7-streaming.md) · [Back to overview](README.md) · [Next: Phase 9 — Frontend →](phase-9-frontend.md)
