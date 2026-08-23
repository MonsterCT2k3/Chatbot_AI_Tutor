# Engineering records

> **Mục đích:** trả lời câu hỏi *"chúng ta đã xây gì, và **vì sao** lại xây như vậy?"*
>
> Đây là **sổ ghi chép kỹ thuật** của dự án — nơi biến việc code thành việc học. Mỗi bản ghi lấy một mảng chức năng và mổ xẻ nó ở mức **hệ thống và quyết định**, không phải mức từng dòng code.

---

## 1. Chỗ đứng của thư mục này

`docs/` có bốn thư mục, mỗi thư mục trả lời một câu hỏi khác nhau. Đừng dùng nhầm:

| Thư mục | Câu hỏi | Nhịp cập nhật |
|---|---|---|
| [`development-plan/`](../development-plan/README.md) | **Sắp xây gì?** | Trước khi code |
| [`architecture/`](../architecture/system-overview.md) | **Hệ thống hoạt động thế nào?** | Ít thay đổi — chỉ khi kiến trúc đổi thật |
| [`explain-logic/`](../explain-logic/README.md) | **Bước đó code ra sao và vì sao vậy?** | Ngay sau mỗi bước nhỏ (6.1, 6.2...) |
| `engineering/` ← đang ở đây | **Đã xây gì, và học được gì?** | Sau khi một mảng chức năng đã hoàn chỉnh |

**Khác biệt giữa `explain-logic/` và `engineering/`** — đây là chỗ dễ lẫn nhất:

- `explain-logic/` bám theo **bước triển khai**. Một file cho một bước (`6.1`, `6.2`). Viết ngay lúc còn nóng, chi tiết, có bằng chứng test cụ thể.
- `engineering/` bám theo **mảng chức năng**. Một file cho cả một hệ thống con (xác thực, RAG pipeline, retrieval). Viết khi mảng đó đã đủ hình hài, nhìn lại được toàn cảnh, và nhấn mạnh vào **đánh đổi, rủi ro, bài học** hơn là chi tiết triển khai.

Nói ngắn gọn: `explain-logic` là **nhật ký**, `engineering` là **bài tổng kết**.

---

## 2. Quy ước đặt tên

```
docs/engineering/
├── 001-authentication.md
├── 002-document-ingestion.md
├── 003-rag-pipeline.md
├── 004-retrieval.md
├── 005-guardrails-observability.md
└── ...
```

- Đánh số tăng dần **theo thứ tự viết**, không theo thứ tự quan trọng. Số chỉ để sắp xếp và tham chiếu, không mang ý nghĩa ưu tiên.
- Tên file mô tả **mảng chức năng**, không phải tên file mã nguồn. `003-rag-pipeline.md` chứ không phải `003-rag-service-py.md`.
- Số không bao giờ được dùng lại, kể cả khi một bản ghi trở nên lỗi thời. Thay vào đó, thêm mục "Cập nhật" vào cuối, hoặc viết bản ghi mới và liên kết chéo hai chiều.

### Các bản ghi hiện có

- [x] [`001-authentication.md`](001-authentication.md) — JWT ngắn hạn + refresh token thu hồi được; vì sao mã lỗi cũng là kênh rò rỉ
- [x] [`002-document-ingestion.md`](002-document-ingestion.md) — bất đồng bộ, chạy nền không bền vững, ba chế độ bóc text
- [x] [`003-rag-pipeline.md`](003-rag-pipeline.md) — bảy chốt chống bịa; vì sao giám khảo phải khác nhà cung cấp
- [x] [`004-retrieval.md`](004-retrieval.md) — năm kỹ thuật, bốn bị loại **có số liệu**; bug index làm mất 14% âm thầm
- [x] [`005-guardrails-observability.md`](005-guardrails-observability.md) — ba lớp hạn mức; biến lỗi âm thầm thành lỗi ồn ào

---

## 3. Cấu trúc một bản ghi

Mỗi bản ghi trả lời **15 câu hỏi** dưới đây, gom thành 5 phần. Không cần theo đúng thứ tự này, nhưng **không nên bỏ sót phần nào** — mỗi phần bù một điểm mù khác nhau.

### Phần A — Cái gì và vì sao

**1. Đã xây gì?**
Mô tả ngắn gọn, đủ để người chưa đọc code hình dung được. Nói về **năng lực**, đừng liệt kê file.

**2. Vì sao phải xây?**
Vấn đề thật nào đã dẫn tới đây? Nếu không xây thì hỏng chuyện gì? Câu này lộ ra ngay những thứ được xây vì "nghe có vẻ nên có".

**3. Nó nằm ở đâu trong hệ thống?**
Liên kết tới [`architecture/`](../architecture/system-overview.md) thay vì chép lại. Chỉ rõ nó **phụ thuộc vào** cái gì và **cái gì phụ thuộc vào nó**.

### Phần B — Cách nó chạy

**4. Luồng request/dữ liệu diễn ra thế nào?**
Dùng sơ đồ (Mermaid hoặc ASCII). Vẽ ở **tầng hệ thống**, không phải tầng dòng lệnh — người đọc cần biết dữ liệu đi qua những hộp nào, không cần biết bên trong một hộp có bao nhiêu vòng lặp.

**5. Có những thành phần nào tham gia?**
Kể cả thành phần bên ngoài: DB, object storage, LLM API, thư viện. Cái gì bên ngoài thì cái đó có thể hỏng.

### Phần C — Vì sao thiết kế thế này

**6. Vì sao chọn thiết kế này?**

**7. Có những phương án nào khác?**
Nếu không viết ra được phương án nào bị loại, khả năng cao là chưa thật sự cân nhắc — chỉ là làm theo cách nghĩ ra đầu tiên.

**8. Đánh đổi là gì?**
**Bắt buộc phải có phần bất lợi.** Một thiết kế không có nhược điểm nào là dấu hiệu của việc chưa hiểu nó đủ sâu, chứ không phải dấu hiệu của thiết kế tốt.

### Phần D — Cái gì có thể hỏng

**9. Cái gì có thể hỏng?**
Phân loại theo mức độ **ồn ào**, vì đây mới là điều quyết định độ nguy hiểm:

| Loại | Nghĩa là gì | Mức nguy hiểm |
|---|---|---|
| 🔊 **Ồn ào ngay** | Có exception, có log, hỏng ở gần chỗ gây lỗi | Thấp — sẽ được sửa |
| 🔊 **Ồn ào nhưng muộn** | Có lỗi, nhưng xa chỗ gây ra cả về thời gian lẫn vị trí | Trung bình |
| 🔇 **Âm thầm** | Dữ liệu sai, kết quả sai, **không có lỗi nào báo ra** | **Cao nhất** |

Phần lớn công sức kỹ thuật tốt là **biến lỗi âm thầm thành lỗi ồn ào**.

**10. Vấn đề bảo mật?**
Ai được đọc dữ liệu này? Kiểm tra quyền nằm ở đâu? Có rò rỉ thông tin qua **mã lỗi** hay **độ trễ** không?

**11. Vấn đề hiệu năng / mở rộng?**
Chỗ nào tắc trước tiên khi tải tăng? Cái gì đang chạy trong tiến trình web mà lẽ ra không nên?

### Phần E — Học được gì

**12. Kiểm chứng bằng cách nào?**
Ghi **con số thật**, không ghi "đã test kỹ". Ghi luôn cả những gì **chưa** kiểm chứng — đó cũng là thông tin.

**13. Học được gì?**
Bài học **mang đi được sang dự án khác**, không chỉ đúng với repo này.

**14. Còn câu hỏi nào chưa trả lời được?**
Chỗ nào đang tin mà chưa chứng minh? Chỗ nào đang làm theo thói quen? Nếu để trống mục này, nhiều khả năng là chưa nghĩ đủ.

**15. Cải tiến hợp lý trong tương lai?**
Kèm **điều kiện kích hoạt**: *"khi số chunk mỗi tài liệu vượt ~10 nghìn thì cân nhắc HNSW"* hữu ích hơn nhiều so với *"cân nhắc thêm index"*.

---

## 4. Nguyên tắc viết

### Giải thích VÌ SAO, không chỉ CÁI GÌ

> ❌ "Tạo `ChatService`."
>
> ✅ "`ChatService` giữ toàn bộ nghiệp vụ xử lý một lượt chat, để phần thuộc về HTTP (mã trạng thái, hình dạng request) nằm lại ở tầng router. Nhờ vậy các script đánh giá offline gọi thẳng service được mà không cần dựng server."

### Giải thích quan hệ, không chỉ liệt kê thành phần

Đừng chỉ mô tả A, B, C riêng lẻ. Phải nói được **A → B → C** và **vì sao mũi tên đó tồn tại**: B cần gì từ A, và điều gì hỏng nếu bỏ B đi.

### Không mặc định cách làm hiện tại là "best practice"

Mỗi lựa chọn đều có bối cảnh. Điều đúng ở quy mô hàng trăm chunk có thể sai hẳn ở hàng triệu. Viết **điều kiện** mà lựa chọn đó còn đúng, đừng viết như thể nó đúng vĩnh viễn.

### Không bịa

Trước khi viết: đọc code, đọc tài liệu đã có, kiểm tra thực tế. Phân biệt rõ ba thứ:

- **Đang có** — đã chạy, kiểm chứng được
- **Đã lên kế hoạch** — dẫn link tới `development-plan/`
- **Có thể làm sau** — ghi rõ là ý tưởng

Nếu không chắc, **đi kiểm tra**, hoặc viết thẳng "chưa xác minh". Một tài liệu sai còn tệ hơn không có tài liệu, vì người đọc sẽ tin nó.

### Ghi lại cả cái sai

Những quyết định **đã thử và bỏ** thường có giá trị dạy học cao hơn quyết định cuối cùng — chúng cho biết đường nào là ngõ cụt. Dự án này đã có sẵn vài ví dụ đắt giá: hybrid search và semantic caching bị loại **sau khi đo**, index `ivfflat` âm thầm làm mất 14% kết quả retrieval, và `now()` của Postgres đứng yên trong suốt một transaction.

---

## 5. Khi nào nên viết một bản ghi

Nên viết khi:

- Một mảng chức năng vừa hoàn chỉnh (xác thực xong, RAG pipeline chạy được end-to-end)
- Một quyết định kiến trúc quan trọng vừa được chốt
- Vừa gỡ được một lỗi khó, mà nguyên nhân dạy được điều gì đó
- Vừa **đo và loại bỏ** một kỹ thuật — ghi lại để sau này không thử lại một cách mù quáng

Không cần viết khi:

- Chỉ sửa lỗi vặt, đổi tên, dọn dẹp
- Nội dung đã được `explain-logic/` bao phủ đầy đủ và không có gì để tổng kết thêm

---

## 6. Bản đồ các bản ghi

Năm mảng đã hoàn thành của dự án đều đã có bản ghi:

| | Mảng | Vì sao đáng viết |
|---|---|---|
| ✅ `001` | Xác thực | Đánh đổi JWT ngắn hạn + refresh token lưu DB; quy tắc 404 thay vì 403 |
| ✅ `002` | Nạp tài liệu | Bất đồng bộ, chạy nền không bền vững, ba chế độ bóc text |
| ✅ `003` | RAG pipeline | Bảy chốt kiểm soát và lý do từng chốt tồn tại |
| ✅ `004` | Retrieval | Câu chuyện đo lường: rerank được nhận, hybrid/multi-query bị loại, và bug index ivfflat |
| ✅ `005` | Guardrails & observability | Quota, circuit breaker, ghi log để trả lời được "prompt mới có tốt hơn không" |
