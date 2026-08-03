# Kết quả bóc tách PDF: b2.pdf



<!-- START PAGE 1 -->

## [Trang 1]


AI IN ACTION · DAY 02

# Xác định *bài toán* cho AI.

Từ yêu cầu mơ hồ đến **Problem Statement** rõ ràng.

Instructor: Mai Anh Nguyen (Blue)


<!-- END PAGE 1 -->


<!-- START PAGE 2 -->

## [Trang 2]


# Instructor

![img-0.jpeg](img-0.jpeg)

## Mai Anh Nguyen (Blue)

*Generalist Product Builder*

|  **2026** | FPT Long Châu (PM · Healthcare Product)  |
| --- | --- |
|  **2025** | Thongtincuuho.org (Co-founder)  |
|  **2025** | FPT Software AI Center (PM · AI Agent)  |
|  **2021–2025** | Xantus (PM · On-chain Analytics, AI Agent)  |
|  **2016–2021** | DYNO, Kalapa (PM · OCR, eKYC, Credit Scoring)  |

LinkedIn | Facebook

MỞ ĐẦU · INSTRUCTOR

DAY 02 · 02 / 76


<!-- END PAGE 2 -->


<!-- START PAGE 3 -->

## [Trang 3]


# Bốn câu hỏi trọng tâm

— Từ xác định bài toán đến quyết định ứng dụng AI

01 Bài toán có thực sự cần AI giải quyết?
02 Nếu có, giải pháp ở cấp độ nào: Rule, Workflow, hay Agent?
03 Problem Statement đã đủ rõ ràng để triển khai?
04 Khi nào quyết định: Go, Not Yet, hay No-Go?

MỞ ĐẦU - 4 CÂU HỎI

DAY 02 - 03 / 76


<!-- END PAGE 3 -->


<!-- START PAGE 4 -->

## [Trang 4]


# Agenda

— Mục tiêu: Biến yêu cầu mơ hồ thành Problem Statement rõ ràng để ra quyết định

SÁNG

KHUNG LÝ THUYẾT (4H)

- Problem Discovery (Double Diamond, HCD)
- Problem Statement & định lượng hóa
- PAIR ① AI có thêm giá trị?
- PAIR ② Automate/Augment → Rule/Workflow/Agent
- PAIR ③ Reward function & success criteria
- Khi AI sai & UX/HITL
- PS hoàn chỉnh → Go/Not Yet/No-Go

CHIỀU

THỰC HÀNH LAB (4H)

- Cá nhân: Tìm 5 bài toán & điền 3 Problem Cards
- Nhóm: Phân biện chéo, chốt 1 bài toán
- Nhóm: Xác thực dữ liệu & vẽ quy trình
- Nhóm: Xác định giải pháp & ra quyết định
- Cá nhân: Viết nhật ký phản tư (Reflection Log)

BÀI NỘP

CUỐI BUỔI

- Nhật ký tìm và lọc bài toán (Cá nhân)
- Problem Statement hoàn chỉnh (Nhóm)
- Nhật ký phản tư (Cá nhân)

MỞ ĐẦU - AGENDA

DAY 02 - 04 / 76


<!-- END PAGE 4 -->


<!-- START PAGE 5 -->

## [Trang 5]


# Nguyên tắc **tương tác** & Thực hành

— Hình thức trao đổi, bài tập nhanh và nộp sản phẩm chính

01

## Thảo luận nhanh qua Discord

Gửi phản hồi ngắn, câu hỏi nhanh hoặc ý kiến phản biện trực tiếp lên Discord.

02

## Khuyến khích chia sẻ ý tưởng sơ khởi

Ý tưởng không cần hoàn hảo ngay từ đầu; các câu trả lời chưa sâu sẽ là chất liệu để cùng phân tích.

03

## Nộp sản phẩm qua GitHub

Báo cáo thực hành Bài tập Lab ngày 02 được nộp trực tiếp trên GitHub Repository.

*Điểm thưởng (Bonus) dành cho học viên tích cực tương tác.*

MỞ ĐẦU - LUẬT CHƠI

DAY 02 - 05 / 76


<!-- END PAGE 5 -->


<!-- START PAGE 6 -->

## [Trang 6]


# Phát triển Sản phẩm AI (AI Product)

— Sản phẩm tích hợp AI bản chất vẫn là một sản phẩm hoàn chỉnh, kế thừa chứ không thay thế nguyên lý sản phẩm truyền thống.

![img-1.jpeg](img-1.jpeg)

MỞ ĐẦU - NỀN TẢNG

DAY 02 - 06 / 76


<!-- END PAGE 6 -->


<!-- START PAGE 7 -->

## [Trang 7]


# Ba trụ cột nền tảng của AI Product

— Kỹ thuật hệ thống AI · Tư duy sản phẩm · Tư duy thiết kế

![img-2.jpeg](img-2.jpeg)

## AI Engineering

Triển khai RAG, Agent, Guardrails, Evaluation (Đánh giá) và vận hành hệ thống AI thực tế.

![img-3.jpeg](img-3.jpeg)

## Product Thinking (Inspired)

Xác định đúng bài toán, thấu hiểu người dùng, tránh xây dựng những tính năng không mang lại giá trị.

![img-4.jpeg](img-4.jpeg)

## Design Thinking (Everyday Things)

Thiết kế dựa trên mô hình tư duy (Mental Model), cơ chế phản hồi (Feedback) và tối ưu trải nghiệm khi AI sai sót.

NGUỒN Chip Huyen — AI Engineering (O'Reilly, 2025) · Marty Cagan — Inspired (2nd ed.) · Don Norman — jnd.org
MỞ ĐẦU · NỀN TẢNG

DAY 02 · 07 / 76


<!-- END PAGE 7 -->


<!-- START PAGE 8 -->

## [Trang 8]


# Tài liệu xuyên suốt buổi học

— Google PAIR Guidebook là "sách giáo khoa" hôm nay; hai tài liệu phụ đọc thêm

SÁCH GIÁO KHOA HÔM NAY - GOOGLE PAIR

## People + AI Guidebook

6 chương — cẩm nang thiết kế sản phẩm AI lấy con người làm trung tâm

1. User Needs + Defining Success
2. Data Collection + Evaluation
3. Mental Models
4. Explainability + Trust
5. Feedback + Control
6. Errors + Graceful Failure

**Chương 1 — User Needs + Defining Success** là xương sống buổi sáng nay (PAIR ①②③).

ĐỌC THÊM - ANTHROPIC

## Building effective agents

Chọn giải pháp đơn giản nhất: rule/workflow trước, agent chỉ khi thật sự cần — dùng ở PAIR ②.

ĐỌC THÊM - GOOGLE

## Rules of Machine Learning

Các quy tắc thực chiến của Google: giải pháp đơn giản (rule, heuristic) trước, ML sau.

NGUỒN Google PAIR — People + AI Guidebook - Anthropic — Building effective agents - Google — Rules of ML
MỞ ĐẦU - TÀI LIỆU

DAY 02 - 08 / 76


<!-- END PAGE 8 -->


<!-- START PAGE 9 -->

## [Trang 9]


THẢO LUẬN NHANH

'Tôi muốn xây dựng *chatbot AI* cho khách hàng.'

THEO BAN CHATBOT ĐỒ ĐANG LÀM GÌ? — VIẾT CÂU TRẢ LỜI LÊN DISCORD · 3 PHÚT


<!-- END PAGE 9 -->


<!-- START PAGE 10 -->

## [Trang 10]


# "AI chatbot" chưa phải là một bài toán

— Đối tượng khác nhau dẫn đến quy trình (workflow), chỉ số (metrics) và rủi ro khác nhau.

PHỤC VỤ KHÁCH HÀNG

- Giải đáp câu hỏi thường gặp (FAQ) về sản phẩm & chính sách
- Tư vấn và hỗ trợ mua hàng
- Chăm sóc sau mua hàng
- Bán thêm & bán chéo (Upsell & Cross-sell)

đối tượng khác
→ metric khác!

HỖ TRỢ NỘI BỘ

- Phân loại yêu cầu hỗ trợ (Tickets/Questions)
- Tra cứu thông tin nghiệp vụ nhanh
- Đề xuất nhập phần hồi để con người phê duyệt
- Chuyển tiếp câu hỏi phức tạp hoặc rủi ro cao cho nhân sự hỗ trợ

BÀI TOÁN - CHATBOT

DAY 02 - 10 / 76


<!-- END PAGE 10 -->


<!-- START PAGE 11 -->

## [Trang 11]


TÌNH HUỐNG THỰC TẾ

Lớp học 1000 học viên (khóa K3 & K4), số lượng Trợ giảng có hạn.
Dùng AI giải quyết thế nào?

VIẾT CÂU TRẢ LỜI LÊN DISCORD — 5 PHÚT


<!-- END PAGE 11 -->


<!-- START PAGE 12 -->

## [Trang 12]


# Khoan đã, bạn có **hỏi** không?

— Cần thấu hiểu bản chất vấn đề trước khi tìm giải pháp

Học viên gặp khó khăn ở công đoạn nào?

Trợ giảng quá tải ở bước nào?

Quy trình hiện tại đang xử lý ra sao?

Giải pháp này xây dựng phục vụ ai?

*Chưa thấu hiểu **điểm đau (pain point)** thì chưa đề xuất giải pháp.*

BÀI TOÁN - PHÂN TÍCH

DAY 02 - 12 / 76


<!-- END PAGE 12 -->


<!-- START PAGE 13 -->

## [Trang 13]


## BÀI TẬP CÁ NHÂN

*Từ trải nghiệm ngày học đầu tiên, liệt kê ít nhất 3 điểm đau (pain points) bạn quan sát hoặc gặp phải.*

# Nhận diện *điểm đau thực tế*

5 PHÚT - GỬI LÊN DISCORD - BẠN GẶP TẮC NGHẼN Ở ĐÂU?


<!-- END PAGE 13 -->


<!-- START PAGE 14 -->

## [Trang 14]


COUNTER-INTUITIVE RULE

"Do not solve the problem
I am asked to solve."

DON NORMAN · jnd.org


<!-- END PAGE 14 -->


<!-- START PAGE 15 -->

## [Trang 15]


SECTION 01

# Problem Discovery

*Tìm đúng vấn đề trước khi tìm giải pháp — Double Diamond, HCD và các kỹ thuật phân kỳ / hội tụ.*


<!-- END PAGE 15 -->


<!-- START PAGE 16 -->

## [Trang 16]


# Tìm đúng vấn đề trước khi tìm giải pháp

— Mô hình Double Diamond — Don Norman / British Design Council (2005)

![img-5.jpeg](img-5.jpeg)

DIAMOND 1 — TÌM ĐÚNG VẤN ĐỀ

Discover: Mở rộng — khảo sát vấn đề căn bản.

Define: Thu hẹp — xác định đúng bài toán gốc.

DIAMOND 2 — TÌM ĐÚNG GIẢI PHÁP

Develop: Mở rộng — nhiều giải pháp tiềm năng.

Deliver: Thu hẹp — chọn và triển khai.

"Kỹ sư và doanh nhân được đào tạo để giải vấn đề. Nhà thiết kế được đào tạo để khám phá vấn đề thật."

Giải pháp xuất sắc cho sai vấn đề có thể còn tệ hơn không có giải pháp.

NGUỒN Don Norman — jnd.org Design Council — The Double Diamond
BÀI TOÁN · DOUBLE DIAMOND

DAY 02 · 16 / 76


<!-- END PAGE 16 -->


<!-- START PAGE 17 -->

## [Trang 17]


# Diamond 1 — Tìm đúng vấn đề

— Phân kỳ để thấu hiểu sâu sắc, hội tụ để lựa chọn chính xác

DISCOVER · PHÂN KỶ

## Khám phá / mở rộng góc nhìn

- Quan sát thực tế (Observation)
- Phỏng vấn người dùng (User Interview)
- Khảo sát (Survey)
- Nhật ký hành vi (Diary Study)
- Phân tích dữ liệu / Nhật ký hệ thống
- Bản đồ các bên liên quan (Stakeholder Mapping)

DEFINE · HỘI TỤ

## Định nghĩa / chọn lọc dựa vào dữ liệu

- Sơ đồ đồng cảm / Gom nhóm (Affinity Mapping)
- Kỹ thuật đặt câu hỏi 5 Whys
- Ma trận Tác động – Nỗ lực (Impact-Effort)
- Biểu quyết bằng chấm tròn (Dot Voting)
- Câu hỏi mở hướng giải quyết (How Might We)
- Phát biểu bài toán (Problem Statement)

BÀI TOÁN · DIAMOND 1

DAY 02 · 17 / 76


<!-- END PAGE 17 -->


<!-- START PAGE 18 -->

## [Trang 18]


# Quy trình HCD

— Thiết kế lấy con người làm trung tâm: vòng lặp 5 bước bên trong mỗi Diamond

![img-6.jpeg](img-6.jpeg)

**Observation** (Quan sát)

Người được quan sát phải phù hợp với đối tượng mục tiêu — quan sát khách hàng tiềm năng trong cuộc sống bình thường, hiểu các tình huống thực tế họ gặp phải.

**Ideation** (Tạo ra ý tưởng)

Tạo nhiều ý tưởng, sáng tạo không bị ràng buộc bởi các hạn chế. Tránh phê bình ý tưởng của bản thân hay người khác. Đặt câu hỏi về tất cả mọi thứ.

**Prototype** (Tạo mẫu thử)

Tạo nguyên mẫu nhanh cho mỗi giải pháp tiềm năng — mục tiêu là kiểm tra nhanh nhất có thể trước khi build.

**Test** (Kiểm tra)

Ngồi quan sát cách người dùng tương tác với Prototype trong thực tế.

**Iteration** (Lặp lại)

Tinh chỉnh và nâng cao liên tục.

NGUỒN Don Norman — jnd.org · IDEO — Design Kit · Stanford d.school
BÀI TOÁN · HCD VÒNG LẬP

DAY 02 · 18 / 76


<!-- END PAGE 18 -->


<!-- START PAGE 19 -->

## [Trang 19]


# Những câu hỏi nguyên bản

— Đôi khi insight bắt đầu từ việc đặt câu hỏi cho những điều hiển nhiên

![img-7.jpeg](img-7.jpeg)

**Isaac Newton**

Quả táo rơi xuống đất — vậy Mặt Trăng có đang 'rơi' tự do không?

![img-8.jpeg](img-8.jpeg)

**Polaroid**

Tại sao không thể xem ảnh ngay lập tức sau khi chụp?

![img-9.jpeg](img-9.jpeg)

**Airbnb**

Liệu không gian sống bỏ trống có thể dùng làm dịch vụ lưu trú?

**Tò mò trước.** Đánh giá sau.

NGUỒN Britannica — Gravity · ACS — Edwin Land & Instant Photography · Airbnb — About us  
BÀI TOÁN - CÂU HỎI NGUYÊN BẢN

DAY 02 - 19 / 76


<!-- END PAGE 19 -->


<!-- START PAGE 20 -->

## [Trang 20]


BÀI TẬP CÁ NHÂN

Bạn có *câu hỏi nào* mà cảm thấy 'ngớ ngẩn' không?

VIẾT LÊN DISCORD — 3 PHÚT


<!-- END PAGE 20 -->


<!-- START PAGE 21 -->

## [Trang 21]


# Câu hỏi gợi mở

BỘ THẺ CÂU HỎI #1 — PHẦN KỲ

— Đặt câu hỏi gợi mở để mở rộng tư duy trước khi lựa chọn bài toán

01

Giả định hiển nhiên nào cần được lặp lại?

02

Có cách tiếp cận nào hoàn toàn mới cho vấn đề?

03

Nếu thiết kế lại từ đầu và không bị giới hạn?

04

Tại sao bài toán này cần AI? Nếu không thì sao?

05

Quy trình nào đang tồn tại chỉ vì thói quen?

06

Có câu hỏi cốt lõi nào đang bị né tránh?

Gửi 1 câu hỏi phản biện lên Discord.

BÀI TOÁN - CÂU HỎI GỢI MỞ

DAY 02 - 21 / 76


<!-- END PAGE 21 -->


<!-- START PAGE 22 -->

## [Trang 22]


# Khởi nguồn từ bài toán, không bắt đầu từ AI

— Ba bài học thực tế về am hiểu lĩnh vực, quy mô thị trường và định vị giải pháp

CURSOR

"Lệch năng lực cốt lõi"

Từ bỏ mạng AI thiết kế cơ khí (CAD) để tập trung vào AI code editor — nơi đội ngũ am hiểu sâu sắc quy trình nghiệp vụ.

ARTIFACT

"Sản phẩm tốt ≠ Thị trường lớn"

Ứng dụng đọc tin tích hợp AI xuất sắc, nhưng quy mô thị trường quá hẹp để thương mại hóa thành công (đóng cửa 1/2024).

NOTEBOOKLM

"Định vị đúng điểm đau"

Tập trung giải quyết nhu cầu hỏi đáp, tóm tắt trên tài liệu cá nhân và đối chiếu nguồn gốc bằng trích dẫn.

Lộ trình: Bài toán → Quy trình vận hành → Chỉ số đo lường → Giải pháp AI

NGUỒN Lenny's Podcast — The rise of Cursor · The Verge — Artifact · Google Blog — NotebookLM

BÀI TOÁN · CASE STUDY

DAY 02 · 22 / 76


<!-- END PAGE 22 -->


<!-- START PAGE 23 -->

## [Trang 23]


# Tìm bài toán AI ở đâu?

— Bắt đầu từ việc quan sát các hoạt động thực tế xung quanh

REPETITIVE

## Tác vụ lặp lại

Việc diễn ra thường xuyên;
công đoạn nào cần chuẩn hóa
để hướng tới tự động hóa?

TIME-CONSUMING

## Tiêu tốn thời gian

Khối lượng xử lý lớn; thời gian
hao phí ở bước nào (tìm kiếm,
đọc hiểu, chờ đợi, định dạng)?

AI ADVANTAGE

## Lợi thế của AI

Tác vụ đòi hỏi phân tích ngữ
cảnh, xử lý ngôn ngữ tự nhiên,
tổng hợp đa nguồn.

USER PAIN POINTS

## Điểm đau người dùng

Ai đang gặp khó khăn, phàn
nàn hoặc bị tắc nghẽn liên tục?

Tập trung nhận diện vấn đề; chưa vội đề xuất giải pháp.

Sàng lọc bài toán sẽ diễn ra vào buổi chiều.

BÀI TOÁN - 4 LENSES

DAY 02 - 23 / 76


<!-- END PAGE 23 -->


<!-- START PAGE 24 -->

## [Trang 24]


# Sai lầm thường gặp — Anti-patterns

— Dấu hiệu cảnh báo bài toán chưa được định hình rõ hoặc giải pháp AI được lựa chọn quá sớm

## Ưu tiên giải pháp (Solution-first)

Xây dựng chatbot/agent trước khi làm rõ quy trình vận hành và điểm nghẽn thực tế.

## Mơ hồ hiện trạng (No baseline)

Không lượng hóa tổn thất hiện tại, dẫn đến mất căn cứ đánh giá hiệu quả cải tiến.

## Bỏ qua đánh giá (No evaluation)

Không thiết lập kịch bản kiểm thử, chỉ số đo lường hoặc phương án đối chứng.

## Mập mờ ranh giới (No boundary)

Không rõ phạm vi tự chủ của AI và thời điểm cần con người phê duyệt (Human-in-the-loop).

Nếu phát hiện mắc các sai lầm trên, hãy **quay lại làm rõ Problem Statement** trước khi chọn công nghệ.

BÀI TOÁN · ANTI-PATTERNS

DAY 02 · 24 / 76


<!-- END PAGE 24 -->


<!-- START PAGE 25 -->

## [Trang 25]


# Discovery interview: 5 câu hỏi nên hỏi stakeholder

BỘ THỂ CÂU HỎI #2 — PHÒNG VẤN

1. Vấn đề nhức nhối (Pain Point) là gì? Tần suất lặp lại trong ngày hoặc trong tuần ra sao?
2. Quy trình (Workflow) hiện tại như thế nào? Công cụ nào được sử dụng ở từng bước, và ai bàn giao công việc cho ai?
3. Thiệt hại (Cost) do vấn đề này gây ra là gì? Hao phí cụ thể về thời gian xử lý, chi phí tài chính, cam kết dịch vụ (SLA) hay tỷ lệ chuyển đổi (conversion)?
4. Hậu quả nếu hệ thống AI sai sót là gì? Khâu nào cần con người tham gia kiểm soát (HITL/phê duyệt), hay AI chỉ hỗ trợ đưa ra gợi ý?
5. Ai là người có quyền phê duyệt dự án (nói YES)? Chỉ số hiệu quả (metric) và mức độ rủi ro (risk) nào sẽ trực tiếp quyết định việc đầu tư?

Lưu ý: Nếu đối tác (stakeholder) không mô tả được quy trình hiện tại và chi phí thiệt hại khi xảy ra lỗi, mọi đề xuất giải pháp AI đều chỉ là phỏng đoán thiếu căn cứ.

PROBLEM DISCOVERY - STAKEHOLDER INTERVIEW

DAY 02 - 25 / 76


<!-- END PAGE 25 -->


<!-- START PAGE 26 -->

## [Trang 26]


PAIR · CHƯƠNG 1 — REFRAME CÂU HỎI

"Can we use AI to _____?"

↓ thay bằng hai câu hỏi: ↓

"How might we
solve _____?"

"Can AI solve this problem
in a unique way?"

Hỏi về bài toán trước, về AI sau — AI chỉ là một phương án trong nhiều phương án khả dĩ.

Câu hỏi đúng quyết định bài toán bạn giải — và giải pháp bạn chọn.

NGUỒN Google PAIR — Ch.1 User Needs + Defining Success
BÀI TOÁN · PAIR REFRAME

DAY 02 · 26 / 76


<!-- END PAGE 26 -->


<!-- START PAGE 27 -->

## [Trang 27]


SECTION 02

# Problem Statement

*Từ pain point đến Problem Statement — bài toán định hình rõ nét qua workflow, bottleneck, metrics và boundary.*


<!-- END PAGE 27 -->


<!-- START PAGE 28 -->

## [Trang 28]


# Quick Problem Card

— Khung định hình bài toán

|  **Bài toán (1 câu)***problem* | Vấn đề cụ thể cần giải quyết (không bao gồm giải pháp).  |
| --- | --- |
|  **Đối tượng ảnh hưởng***actor* | Cá nhân hoặc bộ phận chịu tác động trực tiếp từ vấn đề.  |
|  **Quy trình hiện tại***workflow* | Các bước vận hành thủ công hoặc tự động hiện tại (gồm 3–7 bước).  |
|  **Nút thắt & Tác động***bottleneck + impact* | Khâu gây chậm trễ, sai sót hoặc lặp lại; hệ quả hay tổn thất cụ thể.  |
|  **Chỉ số đo thành công***success metric* | Chỉ số định lượng cụ thể dùng để chứng minh hiệu quả cải tiến.  |
|  **Định hướng giải pháp***direction* | No AI / Rule / Workflow / Agent / Chưa xác định.  |

PROBLEM STATEMENT - QUICK CARD

DAY 02 - 28 / 76


<!-- END PAGE 28 -->


<!-- START PAGE 29 -->

## [Trang 29]


# Quick Problem Card — ví dụ đã điền

— Case: *Weekly Report*

|  **Bài toán** | Mỗi thứ Hai, PM mất khoảng 90 phút tổng hợp Weekly Report từ Jira, Google Sheets và Slack; bước viết narrative tốn thời gian nhất và dễ làm trễ deadline.  |
| --- | --- |
|  **Đối tượng** | Junior PM chịu trách nhiệm gửi weekly report cho Engineering Manager và CEO trước buổi leadership sync.  |
|  **Quy trình** | Export Jira → lấy metrics từ Google Sheets → đọc Slack recap → tổng hợp vào Google Docs → viết narrative → review/format → gửi email.  |
|  **Nút thắt** | Bước viết narrative từ raw data mất khoảng 25 phút. Tổng flow mất khoảng 90 phút/tuần/PM; team 3 PM tương đương khoảng 270 phút/tuần.  |
|  **Chỉ số** | Giảm thời gian làm report từ 90 phút xuống dưới 30 phút, nhưng không làm tăng số câu CEO/EM phải hỏi lại.  |
|  **Định hướng** | **Workflow** — tự động kéo và cấu trúc dữ liệu, AI hỗ trợ draft narrative, PM vẫn review/edit trước khi gửi.  |

PROBLEM STATEMENT - WORKED EXAMPLE

DAY 02 - 29 / 76


<!-- END PAGE 29 -->


<!-- START PAGE 30 -->

## [Trang 30]


# Câu hỏi khai thác bài toán

— Bộ câu hỏi định hình vấn đề dành cho các bên liên quan hoặc chính mình

BỘ THẺ CÂU HỎI #3 — CẤU TRÚC PS

01

Quy trình hiện tại như thế nào?

Công cụ, các bước, cơ chế bàn giao thông tin?

02

Nút thắt nằm ở đâu?

Bước nào chậm, dễ sai sót, lặp lại?

03

Hao phí hiện tại là bao nhiêu?

Thời gian, chi phí nhân sự, SLA, cơ hội bỏ lỡ?

04

Tiêu chí thành công đo bằng gì?

Hiệu quả cải tiến định lượng cụ thể?

05

Hậu quả khi xảy ra sai sót?

Phạm vi tự quyết của AI; điểm cần con người phê duyệt?

06

Có giải pháp phi AI đơn giản hơn?

Quy tắc, checklist, quy trình hay tài liệu hướng dẫn?

PROBLEM STATEMENT - 6 CÂU HỎI

DAY 02 - 30 / 76


<!-- END PAGE 30 -->


<!-- START PAGE 31 -->

## [Trang 31]


# Định lượng hóa bài toán

— Điểm đau chưa được định lượng thì không thể xác định giá trị thực tế của AI

01 · BASELINE

**Hiện trạng** / where we are

Mức hao phí hiện tại là bao nhiêu? Bằng con số cụ thể.

02 · TARGET

**Mục tiêu** / where to go

Kỳ vọng cải thiện ở mức độ nào? Ngưỡng cụ thể là gì?

03 · MEASUREMENT

**Đo lường** / how we know

Chỉ số nào chứng minh tính hiệu quả? Cách thu thập?

VÍ DỤ

THỜI GIAN HOÀN THÀNH

Rút ngắn từ 90 phút xuống dưới 30 phút.

CHẤT LƯỢNG CÔNG VIỆC

Giảm tỷ lệ lỗi phân loại từ 20% xuống dưới 5%.

TẢI TRỌNG VẬN HÀNH

Cắt giảm 40% câu hỏi trùng lặp cần Trợ giảng xử lý.

PROBLEM STATEMENT · ĐỊNH LƯỢNG

DAY 02 · 31 / 76


<!-- END PAGE 31 -->


<!-- START PAGE 32 -->

## [Trang 32]


# Thiết lập chỉ số: Output & Input

— Chỉ số đo lường cần phản ánh kết quả cuối và các đòn bẩy có thể tác động

OUTPUT METRIC

## Kết quả cuối cùng / what we optimize

- Thời lượng hoàn tất quy trình giảm bao nhiêu?
- Tỷ lệ sai sót / chất lượng đầu ra thay đổi thế nào?
- Giá trị thực tế người dùng nhận được rõ nét hơn?

tăng cái này
→ đo cái kia

INPUT METRICS

## Các đòn bẩy / what we can move

- Tỷ lệ câu hỏi được phân loại chính xác.
- Tỷ lệ yêu cầu được chuyển tiếp hỗ trợ kịp thời.
- Thời gian Trợ giảng hiệu chỉnh bản nháp phản hồi.

"Nâng cao hiệu suất" không phải chỉ số — cần gắn với hiện trạng, mục tiêu và phương pháp đo.

NGUỒN Amplitude — North Star Playbook · Lenny Rachitsky — Choosing Your North Star Metric
PROBLEM STATEMENT · METRICS

DAY 02 · 32 / 76


<!-- END PAGE 32 -->


<!-- START PAGE 33 -->

## [Trang 33]


BÀI TẬP NHANH

Lựa chọn một điểm đau đã nhận diện
và thiết lập phương án đo lường cụ thể.

# Chuyển điểm đau thành
*chỉ số định lượng*

5 PHÚT · BASELINE → TARGET → MEASUREMENT


<!-- END PAGE 33 -->


<!-- START PAGE 34 -->

## [Trang 34]


SECTION 03

# Có nên ứng dụng AI?

*AI chỉ thực sự mang lại giá trị khi tích hợp chính xác vào quy trình nghiệp vụ và giải quyết đúng điểm đau — theo Google PAIR Guidebook, Ch.1.*


<!-- END PAGE 34 -->


<!-- START PAGE 35 -->

## [Trang 35]


# Ba bước quyết định AI theo PAIR

— Google People + AI Guidebook - Chương 1: User Needs + Defining Success

BƯỚC ①

## Giao điểm: nhu cầu × thế mạnh AI

Bài toán của bạn có nằm trong nhóm việc AI làm **tốt hơn hẳn** rule/heuristic không?

VD: câu hỏi trùng lặp của 1000 học viên K3 & K4 có nằm trong thế mạnh của AI?

→ trả lời câu hỏi 1: có thực sự cần AI?

BƯỚC ②

## Automate hay Augment?

AI **thay thế** hay **hỗ trợ** con người? Mức tự động hóa tăng dần theo độ tin cậy và rủi ro.

VD: AI trả lời thay TA luôn, hay chỉ soạn nháp để TA duyệt?

→ trả lời câu hỏi 2: giải pháp ở cấp độ nào?

BƯỚC ③

## Reward function & tiêu chí thành công

Định nghĩa "đúng/sai" của hệ thống (precision ↔ recall) và ngưỡng thành công đo được.

VD: đo bằng gì — thời gian phản hồi? tỷ lệ định hướng sai?

→ trả lời câu hỏi 3: PS đã đủ rõ để đo?

Ảnh xạ về 4 câu hỏi trọng tâm của ngày: ① Có cần AI? · ② Cấp độ nào? · ③ Đủ rõ để đo? · Tổng hợp ①②③ → ④ Go / Not Yet / No-Go

Đi hết 3 bước này, bạn trả lời được cả 4 câu hỏi của ngày hôm nay — từ "có thực sự cần AI?" đến "Go, Not Yet hay No-Go".

NGUỒN Google PAIR — People + AI Guidebook - PAIR - Ch.1 User Needs + Defining Success
CÓ NỀN ỨNG DỤNG AI - PAIR 3 BƯỚC

DAY 02 - 35 / 76


<!-- END PAGE 35 -->


<!-- START PAGE 36 -->

## [Trang 36]


# Khi nào AI có lợi thế?

PAIR

— Tám trường hợp PAIR gọi là "AI probably better" - Chương 1

## Gợi ý theo từng người - recommendation

Mỗi người dùng nhận một nội dung gợi ý khác nhau.

## Cá nhân hóa - personalization

Trải nghiệm tự điều chỉnh theo từng người, ngày càng hợp hơn.

## Nhận diện cả một lớp thực thể

Nhận ra mọi đối tượng cùng loại — VD mọi khuôn mặt.

## Agent/bot cho một lĩnh vực cụ thể

Trợ lý ảo xử lý trọn một phạm vi việc chuyên biệt.

## Dự đoán tương lai - prediction

Đoán trước sự kiện sắp xảy ra để chuẩn bị phản ứng.

## Hiểu ngôn ngữ tự nhiên - natural language

Hiểu câu hỏi viết tự do bằng lời nói hằng ngày.

## Phát hiện cái hiểm & biến đổi

Bắt sự kiện hiểm, thay đổi theo thời gian — VD gian lận.

## Nội dung động thay giao diện tĩnh

Nội dung linh hoạt hiệu quả hơn layout cố định, dễ đoán.

AI chỉ đáng làm khi bài toán nằm trong nhóm này.

NGUỒN PAIR — Ch.1 User Needs + Defining Success
CÓ NÊN ỨNG DỤNG AI - AI PROBABLY BETTER

DAY 02 - 36 / 76


<!-- END PAGE 36 -->


<!-- START PAGE 37 -->

## [Trang 37]


# Khi nào AI **KHÔNG tốt hơn?**

PAIR

— Sáu trường hợp PAIR gọi là "AI probably NOT better" - Chương 1

## Cần duy trì tính dự đoán được

Nút Home / Cancel phải luôn nằm ở một chỗ quen thuộc — người dùng không phải đoán mỗi lần.

## Thông tin tĩnh, ít thay đổi

Nội dung cố định thì cứ hiển thị trực tiếp — không cần AI sinh lại mỗi lần.

## Lỗi quá tốn kém

Chi phí của một lần sai lớn hơn lợi ích của nhiều lần đúng.

## Yêu cầu minh bạch tuyệt đối

Mọi quyết định phải giải thích được từng bước, truy vết được.

## Tối ưu tốc độ & chi phí thấp

Cần ra thị trường nhanh (time-to-market), vận hành rẻ — AI chỉ thêm độ trễ và chi phí.

## Việc giá trị cao người dùng muốn tự làm

Tác vụ mang ý nghĩa cá nhân mà người dùng **KHÔNG** muốn bị tự động hóa.

**Rule/heuristic dễ build, dễ giải thích, dễ debug và bảo trì hơn — nếu nó giải quyết được, đó là lựa chọn tối ưu.**

NGUỒN PAIR — Ch.1 User Needs + Defining Success
CÓ NÊN ỨNG DỤNG AI - KHI NÀO KHÔNG CẦN AI

DAY 02 - 37 / 76


<!-- END PAGE 37 -->


<!-- START PAGE 38 -->

## [Trang 38]


# Khi nào AI đáng để làm?

— Dấu hiệu nhận biết bài toán phù hợp và động lực đầu tư của doanh nghiệp

AI HỢP KHI NÀO

- Tác vụ mang tính lặp lại nhưng có độ biến thiên vừa phải.
- Yêu cầu tổng hợp hoặc tìm kiếm tri thức từ nhiều nguồn.
- Quy trình gồm nhiều bước phức tạp và cần tương tác với nhiều công cụ.

Nếu quy trình hoàn toàn có tính xác định (deterministic), các quy tắc luật tính (rule) sẽ tối ưu hơn.

VÌ SAO DOANH NGHIỆP ĐẦU TƯ

01 · Sống còn — Bắt buộc phải tích hợp AI để duy trì lợi thế cạnh tranh trước đối thủ.
02 · Hiệu quả — Giảm thiểu chi phí vận hành, tăng tốc độ xử lý và nâng cao năng suất nghiệp vụ.
03 · Khám phá — Tích lũy năng lực công nghệ, tránh tụt hậu và tìm kiếm các mô hình cơ hội mới.

Mục tiêu áp dụng AI sẽ trực tiếp quyết định phương thức xây dựng giải pháp, mức độ tự động hóa và quy mô đầu tư.

CÔ NÊN ỨNG DỤNG AI - KHI NÀO HỢP

DAY 02 - 38 / 76


<!-- END PAGE 38 -->


<!-- START PAGE 39 -->

## [Trang 39]


# Tự xây dựng hay mua giải pháp?

— Hai góc nhìn bổ sung nhau giúp định hình chiến lược triển khai

GÓC NHÌN 1 — CHIP HUYEN, AI ENGINEERING (2025)

## In-house (Build)

Khi công nghệ AI là lợi thế cạnh tranh cốt lõi và yếu tố sống còn.

## Mua / SaaS (Buy)

Khi giải pháp AI đóng vai trò như một công cụ tối ưu hóa năng suất (productivity layer).

GÓC NHÌN 2 — MIT CISR

### Buy

Giải pháp may sẵn (off-the-shelf), do vendor duy trì. Triển khai nhanh, ít khác biệt cạnh tranh. Phụ thuộc roadmap vendor.

### Boost

Mua mô hình sẵn có, cải tiến bằng dữ liệu nội bộ (fine-tune hoặc RAG). Đòi hỏi quản trị dữ liệu (data governance) tốt.

### Build

Tự xây mô hình tùy biến (custom model). Kiểm soát cao nhất, chi phí đắt nhất. Đòi hỏi đội kỹ sư AI mạnh.

Thực tế: đa số đội ngũ đang ở giữa — Boost (RAG / fine-tune), thay vì tự xây lại mọi thứ từ đầu (build from scratch).

NGUỒN Chip Huyen — AI Engineering (O'Reilly, 2025) - MIT Sloan — Buy, Boost, or Build?

CÓ NỀN ỨNG DỤNG AI - BUILD / BOOST / BUY

DAY 02 - 39 / 76


<!-- END PAGE 39 -->


<!-- START PAGE 40 -->

## [Trang 40]


# Vòng đời Sản phẩm AI

— Mỗi giai đoạn từ ý tưởng đến vận hành thực tế yêu cầu phương thức xác thực chuyên biệt

![img-10.jpeg](img-10.jpeg)

Day 02 nằm ở 2 milestone đầu — Planning & Expectations: xác định bài toán và thiết lập kỳ vọng trước khi chọn model.

NGUỒN Chip Huyen — AI Engineering (O'Reilly, 2025)

QUYẾT ĐỊNH AI - LIFECYCLE

DAY 02 - 40 / 76


<!-- END PAGE 40 -->


<!-- START PAGE 41 -->

## [Trang 41]


SECTION 04

# Rule / Workflow / Agent

*Phân tích cấp độ giải pháp. Cấp độ tối ưu là cấp độ đơn giản nhất đủ để giải quyết bài toán.*


<!-- END PAGE 41 -->


<!-- START PAGE 42 -->

## [Trang 42]


# Hệ thống AI = Model + Context + Planning + Tools

— Một giải pháp AI thực tế là một hệ thống nhiều thành phần, không chỉ dừng lại ở mô hình ngôn ngữ

![img-11.jpeg](img-11.jpeg)

MODEL

Tư duy & Sáng tạo

Xử lý đọc hiểu, soạn thảo, tổng hợp, phân loại và đưa ra gợi ý.

CONTEXT

Tri thức chuyên biệt

Cơ sở dữ liệu, tài liệu nghiệp vụ, hồ sơ lịch sử giúp AI phản hồi chính xác theo bối cảnh.

PLANNING

Điều phối quy trình

Tự động phân rã tác vụ phức tạp và linh hoạt điều chỉnh.

TOOLS

Liên kết hệ thống

Tích hợp CRM, database, lịch làm việc hoặc API bên thứ ba.

Giải pháp AI là một HỆ THỐNG — model chỉ là một thành phần.

NGUỒN Anthropic — Building effective agents · Chip Huyen — AI Engineering
HỆ THỐNG AI · KIẾN TRÚC

DAY 02 · 42 / 76


<!-- END PAGE 42 -->


<!-- START PAGE 43 -->

## [Trang 43]


# Automation vs Augmentation

— Bước ② của PAIR: với từng tác vụ, AI nên làm thay hay hỗ trợ con người?

AUTOMATE

## AI làm thay

Chọn khi:

- Việc khó, nhàm chán, nguy hiểm hoặc cần scale
- Người dùng thiếu kiến thức / khả năng tự làm
- Có "đáp án đúng" mà mọi người cùng đồng thuận

Đo thành công bằng: hiệu quả tăng · an toàn hơn · giảm việc tẻ nhạt.

quyết định theo từng tác vụ

AUGMENT

## AI hỗ trợ con người

Chọn khi:

- Người dùng thích tự làm việc đó
- Stakes cao: tiền bạc, pháp lý, sức khỏe
- Kết quả cần trách nhiệm cá nhân / social capital
- Sở thích khó diễn đạt thành lời

Đo bằng: mức độ thích thú · cảm giác kiểm soát · sáng tạo tăng.

Việc đã automate vẫn gần như luôn cần human oversight — preview, edit, undo.

NGUỒN Google PAIR — Ch.1 User Needs + Defining Success
RWA · AUTOMATE VS AUGMENT

DAY 02 · 43 / 76


<!-- END PAGE 43 -->


<!-- START PAGE 44 -->

## [Trang 44]


# Tăng mức tự động hóa theo pha

— Mức tự động hóa tỷ lệ nghịch với rủi ro — áp dụng vào case 1000 học viên K3 & K4

PHA 1

AI chỉ gợi ý

AI đọc câu hỏi của học viên và gợi ý câu trả lời — Trợ giảng viết lại toàn bộ.

risk ↓ khi dữ liệu đánh giá ↑

PHA 2

AI soạn nháp, TA duyệt

Rủi ro thấp hơn sau khi đo được chất lượng gợi ý ở Pha 1 — TA hiệu chỉnh bản nháp trước khi gửi.

risk ↓ khi dữ liệu đánh giá ↑

PHA 3

AI tự động có giám sát

Chỉ áp dụng cho nhóm câu hỏi đã chứng minh an toàn qua dữ liệu — TA giám sát, can thiệp khi cần.

risk ↓ khi dữ liệu đánh giá ↑

Pattern #14 — "Automate more when risk is low"

Pattern #17 — "Automate in phases"

Không bật full-auto từ đầu — mức tự động hóa đi lên cùng độ tin cậy.

NGUỒN Google PAIR — 23 Design Patterns
RWA · AUTOMATE IN PHASES

DAY 02 · 44 / 76


<!-- END PAGE 44 -->


<!-- START PAGE 45 -->

## [Trang 45]


# Ba mức giải pháp: Rule / Workflow / Agent

— Rule/Workflow/Agent là cấp độ KỸ THUẬT — còn Automate/Augment (PAIR) là cấp độ VAI TRÒ của con người trong hệ thống

CẤP ĐỘ 1

Rule / Script

- Đầu vào ổn định, ít thay đổi
- Logic viết được thành if/else
- Cần kết quả luôn đúng 100%
- Quy định pháp lý / tuân thủ chặt

Ví dụ: Tính thuế · chặn email spam theo từ khóa · auto-reply theo template.

CẤP ĐỘ 2

LLM Feature / Workflow

- Đầu vào đa dạng, không viết hết rule được
- Đầu ra cần linh hoạt (tóm tắt, dịch, phân loại)
- Có cách đo chất lượng
- Người có thể kiểm tra trước khi gửi

Ví dụ: Tóm tắt email · chatbot FAQ · phân loại ticket hỗ trợ.

CẤP ĐỘ 3

Agent

- Nhiều bước, dùng nhiều công cụ
- Tình huống thay đổi liên tục
- Cần tự ra quyết định giữa các bước
- Có kiểm soát rủi ro rõ ràng

Ví dụ: Agent nghiên cứu thị trường · coding agent sửa nhiều file.

Thứ tự ưu tiên thực dụng: bắt đầu từ bên trái, chỉ đi sang bên phải khi giá trị tăng hơn độ phức tạp.

RWA - TỔNG QUAN

DAY 02 - 45 / 76


<!-- END PAGE 45 -->


<!-- START PAGE 46 -->

## [Trang 46]


# Tình huống: Tối ưu nguồn lực Trợ giảng

![img-12.jpeg](img-12.jpeg)

— Quy trình nghiệp vụ hiện tại cần được mô hình hóa trước khi cân nhắc giải pháp AI

BỐI CẢNH & BÀI TOÁN — CASE XUYÊN SUỐT BUỔI HỌC

Lớp học **1000 học viên (khóa K3 & K4)** nhưng nguồn lực Trợ giảng (TA) có hạn. TA quá tải vì rà soát thủ công các câu hỏi trùng lặp và các yêu cầu hỗ trợ thiếu thông tin. **Mục tiêu:** tối ưu quy trình để giảm tải cho TA, giúp học viên không bị kẹt lâu.

![img-13.jpeg](img-13.jpeg)

BOTTLENECK

Nhiều câu hỏi trùng lặp hoặc thiếu thông tin chi tiết; Trợ giảng mất thời gian rà soát thủ công.

METRICS

Thời gian học viên chờ phản hồi, tỷ lệ câu hỏi trùng lặp, số học viên bị kẹt kéo dài.

RISKS

AI hướng dẫn sai hoặc nhầm kiến thức khiến học viên đi sai hướng thực hành.

Cùng một tình huống này, ta sẽ đi qua cả 3 cấp độ giải pháp: Rule → Workflow → Agent.

RWA - TÌNH HUỐNG

DAY 02 - 46 / 76


<!-- END PAGE 46 -->


<!-- START PAGE 47 -->

## [Trang 47]


# Cấp độ 1 — Rule-based

— Áp dụng khi logic nghiệp vụ tường minh, kết quả cố định và yêu cầu kiểm soát rủi ro nghiêm ngặt

ĐIỀU KIỆN ÁP DỤNG

Khi nào chọn Rule / when to use

- Logic phân nhánh rành mạch (If/Else)
- Yêu cầu hoặc trạng thái lặp lại hoàn toàn
- Không đòi hỏi khả năng tự suy luận của AI
- Yêu cầu kết quả dự đoán và kiểm soát tuyệt đối

ỨNG DỤNG TRONG LAB

Ví dụ thực tế / in our context

- Hỏi lịch nộp bài → Tự động gửi link thời khóa biểu
- Nộp thiếu file bài tập → Tự động nhắc checklist
- Hỏi lỗi cài đặt quen thuộc → Gửi link hướng dẫn
- Câu hỏi ngoài danh mục → Chuyển cho Trợ giảng

Giải pháp dựa trên Luật (Rule) không thua kém AI — nếu giải quyết triệt để bài toán, đó luôn là lựa chọn tối ưu.

RWA - MỨC 1: RULE

DAY 02 - 47 / 76


<!-- END PAGE 47 -->


<!-- START PAGE 48 -->

## [Trang 48]


## Cấp độ 2 — Workflow

— Các bước xử lý đã định hình rõ, nhưng từng công đoạn cần AI hỗ trợ ngôn ngữ hoặc đánh giá

![img-14.jpeg](img-14.jpeg)

NGUỒN Anthropic — Building effective agents
RWA - MỨC 2: WORKFLOW

DAY 02 - 48 / 76


<!-- END PAGE 48 -->


<!-- START PAGE 49 -->

## [Trang 49]


# Cấp độ 3 — Agent

— Hệ thống tự động lập kế hoạch, phối hợp công cụ và linh hoạt thích ứng theo tình huống

ĐIỀU KIỆN CÂN NHẮC

Khi nào dùng Agent / when to consider

- Không thể xác định trước toàn bộ các bước thực thi
- Môi trường nhiều biến số, đòi hỏi thay đổi kế hoạch linh hoạt
- Cần tương tác nhiều công cụ, truy xuất nhiều nguồn dữ liệu
- Có vòng phản hồi và chốt chặn giám sát từ con người

ỨNG DỤNG TRONG LAB

Ví dụ thực tế / in our context

- Theo dõi thảo luận và nộp bài trên các kênh học tập
- Phát hiện học viên hoặc nhóm bị kẹt quá lâu
- Tự động tổng hợp vấn đề, gợi ý cách hỗ trợ
- Trợ giảng chỉ cần duyệt và nhấn gửi phương án

Tác động của Agent mạnh mẽ hơn, nhưng đi kèm chi phí vận hành cao hơn, độ trễ lớn hơn, khó kiếm thử và các dạng lỗi phức tạp hơn.

RWA - MỨC 3: AGENT

DAY 02 - 49 / 76


<!-- END PAGE 49 -->


<!-- START PAGE 50 -->

## [Trang 50]


# Một tình huống, ba cấp độ giải pháp

— Ưu tiên giải pháp đơn giản nhất có thể giải quyết bài toán và mang lại cải tiến đo lường được

CẤP ĐỘ 1 — RULE (LUẬT TÍNH)

Trả lời tự động

- Tự động trả lời FAQ, gửi link thời khóa biểu
- Gửi tài liệu sửa lỗi cài đặt cơ bản
- Nhắc nhở checklist nộp bài

Khi nào? Logic tường minh, kết quả cố định.

CẤP ĐỘ 2 — WORKFLOW (QUY TRÌNH)

Duyệt Problem Card

- AI kiểm tra độ đầy đủ của Problem Card
- Yêu cầu bổ sung nếu thiếu thông tin
- Chuyển cho Trợ giảng giải quyết

Khi nào? Có quy trình rõ, AI hỗ trợ từng bước.

CẤP ĐỘ 3 — AGENT (TÁC NHÂN)

Đề xuất can thiệp chủ động

- Tự động theo dõi tiến độ nộp bài
- Phát hiện nhóm học viên bị kẹt lâu
- Chuẩn bị câu trả lời, đề xuất TA duyệt

Khi nào? Tình huống động, đa công cụ.

Không bắt buộc nâng cấp tuần tự từ Rule lên Agent → dừng ở cấp tối giản nhất nếu đã đáp ứng mục tiêu đề ra.

RWA - SO SÁNH

DAY 02 - 50 / 76


<!-- END PAGE 50 -->


<!-- START PAGE 51 -->

## [Trang 51]


# Đọc workflow patterns như người làm product

— Mỗi pattern là một tradeoff — không phải "càng nâng cao càng tốt"

WORKFLOW

Lộ trình do CODE ĐIỀU PHỐI — định trước bằng code path

CÂU HỎI QUYẾT ĐỊNH

"Lộ trình xử lý có viết trước được không?"

AGENT

MODEL TỰ ĐIỀU PHỐI lộ trình & cách dùng tools

MỖI PATTERN = MỘT TRADEOFF

|  Pattern | Được gì | Mất gì  |
| --- | --- | --- |
|  Prompt chaining | Chính xác hơn — có gate kiểm tra giữa các bước | Chậm hơn — độ trễ cộng dồn qua từng bước  |
|  Routing | Tối ưu chi phí — mỗi loại input một nhánh chuyên biệt | Cần phân loại đúng ngay từ đầu  |
|  Parallelization | Tin cậy hơn — vote, guardrail chạy song song | Chi phí nhân lên theo số nhánh  |
|  Orchestrator-workers | Xử lý được bài toán không biết trước subtasks | Khó kiểm thử, hành vi khó dự đoán  |
|  Evaluator-optimizer | Chất lượng tăng qua vòng lặp đánh giá | Cần tiêu chí chậm rõ ràng  |
|  Agent | Giải được bài toán mờ | Chi phí cao, lỗi cộng dồn  |

PM không cần code pattern — nhưng phải đọc được sơ đồ và nói được tradeoff, vì nó quyết định chi phí, độ trễ, khả năng kiểm thử và dạng lỗi của hệ thống — đầu vào của ô Boundary, Metric, HITL trong Problem Statement.

NGUỒN Anthropic — Building effective agents

WORKFLOW - PM MENTAL MODEL

DAY 02 - 51 / 76


<!-- END PAGE 51 -->


<!-- START PAGE 52 -->

## [Trang 52]


# Workflow patterns — đủ cho hầu hết bài toán

— Ba mô hình cơ bản theo Anthropic · Building Effective Agents (2024)

## 1. Prompt Chaining

![img-15.jpeg](img-15.jpeg)

Chia task thành chuỗi bước tuần tự, có **gate** kiểm tra giữa các bước. VD: *Viết outline* → *check* → *viết bài*.

Ý nghĩa quyết định: đối độ trễ lấy độ chính xác.

## 2. Routing

![img-16.jpeg](img-16.jpeg)

Phân loại input → đưa vào nhánh chuyên biệt, tối ưu từng loại riêng. VD: *CS query* → *FAQ / refund / kỹ thuật*.

Ý nghĩa quyết định: câu dễ đi model rẻ, câu khó đi model mạnh.

## 3. Parallelization

![img-17.jpeg](img-17.jpeg)

Chạy song song rồi tổng hợp (**sectioning**), hoặc chạy nhiều lần lấy **vote**. VD: *Guardrail + response đồng thời*.

Ý nghĩa quyết định: vote để giảm rủi ro một đầu ra sai.

### NGUYÊN TẮC ANTHROPIC

→ Luôn ưu tiên **giải pháp đơn giản nhất**; chỉ tăng độ phức tạp khi thực sự cần thiết.

3 mô hình cơ bản bên cạnh đã đủ đáp ứng **hầu hết bài toán thực tế**.

NGUỒN Anthropic — Building effective agents
WORKFLOW PATTERNS · BASIC

DAY 02 · 52 / 76


<!-- END PAGE 52 -->


<!-- START PAGE 53 -->

## [Trang 53]


# Khi nào cần **phức tạp hơn**?

— *Orchestrator-Workers, Evaluator-Optimizer và Agent*

## 4. Orchestrator-Workers

![img-18.jpeg](img-18.jpeg)

1 LLM phân việc động cho workers — **subtasks không biết trước**. *VD: Coding agent sửa nhiều file.*

Ý nghĩa quyết định: dùng khi không liệt kê trước được các bước.

## 5. Evaluator-Optimizer

![img-19.jpeg](img-19.jpeg)

1 LLM tạo, 1 LLM đánh giá → **lập cho đến khi đạt**. *VD: Dịch văn học → review → sửa.*

Ý nghĩa quyết định: cần tiêu chí chấm rõ — chính là reward function ở bước ③.

## 6. Agent

![img-20.jpeg](img-20.jpeg)

LLM tự lập kế hoạch + gọi tools + iterate — **autonomous loop**. Action → Environment → Feedback. *VD: SWE-bench, computer use.*

Ý nghĩa quyết định: cần guardrails + stopping conditions.

## ANTHROPIC — BUILDING EFFECTIVE AGENTS

*'Agents' autonomy makes them ideal for scaling tasks in trusted environments.'*

→ **Chi phí vận hành cao, dễ tích tụ sai số (lỗi cộng dồn).**

NGUỒN Anthropic — Building effective agents  
WORKFLOW PATTERNS - ADVANCED

DAY 02 - 53 / 76


<!-- END PAGE 53 -->


<!-- START PAGE 54 -->

## [Trang 54]


# Thang câu hỏi lựa chọn cấp độ giải pháp

— Khung câu hỏi tuần tự giúp tránh bẫy “nhảy vọt” lên Agent phức tạp

01

TẦN SUẤT & TÁC ĐỘNG

**Tần suất & tác động có đủ lớn?**

Nếu thấp → Xử lý thủ công hoặc hiệu chỉnh quy trình nghiệp vụ trước.

02

LOGIC

**Logic xử lý có rành mạch?**

Nếu tường minh → Ưu tiên giải pháp Rule, kịch bản tự động, danh mục kiểm tra.

03

QUY TRÌNH

**Quy trình thực hiện có cố định?**

Nếu có → Xây dựng Workflow tích hợp AI hỗ trợ từng công đoạn.

04

TỰ THÍCH ỨNG

**Quy trình đòi hỏi khả năng tự thích ứng linh hoạt?**

Chỉ khi có nhiều biến số phức tạp → Mới cân nhắc Agent.

05

GIÁ TRỊ VS RỦI RO

**Giá trị mang lại có vượt trội chi phí & rủi ro?**

Nếu không → Đặt chốt chặn phê duyệt (Human-in-the-loop) hoặc chọn Not Yet / No-Go.

NGUỒN Anthropic — Building effective agents

WORKFLOW - THANG QUYẾT ĐỊNH

DAY 02 - 54 / 76


<!-- END PAGE 54 -->


<!-- START PAGE 55 -->

## [Trang 55]


# Cây quyết định: Lựa chọn cấp độ giải pháp

— Từ bài toán cốt lõi đến lựa chọn Rule, Workflow hay Agent

![img-21.jpeg](img-21.jpeg)

Đi từ trên xuống — mỗi nhánh "KHÔNG" là một lần tránh được độ phức tạp không cần thiết.

NGUỒN Anthropic — Building effective agents · Google — Rules of ML
WORKFLOW · DECISION TREE

DAY 02 - 55 / 76


<!-- END PAGE 55 -->


<!-- START PAGE 56 -->

## [Trang 56]


# Ví dụ thực tế ngoài lớp học

— Phân biệt cấp độ giải pháp Rule, Workflow và Agent trong các tình huống thực hành

CHĂM SÓC KHÁCH HÀNG

RULE

Định tuyến phiếu hỗ trợ theo từ khóa.

WORKFLOW

Tự động soạn nhập câu trả lời có trích dẫn nguồn.

AGENT

Xử lý quy trình đa bước, truy vấn CRM, tạo yêu cầu hoàn tiền.

NGHIÊN CỨU BÁN HÀNG

RULE

Lọc khách hàng tiềm năng theo lĩnh vực, quy mô.

WORKFLOW

Thu thập thông tin → tóm tắt → soạn email tiếp cận.

AGENT

Giám sát tín hiệu thị trường, cập nhật CRM, đề xuất bước tiếp theo.

KHO TRI THỨC NỘI BỘ

RULE

Phân phối chính sách theo nhu cầu tra cứu.

WORKFLOW

Hỏi đáp dựa trên tài liệu nội bộ kèm trích dẫn nguồn.

AGENT

Giám sát thay đổi pháp lý, nhắc nhở cập nhật tài liệu.

WORKFLOW - VÍ DỤ THỰC TẾ

DAY 02 - 56 / 76


<!-- END PAGE 56 -->


<!-- START PAGE 57 -->

## [Trang 57]


# Reward function: hệ thống hiểu "đúng / sai" thế nào?

① Nhu cầu

② Auto / Augment

③ Reward function

— PAIR Bước ③ · Case: AI gợi ý câu trả lời cho câu hỏi của 1000 học viên (khóa K3 & K4)

Reward function là công thức quyết định đầu là dự đoán "đúng", đầu là "sai" — và chính nó định hình trải nghiệm người dùng cuối. Vì vậy nó phải được thiết kế liên chức năng: tối thiểu UX × Product × Engineering cùng ngồi lại.

BỐN KẾT QUẢ CÓ THỂ XẢY RA — CASE AI GỢI Ý CÂU TRẢ LỜI

TP — TRUE POSITIVE · ĐÚNG-TÍCH CỰC

Câu hỏi nghẽn thật → AI gợi ý đúng câu trả lời. Học viên được giải tỏa, TA đỡ tải.

TN — TRUE NEGATIVE · ĐÚNG-TIÊU CỰC

Câu hỏi đã có tài liệu sẵn → AI không can thiệp. Đúng — không cần gợi ý gì thêm.

FP — FALSE POSITIVE · BÁO ĐỘNG GIẢ

AI gợi ý câu trả lời SAI (hallucination) và gửi thẳng cho học viên → học viên đi sai hướng thực hành.

FN — FALSE NEGATIVE · BỎ SÓT

Học viên đang kẹt thật nhưng AI bỏ sót, không gợi ý → học viên vẫn chờ lâu như cũ.

Chi phí của FP và FN KHÔNG đối xứng — báo cháy giả ≠ bỏ sót đám cháy. Cần nhắc đánh đổi này là quyết định then chốt khi thiết kế reward function.

NGUỒN PAIR — Ch.1 User Needs + Defining Success
REWARD · HÀM THƯỜNG

DAY 02 · 57 / 76


<!-- END PAGE 57 -->


<!-- START PAGE 58 -->

## [Trang 58]


# Precision ↔ Recall: đánh đổi không tránh khỏi

— Cùng một hệ thống AI, hai hướng vận nút ngược nhau

① Nhu cầu

② Auto / Augment

③ Reward function

PRECISION CAO

TP / (TP + FP)

Ít gợi ý — nhưng gợi ý nào cũng chắc đúng. Người dùng tin vào từng gợi ý nhận được.

HỆ QUẢ

Nhiều False Negative — bỏ sót học viên đang thực sự cần giúp.

ĐÒN BẮY

Vận nút bên này lên, chất lượng bên kia xấu đi.

RECALL CAO

TP / (TP + FN)

Bao trọn mọi trường hợp cần giúp — không học viên nào bị bỏ lại phía sau.

HỆ QUẢ

Nhiều False Positive — gợi ý sai nhiều, TA phải lọc lại thủ công.

Không có cấu hình đúng tuyệt đối — phải test điểm cân bằng với chính người dùng.

NGUỒN PAIR — Ch.1 User Needs + Defining Success

REWARD - PRECISION ↔ RECALL

DAY 02 - 58 / 76


<!-- END PAGE 58 -->


<!-- START PAGE 59 -->

## [Trang 59]


# Viết tiêu chí thành công mà hành động được

— PAIR Bước ③ · Metric tốt = chỉ số cụ thể + ngưỡng có nghĩa + hành động cụ thể

① Nhu cầu

② Auto / Augment

③ Reward function

TEMPLATE CỦA PAIR

If {chỉ số cụ thể} for {tính năng AI} {drops below / goes above} {ngưỡng có nghĩa}, we will {hành động cụ thể}.

VÍ DỤ ĐIỂN SẴN — CASE TA 1000 HỌC VIÊN

Nếu tỷ lệ câu trả lời AI gợi ý bị TA sửa > 30% trong 2 tuần, ta sẽ hạ mức tự động về pha 1 (chỉ gợi ý, không gửi thẳng cho học viên).

CHECKLIST TRƯỚC KHI CHỐT METRIC

01

Metric có ý nghĩa với MỌI người dùng không?

02

Có nhóm nào bị ảnh hưởng tiêu cực không?

03

Đây là thành công của ngày 1 — còn ngày 1000 thì sao?

→ Và đừng quên: lên lịch review metric định kỳ — tiêu chí thành công cũng cần được bảo trì theo thời gian.

NGUỒN PAIR — Ch.1 User Needs + Defining Success PAIR Worksheet — User Needs (PDF)
REWARD · SUCCESS CRITERIA

DAY 02 · 59 / 76


<!-- END PAGE 59 -->


<!-- START PAGE 60 -->

## [Trang 60]


# Thiết lập kỳ vọng

— Đo lường các chỉ số để xác định mức độ hiệu quả trước khi chính thức phát hành giải pháp

01 - TÁC ĐỘNG KINH DOANH

Giải pháp tạo giá trị gì cho doanh nghiệp?

- ✓ Tỷ lệ tự động hóa tác vụ / yêu cầu (%)
- ✓ Quy mô xử lý khối lượng công việc tăng thêm
- ✓ Tốc độ phản hồi & thời gian quy trình được tối ưu

02 - SỰ HÀI LÒNG KHÁCH HÀNG

Người dùng thực tế có thấy tốt hơn không?

- ✓ Chỉ số hài lòng CSAT / NPS
- ✓ Đánh giá chất lượng trực tiếp từ người dùng
- ✓ Tỷ lệ hoàn thành tác vụ vs tỷ lệ bỏ ngang giữa chừng

03 - NGƯỜNG HỮU DỤNG

Hệ thống đạt tiêu chí nào thì có thể phát hành?

- ✓ Chất lượng: độ chính xác và tính hữu ích của đầu ra
- ✓ Độ trễ: tốc độ phản hồi của hệ thống (latency)
- ✓ Chi phí: chi phí tài chính trên mỗi lượt yêu cầu

CÔ NÊN ỨNG DỤNG AI - THIẾT LẬP KỲ VỌNG

DAY 02 - 60 / 76


<!-- END PAGE 60 -->


<!-- START PAGE 61 -->

## [Trang 61]


# Khoảng cách giữa Demo và Production

— Phản hồi chính xác trong vài lần thử chưa đủ cơ sở để triển khai hệ thống thực tế

01 · BASELINE

## Thiết lập đối chứng

Đối chiếu hiệu quả với quy tắc tĩnh, nhân sự hay quy trình hiện tại?

02 · EVALUATION

## Kiểm thử hệ thống

Bộ dữ liệu kiểm thử, kịch bản biên (edge cases) và tiêu chí nghiệm thu?

03 · CONTROLS

## Cơ chế kiểm soát

Logging, fallback, rollback và nhân sự chịu trách nhiệm?

04 · OPERATIONS

## Vận hành liên tục

Ai giám sát lỗi, cập nhật tri thức nền và tối ưu hệ thống?

Mục tiêu Day 02 là xác định tính khả thi để tiếp tục nghiên cứu — chưa phải quyết định triển khai ngay.

NGUỒN Google — Rules of ML · Chip Huyen — AI Engineering
QUYẾT ĐỊNH AI · DEMO TO PRODUCTION

DAY 02 · 61 / 76


<!-- END PAGE 61 -->


<!-- START PAGE 62 -->

## [Trang 62]


# Từ Problem Statement đến Eval Plan

— Problem Statement rõ ràng giúp định hình cụ thể các tiêu chí kiểm thử

01 · INPUT

Problem Statement

9 trường đã hoàn chỉnh — từ Actor, Workflow, Bottleneck đến Boundary & HITL.

02 · TEST CASES

Kịch bản kiểm thử

Dữ liệu thực tế và các trường hợp biên (edge cases).

03 · SUCCESS

Chỉ số hiệu năng

Đạt yêu cầu (pass) / Không đạt (fail) / Chuyển tiếp kiểm duyệt thủ công (HITL).

TÁC VỤ ĐƠN LỄ

Hệ thống có **phân loại chính xác** các câu hỏi đầu vào không?

HIỆU NĂNG QUY TRÌNH

Nhóm học viên có **hoàn thành bài lab nhanh hơn và ít kẹt hơn** không?

RỦI RO & SAI SỐ

Hệ thống có **phản hồi sai lệch** mà không chuyển tiếp cho Lab Coach phê duyệt không?

PROBLEM STATEMENT - EVAL PLAN

DAY 02 - 62 / 76


<!-- END PAGE 62 -->


<!-- START PAGE 63 -->

## [Trang 63]


# Chuyển dịch từ PS sang Eval Plan

— Phương pháp đánh giá, bộ dữ liệu mẫu và ngưỡng chấp nhận

![img-22.jpeg](img-22.jpeg)

"Nếu không suy ra được 3 thứ bên phải -> PS chưa đủ chặt"

Không suy ra được test cases, eval metric và architecture boundary từ PS -> PS chưa đủ chặt.

PROBLEM STATEMENT - EVAL FLOW

DAY 02 - 63 / 76


<!-- END PAGE 63 -->


<!-- START PAGE 64 -->

## [Trang 64]


# Lỗi AI được định nghĩa bởi kỳ vọng người dùng

— PAIR Chương 6 · Errors + Graceful Failure

Cùng một hệ gợi ý đúng 60% — là thành công hay thất bại? Tùy vào kỳ vọng bạn đã hứa với người dùng.

LOẠI 1 · CONTEXT ERRORS

Sai bối cảnh

Hệ thống chạy "đúng" nhưng giả định sai về người dùng, thời điểm hoặc bối cảnh.

VD: gợi ý ôn bài giữa kỳ vọng.

LOẠI 2 · FAILSTATES

Không trả lời được

Hệ thống không trả lời được hoặc không có câu trả lời đúng cho tình huống này.

LOẠI 3 · BACKGROUND ERRORS

Lỗi ngầm

Cả người dùng lẫn hệ thống đều không nhận ra — "unknown unknowns".

→ Cần QA chủ động, không chờ người dùng báo lỗi.

Viết Boundary & HITL trong Problem Statement chính là khai báo trước: lỗi nào được phép xảy ra, lỗi nào không — và ai bắt lỗi đó.

NGUỒN PAIR — Ch.6 Errors + Graceful Failure
ERRORS · ĐỊNH NGHĨA LỖI

DAY 02 · 64 / 76


<!-- END PAGE 64 -->


<!-- START PAGE 65 -->

## [Trang 65]


# Vai trò UX + Human-in-the-loop

— UX là chốt chặn khi AI thiếu dữ liệu, độ tin cậy thấp hoặc cần phê duyệt thủ công

![img-23.jpeg](img-23.jpeg)

## AI không cần hoàn hảo, nếu UX đỡ được chỗ nó yếu

**Không chắc**
(low confidence)

Xin user xác nhận
trước khi thực hiện

**Risk cao**
(sai = hậu quả nghiêm trọng)

Chỉ suggest,
không auto-action

**Câu trả lời dài**
(quá tải thông tin)

Chia option / card /
summary cho user chọn

**Thiếu context**
(input mơ hồ)

Hỏi lại đúng chỗ
thay vì đoán sai

AI Product = AI + UX. Dùng UX để hỗ trợ chỗ AI chưa đủ tốt.

**PAIR — paths forward from failure:** luôn mở kênh feedback (kể cả trên output "đúng") và trả quyền kiểm soát cho người dùng khi automation hỏng.

NGUỒN PAIR — Ch.6 Errors + Graceful Failure

ERRORS - UX + HITL

4 PATTERN HUMAN-IN-THE-LOOP

Làm rõ ý định

Yêu cầu bổ sung ngữ cảnh khi thông tin chưa đủ.

Minh bạch thông tin

Trích dẫn nguồn minh chứng cho câu trả lời.

Phê duyệt thủ công

Con người kiểm duyệt trước tác vụ rủi ro cao.

Thiết lập ranh giới

Giới hạn phạm vi hoạt động tự chủ của AI.

DAY 02 - 65 / 76


<!-- END PAGE 65 -->


<!-- START PAGE 66 -->

## [Trang 66]


SECTION 05

# Problem Statement hoàn chỉnh

*Liên kết chặt chẽ giữa bài toán, workflow, metrics và quyết định AI — thành đầu vào cho Eval Plan.*


<!-- END PAGE 66 -->


<!-- START PAGE 67 -->

## [Trang 67]


# Problem Statement cho hệ thống AI

— 6 yếu tố bài toán cốt lõi và 3 yếu tố quyết định AI

## 6 YẾU TỐ BÀI TOÁN CỐT LÕI

|  **Actor** | *đối tượng ảnh hưởng* | Đối tượng trực tiếp chịu ảnh hưởng bởi vấn đề.  |
| --- | --- | --- |
|  **Workflow** | *quy trình hiện tại* | Quy trình vận hành hiện tại gồm các bước cụ thể nào?  |
|  **Bottleneck** | *nút thắt* | Khâu nào gặp tình trạng chậm trễ, sai sót, lặp lại?  |
|  **Impact** | *tác động* | Tổn thất lượng hóa bằng thời gian, chi phí, SLA hoặc chất lượng.  |
|  **Success Metric** | *chỉ số thành công* | Chỉ số đo lường cụ thể để xác định sự cải thiện.  |
|  **Boundary** | *ranh giới* | AI không được làm gì; khâu nào bắt buộc có con người.  |

## 3 YẾU TỐ QUYẾT ĐỊNH AI

|  **Điểm AI can thiệp** | *decision - entry* | AI hỗ trợ hoặc tự động hóa ở bước cụ thể nào?  |
| --- | --- | --- |
|  **Mức chọn** | *decision - level* | Rule / Workflow / Agent?  |
|  **Rủi ro & HITL** | *decision - safety* | Phương án xử lý khi AI sai sót và quy trình phê duyệt thủ công.  |

PROBLEM STATEMENT - 9 TRƯỜNG

DAY 02 - 67 / 76


<!-- END PAGE 67 -->


<!-- START PAGE 68 -->

## [Trang 68]


# Ví dụ mẫu: Hỗ trợ Lab Coach/TA

— Một Problem Statement hoàn chỉnh làm căn cứ ra quyết định

|  **Actor** | Lab Coach hỗ trợ các nhóm học viên trong lớp 1000 học viên (khóa K3 & K4).  |
| --- | --- |
|  **Workflow** | Học viên đặt câu hỏi → Lab Coach nghiên cứu ngữ cảnh → Phản hồi / yêu cầu làm rõ → Học viên cập nhật bài.  |
|  **Bottleneck** | Câu hỏi trùng lặp hoặc thiếu thông tin nền tảng cao; Lab Coach mất thời gian phân loại thủ công.  |
|  **Impact** | Học viên chờ phản hồi lâu; Lab Coach quá tải, thiếu thời gian cho câu hỏi phức tạp.  |
|  **Success Metric** | Giảm tỷ lệ câu hỏi lập duyệt thủ công; rút ngắn thời gian phản hồi trung bình; không tăng tỷ lệ định hướng sai.  |
|  **Boundary** | AI không tự đánh giá/chấm điểm bài; chỉ hỗ trợ gợi ý làm rõ và điều phối quy trình.  |
|  **Điểm AI can thiệp** | Ngay sau khi học viên gửi câu hỏi hoặc Problem Card thiếu thông tin ngữ cảnh.  |
|  **Mức chọn** | **Workflow:** AI phát hiện thông tin còn thiếu; Lab Coach phê duyệt câu hỏi chuyên sâu.  |
|  **Rủi ro & HITL** | AI định hướng sai → Lab Coach kiểm duyệt trước khi gửi phản hồi.  |

Một Problem Statement đủ 9 trường — như ví dụ này — là căn cứ để ra quyết định Go, Not Yet hay No-Go.

PROBLEM STATEMENT - VÍ DỤ

DAY 02 - 68 / 76


<!-- END PAGE 68 -->


<!-- START PAGE 69 -->

## [Trang 69]


# Đánh giá mức độ phù hợp của AI

BỘ THẺ CÂU HỎI #4 — GATE QUYẾT ĐỊNH

— Năm câu hỏi kiểm tra mức sẵn sàng — gate cuối trước khi ra quyết định

01 Nghiệp vụ có đòi hỏi xử lý ngôn ngữ, tri thức chuyên môn hoặc suy luận?
02 Dữ liệu đầu vào có cung cấp đủ ngữ cảnh để AI phản hồi chính xác?
03 Đã thiết lập các chỉ số định lượng để đánh giá hiệu quả?
04 Hậu quả khi AI sai sót có nằm trong phạm vi kiểm soát?
05 Có giải pháp thay thế đơn giản và tối ưu chi phí hơn AI không?

Nếu phần lớn câu trả lời chưa rõ ràng → Quyết định: Not Yet.

NGUỒN Google — Rules of Machine Learning — Anthropic — Building effective agents
QUYẾT ĐỊNH AI - 5 CÂU HỎI

DAY 02 - 69 / 76


<!-- END PAGE 69 -->


<!-- START PAGE 70 -->

## [Trang 70]


# Khung ra quyết định: Go / Not Yet / No-Go

— Lập luận dựa trên tính khả thi của Problem Statement, tránh thiên kiến công nghệ

## ✓ Go

*thực hiện*

### ĐỦ ĐIỀU KIỆN

- — Bài toán rõ ràng
- — Chỉ số đo lường khả thi
- — Điểm can thiệp AI phù hợp
- — Kiểm soát được rủi ro

## || Not Yet

*tạm hoãn*

### CÓ TRIỂN VỌNG

- — Cần bổ sung dữ liệu thực tế
- — Chuẩn hóa quy trình
- — Thiết lập chỉ số
- — Xác định ranh giới

## ✕ No-Go

*không triển khai*

### KHÔNG PHÙ HỢP

- — AI không mang giá trị vượt trội
- — Rủi ro vận hành quá cao
- — Giải pháp không dùng AI tối ưu hơn

Quyết định "Not Yet" thể hiện sự chín chắn trong tư duy thiết kế sản phẩm, không phải sự thất bại.

QUYẾT ĐỊNH - GO / NOT YET / NO-GO

DAY 02 - 70 / 76


<!-- END PAGE 70 -->


<!-- START PAGE 71 -->

## [Trang 71]


# Sáu nguyên tắc cốt lõi sau Day 02

— Kim chỉ nam để thẩm định mọi đề xuất ứng dụng AI

## 01 Brief mơ hồ không thay thế Problem Statement.

Một bản tóm tắt mơ hồ không thể thay thế cho một Problem Statement hoàn chỉnh.

## 02 Mô hình hóa workflow trước khi tích hợp AI.

Bắt buộc phải mô hình hóa quy trình trước khi xem xét tích hợp giải pháp AI.

## 03 Pain point phải được lượng hóa.

Mọi điểm đau cần được lượng hóa bằng baseline và chỉ số đo lường cụ thể.

## 04 Phức tạp không đồng nghĩa với hiệu quả.

Rule, Workflow và Agent là ba cấp độ khác nhau; độ phức tạp kỹ thuật không đồng nghĩa với hiệu quả tối ưu.

## 05 Quyết định dựa trên lập luận thực tế.

Quyết định Go / Not Yet / No-Go phải được thiết lập dựa trên lập luận thực tế và số liệu kiểm thử rõ ràng.

## 06 Đo reward function bằng trải nghiệm người dùng, không chỉ accuracy. **MỚI - PAIR**

Thiết kế đánh đổi precision ↔ recall theo lợi ích người dùng và kiểm chứng với người dùng thật.

NGUỒN PAIR — Ch.1 User Needs + Defining Success

RECAP - 6 NGUYÊN TẮC

DAY 02 - 71 / 76


<!-- END PAGE 71 -->


<!-- START PAGE 72 -->

## [Trang 72]


# Bốn nguồn gốc của lỗi AI

— PAIR Chương 6: Errors + Graceful Failure

APPENDIX - ĐỌC THÊM

NGUỒN LỖI 1

Lỗi dữ liệu & dự đoán

Dữ liệu gán nhân sai, suy luận kém, hoặc thiếu dữ liệu huấn luyện.

NGUỒN LỖI 2

Lỗi đầu vào

Input bất ngờ ngoài thiết kế, phá vỡ thói quen của người dùng.

NGUỒN LỖI 3

Lỗi liên quan

Độ tin cậy thấp, kết quả không liên quan — VD: gợi ý "hoạt động vui chơi" cho chuyến đi đám tang.

NGUỒN LỖI 4

Lỗi phân cấp hệ thống

Nhiều hệ thống AI cùng hoạt động và xung đột tín hiệu với nhau.

"Lỗi" được định nghĩa bởi kỳ vọng và mô hình tâm trí của người dùng — cùng một hệ thống có thể là thành công hoặc thất bại tùy kỳ vọng.

NGUỒN PAIR — Ch.6 Errors + Graceful Failure

APPENDIX - PAIR CH.6 (1/2)

DAY 02 - 72 / 76


<!-- END PAGE 72 -->


<!-- START PAGE 73 -->

## [Trang 73]


# Paths forward from failure

— PAIR Chương 6: Errors + Graceful Failure

APPENDIX - ĐỌC THÊM

PATH 1

Mở kênh feedback

Tạo cơ hội cho người dùng phản hồi về chất lượng hệ thống — kể cả trên những output "đúng".

PATH 2

Trả quyền kiểm soát

Khi automation thất bại, trả quyền kiểm soát cho người dùng — kèm đủ thông tin để họ tiếp quản công việc.

PATH 3

Giả định người dùng sẽ dùng sai

Thiết kế để thất bại trở nên "an toàn, nhàm chán" — thay vì trở thành thảm họa.

Nguyên tắc thông báo lỗi: "be human, not machine".

Thiết kế trải nghiệm khi AI sai sẽ học kỹ ở Day 18 — Human-centered AI design.

NGUỒN PAIR — Ch.6 Errors + Graceful Failure

APPENDIX - PAIR CH.6 (2/2)

DAY 02 - 73 / 76


<!-- END PAGE 73 -->


<!-- START PAGE 74 -->

## [Trang 74]


# Workflow Patterns theo Anthropic

APPENDIX - ĐỌC THÊM

— Bảng tổng quan các mô hình từ cơ bản đến tự chủ

BASIC PATTERNS

Mô hình cơ bản

đáp ứng đa số tác vụ

Prompt Chaining — Chuỗi liên kết

Routing — Phân luồng

Parallelization — Song song

ADVANCED PATTERNS

Mô hình nâng cao

khi nghiệp vụ đòi hỏi

Orchestrator-Workers — Điều phối – Thực thi

Evaluator-Optimizer — Đánh giá – Tối ưu

AUTONOMOUS

Agent

tác nhân tự chủ

LLM tự lập kế hoạch, sử dụng công cụ, quan sát phản hồi và linh hoạt điều chỉnh bước tiếp theo.

Nguyên tắc: Bắt đầu bằng giải pháp đơn giản nhất; chỉ tăng độ phức tạp khi quy trình thực tế yêu cầu.

NGUỒN Anthropic — Building effective agents
APPENDIX - ANTHROPIC PATTERNS

DAY 02 - 74 / 76


<!-- END PAGE 74 -->


<!-- START PAGE 75 -->

## [Trang 75]


# Vòng đời Sản phẩm AI

APPENDIX - ĐỌC THÊM

— Mỗi giai đoạn từ ý tưởng đến vận hành thực tế yêu cầu phương thức xác thực chuyên biệt

![img-24.jpeg](img-24.jpeg)

NGUỒN Chip Huyen — AI Engineering (O'Reilly, 2025)
APPENDIX - LIFECYCLE

DAY 02 - 75 / 76


<!-- END PAGE 75 -->


<!-- START PAGE 76 -->

## [Trang 76]


# Bộ thẻ câu hỏi #1–#4 tổng hợp

APPENDIX • ÔN TẬP

— 22 câu hỏi theo hành trình: Phân kỳ → Phỏng vấn → Cấu trúc PS → Gate quyết định

#1 • PHÂN KỶ

6 câu gợi mở → slide 21

1. Giả định hiển nhiên nào cần lật lại?
2. Cách tiếp cận nào hoàn toàn mới?
3. Nếu thiết kế lại từ đầu, không giới hạn?
4. Tại sao bài toán này cần AI?
5. Quy trình nào tồn tại chỉ vì thói quen?
6. Câu hỏi cốt lõi nào đang bị né tránh?

#2 • PHỎNG VẤN

5 câu stakeholder → slide 25

1. Pain point là gì, tần suất ra sao?
2. Workflow hiện tại như thế nào?
3. Thiệt hại do vấn đề gây ra?
4. Hậu quả nếu AI sai sót?
5. Ai có quyền phê duyệt (nói YES)?

#3 • CẤU TRÚC PS

6 câu khai thác → slide 30

1. Quy trình hiện tại như thế nào?
2. Nút thắt nằm ở đâu?
3. Hao phí hiện tại là bao nhiêu?
4. Tiêu chí thành công đo bằng gì?
5. Hậu quả khi xảy ra sai sót?
6. Có giải pháp phi AI đơn giản hơn?

#4 • GATE QUYẾT ĐỊNH

5 câu readiness → slide 69

1. Có đòi hỏi ngôn ngữ, tri thức, suy luận?
2. Dữ liệu đủ ngữ cảnh để AI chính xác?
3. Đã có chỉ số định lượng?
4. Hậu quả sai sót có kiểm soát được?
5. Có giải pháp đơn giản hơn AI?

APPENDIX • QUESTION CARDS

DAY 02 • 76 / 76


<!-- END PAGE 76 -->
