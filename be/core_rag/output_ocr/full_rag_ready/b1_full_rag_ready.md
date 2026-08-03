# Kết quả bóc tách PDF: b1.pdf



<!-- START PAGE 1 -->

## [Trang 1]


AI IN ACTION - Day 1

# AI & LLM Foundation

*Bạn đang dùng AI mỗi ngày — nhưng thực sự bên trong nó đang làm gì?*

Instructor: Mai Anh Nguyen (Blue)


<!-- END PAGE 1 -->


<!-- START PAGE 2 -->

## [Trang 2]


# Instructor



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 2]**:
> 🖼️ *[Hình ảnh chân dung]*



## Mai Anh Nguyen (Blue)

Generalist Product Builder

- 2026 FPT Long Châu (PM · Healthcare Product)
- 2025 Thongtincuuho.org (Co-founder)
- 2025 FPT Software AI Center (PM · AI Agent)
- 2021 - 2025 Xantus (PM · On-chain Analytics, AI Agent)
- 2016 - 2021 DYNO, Kalapa (PM · OCR, eKYC, Credit Scoring)

Linkedin | Facebook


<!-- END PAGE 2 -->


<!-- START PAGE 3 -->

## [Trang 3]


AI IN ACTION - Day 1

# Agenda

- Bức tranh AI & các tầng của AI
- Lịch sử AI 70 năm
- Bên trong LLM: cơ chế vận hành
- Từ LLM đến AI Agent
- Landscape: model hôm nay & cuộc đua hiện tại
- Chọn model & chi phí token
- Gọi API lần đầu
- Tổng kết — những ý đề mang về

**AI & LLM Foundation**

*Từ "nghe AI" đến "gọi AI" trong một ngày*


<!-- END PAGE 3 -->


<!-- START PAGE 4 -->

## [Trang 4]


# Hôm nay mình đi từ "nghe AI" đến "gọi AI"

Cuối ngày này, mỗi bạn sẽ ra về với 4 thứ:

1 Hiểu được

Giải thích được LLM hoạt động thế nào — bằng trực giác, không cần công thức

2 Nắm được

Token, context, chi phí, độ trễ liên hệ với nhau ra sao

3 Gọi được

Lần gọi API đầu tiên — và hiểu cấu trúc của một lần gọi model

4 Build được

Một chatbot dòng lệnh đơn giản có streaming — sản phẩm của chính bạn

Không cần nền toán. Chỉ cần tò mò và một chiếc máy tính.


<!-- END PAGE 4 -->


<!-- START PAGE 5 -->

## [Trang 5]


# PHẦN 01

# Bức tranh AI

*AI, machine learning, LLM nằm ở đâu trong cùng một hệ?*


<!-- END PAGE 5 -->


<!-- START PAGE 6 -->

## [Trang 6]


# AI, ML, Deep Learning, GenAI, LLM — nằm ở đâu trong cùng một hệ?

từ rộng đến hẹp



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 6]**:
```markdown
---
### **Tên/Chủ đề sơ đồ**: Sơ đồ phân cấp các khái niệm trong lĩnh vực Trí tuệ nhân tạo (AI) với trọng tâm vào Large Language Models (LLM)

---

### **Các cột mốc / Thành phần chính**:
1. **Artificial Intelligence (AI)**
   - Lớp ngoài cùng, bao quát toàn bộ lĩnh vực trí tuệ nhân tạo.

2. **Machine Learning (ML)**
   - Một phân nhánh của AI, tập trung vào việc hệ thống học từ dữ liệu mà không cần lập trình cứng.

3. **Deep Learning (DL)**
   - Một nhánh của Machine Learning sử dụng mạng nơ-ron sâu để phân tích và học từ dữ liệu phức tạp.

4. **Generative AI**
   - Một phân nhánh của Deep Learning, tập trung vào việc tạo ra nội dung mới (text, hình ảnh, âm thanh, code,...).

5. **Large Language Models (LLM)**
   - Một loại mô hình trong Generative AI, được đào tạo trên lượng dữ liệu lớn để hiểu và tạo ra văn bản.
   - Các ví dụ cụ thể: **GPT, Claude, KimI**.

6. **Các ứng dụng cụ thể của LLM** (từ trong ra ngoài):
   - **Văn bản, ảnh, code**: Tạo nội dung đa dạng.
   - **Nhận diện ảnh, giọng nói**: Xử lý và phân tích hình ảnh và âm thanh.
   - **Lọc spam, gợi ý phím**: Ứng dụng trong email và giao diện người dùng.
   - **Kế hoạch lữ hành, robot...**: Ứng dụng trong các hệ thống phức tạp hơn như hỗ trợ quyết định và tự động hóa.

---

### **Số liệu & Insight quan trọng**:
- **Tên công nghệ chính**: GPT, Claude, KimI (các mô hình LLM nổi bật).
- **Phân cấp rõ ràng**: AI → Machine Learning → Deep Learning → Generative AI → LLM.
- **Mô hình LLM** là một phần nhỏ nhưng quan trọng của Generative AI, được ứng dụng rộng rãi trong nhiều lĩnh vực từ đơn giản đến phức tạp.

---

### **Ý nghĩa bài học**:
Sơ đồ này minh họa cách các khái niệm trong AI liên quan và phát triển từ tổng quát đến cụ thể. **Large Language Models (LLM)** là một trong những công nghệ tiên tiến nhất hiện nay, có khả năng tạo ra và xử lý nội dung đa dạng, từ văn bản, hình ảnh đến các ứng dụng thực tế như lọc spam, hỗ trợ lữ hành và tự động hóa. Hiểu phân cấp này giúp nhận diện được vị trí và tầm quan trọng của các mô hình ngôn ngữ lớn trong bối cảnh AI hiện đại.
---
```



- AI — chiếc ô lớn nhất: mọi hệ thống có yếu tố "thông minh".
- Machine learning — học từ dữ liệu thay vì viết luật tay.
- Deep learning — mạng nơ-ron nhiều tầng tự học đặc trưng.
- Generative AI — sinh nội dung mới: văn bản, ảnh, code.
- LLM — model nền chuyên ngôn ngữ, tìm của làn sóng hiện nay.

LLM không phải toàn bộ AI — nhưng nó là tầng nền của gần hết trải nghiệm AI bạn dùng hôm nay


<!-- END PAGE 6 -->


<!-- START PAGE 7 -->

## [Trang 7]


# Ba nhóm AI chính: phân loại · sinh nội dung · hành động

Discriminative AI

Giỏi **phân loại, dự đoán**: lọc spam, phát hiện gian lận, nhận diện ảnh.

*Input → một nhân, một con số*

Generative AI

**Sinh ra thứ mới**: văn bản, ảnh, code.
ChatGPT, Claude, Midjourney.

*Prompt → nội dung mới*

Agentic AI

Nhận **mục tiêu** rồi tự làm nhiều bước:
lập kế hoạch, dùng công cụ, hành động.

*Goal → Plan → Action*

LLM là **engine chung** của cả Generative lẫn Agentic — cuối buổi sáng mình sẽ thấy agent khác LLM ở đâu

Hành trình khóa học: LLM Foundation → Agent → Multi-Agent → Deploy → Evaluate


<!-- END PAGE 7 -->


<!-- START PAGE 8 -->

## [Trang 8]


PHẦN 02

# Lịch sử AI

*70 năm của những lần chạm trần và đổi nền tảng*


<!-- END PAGE 8 -->


<!-- START PAGE 9 -->

## [Trang 9]


# Lịch sử AI 70 năm



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 9]**:
```markdown
---
### **Tên/Chủ đề sơ đồ**: Lịch sử AI 70 năm (1956–2026)
**Loại**: Timeline sự phát triển của Trí tuệ nhân tạo (AI)

---

### **Các cột mốc / Thành phần chính**
#### **Trục X (Thời gian)**
- **1956–1973**: Các cự sức đầu tiên (Khai sinh, lời hứa đầu tiên)
- **1974–1980**: Mùa đông lần 1 (Thời kỳ bi quan)
- **1980–1987**: Hệ chuyên gia (Sự hồi sinh)
- **1987–1993**: Mùa đông lần 2 (Sự suy giảm)
- **1993–2006**: Thời kỳ chờ đợi (Sự phát triển ẩn)
- **2006–2026**: Phát triển mạnh mẽ (Deep Learning, AI hiện đại)

#### **Trục Y (Mức độ quan tâm/Phát triển)**
- Dùng đường cong màu xanh biểu thị sự phát triển và sự quan tâm của cộng đồng khoa học.

#### **Các sự kiện/Thành phần chính**
| Năm       | Sự kiện/Công nghệ                     | Mô tả                                                                                     |
|------------|----------------------------------------|-------------------------------------------------------------------------------------------|
| **1956**   | Dartmouth Workshop                    | Sự kiện khai sinh AI, lời hứa đầu tiên.                                                  |
| **1969**   | Perceptron                             | Báo cáo Perceptron của Minsky và Papert, gây tranh cãi.                                    |
| **1973**   | Mùa đông lần 1                         | Thời kỳ bi quan, dự án bị cắt giảm.                                                     |
| **1980**   | Hệ chuyên gia                         | Sự hồi sinh với hệ chuyên gia (Expert Systems).                                          |
| **1987**   | 5 máy Lisp                            | Sự phát triển của máy tính chuyên dụng cho AI.                                            |
| **1993**   | Mùa đông lần 2                         | Sự suy giảm do kỳ vọng quá cao và thiếu kết quả thực tế.                               |
| **2006**   | Deep Learning                          | Sự xuất hiện của Deep Learning, một bước ngoặt quan trọng.                              |
| **2012**   | AlexNet                                | Mô hình AlexNet giành chiến thắng trong cuộc thi ImageNet, thúc đẩy phát triển CNN.      |
| **2016**   | AlphaGo                                | AlphaGo đánh bại người chơi Go chuyên nghiệp, chứng minh khả năng của AI.             |
| **2017**   | Transformer                            | Xuất hiện mô hình Transformer, cơ sở cho các mô hình ngôn ngữ hiện đại.               |
| **2018**   | GPT-1/BERT                             | Các mô hình ngôn ngữ lớn như GPT-1 và BERT được giới thiệu.                              |
| **2022**   | ChatGPT                                | ChatGPT được phát hành, mang AI đến gần với công chúng.                                 |
| **2024**   | Ký nguyên Agent                        | Dự đoán sự phát triển của các Agent AI.                                                   |
| **2026**   | Hiện tại dự đoán                       | Tương lai tiếp tục phát triển mạnh mẽ.                                                   |

---

### **Số liệu & Insight quan trọng**
- **Thời kỳ phát triển mạnh mẽ**: Từ năm 2006 đến nay, đặc biệt là sau sự ra đời của Deep Learning.
- **Các công nghệ đột phá**:
  - **1956**: Dartmouth Workshop.
  - **2012**: AlexNet.
  - **2016**: AlphaGo.
  - **2017**: Transformer.
  - **2022**: ChatGPT.
- **Các mùa đông AI**: Hai giai đoạn suy giảm (1974–1980 và 1987–1993) do kỳ vọng quá cao và thiếu kết quả thực tế.

---

### **Ý nghĩa bài học**
1. **Sự phát triển không đều**: Lịch sử AI có nhiều giai đoạn phát triển mạnh và suy giảm, thể hiện sự phức tạp trong nghiên cứu khoa học.
2. **Tầm quan trọng của công nghệ nền tảng**: Các đột phá như Deep Learning và Transformer đã mở ra thời đại mới cho AI.
3. **Tương lai AI**: Sự phát triển của các Agent AI và mô hình ngôn ngữ lớn cho thấy AI sẽ tiếp tục thay đổi xã hội và công nghệ trong tương lai gần.
```

---



2 lần mùa đông, cách tiếp cận chậm trễ

Từ model đơn lẻ sang system có khả năng hành động như agent


<!-- END PAGE 9 -->


<!-- START PAGE 10 -->

## [Trang 10]


# 1956: Dartmouth Workshop



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 10]**:
```markdown
### 1. **Tên/Chủ đề sơ đồ**: Timeline Phát triển Trí tuệ Nhân tạo (AI) từ năm 1956 đến 2026

---

### **Các cột mốc / Thành phần chính**:

#### **Trục X (Thời gian)**:
- **1956**: Dartmouth Workshop (bắt đầu)
- **1966-1973**: Các cự sởc (AI winter đầu tiên)
- **1974-1980**: Mùa đông lần 1 (Mùa đông AI)
- **1980-1987**: Mùa đông lần 2 (Mùa đông AI)
- **1987-1993**: Sụp đổ Lisp machine, Hệ chuyên gia (Expert Systems)
- **1993-2006**: Thời kỳ "không mấy nổi bật" (AI không phát triển mạnh)
- **2006-2012**: Deep Learning xuất hiện
- **2012-2026**: Phát triển mạnh mẽ của AI hiện đại

#### **Trục Y (Mức độ phát triển AI)**:
- Dùng đường cong để thể hiện sự phát triển và suy thoái của AI qua các thời kỳ.

#### **Các thành phần chính trên timeline**:
- **1956**: Dartmouth Workshop (bắt đầu nghiên cứu AI)
- **1969**: Báo cáo Lighthill (Phê phán quá cao kỳ vọng AI)
- **1980**: Hệ chuyên gia (Expert Systems) phát triển
- **1987**: Sụp đổ của Lisp machine
- **2006**: Deep Learning xuất hiện
- **2012**: AlexNet (một bước tiến lớn trong học sâu)
- **2016**: AlphaGo đánh bại người chơi cờ vây chuyên nghiệp
- **2017**: Transformer mô hình được giới thiệu
- **2018**: GPT-1/BERT (mô hình ngôn ngữ)
- **2022**: ChatGPT (mô hình ngôn ngữ lớn)
- **2024**: Kỳ ngộ Agent (Agent AI)
- **2026**: Hiện tại dự đoán (tương lai AI)

---

### **Số liệu & Insight quan trọng**:
- **1956**: Dartmouth Workshop được coi là sự ra đời chính thức của AI.
- **1966-1973**: Thời kỳ đầu tiên của mùa đông AI (AI winter lần 1).
- **1974-1980**: Mùa đông AI lần 2.
- **1980**: Hệ chuyên gia (Expert Systems) đạt đỉnh cao.
- **1987**: Sụp đổ của Lisp machine, kết thúc thời kỳ phát triển hệ chuyên gia.
- **2006**: Deep Learning được giới thiệu, đánh dấu sự khởi đầu của thời kỳ phát triển mạnh mẽ.
- **2012**: AlexNet đánh dấu bước đột phá trong học sâu (Deep Learning).
- **2016**: AlphaGo đánh bại người chơi cờ vây chuyên nghiệp, chứng minh khả năng của AI.
- **2017**: Transformer mô hình được giới thiệu, ảnh hưởng lớn đến ngôn ngữ và xử lý ngôn ngữ tự nhiên (NLP).
- **2018**: GPT-1/BERT được phát triển, mở ra thời đại của mô hình ngôn ngữ lớn.
- **2022**: ChatGPT được phát hành, làm nổi bật ứng dụng thực tế của AI.
- **2024**: Dự đoán phát triển của Kỳ ngộ Agent (Agent AI).
- **2026**: Dự đoán sự phát triển tiếp tục mạnh mẽ của AI.

---

### **Ý nghĩa bài học**:
- **Sự phát triển không đều**: AI đã trải qua nhiều giai đoạn phát triển và suy thoái (mùa đông AI), nhưng mỗi lần đều có những bước tiến mới.
- **Tầm quan trọng của công nghệ nền tảng**: Các bước tiến như Deep Learning, Transformer và mô hình ngôn ngữ lớn đã thay đổi hoàn toàn khả năng của AI.
- **Tương lai AI**: Dự đoán rằng AI sẽ tiếp tục phát triển mạnh mẽ và có những ứng dụng thực tế rộng rãi trong tương lai gần.
```

> 📌 *Ghi chú*: Biểu đồ này nhấn mạnh sự tuần hoàn và phát triển không đều của AI, đồng thời dự đoán tiềm năng to lớn của nó trong tương lai.




<!-- END PAGE 10 -->


<!-- START PAGE 11 -->

## [Trang 11]


# 1969: Perceptrons



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 11]**:
```markdown
---
### 1. Tên/Chủ đề sơ đồ: Timeline Phát triển của Trí tuệ Nhân tạo (AI) và các công nghệ Perceptrons/Deep Learning

---
### 2. Các cột mốc / Thành phần chính:

#### **Trục X (Thời gian):**
- Từ năm 1956 đến năm 2026 (dự báo).
- Được chia thành các giai đoạn lớn:
  - **Các cự sĩ sớm (1956-1973)**
  - **Mùa đông lần 1 (1974-1980)**
  - **Mùa đông lần 2 (1980-1993)**
  - **Hiện tại (2026)**

#### **Trục Y (Sự phát triển của AI):**
- Dạng đồ thị sóng, thể hiện sự lên xuống của niềm tin và đầu tư vào AI qua các thời kỳ.

#### **Các sự kiện và công nghệ quan trọng:**
- **1956:** Dartmouth Workshop (bắt đầu nghiên cứu AI).
- **1958:** Perceptrons (Frank Rosenblatt) – mô hình cơ bản của mạng nơ-ron.
- **1973:** "Report from Lighthill" – đánh giá tiêu cực, dẫn đến Mùa đông lần 1.
- **1980:** Hệ chuyên gia (Expert Systems) – sự hồi sinh tạm thời.
- **1987:** Máy Lisp (Lisp machine) – sự phát triển của ngôn ngữ lập trình AI.
- **2006:** Deep Learning (Học sâu) – sự phát triển mạnh mẽ của mạng nơ-ron sâu.
- **2012:** AlexNet – mạng nơ-ron chinh phục ImageNet, đánh dấu sự trở lại của Deep Learning.
- **2016:** AlphaGo đánh bại người chơi Go chuyên nghiệp.
- **2017:** Transformer – mô hình ngôn ngữ mới.
- **2018:** GPT-1/BERT – mô hình ngôn ngữ lớn.
- **2022:** ChatGPT – ứng dụng thực tế của mô hình ngôn ngữ.
- **2024 (dự báo):** Kỳ nguyên Agent (Agent Revolution).
- **2026 (dự báo):** Hiện tại (Hiện tượng AI tiếp tục phát triển).

---
### 3. Số liệu & Insight quan trọng:
- **Perceptrons (1958):** Mô hình cơ bản của mạng nơ-ron, đặt nền móng cho AI hiện đại.
- **Mùa đông lần 1 (1974-1980):** Sự sụt giảm niềm tin và đầu tư vào AI do đánh giá tiêu cực từ báo cáo Lighthill.
- **Deep Learning (2006):** Sự phát triển mạnh mẽ của mạng nơ-ron sâu, sử dụng GPU và lượng dữ liệu lớn.
- **AlexNet (2012):** Đánh bại các phương pháp truyền thống trong lĩnh vực xử lý hình ảnh.
- **ChatGPT (2022):** Ứng dụng thực tế của mô hình ngôn ngữ lớn, mang lại sự quan tâm lớn đến AI trong đời sống.

---
### 4. Ý nghĩa bài học:
- **Sự phát triển của AI không phải là đường thẳng:** Có nhiều giai đoạn tăng trưởng và suy giảm do các giới hạn kỹ thuật và nhận thức.
- **Mạng nơ-ron và Deep Learning là chìa khóa:** Sự phát triển của các mô hình như Perceptrons, AlexNet, Transformer và GPT đã đưa AI đến một giai đoạn mới.
- **Tương lai AI sáng sủa:** Dự báo cho thấy sự phát triển tiếp tục với các ứng dụng thực tế và sáng tạo như các Agent thông minh.
```

---



Các hướng đi lần lượt **chạm trần**:

- **Hướng symbolic** (dạy máy bằng luật/quy tắc): bắt đầu đuổi trước thế giới quá nhiều ngữ cảnh
- **Hướng Perceptron** (thay vì viết hết luật, mình có thể cho máy học từ ví dụ) cũng gặp vấn đề vì quá đơn giản


<!-- END PAGE 11 -->


<!-- START PAGE 12 -->

## [Trang 12]


# 1973: Báo cáo Lighthill — cú hích kết thúc kỳ lạc quan đầu



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 12]**:
```markdown
### 1. Tên/Chủ đề sơ đồ:
**Timeline: Sự phát triển của trí tuệ nhân tạo (AI) và các cột mốc quan trọng trong lĩnh vực học máy (Machine Learning) và xử lý ngôn ngữ tự nhiên (NLP)**

---

### 2. Các cột mốc / Thành phần chính:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026.
- **Trục Y (Sự phát triển)**: Diễn biến của các công nghệ AI qua các giai đoạn, thể hiện bằng đường cong và các sự kiện quan trọng.

#### Các giai đoạn và sự kiện chính:
- **1956**: Dartmouth Workshop (bắt đầu nghiên cứu AI).
- **1969**: Báo cáo Lighthill (đánh giá và đặt ra những thách thức cho lĩnh vực AI).
- **1974-1980 (Mùa đông AI lần 1)**: Thời kỳ chậm phát triển do những đánh giá tiêu cực và hạn chế về tài chính.
- **1980**: Hệ chuyên gia (Expert Systems) phát triển.
- **1987**: Máy Lisp (Lisp machine) và sự xuất hiện của Sup đổ Lisp machine.
- **1993**: Kết thúc Mùa đông AI lần 2.
- **2006**: Sự ra đời của Deep Learning.
- **2012**: AlexNet (một mô hình mạng nơ-ron sâu) và sự phát triển của Transformer.
- **2016**: AlphaGo đánh bại người chơi cờ vây chuyên nghiệp.
- **2018**: GPT-1 và BERT (các mô hình ngôn ngữ lớn).
- **2022**: ChatGPT (mô hình ngôn ngữ lớn có khả năng tương tác).
- **2024 (dự kiến)**: Kỳ ngộ Agent (Agent Surprise).
- **2026 (dự kiến)**: Tương lai tiếp tục phát triển.

---

### 3. Số liệu & Insight quan trọng:
- **Các công nghệ quan trọng**:
  - Dartmouth Workshop (1956)
  - Báo cáo Lighthill (1969)
  - Hệ chuyên gia (1980)
  - Deep Learning (2006)
  - AlexNet (2012)
  - Transformer (2017)
  - AlphaGo (2016)
  - GPT-1/BERT (2018)
  - ChatGPT (2022)
  - Kỳ ngộ Agent (2024 dự kiến)

- **Các giai đoạn Mùa đông AI**:
  - Lần 1: 1974-1980
  - Lần 2: Sau 1987 đến khoảng đầu thập niên 1990.

---

### 4. Ý nghĩa bài học:
- **Sự phát triển không đều**: Lĩnh vực AI đã trải qua những giai đoạn phát triển mạnh và những thời kỳ trì trệ (Mùa đông AI).
- **Tiến bộ công nghệ**: Các bước đột phá như Deep Learning và Transformer đã mở ra khả năng mới cho AI, đặc biệt trong xử lý ngôn ngữ tự nhiên.
- **Tương lai AI**: Dự đoán sự phát triển tiếp tục với các mô hình như Kỳ ngộ Agent, mang lại những khả năng mới trong tương tác và tự động hóa.
```

> **Ghi chú**: Biểu đồ thể hiện sự phát triển của AI qua các thời kỳ, đặc biệt nhấn mạnh vào các công nghệ đột phá và các giai đoạn trì trệ, giúp hiểu rõ hơn về tiến trình lịch sử và tương lai của trí tuệ nhân tạo.



Chính phủ Anh nhờ James Lighthill đánh giá lại toàn ngành AI. Ông kết luận thẳng: **những gì AI làm được đi quá xa so với lời hứa.**

Nguồn tiền đổ vào AI ở Anh và Mỹ bị cắt mạnh → mở màn **mùa đông AI lần thứ nhất.**


<!-- END PAGE 12 -->


<!-- START PAGE 13 -->

## [Trang 13]


# Mùa đông AI lần 1: 1974-1980



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 13]**:
```markdown
# 1. **Biểu đồ Timeline: Phát triển Trí tuệ Nhân tạo (AI) từ 1956–2026**

---
### **Tên/Chủ đề sơ đồ**:
Biểu đồ tiến trình phát triển các công nghệ và mốc quan trọng trong lĩnh vực Trí tuệ Nhân tạo (AI) từ năm 1956 đến dự báo năm 2026, với tập trung vào giai đoạn **Mùa Đông AI lần 1 (1974–1980)**.

---

### **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026.
- **Trục Y (Tiến bộ)**: Diễn biến thành công/thất bại của AI qua các thời kỳ.
- **Các giai đoạn quan trọng**:
  - **Mùa Hè AI (1956–1974)**:
    - **Dartmouth Workshop (1956)**: Sự kiện khai sinh khái niệm AI.
    - **Các cú sốc (CAC CƯ SỐC, 1966–1973)**: Thời kỳ kỳ vọng cao nhưng kết quả hạn chế.
    - **Rảo cản LightHill (1969)**: Báo cáo chỉ trích về tiến độ chậm.
    - **Perceptron (1969)**: Một trong những mô hình học máy sớm.
  - **Mùa Đông AI lần 1 (1974–1980)**:
    - **Mùa Đông lần 1 (Mùa Đông Lần 1, 1974–1980)**: Thời kỳ ngân sách cắt giảm và sự nghi ngờ.
    - **Hệ chuyên gia (Hệ chuyên gia, 1980)**: Một trong những thành tựu quan trọng cuối thời kỳ.
  - **Mùa Đông lần 2 (1987–1993)**:
    - **Sự đổ lụi (Sụp đổ Lisp, 1987)**: Thất vọng về ngôn ngữ lập trình Lisp và các dự án lớn.
  - **Phục hồi và phát triển (1993–2006)**:
    - **Deep Learning (2006)**: Khởi đầu của mạng nơ-ron sâu.
  - **Thời kỳ hiện đại (2012–2026)**:
    - **AlexNet (2012)**: Mô hình mạng nơ-ron sâu đột phá.
    - **Transformer (2017)**: Kiến trúc cho xử lý ngôn ngữ tự nhiên.
    - **AlphaGo (2016)**: AI đánh bại người chơi Go.
    - **GPY-3/BERT (2018)**: Các mô hình ngôn ngữ tiên tiến.
    - **ChatGPT (2022)**: Chatbot ngôn ngữ tự nhiên.
    - **Dự báo (2024–2026)**: Ký nguyên Agent (Agent AGI) và Hiến tái (Hiến tái 2026).

---

### **Số liệu & Insight quan trọng**:
| Năm       | Sự kiện/Công nghệ                     | Ghi chú                                                                 |
|------------|----------------------------------------|--------------------------------------------------------------------------|
| 1956       | Dartmouth Workshop                    | Khởi đầu AI.                                                            |
| 1966–1973  | Các cú sốc (CAC CƯ SỐC)               | Kỳ vọng cao nhưng kết quả hạn chế.                                      |
| 1974–1980  | Mùa Đông AI lần 1                    | Ngân sách cắt giảm, sự nghi ngờ.                                        |
| 1980       | Hệ chuyên gia                         | Thành tựu quan trọng cuối thời kỳ.                                      |
| 1987       | Sụp đổ Lisp                           | Thất vọng về ngôn ngữ lập trình Lisp và dự án lớn.                     |
| 2006       | Deep Learning                         | Khởi đầu mạng nơ-ron sâu.                                              |
| 2012       | AlexNet                                | Mô hình mạng nơ-ron sâu đột phá.                                       |
| 2016       | AlphaGo                                | AI đánh bại người chơi Go.                                             |
| 2017       | Transformer                            | Kiến trúc cho xử lý ngôn ngữ tự nhiên.                                 |
| 2018       | GPY-3/BERT                             | Các mô hình ngôn ngữ tiên tiến.                                         |
| 2022       | ChatGPT                                | Chatbot ngôn ngữ tự nhiên.                                              |
| 2024–2026  | Ký nguyên Agent, Hiến tái 2026         | Dự báo về Agent AGI và tiến bộ tiếp theo.                              |

---

### **Ý nghĩa bài học**:
- **Tiến bộ không tuyến tính**: AI phát triển qua các giai đoạn cao trào và thất vọng, nhưng mỗi lần phục hồi lại mạnh mẽ hơn.
- **Tầm quan trọng của dữ liệu và tính toán**: Sự phát triển mạnh mẽ của AI trong thập niên 2010–2020 nhờ vào dữ liệu lớn và sức mạnh tính toán.
- **Tương lai AI**: Dự báo về Agent AGI (Artificial General Intelligence) và các ứng dụng tiên tiến trong tương lai gần, thể hiện tầm nhìn về một kỷ nguyên mới của trí tuệ nhân tạo.
```



Bài toán nhỏ — trông khá thông minh ✓



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 13]**:
```markdown
# 1. **Biểu đồ Timeline: Phát triển Trí tuệ Nhân tạo (AI) từ 1956–2026**

---
### **Tên/Chủ đề sơ đồ**:
Biểu đồ tiến trình phát triển các công nghệ và mốc quan trọng trong lĩnh vực Trí tuệ Nhân tạo (AI) từ năm 1956 đến dự báo năm 2026, với tập trung vào giai đoạn **Mùa Đông AI lần 1 (1974–1980)**.

---

### **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026.
- **Trục Y (Tiến bộ)**: Diễn biến thành công/thất bại của AI qua các thời kỳ.
- **Các giai đoạn quan trọng**:
  - **Mùa Hè AI (1956–1974)**:
    - **Dartmouth Workshop (1956)**: Sự kiện khai sinh khái niệm AI.
    - **Các cú sốc (CAC CƯ SỐC, 1966–1973)**: Thời kỳ kỳ vọng cao nhưng kết quả hạn chế.
    - **Rảo cản LightHill (1969)**: Báo cáo chỉ trích về tiến độ chậm.
    - **Perceptron (1969)**: Một trong những mô hình học máy sớm.
  - **Mùa Đông AI lần 1 (1974–1980)**:
    - **Mùa Đông lần 1 (Mùa Đông Lần 1, 1974–1980)**: Thời kỳ ngân sách cắt giảm và sự nghi ngờ.
    - **Hệ chuyên gia (Hệ chuyên gia, 1980)**: Một trong những thành tựu quan trọng cuối thời kỳ.
  - **Mùa Đông lần 2 (1987–1993)**:
    - **Sự đổ lụi (Sụp đổ Lisp, 1987)**: Thất vọng về ngôn ngữ lập trình Lisp và các dự án lớn.
  - **Phục hồi và phát triển (1993–2006)**:
    - **Deep Learning (2006)**: Khởi đầu của mạng nơ-ron sâu.
  - **Thời kỳ hiện đại (2012–2026)**:
    - **AlexNet (2012)**: Mô hình mạng nơ-ron sâu đột phá.
    - **Transformer (2017)**: Kiến trúc cho xử lý ngôn ngữ tự nhiên.
    - **AlphaGo (2016)**: AI đánh bại người chơi Go.
    - **GPY-3/BERT (2018)**: Các mô hình ngôn ngữ tiên tiến.
    - **ChatGPT (2022)**: Chatbot ngôn ngữ tự nhiên.
    - **Dự báo (2024–2026)**: Ký nguyên Agent (Agent AGI) và Hiến tái (Hiến tái 2026).

---

### **Số liệu & Insight quan trọng**:
| Năm       | Sự kiện/Công nghệ                     | Ghi chú                                                                 |
|------------|----------------------------------------|--------------------------------------------------------------------------|
| 1956       | Dartmouth Workshop                    | Khởi đầu AI.                                                            |
| 1966–1973  | Các cú sốc (CAC CƯ SỐC)               | Kỳ vọng cao nhưng kết quả hạn chế.                                      |
| 1974–1980  | Mùa Đông AI lần 1                    | Ngân sách cắt giảm, sự nghi ngờ.                                        |
| 1980       | Hệ chuyên gia                         | Thành tựu quan trọng cuối thời kỳ.                                      |
| 1987       | Sụp đổ Lisp                           | Thất vọng về ngôn ngữ lập trình Lisp và dự án lớn.                     |
| 2006       | Deep Learning                         | Khởi đầu mạng nơ-ron sâu.                                              |
| 2012       | AlexNet                                | Mô hình mạng nơ-ron sâu đột phá.                                       |
| 2016       | AlphaGo                                | AI đánh bại người chơi Go.                                             |
| 2017       | Transformer                            | Kiến trúc cho xử lý ngôn ngữ tự nhiên.                                 |
| 2018       | GPY-3/BERT                             | Các mô hình ngôn ngữ tiên tiến.                                         |
| 2022       | ChatGPT                                | Chatbot ngôn ngữ tự nhiên.                                              |
| 2024–2026  | Ký nguyên Agent, Hiến tái 2026         | Dự báo về Agent AGI và tiến bộ tiếp theo.                              |

---

### **Ý nghĩa bài học**:
- **Tiến bộ không tuyến tính**: AI phát triển qua các giai đoạn cao trào và thất vọng, nhưng mỗi lần phục hồi lại mạnh mẽ hơn.
- **Tầm quan trọng của dữ liệu và tính toán**: Sự phát triển mạnh mẽ của AI trong thập niên 2010–2020 nhờ vào dữ liệu lớn và sức mạnh tính toán.
- **Tương lai AI**: Dự báo về Agent AGI (Artificial General Intelligence) và các ứng dụng tiên tiến trong tương lai gần, thể hiện tầm nhìn về một kỷ nguyên mới của trí tuệ nhân tạo.
```



Ít nhanh, máy duyệt hết được → kết quả trông “thông minh”.

Thế giới thật — mỗi bước sinh ra quá nhiều nhánh



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 13]**:
```markdown
# 1. **Biểu đồ Timeline: Phát triển Trí tuệ Nhân tạo (AI) từ 1956–2026**

---
### **Tên/Chủ đề sơ đồ**:
Biểu đồ tiến trình phát triển các công nghệ và mốc quan trọng trong lĩnh vực Trí tuệ Nhân tạo (AI) từ năm 1956 đến dự báo năm 2026, với tập trung vào giai đoạn **Mùa Đông AI lần 1 (1974–1980)**.

---

### **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026.
- **Trục Y (Tiến bộ)**: Diễn biến thành công/thất bại của AI qua các thời kỳ.
- **Các giai đoạn quan trọng**:
  - **Mùa Hè AI (1956–1974)**:
    - **Dartmouth Workshop (1956)**: Sự kiện khai sinh khái niệm AI.
    - **Các cú sốc (CAC CƯ SỐC, 1966–1973)**: Thời kỳ kỳ vọng cao nhưng kết quả hạn chế.
    - **Rảo cản LightHill (1969)**: Báo cáo chỉ trích về tiến độ chậm.
    - **Perceptron (1969)**: Một trong những mô hình học máy sớm.
  - **Mùa Đông AI lần 1 (1974–1980)**:
    - **Mùa Đông lần 1 (Mùa Đông Lần 1, 1974–1980)**: Thời kỳ ngân sách cắt giảm và sự nghi ngờ.
    - **Hệ chuyên gia (Hệ chuyên gia, 1980)**: Một trong những thành tựu quan trọng cuối thời kỳ.
  - **Mùa Đông lần 2 (1987–1993)**:
    - **Sự đổ lụi (Sụp đổ Lisp, 1987)**: Thất vọng về ngôn ngữ lập trình Lisp và các dự án lớn.
  - **Phục hồi và phát triển (1993–2006)**:
    - **Deep Learning (2006)**: Khởi đầu của mạng nơ-ron sâu.
  - **Thời kỳ hiện đại (2012–2026)**:
    - **AlexNet (2012)**: Mô hình mạng nơ-ron sâu đột phá.
    - **Transformer (2017)**: Kiến trúc cho xử lý ngôn ngữ tự nhiên.
    - **AlphaGo (2016)**: AI đánh bại người chơi Go.
    - **GPY-3/BERT (2018)**: Các mô hình ngôn ngữ tiên tiến.
    - **ChatGPT (2022)**: Chatbot ngôn ngữ tự nhiên.
    - **Dự báo (2024–2026)**: Ký nguyên Agent (Agent AGI) và Hiến tái (Hiến tái 2026).

---

### **Số liệu & Insight quan trọng**:
| Năm       | Sự kiện/Công nghệ                     | Ghi chú                                                                 |
|------------|----------------------------------------|--------------------------------------------------------------------------|
| 1956       | Dartmouth Workshop                    | Khởi đầu AI.                                                            |
| 1966–1973  | Các cú sốc (CAC CƯ SỐC)               | Kỳ vọng cao nhưng kết quả hạn chế.                                      |
| 1974–1980  | Mùa Đông AI lần 1                    | Ngân sách cắt giảm, sự nghi ngờ.                                        |
| 1980       | Hệ chuyên gia                         | Thành tựu quan trọng cuối thời kỳ.                                      |
| 1987       | Sụp đổ Lisp                           | Thất vọng về ngôn ngữ lập trình Lisp và dự án lớn.                     |
| 2006       | Deep Learning                         | Khởi đầu mạng nơ-ron sâu.                                              |
| 2012       | AlexNet                                | Mô hình mạng nơ-ron sâu đột phá.                                       |
| 2016       | AlphaGo                                | AI đánh bại người chơi Go.                                             |
| 2017       | Transformer                            | Kiến trúc cho xử lý ngôn ngữ tự nhiên.                                 |
| 2018       | GPY-3/BERT                             | Các mô hình ngôn ngữ tiên tiến.                                         |
| 2022       | ChatGPT                                | Chatbot ngôn ngữ tự nhiên.                                              |
| 2024–2026  | Ký nguyên Agent, Hiến tái 2026         | Dự báo về Agent AGI và tiến bộ tiếp theo.                              |

---

### **Ý nghĩa bài học**:
- **Tiến bộ không tuyến tính**: AI phát triển qua các giai đoạn cao trào và thất vọng, nhưng mỗi lần phục hồi lại mạnh mẽ hơn.
- **Tầm quan trọng của dữ liệu và tính toán**: Sự phát triển mạnh mẽ của AI trong thập niên 2010–2020 nhờ vào dữ liệu lớn và sức mạnh tính toán.
- **Tương lai AI**: Dự báo về Agent AGI (Artificial General Intelligence) và các ứng dụng tiên tiến trong tương lai gần, thể hiện tầm nhìn về một kỷ nguyên mới của trí tuệ nhân tạo.
```



## BÙNG NỔ TỐ HỢP



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 13]**:
```markdown
# 1. **Biểu đồ Timeline: Phát triển Trí tuệ Nhân tạo (AI) từ 1956–2026**

---
### **Tên/Chủ đề sơ đồ**:
Biểu đồ tiến trình phát triển các công nghệ và mốc quan trọng trong lĩnh vực Trí tuệ Nhân tạo (AI) từ năm 1956 đến dự báo năm 2026, với tập trung vào giai đoạn **Mùa Đông AI lần 1 (1974–1980)**.

---

### **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026.
- **Trục Y (Tiến bộ)**: Diễn biến thành công/thất bại của AI qua các thời kỳ.
- **Các giai đoạn quan trọng**:
  - **Mùa Hè AI (1956–1974)**:
    - **Dartmouth Workshop (1956)**: Sự kiện khai sinh khái niệm AI.
    - **Các cú sốc (CAC CƯ SỐC, 1966–1973)**: Thời kỳ kỳ vọng cao nhưng kết quả hạn chế.
    - **Rảo cản LightHill (1969)**: Báo cáo chỉ trích về tiến độ chậm.
    - **Perceptron (1969)**: Một trong những mô hình học máy sớm.
  - **Mùa Đông AI lần 1 (1974–1980)**:
    - **Mùa Đông lần 1 (Mùa Đông Lần 1, 1974–1980)**: Thời kỳ ngân sách cắt giảm và sự nghi ngờ.
    - **Hệ chuyên gia (Hệ chuyên gia, 1980)**: Một trong những thành tựu quan trọng cuối thời kỳ.
  - **Mùa Đông lần 2 (1987–1993)**:
    - **Sự đổ lụi (Sụp đổ Lisp, 1987)**: Thất vọng về ngôn ngữ lập trình Lisp và các dự án lớn.
  - **Phục hồi và phát triển (1993–2006)**:
    - **Deep Learning (2006)**: Khởi đầu của mạng nơ-ron sâu.
  - **Thời kỳ hiện đại (2012–2026)**:
    - **AlexNet (2012)**: Mô hình mạng nơ-ron sâu đột phá.
    - **Transformer (2017)**: Kiến trúc cho xử lý ngôn ngữ tự nhiên.
    - **AlphaGo (2016)**: AI đánh bại người chơi Go.
    - **GPY-3/BERT (2018)**: Các mô hình ngôn ngữ tiên tiến.
    - **ChatGPT (2022)**: Chatbot ngôn ngữ tự nhiên.
    - **Dự báo (2024–2026)**: Ký nguyên Agent (Agent AGI) và Hiến tái (Hiến tái 2026).

---

### **Số liệu & Insight quan trọng**:
| Năm       | Sự kiện/Công nghệ                     | Ghi chú                                                                 |
|------------|----------------------------------------|--------------------------------------------------------------------------|
| 1956       | Dartmouth Workshop                    | Khởi đầu AI.                                                            |
| 1966–1973  | Các cú sốc (CAC CƯ SỐC)               | Kỳ vọng cao nhưng kết quả hạn chế.                                      |
| 1974–1980  | Mùa Đông AI lần 1                    | Ngân sách cắt giảm, sự nghi ngờ.                                        |
| 1980       | Hệ chuyên gia                         | Thành tựu quan trọng cuối thời kỳ.                                      |
| 1987       | Sụp đổ Lisp                           | Thất vọng về ngôn ngữ lập trình Lisp và dự án lớn.                     |
| 2006       | Deep Learning                         | Khởi đầu mạng nơ-ron sâu.                                              |
| 2012       | AlexNet                                | Mô hình mạng nơ-ron sâu đột phá.                                       |
| 2016       | AlphaGo                                | AI đánh bại người chơi Go.                                             |
| 2017       | Transformer                            | Kiến trúc cho xử lý ngôn ngữ tự nhiên.                                 |
| 2018       | GPY-3/BERT                             | Các mô hình ngôn ngữ tiên tiến.                                         |
| 2022       | ChatGPT                                | Chatbot ngôn ngữ tự nhiên.                                              |
| 2024–2026  | Ký nguyên Agent, Hiến tái 2026         | Dự báo về Agent AGI và tiến bộ tiếp theo.                              |

---

### **Ý nghĩa bài học**:
- **Tiến bộ không tuyến tính**: AI phát triển qua các giai đoạn cao trào và thất vọng, nhưng mỗi lần phục hồi lại mạnh mẽ hơn.
- **Tầm quan trọng của dữ liệu và tính toán**: Sự phát triển mạnh mẽ của AI trong thập niên 2010–2020 nhờ vào dữ liệu lớn và sức mạnh tính toán.
- **Tương lai AI**: Dự báo về Agent AGI (Artificial General Intelligence) và các ứng dụng tiên tiến trong tương lai gần, thể hiện tầm nhìn về một kỷ nguyên mới của trí tuệ nhân tạo.
```




<!-- END PAGE 13 -->


<!-- START PAGE 14 -->

## [Trang 14]


# 1980: Hệ chuyên gia (expert system)



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 14]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Timeline Phát triển Trí tuệ Nhân tạo (AI) và Hệ chuyên gia (Expert System)**
*(Dữ liệu tập trung vào các mốc quan trọng trong lịch sử AI, đặc biệt nhấn mạnh đến hệ chuyên gia vào năm 1980)*

---

### **2. Các cột mốc / Thành phần chính**
#### **Trục X (Thời gian)**
- **1956–1993**: Giai đoạn đầu của AI, bao gồm các sự kiện quan trọng như Dartmouth Workshop (1956) và các nghiên cứu về Perceptron (1969).
- **1974–1980**: Thời kỳ "Mùa đông AI lần 1" (AI Winter 1), khi sự phát triển AI chậm lại do hạn chế kỹ thuật.
- **1980–1987**: Thời kỳ "Mùa đông AI lần 2" và sự nổi lên của hệ chuyên gia (Expert System).
- **1987–2026**: Sự phát triển mạnh mẽ của AI hiện đại, bao gồm Deep Learning, Transformer, và các mô hình ngôn ngữ hiện đại.

#### **Trục Y (Mức độ quan tâm/Phát triển)**
- Dùng để thể hiện sự nổi lên và suy giảm của các công nghệ AI qua thời gian.

#### **Các sự kiện/Box quan trọng**
- **1956**: Dartmouth Workshop – Sự kiện khai sinh AI.
- **1969**: Perceptron (Nguyên lý của mạng nơ-ron đơn giản).
- **1973**: Báo cáo Lighthill – Gây ra "Mùa đông AI lần 1".
- **1980**: **Hệ chuyên gia (Expert System)** đạt đỉnh cao.
- **1987**: Sự xuất hiện của máy Lisp (một ngôn ngữ lập trình quan trọng cho AI).
- **2006**: Deep Learning (Học sâu) được giới thiệu.
- **2012**: AlexNet – Đột phá trong học sâu với CNN.
- **2016**: AlphaGo đánh bại người chơi Go chuyên nghiệp.
- **2017**: Transformer mô hình được giới thiệu.
- **2018**: GPT-1/BERT – Mô hình ngôn ngữ tiên tiến.
- **2022**: ChatGPT – Mô hình ngôn ngữ lớn được phổ biến rộng rãi.
- **2024**: Kỳ vọng phát triển của các Agent AI.

#### **Mũi tên và chú thích**
- Mũi tên đỏ từ năm 1980 chỉ ra **Hệ chuyên gia (Expert System)** là trọng tâm của giai đoạn này.
- Các mốc thời gian được đánh dấu bằng các biểu tượng hình tròn và chữ màu xanh/ tím.

---

### **3. Số liệu & Insight quan trọng**
| **Năm**  | **Sự kiện/Công nghệ**               | **Ghi chú**                                                                 |
|----------|--------------------------------------|-----------------------------------------------------------------------------|
| 1956     | Dartmouth Workshop                   | Sự kiện khai sinh AI.                                                     |
| 1969     | Perceptron                            | Mạng nơ-ron đơn giản, gây tranh cãi về khả năng học tập.                 |
| 1973     | Báo cáo Lighthill                    | Gây ra "Mùa đông AI lần 1" do đánh giá quá cao về khả năng của AI.         |
| 1974–1980| Mùa đông AI lần 1                    | Thời kỳ chậm phát triển do hạn chế kỹ thuật và kinh phí.                  |
| 1980     | Hệ chuyên gia (Expert System)        | Đạt đỉnh cao, được ứng dụng rộng rãi trong các lĩnh vực chuyên môn.       |
| 1987     | Máy Lisp                             | Ngôn ngữ lập trình quan trọng cho AI.                                       |
| 2006     | Deep Learning                        | Khởi đầu cho sự phát triển mạnh mẽ của học sâu.                           |
| 2012     | AlexNet                               | Đột phá trong học sâu với mạng nơ-ron CNN.                                |
| 2016     | AlphaGo                               | AI đánh bại người chơi Go chuyên nghiệp.                                 |
| 2017     | Transformer                           | Mô hình mới cho xử lý ngôn ngữ tự nhiên.                                 |
| 2018     | GPT-1/BERT                            | Các mô hình ngôn ngữ tiên tiến.                                           |
| 2022     | ChatGPT                               | Mô hình ngôn ngữ lớn được phổ biến rộng rãi.                              |
| 2024     | Kỳ vọng Agent AI                     | Phát triển các hệ thống AI tự động và thông minh hơn.                     |

---

### **4. Ý nghĩa bài học**
- **Sự phát triển không đều**: AI đã trải qua nhiều giai đoạn "nóng" và "lạnh" do hạn chế kỹ thuật và kỳ vọng quá cao.
- **Hệ chuyên gia (1980)**: Là một trong những đỉnh cao quan trọng trong lịch sử AI, thể hiện khả năng ứng dụng AI trong các lĩnh vực chuyên môn.
- **Sự hồi sinh của AI hiện đại**: Từ năm 2006 trở đi, sự phát triển của Deep Learning và các mô hình ngôn ngữ lớn đã đưa AI vào một kỷ nguyên mới, với ứng dụng rộng rãi trong cuộc sống.
- **Tương lai AI**: Các mô hình như Agent AI và ChatGPT cho thấy AI đang tiến gần hơn đến việc tự động hóa và tương tác thông minh với con người.
```

---
> **Ghi chú**: Biểu đồ này tập trung vào các mốc quan trọng của AI, đặc biệt nhấn mạnh vai trò của hệ chuyên gia vào năm 1980 và sự phát triển mạnh mẽ của AI hiện đại.



Đặt lại vấn đề: 'Nếu AI chỉ giải thật tốt một loại bài toán chuyên môn hẹp thì sao?'

→ Sự ra đời của **expert systems**

AI đổi chiến lược: thôi theo đuổi trí tuệ tổng quát và **tập trung giải thật tốt một miền hẹp** bằng cách mã hóa tri thức chuyên gia thành luật


<!-- END PAGE 14 -->


<!-- START PAGE 15 -->

## [Trang 15]


## Mùa đông AI lần 2



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 15]**:
```markdown
---
### **Tên/Chủ đề sơ đồ**: Timeline Phát triển Trí tuệ Nhân tạo (AI) qua các giai đoạn và sự kiện quan trọng

---

### **Các cột mốc / Thành phần chính**:
1. **Trục thời gian (X)**:
   - Bắt đầu từ năm **1956** đến **2026** (dự báo).
   - Chia thành các giai đoạn:
     - **Các cự sốc (1966–1973)**
     - **Mùa đông lần 1 (1974–1980)**
     - **Mùa đông lần 2 (1987–1993)**
     - **Phát triển hiện đại (2006–2026)**

2. **Trục tiến triển (Y)**:
   - Dùng đường cong màu xanh để thể hiện sự phát triển và suy giảm của AI qua các thời kỳ.
   - Các đỉnh và điểm quan trọng được đánh dấu bằng các biểu tượng (chấm tròn, vuông, hình sao).

3. **Các sự kiện và công nghệ quan trọng**:
   - **1956**: Dartmouth Workshop (bắt đầu nghiên cứu AI).
   - **1969**: Perceptron (một trong những mô hình đầu tiên của học máy).
   - **1973**: Báo cáo Lighthill (gây "cự sốc" đầu tiên, dẫn đến mùa đông lần 1).
   - **1980**: Hệ chuyên gia (Expert Systems) nổi lên.
   - **1987**: Sự xuất hiện của Lisp machine (được nhấn mạnh trong hình).
   - **1993**: Mùa đông lần 2 kết thúc.
   - **2006**: Deep Learning (học sâu) xuất hiện.
   - **2012**: AlexNet (một bước đột phá trong học sâu).
   - **2016**: AlphaGo đánh bại người chơi Go chuyên nghiệp.
   - **2018**: GPT-1 và BERT (các mô hình ngôn ngữ tiên tiến).
   - **2022**: ChatGPT (mô hình ngôn ngữ lớn của OpenAI).
   - **2024**: Kỳ ngộn Agent (Agent Surprise).
   - **2026**: Dự báo hiện tại (Hiện tại 2026).

---

### **Số liệu & Insight quan trọng**:
- **Các mùa đông AI**:
  - **Mùa đông lần 1 (1974–1980)**: Do sự thất vọng từ những kỳ vọng quá cao và hạn chế kỹ thuật.
  - **Mùa đông lần 2 (1987–1993)**: Do sự suy giảm quan tâm và tài trợ sau sự sụp đổ của Lisp machine.
- **Các bước đột phá**:
  - **Deep Learning (2006)**: Khởi đầu cho sự phát triển mạnh mẽ của AI hiện đại.
  - **AlexNet (2012)**: Đột phá trong xử lý hình ảnh.
  - **AlphaGo (2016)**: Chứng minh khả năng của AI trong các trò chơi phức tạp.
  - **ChatGPT (2022)**: Mô hình ngôn ngữ lớn làm thay đổi cách tương tác giữa con người và máy tính.

---

### **Ý nghĩa bài học**:
- **Sự phát triển của AI không phải là đường thẳng**: Có những giai đoạn phát triển mạnh và những giai đoạn suy giảm do hạn chế kỹ thuật và kỳ vọng quá cao.
- **Các bước đột phá quan trọng**: Những tiến bộ như Deep Learning và các mô hình ngôn ngữ lớn đã thay đổi hoàn toàn khả năng của AI.
- **Tương lai AI**: Dự báo tiếp tục phát triển mạnh mẽ với các mô hình như Agent Surprise và các ứng dụng thực tế ngày càng tăng.
```

> **Ghi chú**: Biểu đồ này thể hiện sự phát triển không đều của AI và tầm quan trọng của các công nghệ đột phá trong việc đưa ngành này tiến lên.



Expert systems từng tạo ra giá trị thật, nhưng càng mở rộng thì càng lộ trần: tri thức phải nhập bằng tay, luật càng nhiều càng khó cập nhật, và hệ thống khó đứng vững trước ngoại lệ mới.

→ Mùa đông AI lần 2


<!-- END PAGE 15 -->


<!-- START PAGE 16 -->

## [Trang 16]


# Sự ra đời của Deep Learning



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 16]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Timeline sự phát triển của Deep Learning (Học sâu) và các cột mốc AI quan trọng**

---

### **2. Các cột mốc / Thành phần chính**
#### **Trục X (Thời gian)**
- Dải thời gian từ năm **1956** đến **2026** (dự báo).
- Được chia thành các giai đoạn:
  - **Các cự sốc (1966–1973)**
  - **Mùa đông lần 1 (1974–1980)**
  - **Mùa đông lần 2 (1987–1993)**
  - **Phát triển hiện đại (2006–2026)**

#### **Trục Y (Sự quan tâm/Phát triển)**
- Dùng đường cong để thể hiện mức độ phát triển và sự quan tâm của cộng đồng nghiên cứu.

#### **Các box và mốc thời gian quan trọng**
- **1956**: Dartmouth Workshop (bắt đầu nghiên cứu AI).
- **1969**: Perceptron (quyển sách của Rosenblatt).
- **1973**: Báo cáo Lighthill (giai đoạn "mùa đông" lần 1 bắt đầu).
- **1980**: Hệ chuyên gia (Expert Systems) nổi lên.
- **1987**: Sơ đồ Lisp machine (mùa đông lần 2).
- **2006**: Deep Learning (Học sâu) được giới thiệu lại.
- **2012**: AlexNet (thắng giải ImageNet, đánh dấu sự phát triển mạnh mẽ của Deep Learning).
- **2016**: AlphaGo đánh bại người chơi Go chuyên nghiệp.
- **2017**: Transformer (công nghệ cơ sở cho các mô hình ngôn ngữ hiện đại).
- **2018**: GPT-1/BERT (mô hình ngôn ngữ tiên tiến).
- **2022**: ChatGPT (mô hình ngôn ngữ lớn được phổ biến rộng rãi).
- **2024**: Dự báo ra mắt các Agent tự động (Autonomous Agents).
- **2026**: Dự báo tiếp tục phát triển mạnh mẽ (Hiện tại 2026).

---

### **3. Số liệu & Insight quan trọng**
- **1956–1973**: Giai đoạn đầu tiên của AI, nhưng sau đó gặp "mùa đông" do hạn chế kỹ thuật.
- **1980**: Sự nổi lên của hệ chuyên gia (Expert Systems) làm dấy lên hy vọng mới.
- **1987–1993**: Mùa đông lần 2 do hạn chế về máy tính và thuật toán.
- **2006**: Deep Learning được giới thiệu lại, đánh dấu sự khởi đầu của thời đại hiện đại.
- **2012**: AlexNet đánh dấu bước đột phá trong xử lý hình ảnh.
- **2016–2018**: AlphaGo và GPT-1/BERT chứng minh khả năng của AI trong các lĩnh vực phức tạp.
- **2022–2026**: Sự phát triển nhanh chóng của các mô hình ngôn ngữ lớn và các Agent tự động.

---

### **4. Ý nghĩa bài học**
- **Sự phát triển của AI không phải là đường thẳng**, mà có những giai đoạn "mùa đông" do hạn chế kỹ thuật và nguồn lực.
- **Deep Learning (2006–nay)** là một bước đột phá quan trọng nhờ vào sự tiến bộ của máy tính và thuật toán.
- **Tương lai của AI** dự báo sẽ tiếp tục phát triển mạnh mẽ với các ứng dụng tự động và thông minh hơn, như các Agent tự động (2024) và các mô hình ngôn ngữ tiên tiến (2026).
```

> **Ghi chú**: Biểu đồ này thể hiện rõ sự phát triển không đều và các cột mốc quan trọng trong lịch sử AI, đặc biệt nhấn mạnh vai trò của Deep Learning trong thời kỳ hiện đại.



Sau mùa đông lần hai, câu hỏi của cả ngành đổi hẳn:
"Nếu không thể viết hết trí thức thế giới vào máy, thì có thể để máy tự học nó từ dữ liệu không?"


<!-- END PAGE 16 -->


<!-- START PAGE 17 -->

## [Trang 17]


## 2009: Fei-Fei Li và ImageNet — cuộc cách mạng của dữ liệu



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 17]**:
```markdown
### 1. **Tên/Chủ đề sơ đồ**:
Biểu đồ Timeline về sự phát triển của trí tuệ nhân tạo (AI) và các cột mốc quan trọng trong lĩnh vực xử lý và nhận diện hình ảnh, đặc biệt tập trung vào vai trò của Fei-Fei Li và ImageNet.

---

### **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026 (dự báo).
- **Trục Y (Mức độ quan tâm/phát triển)**: Dùng đường cong để thể hiện sự nổi lên và suy giảm của các lĩnh vực nghiên cứu.

#### **Các giai đoạn và sự kiện chính**:
- **1956**: Dartmouth Workshop (bắt đầu nghiên cứu AI).
- **1966-1973**: Các cự số (Các cuộc thi theo dõi thuật toán thông minh hòn).
- **1969**: Perceptron (một mô hình AI sớm).
- **1973**: Báo cáo Lighthill (sự thất vọng về AI).
- **1980**: Hệ chuyên gia (Expert Systems) nổi lên.
- **1987**: Sụp đổ của Lisp machine (sự suy giảm).
- **1993-2006**: Thời kỳ "đồi thẳm" (AI winter).
- **2006**: Deep Learning xuất hiện.
- **2012**: AlexNet (sử dụng ImageNet) và sự bùng nổ của học sâu (Deep Learning).
- **2016**: AlphaGo đánh bại người chơi cờ vây chuyên nghiệp.
- **2017**: Transformer mô hình được giới thiệu.
- **2018**: GPT-1/BERT (mô hình ngôn ngữ).
- **2022**: ChatGPT xuất hiện.
- **2024**: Ký nguyên Agent (Agent Revolution).
- **2026 (dự báo)**: Hiện tại (tương lai gần).

#### **Vai trò của Fei-Fei Li và ImageNet**:
- Năm 2009, Fei-Fei Li và nhóm của cô xây dựng bộ dữ liệu ImageNet với 14 triệu ảnh, bao gồm hơn 20.000 loại vật thể.
- Năm 2012, ImageNet được sử dụng trong cuộc thi AlexNet, đánh dấu bước ngoặt trong học sâu và nhận diện hình ảnh.

---

### **Số liệu & Insight quan trọng**:
- **Năm 2009**: ImageNet được xây dựng với 14 triệu ảnh và 20.000 loại vật thể.
- **Năm 2012**: Cuộc thi AlexNet sử dụng ImageNet, dẫn đến bùng nổ học sâu.
- **Năm 2016**: AlphaGo đánh bại người chơi cờ vây chuyên nghiệp.
- **Năm 2017**: Xuất hiện mô hình Transformer.
- **Năm 2018**: GPT-1 và BERT được giới thiệu.
- **Năm 2022**: ChatGPT ra đời.
- **Dự báo 2024-2026**: Kỷ nguyên Agent và các tiến bộ tiếp theo trong AI.

---

### **Ý nghĩa bài học**:
1. **Tầm quan trọng của dữ liệu**: Sự phát triển của AI phụ thuộc rất lớn vào sự có mặt của bộ dữ liệu chất lượng cao như ImageNet.
2. **Cuộc thi và cộng đồng**: Các cuộc thi như AlexNet đã thúc đẩy sự cạnh tranh và tiến bộ nhanh chóng trong lĩnh vực học sâu.
3. **Sự tuần hoàn của sự quan tâm**: AI thường trải qua các chu kỳ nổi và suy giảm, nhưng mỗi lần bùng nổ đều mang lại những tiến bộ vượt bậc.
4. **Tương lai AI**: Sự phát triển của các mô hình như Transformer và Agent sẽ tiếp tục mở ra nhiều khả năng mới trong tương lai gần.
```




<!-- END PAGE 17 -->


<!-- START PAGE 18 -->

## [Trang 18]


# Deep Learning khác Machine Learning truyền thống ở chỗ nào?

## Machine Learning



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 18]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Quy trình phân loại hình ảnh trong học máy (Object Classification - Car Detection)**

---

### **2. Các cột mốc / Thành phần chính**
- **Input (Đầu vào)**
  - Hình ảnh đầu vào (ví dụ: ảnh một chiếc xe ô tô).

- **Feature Extraction (Trích xuất đặc trưng)**
  - Bước chuyển đổi hình ảnh thành dữ liệu số (tính năng) để mô hình có thể xử lý.
  - Được thể hiện bằng biểu tượng người ngồi trước máy tính (tương tự quá trình phân tích đặc trưng bằng thuật toán).

- **Classification (Phân loại)**
  - Mạng nơ-ron (neural network) xử lý dữ liệu đặc trưng.
  - Các nút (nodes) và kết nối (edges) biểu thị các lớp (layers) và quá trình tính toán trong mạng nơ-ron.

- **Output (Đầu ra)**
  - Kết quả phân loại: "Car" (Xe ô tô) hoặc "Not Car" (Không phải xe ô tô).

---

### **3. Số liệu & Insight quan trọng**
- **Công nghệ**: Sử dụng mạng nơ-ron (neural network) để phân loại hình ảnh.
- **Bước xử lý**: Input → Trích xuất đặc trưng → Phân loại → Output.
- **Ví dụ ứng dụng**: Phân biệt đối tượng trong hình ảnh (Car vs. Not Car).

---

### **4. Ý nghĩa bài học**
Sơ đồ minh họa một quy trình cơ bản trong **học máy (Machine Learning)** và **học sâu (Deep Learning)** để phân loại hình ảnh. Bước đầu tiên là trích xuất đặc trưng từ dữ liệu đầu vào, sau đó sử dụng mô hình mạng nơ-ron để phân loại và đưa ra kết quả. Đây là cơ sở cho nhiều ứng dụng như nhận diện đối tượng, tự động lái xe, và hệ thống an ninh camera.
---
```



## Deep Learning



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 18]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Quy trình phân loại hình ảnh trong học máy (Object Classification - Car Detection)**

---

### **2. Các cột mốc / Thành phần chính**
- **Input (Đầu vào)**
  - Hình ảnh đầu vào (ví dụ: ảnh một chiếc xe ô tô).

- **Feature Extraction (Trích xuất đặc trưng)**
  - Bước chuyển đổi hình ảnh thành dữ liệu số (tính năng) để mô hình có thể xử lý.
  - Được thể hiện bằng biểu tượng người ngồi trước máy tính (tương tự quá trình phân tích đặc trưng bằng thuật toán).

- **Classification (Phân loại)**
  - Mạng nơ-ron (neural network) xử lý dữ liệu đặc trưng.
  - Các nút (nodes) và kết nối (edges) biểu thị các lớp (layers) và quá trình tính toán trong mạng nơ-ron.

- **Output (Đầu ra)**
  - Kết quả phân loại: "Car" (Xe ô tô) hoặc "Not Car" (Không phải xe ô tô).

---

### **3. Số liệu & Insight quan trọng**
- **Công nghệ**: Sử dụng mạng nơ-ron (neural network) để phân loại hình ảnh.
- **Bước xử lý**: Input → Trích xuất đặc trưng → Phân loại → Output.
- **Ví dụ ứng dụng**: Phân biệt đối tượng trong hình ảnh (Car vs. Not Car).

---

### **4. Ý nghĩa bài học**
Sơ đồ minh họa một quy trình cơ bản trong **học máy (Machine Learning)** và **học sâu (Deep Learning)** để phân loại hình ảnh. Bước đầu tiên là trích xuất đặc trưng từ dữ liệu đầu vào, sau đó sử dụng mô hình mạng nơ-ron để phân loại và đưa ra kết quả. Đây là cơ sở cho nhiều ứng dụng như nhận diện đối tượng, tự động lái xe, và hệ thống an ninh camera.
---
```



Không cần con người thiết kế đặc trưng bằng tay — mạng sâu TỰ học đặc trưng từ dữ liệu thô, từ đơn giản đến phức tạp


<!-- END PAGE 18 -->


<!-- START PAGE 19 -->

## [Trang 19]


# 2012: AlexNet



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 19]**:
```markdown
### 1. Tên/Chủ đề sơ đồ:
**Timeline phát triển nghệ thuật/phong trào văn học Việt Nam (1956–1974)**

---

### 2. Các cột mốc / Thành phần chính:
- **Trục X**: Thời gian (1956 → 1974), chia làm 2 giai đoạn:
  - **Các Cụ Sóc (1966–1973)**
  - **Mùa Đông Lần 1 (1974–1980)** *(giai đoạn này chỉ được nhắc đến một phần)*
- **Trục Y**: Sự kiện văn học/nghệ thuật quan trọng (không rõ đơn vị đo lường, nhưng thể hiện sự phát triển qua thời gian).

#### Các điểm mốc chính:
1. **Dartmouth Workshop (1956)**
   - Điểm xuất phát (mốc 1), thể hiện sự khởi đầu của phong trào văn học/nghệ thuật hiện đại.
2. **Báo cáo Lighthouse (LightHill) (1973)**
   - Điểm trung gian (mốc 2), đánh dấu sự chuyển tiếp quan trọng.
3. **Perceptron (1969)**
   - Sự kiện/phát minh liên quan đến nghệ thuật hoặc công nghệ (mốc 3).
4. **Hệ chữ (1974)**
   - Điểm kết thúc (mốc 4), thể hiện kết quả cuối cùng của giai đoạn này.

---
### 3. Số liệu & Insight quan trọng:
- **Thời gian chính xác**:
  - **1956**: Dartmouth Workshop (bắt đầu).
  - **1966–1973**: Giai đoạn **Các Cụ Sóc**.
  - **1969**: Sự kiện **Perceptron** (có thể liên quan đến nghệ thuật kỹ thuật số hoặc trí tuệ nhân tạo).
  - **1973**: Báo cáo **LightHill**.
  - **1974**: Hệ chữ (mốc kết thúc).
- **Tên công nghệ/sự kiện**:
  - Dartmouth Workshop, Perceptron, LightHill, Hệ chữ.

---
### 4. Ý nghĩa bài học:
Biểu đồ thể hiện **quá trình phát triển của một phong trào văn học/nghệ thuật Việt Nam từ năm 1956 đến 1974**, với các mốc quan trọng như Dartmouth Workshop và sự kiện Perceptron (1969) đóng vai trò là những bước ngoặt. Giai đoạn **Các Cụ Sóc (1966–1973)** và **Mùa Đông Lần 1 (1974–1980)** cho thấy sự chuyển tiếp từ khái niệm đến thực hiện, thể hiện sự kết hợp giữa truyền thống và hiện đại trong nghệ thuật. Biểu đồ có thể được sử dụng để phân tích **tiến trình sáng tạo và ảnh hưởng của các sự kiện lịch sử** trong văn học nghệ thuật Việt Nam.
```

---
> **Ghi chú**: Nếu đây là một biểu đồ về **phong trào nghệ thuật** (chứ không phải khoa học máy tính), thì các thuật ngữ như *Perceptron* và *LightHill* có thể là tên các tác phẩm, nhóm nghệ sĩ hoặc sự kiện văn hóa. Nếu có thêm ngữ cảnh chi tiết, có thể phân tích sâu hơn.





> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 19]**:
```markdown
### 1. Tên/Chủ đề sơ đồ:
**Timeline phát triển nghệ thuật/phong trào văn học Việt Nam (1956–1974)**

---

### 2. Các cột mốc / Thành phần chính:
- **Trục X**: Thời gian (1956 → 1974), chia làm 2 giai đoạn:
  - **Các Cụ Sóc (1966–1973)**
  - **Mùa Đông Lần 1 (1974–1980)** *(giai đoạn này chỉ được nhắc đến một phần)*
- **Trục Y**: Sự kiện văn học/nghệ thuật quan trọng (không rõ đơn vị đo lường, nhưng thể hiện sự phát triển qua thời gian).

#### Các điểm mốc chính:
1. **Dartmouth Workshop (1956)**
   - Điểm xuất phát (mốc 1), thể hiện sự khởi đầu của phong trào văn học/nghệ thuật hiện đại.
2. **Báo cáo Lighthouse (LightHill) (1973)**
   - Điểm trung gian (mốc 2), đánh dấu sự chuyển tiếp quan trọng.
3. **Perceptron (1969)**
   - Sự kiện/phát minh liên quan đến nghệ thuật hoặc công nghệ (mốc 3).
4. **Hệ chữ (1974)**
   - Điểm kết thúc (mốc 4), thể hiện kết quả cuối cùng của giai đoạn này.

---
### 3. Số liệu & Insight quan trọng:
- **Thời gian chính xác**:
  - **1956**: Dartmouth Workshop (bắt đầu).
  - **1966–1973**: Giai đoạn **Các Cụ Sóc**.
  - **1969**: Sự kiện **Perceptron** (có thể liên quan đến nghệ thuật kỹ thuật số hoặc trí tuệ nhân tạo).
  - **1973**: Báo cáo **LightHill**.
  - **1974**: Hệ chữ (mốc kết thúc).
- **Tên công nghệ/sự kiện**:
  - Dartmouth Workshop, Perceptron, LightHill, Hệ chữ.

---
### 4. Ý nghĩa bài học:
Biểu đồ thể hiện **quá trình phát triển của một phong trào văn học/nghệ thuật Việt Nam từ năm 1956 đến 1974**, với các mốc quan trọng như Dartmouth Workshop và sự kiện Perceptron (1969) đóng vai trò là những bước ngoặt. Giai đoạn **Các Cụ Sóc (1966–1973)** và **Mùa Đông Lần 1 (1974–1980)** cho thấy sự chuyển tiếp từ khái niệm đến thực hiện, thể hiện sự kết hợp giữa truyền thống và hiện đại trong nghệ thuật. Biểu đồ có thể được sử dụng để phân tích **tiến trình sáng tạo và ảnh hưởng của các sự kiện lịch sử** trong văn học nghệ thuật Việt Nam.
```

---
> **Ghi chú**: Nếu đây là một biểu đồ về **phong trào nghệ thuật** (chứ không phải khoa học máy tính), thì các thuật ngữ như *Perceptron* và *LightHill* có thể là tên các tác phẩm, nhóm nghệ sĩ hoặc sự kiện văn hóa. Nếu có thêm ngữ cảnh chi tiết, có thể phân tích sâu hơn.





> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 19]**:
```markdown
### 1. Tên/Chủ đề sơ đồ:
**Timeline phát triển nghệ thuật/phong trào văn học Việt Nam (1956–1974)**

---

### 2. Các cột mốc / Thành phần chính:
- **Trục X**: Thời gian (1956 → 1974), chia làm 2 giai đoạn:
  - **Các Cụ Sóc (1966–1973)**
  - **Mùa Đông Lần 1 (1974–1980)** *(giai đoạn này chỉ được nhắc đến một phần)*
- **Trục Y**: Sự kiện văn học/nghệ thuật quan trọng (không rõ đơn vị đo lường, nhưng thể hiện sự phát triển qua thời gian).

#### Các điểm mốc chính:
1. **Dartmouth Workshop (1956)**
   - Điểm xuất phát (mốc 1), thể hiện sự khởi đầu của phong trào văn học/nghệ thuật hiện đại.
2. **Báo cáo Lighthouse (LightHill) (1973)**
   - Điểm trung gian (mốc 2), đánh dấu sự chuyển tiếp quan trọng.
3. **Perceptron (1969)**
   - Sự kiện/phát minh liên quan đến nghệ thuật hoặc công nghệ (mốc 3).
4. **Hệ chữ (1974)**
   - Điểm kết thúc (mốc 4), thể hiện kết quả cuối cùng của giai đoạn này.

---
### 3. Số liệu & Insight quan trọng:
- **Thời gian chính xác**:
  - **1956**: Dartmouth Workshop (bắt đầu).
  - **1966–1973**: Giai đoạn **Các Cụ Sóc**.
  - **1969**: Sự kiện **Perceptron** (có thể liên quan đến nghệ thuật kỹ thuật số hoặc trí tuệ nhân tạo).
  - **1973**: Báo cáo **LightHill**.
  - **1974**: Hệ chữ (mốc kết thúc).
- **Tên công nghệ/sự kiện**:
  - Dartmouth Workshop, Perceptron, LightHill, Hệ chữ.

---
### 4. Ý nghĩa bài học:
Biểu đồ thể hiện **quá trình phát triển của một phong trào văn học/nghệ thuật Việt Nam từ năm 1956 đến 1974**, với các mốc quan trọng như Dartmouth Workshop và sự kiện Perceptron (1969) đóng vai trò là những bước ngoặt. Giai đoạn **Các Cụ Sóc (1966–1973)** và **Mùa Đông Lần 1 (1974–1980)** cho thấy sự chuyển tiếp từ khái niệm đến thực hiện, thể hiện sự kết hợp giữa truyền thống và hiện đại trong nghệ thuật. Biểu đồ có thể được sử dụng để phân tích **tiến trình sáng tạo và ảnh hưởng của các sự kiện lịch sử** trong văn học nghệ thuật Việt Nam.
```

---
> **Ghi chú**: Nếu đây là một biểu đồ về **phong trào nghệ thuật** (chứ không phải khoa học máy tính), thì các thuật ngữ như *Perceptron* và *LightHill* có thể là tên các tác phẩm, nhóm nghệ sĩ hoặc sự kiện văn hóa. Nếu có thêm ngữ cảnh chi tiết, có thể phân tích sâu hơn.



## ImageNet: **AlexNet chiến thắng ở ImageNet Large Scale Visual Recognition Challenge**



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 19]**:
```markdown
### 1. Tên/Chủ đề sơ đồ:
**Timeline phát triển nghệ thuật/phong trào văn học Việt Nam (1956–1974)**

---

### 2. Các cột mốc / Thành phần chính:
- **Trục X**: Thời gian (1956 → 1974), chia làm 2 giai đoạn:
  - **Các Cụ Sóc (1966–1973)**
  - **Mùa Đông Lần 1 (1974–1980)** *(giai đoạn này chỉ được nhắc đến một phần)*
- **Trục Y**: Sự kiện văn học/nghệ thuật quan trọng (không rõ đơn vị đo lường, nhưng thể hiện sự phát triển qua thời gian).

#### Các điểm mốc chính:
1. **Dartmouth Workshop (1956)**
   - Điểm xuất phát (mốc 1), thể hiện sự khởi đầu của phong trào văn học/nghệ thuật hiện đại.
2. **Báo cáo Lighthouse (LightHill) (1973)**
   - Điểm trung gian (mốc 2), đánh dấu sự chuyển tiếp quan trọng.
3. **Perceptron (1969)**
   - Sự kiện/phát minh liên quan đến nghệ thuật hoặc công nghệ (mốc 3).
4. **Hệ chữ (1974)**
   - Điểm kết thúc (mốc 4), thể hiện kết quả cuối cùng của giai đoạn này.

---
### 3. Số liệu & Insight quan trọng:
- **Thời gian chính xác**:
  - **1956**: Dartmouth Workshop (bắt đầu).
  - **1966–1973**: Giai đoạn **Các Cụ Sóc**.
  - **1969**: Sự kiện **Perceptron** (có thể liên quan đến nghệ thuật kỹ thuật số hoặc trí tuệ nhân tạo).
  - **1973**: Báo cáo **LightHill**.
  - **1974**: Hệ chữ (mốc kết thúc).
- **Tên công nghệ/sự kiện**:
  - Dartmouth Workshop, Perceptron, LightHill, Hệ chữ.

---
### 4. Ý nghĩa bài học:
Biểu đồ thể hiện **quá trình phát triển của một phong trào văn học/nghệ thuật Việt Nam từ năm 1956 đến 1974**, với các mốc quan trọng như Dartmouth Workshop và sự kiện Perceptron (1969) đóng vai trò là những bước ngoặt. Giai đoạn **Các Cụ Sóc (1966–1973)** và **Mùa Đông Lần 1 (1974–1980)** cho thấy sự chuyển tiếp từ khái niệm đến thực hiện, thể hiện sự kết hợp giữa truyền thống và hiện đại trong nghệ thuật. Biểu đồ có thể được sử dụng để phân tích **tiến trình sáng tạo và ảnh hưởng của các sự kiện lịch sử** trong văn học nghệ thuật Việt Nam.
```

---
> **Ghi chú**: Nếu đây là một biểu đồ về **phong trào nghệ thuật** (chứ không phải khoa học máy tính), thì các thuật ngữ như *Perceptron* và *LightHill* có thể là tên các tác phẩm, nhóm nghệ sĩ hoặc sự kiện văn hóa. Nếu có thêm ngữ cảnh chi tiết, có thể phân tích sâu hơn.



- **ImageNet** cho mô hình ăn một lượng dữ liệu chưa từng có ở thời điểm đó.
- **Kiến trúc sâu** cho phép học dần từ cạnh, hình, bộ phận, rồi đến đối tượng.
- **GPU** cung cấp đủ năng lực tính toán để quá trình huấn luyện trở nên khả thi.


<!-- END PAGE 19 -->


<!-- START PAGE 20 -->

## [Trang 20]


# 2016: AlphaGo



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 20]**:
```markdown
> 🖼️ *[Hình ảnh minh họa / Trận đấu Go giữa AlphaGo và Lee Sedol]*

---
### **Mô tả chi tiết**
- **Tên/Chủ đề**: Trận đấu Go giữa **AlphaGo (AI)** và **Lee Sedol** (người chơi chuyên nghiệp hàng đầu thế giới).
- **Thành phần chính**:
  - **Hai bên tham gia**:
    - Bên trái: AI AlphaGo (do DeepMind phát triển, thuộc Alphabet/Google).
    - Bên phải: Lee Sedol (cầu thủ Go chuyên nghiệp người Hàn Quốc, 9p).
  - **Bàn cờ Go**: Bàn cờ truyền thống 19x19 ô.
  - **Bối cảnh**: Trận đấu diễn ra trong sự kiện lịch sử năm **2016**, đánh dấu lần đầu tiên AI đánh bại người chơi hàng đầu trong môn Go.
  - **Logo/Thương hiệu**: Nhãn hiệu AlphaGo và quốc kỳ Anh (UK) + Hàn Quốc (KR) được thể hiện.

- **Số liệu & Insight quan trọng**:
  - **Năm**: 2016 (tháng 3).
  - **Kết quả**: AlphaGo thắng **4 trận** (trong 5 trận đấu), bao gồm chiến thắng quyết định ở trận thứ 4.
  - **Ý nghĩa**: Đánh dấu bước ngoặt trong trí tuệ nhân tạo, chứng minh khả năng của AI trong giải quyết các vấn đề phức tạp đòi hỏi sự sáng tạo và chiến lược cao.

- **Ý nghĩa bài học**:
  - Thể hiện sức mạnh của **học máy (Machine Learning)** và **Deep Learning** trong các lĩnh vực đòi hỏi trí tuệ cao.
  - Khẳng định khả năng của AI trong việc vượt qua con người trong các trò chơi chiến lược phức tạp.
  - Động lực cho nghiên cứu và phát triển trí tuệ nhân tạo trong tương lai.
```

---
> **Ghi chú**: Ảnh không chứa thông tin văn bản hoặc mã nguồn có thể trích xuất, chỉ là hình minh họa cho sự kiện lịch sử.





> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 20]**:
```markdown
> 🖼️ *[Hình ảnh minh họa / Trận đấu Go giữa AlphaGo và Lee Sedol]*

---
### **Mô tả chi tiết**
- **Tên/Chủ đề**: Trận đấu Go giữa **AlphaGo (AI)** và **Lee Sedol** (người chơi chuyên nghiệp hàng đầu thế giới).
- **Thành phần chính**:
  - **Hai bên tham gia**:
    - Bên trái: AI AlphaGo (do DeepMind phát triển, thuộc Alphabet/Google).
    - Bên phải: Lee Sedol (cầu thủ Go chuyên nghiệp người Hàn Quốc, 9p).
  - **Bàn cờ Go**: Bàn cờ truyền thống 19x19 ô.
  - **Bối cảnh**: Trận đấu diễn ra trong sự kiện lịch sử năm **2016**, đánh dấu lần đầu tiên AI đánh bại người chơi hàng đầu trong môn Go.
  - **Logo/Thương hiệu**: Nhãn hiệu AlphaGo và quốc kỳ Anh (UK) + Hàn Quốc (KR) được thể hiện.

- **Số liệu & Insight quan trọng**:
  - **Năm**: 2016 (tháng 3).
  - **Kết quả**: AlphaGo thắng **4 trận** (trong 5 trận đấu), bao gồm chiến thắng quyết định ở trận thứ 4.
  - **Ý nghĩa**: Đánh dấu bước ngoặt trong trí tuệ nhân tạo, chứng minh khả năng của AI trong giải quyết các vấn đề phức tạp đòi hỏi sự sáng tạo và chiến lược cao.

- **Ý nghĩa bài học**:
  - Thể hiện sức mạnh của **học máy (Machine Learning)** và **Deep Learning** trong các lĩnh vực đòi hỏi trí tuệ cao.
  - Khẳng định khả năng của AI trong việc vượt qua con người trong các trò chơi chiến lược phức tạp.
  - Động lực cho nghiên cứu và phát triển trí tuệ nhân tạo trong tương lai.
```

---
> **Ghi chú**: Ảnh không chứa thông tin văn bản hoặc mã nguồn có thể trích xuất, chỉ là hình minh họa cho sự kiện lịch sử.



## AlphaGo và nước đi số 37

Ban đầu nó học từ khoảng 150.000 ván cờ của chuyên gia con người để có trực giác khởi đầu

→ Tạo ra nhiều bản sao của AlphaGo và để chúng **tự chơi với chính mình** hàng triệu lần

→ Hệ thống không chỉ học từ những gì con người đã biết, mà còn **tự mở rộng không gian chiến lược** bằng cách **khám phá những nước đi chưa từng được thử** trước đó.


<!-- END PAGE 20 -->


<!-- START PAGE 21 -->

## [Trang 21]


# Nút thắt của RNN: đọc hết rồi mới nói — từng bước một



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 21]**:
1. **Tên/Chủ đề sơ đồ**:
   Sơ đồ mô tả quá trình chuyển đổi từ **dòng chữ tiếng Trung sang vector "ý cầu"** và sinh từ một (decoder) để tạo ra câu tiếng Anh tương ứng.

---

2. **Các cột mốc / Thành phần chính**:
   - **Trục X (Input)**:
     - Các ký tự tiếng Trung: 知识就是力量 (zhīshi jiùshì lìliàng).
     - Các ký tự được đánh số từ (1) đến (6): 知 (1), 识 (2), 就 (3), 是 (4), 力 (5), 量 (6).
   - **Vector "ý cầu"**:
     - Dòng chữ được mã hóa thành **một vector** đại diện cho ý nghĩa tổng thể của câu.
   - **Decoder (Sinh từ một)**:
     - Chuyển đổi vector "ý cầu" thành câu tiếng Anh tương ứng: "Knowledge is power".
     - Các từ được đánh số (1) đến (3): Knowledge (1), is (2), power (3).
   - **Ghi chú**:
     - "nên cả câu vào MỘT vector" (mã hóa toàn bộ câu thành một vector).
     - "1 vector 'ý cầu'" (vector này đại diện cho ý nghĩa của câu).
     - "CÓ CHAI" (có nghĩa là quá trình này có thể bị giới hạn về độ dài hoặc số lượng từ).

---

3. **Số liệu & Insight quan trọng**:
   - Số lượng ký tự tiếng Trung: 6 ký tự.
   - Số lượng từ tiếng Anh output: 3 từ.
   - Công nghệ liên quan: Mã hóa câu thành vector (thường liên quan đến NLP, mô hình ngôn ngữ như BERT, Word2Vec, hoặc các mô hình transformer).
   - Khái niệm: Sinh từ một (decoder) để tạo ra câu tiếng Anh từ vector.

---

4. **Ý nghĩa bài học**:
   Sơ đồ minh họa quá trình chuyển đổi văn bản từ một ngôn ngữ sang ngôn ngữ khác thông qua việc mã hóa ý nghĩa của câu thành một vector trung gian. Điều này thể hiện cách các mô hình ngôn ngữ hiện đại (NLP) sử dụng vector để hiểu và sinh ra văn bản, đồng thời nhấn mạnh vào việc chuyển đổi ý nghĩa thay vì chỉ chuyển đổi từ một cách trực tiếp. Quá trình này là cơ sở cho các hệ thống dịch máy và sinh văn bản tự động.



## ① Câu càng dài → càng quên chữ đầu

Hôm qua tôi đi chợ
mua được một con cá to

chữ đầu "mở" dẫn trong vector duy nhất — như người cố nhớ một câu rất dài bằng trí nhớ ngắn hạn

## ② Từng bước một → chậm, khó mở rộng

1 → 2 → 3 → ... → 100

muốn chữ thứ 100 phải chờ đủ 99 bước trước — không song song được, khó scale lên model lớn

**Transformer thẳng không phải vì phép màu — nó tháo đúng nút thắt này: cho mọi từ nhìn nhau cùng lúc**

Sutskever et al. (2014), "Sequence to Sequence Learning with Neural Networks" — Wu et al. (2016), Google Neural Machine Translation — arxiv.org/abs/1609.08144


<!-- END PAGE 21 -->


<!-- START PAGE 22 -->

## [Trang 22]


# 2017: Transformer



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 22]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Timeline Phát triển Trí tuệ Nhân tạo (AI) và Kỹ thuật Học máy (Machine Learning)**
*(Tập trung vào các cột mốc quan trọng từ năm 1956 đến 2026)*

---

### **2. Các cột mốc / Thành phần chính**
#### **Trục X (Thời gian)**
- Duyệt theo chiều từ trái sang phải: **1956 → 2026**.

#### **Trục Y (Phát triển công nghệ)**
- **Dartmouth Workshop (1956)**: Sự kiện khai sinh khái niệm AI.
- **Báo cáo Lighthill (1969)**: Phê phán và đánh giá lại tiến độ AI.
- **Hệ chuyên gia (Expert Systems) (1980)**: Giai đoạn phát triển các chương trình mô phỏng logic chuyên gia.
- **Sự xuất hiện của Sơ đồ Lisp Machine (1987)**: Máy tính chuyên dụng cho ngôn ngữ Lisp.
- **CAC CƯ SỞC (1960–1973) và MUA ĐỔNG LẦN 1 (1974–1980)**: Các dự án nghiên cứu AI tại Việt Nam.
- **Deep Learning (2006)**: Khởi đầu của mạng nơ-ron sâu.
- **AlphaGo (2016)**: Thắng máy tính chuyên nghiệp trong cờ vây.
- **Transformer (2017)**: Kiến trúc mạng nơ-ron thay đổi game trong xử lý ngôn ngữ tự nhiên.
- **GPT-1/BERT (2018)**: Mô hình ngôn ngữ tiền huấn luyện.
- **ChatGPT (2022)**: Ứng dụng thương mại hóa của mô hình ngôn ngữ.
- **GPT-4 / Kỳ Nguyên Agent (2024–2026)**: Dự đoán tương lai của AI.

#### **Các box và mũi tên**
- **Mũi tên màu xanh lá cây**: Diễn tả sự phát triển của AI truyền thống (Expert Systems, Lisp Machine).
- **Mũi tên màu xám**: Diễn tả sự suy giảm và đánh giá lại trong các giai đoạn.
- **Mũi tên màu đỏ (Transformer, 2017)**: Đánh dấu sự bùng nổ của mô hình học sâu hiện đại.
- **Mũi tên màu tím (ChatGPT, 2022)**: Phát triển ứng dụng thực tế của AI.
- **Các tên tác giả và tổ chức**:
  - **Google Brain, Google Research, DeepMind, OpenAI** và các nhà nghiên cứu như **Ashish Vaswani, Noam Shazeer, Illia Polosukhin**.

---

### **3. Số liệu & Insight quan trọng**
| **Năm**   | **Công nghệ / Sự kiện**               | **Chi tiết**                                                                 |
|------------|----------------------------------------|------------------------------------------------------------------------------|
| 1956       | Dartmouth Workshop                    | Sự kiện khai sinh AI.                                                      |
| 1969       | Báo cáo Lighthill                     | Phê phán quá cao về khả năng AI.                                           |
| 1980       | Hệ chuyên gia                         | Giai đoạn phát triển các chương trình mô phỏng logic chuyên gia.            |
| 1987       | Sơ đồ Lisp Machine                     | Máy tính chuyên dụng cho ngôn ngữ Lisp.                                    |
| 2006       | Deep Learning                         | Khởi đầu của mạng nơ-ron sâu.                                             |
| 2016       | AlphaGo                                | Thắng máy tính chuyên nghiệp trong cờ vây.                                 |
| 2017       | Transformer                            | Kiến trúc mạng nơ-ron thay đổi game trong xử lý ngôn ngữ tự nhiên.         |
| 2018       | GPT-1/BERT                             | Mô hình ngôn ngữ tiền huấn luyện.                                         |
| 2022       | ChatGPT                                | Ứng dụng thương mại hóa của mô hình ngôn ngữ.                              |
| 2024–2026  | GPT-4 / Kỳ Nguyên Agent               | Dự đoán tương lai của AI.                                                  |

---

### **4. Ý nghĩa bài học**
- **Sự phát triển không đều**: AI đã trải qua các giai đoạn bùng nổ và suy thoái, đặc biệt là trước và sau năm 1980.
- **Nền tảng công nghệ quyết định**: Sự xuất hiện của Transformer (2017) và Deep Learning (2006) đã mở ra kỷ nguyên mới cho AI.
- **Tương lai AI**: Dự đoán về các mô hình như GPT-4 và Kỳ Nguyên Agent cho thấy sự phát triển mạnh mẽ trong tương lai gần, đặc biệt trong lĩnh vực xử lý ngôn ngữ tự nhiên và trí tuệ nhân tạo tổng quát.
```

> **Ghi chú**: Biểu đồ này tập trung vào các cột mốc quan trọng trong lịch sử AI, đặc biệt nhấn mạnh đến sự phát triển của các mô hình học sâu hiện đại và các dự đoán tương lai.



**Transformer** là bước ngoặt vì nó cho mô hình hiểu ngôn ngữ theo cách linh hoạt hơn: **mỗi từ có thể nhìn sang những từ quan trọng khác** trong cả câu, thay vì chỉ đi tuần tự từng bước → trở thành nền móng kỹ thuật cho GPT, BERT và toàn bộ làn sóng LLM sau đó.


<!-- END PAGE 22 -->


<!-- START PAGE 23 -->

## [Trang 23]


# 2022: ChatGPT



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 23]**:
```markdown
---
### 1. **Tên/Chủ đề sơ đồ**: Timeline Phát triển Trí tuệ Nhân tạo (AI) và các công nghệ NLP chính
---

### 2. **Các cột mốc / Thành phần chính**:
- **Trục X (Thời gian)**: Từ năm 1956 đến 2026, chia thành các giai đoạn:
  - **1956–1973**: Các cự soc (Dartmouth Workshop, Perceptron)
  - **1974–1980**: Mùa đông lần 1 (AI Winter 1)
  - **1980–1987**: Hệ chuyên gia (Expert Systems)
  - **1987–1993**: Mùa đông lần 2 (AI Winter 2)
  - **1993–2006**: Sự phát triển của các công nghệ cơ sở (Lisp Machine, Deep Learning)
  - **2006–2026**: Phát triển mạnh mẽ của AI hiện đại (Deep Learning, Transformer, ChatGPT)

- **Trục Y (Sự phát triển)**: Dùng đường cong để thể hiện sự nổi lên và suy giảm của các xu hướng AI qua các thời kỳ.

- **Các box và mốc thời gian quan trọng**:
  - **1956**: Dartmouth Workshop (bắt đầu AI)
  - **1969**: Perceptron (mạng nơ-ron đầu tiên)
  - **1973**: Báo cáo Lighthill (bắt đầu mùa đông AI lần 1)
  - **1980**: Hệ chuyên gia (Expert Systems)
  - **1987**: Sụp đổ của Lisp Machine (bắt đầu mùa đông AI lần 2)
  - **2006**: Deep Learning (sự trở lại của AI)
  - **2012**: AlexNet (một bước đột phá trong học sâu)
  - **2016**: AlphaGo (thắng người chơi Go)
  - **2017**: Transformer (công nghệ nền tảng cho NLP hiện đại)
  - **2018**: GPT-1/BERT (mô hình ngôn ngữ lớn)
  - **2022**: ChatGPT (ứng dụng thực tế của mô hình ngôn ngữ)
  - **2024**: Kỳ ngộ Agent (Agent AI)
  - **2026**: Hiện tại dự đoán (tương lai của AI)

---

### 3. **Số liệu & Insight quan trọng**:
- **Mốc thời gian chính**:
  - **1956**: Dartmouth Workshop (sự ra đời của AI)
  - **1973**: Báo cáo Lighthill đánh dấu mùa đông AI lần 1
  - **1980**: Hệ chuyên gia đạt đỉnh cao
  - **1987**: Sụp đổ của Lisp Machine, bắt đầu mùa đông AI lần 2
  - **2006**: Deep Learning trở lại với sức mạnh mới
  - **2012**: AlexNet đánh dấu bước phát triển của học sâu
  - **2016**: AlphaGo đánh bại người chơi Go chuyên nghiệp
  - **2017**: Transformer xuất hiện, trở thành nền tảng cho các mô hình ngôn ngữ hiện đại
  - **2018**: GPT-1 và BERT được giới thiệu
  - **2022**: ChatGPT được phát hành, mở ra kỷ nguyên ứng dụng AI thực tế
  - **2024**: Dự đoán sự ra đời của các Agent AI
  - **2026**: Dự đoán tiếp tục phát triển của AI

---

### 4. **Ý nghĩa bài học**:
- **Sự phát triển của AI không phải là đường thẳng**: Có những giai đoạn phát triển mạnh (như hệ chuyên gia và hiện tại) và những giai đoạn suy giảm (mùa đông AI).
- **Công nghệ là nền tảng**: Các bước tiến như Perceptron, Deep Learning, và Transformer đã tạo ra những bước nhảy vọt quan trọng.
- **Tương lai AI**: Dự đoán tiếp tục phát triển với các ứng dụng thực tế và các Agent AI, mở ra nhiều khả năng mới trong tương lai.

---
```



## ChatGPT xuất hiện như một trải nghiệm đại chúng

Lần đầu tiên rất đông người dùng phổ thông có thể trực tiếp chạm vào một mô hình ngôn ngữ mạnh, thông qua một giao diện đơn giản đến mức ai cũng hiểu cách dùng


<!-- END PAGE 23 -->


<!-- START PAGE 24 -->

## [Trang 24]




> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 24]**:
```markdown
---
# **1. Biểu đồ Evolutionary Tree của các mô hình ngôn ngữ lớn (LLMs)**
**Tên/Chủ đề sơ đồ**: *Biểu đồ phát triển tiến hóa các mô hình ngôn ngữ AI (2018–2024)*
**Loại**: Timeline + Sơ đồ cây phả hệ công nghệ AI

---

## **Các cột mốc / Thành phần chính**

### **Trục thời gian (2018–2024)**
- **2018**: BERT (Google), ELMo (Allen AI), GPT-1 (OpenAI)
- **2019**: RoBERTa, ALBERT, XLNet, GPT-2
- **2020**: ELECTRA, DeBERTa, T5, UniLM, GPT-3
- **2021**: Switch-C, FLAN, MT-NLG, Codex, GPT-Neo, Gopher (DeepMind)
- **2022**: Chinchilla, PaLM (Google), LaMDA, GPT-3.5, LLaMA (Meta), Claude (Anthropic)
- **2023**: GPT-4, Llama 2, Claude 2, Gemini (Google), Durasstic-2 (Mistral AI)
- **2024**: GPT-4o (OpenAI), các mô hình mới nhất (tên chưa đầy đủ trong ảnh)

### **Các nhánh chính trong sơ đồ**
1. **Nhánh GPT (OpenAI)**
   - GPT-1 → GPT-2 → GPT-3 → GPT-3.5 → GPT-4 → GPT-4o
   - Các biến thể: GPT-Neo, GPT-J

2. **Nhánh Google (PaLM/LaMDA)**
   - BERT → T5 → PaLM → LaMDA → Gemini

3. **Nhánh Meta (LLaMA)**
   - LLaMA → Llama 2

4. **Nhánh DeepMind**
   - Gopher → Sparrow → Chinchilla

5. **Nhánh Anthropic**
   - Claude → Claude 2

6. **Nhánh Mistral AI**
   - Durasstic-2

7. **Nhánh các mô hình mở khác**
   - FLAN, MT-NLG, Codex, Bloom, OPT, Galactica, StableLM, Ai2

### **Phân biệt Open-Source vs Closed-Source**
- **Open-Source** (Màu xanh nhạt + biểu tượng QR code):
  - LLaMA, LLaMA 2, OPT, Bloom, StableLM, FLAN, T5, BERT, RoBERTa, ...
- **Closed-Source** (Màu xám + biểu tượng khóa):
  - GPT-3/3.5/4, Claude, PaLM, LaMDA, Gemini, Durasstic-2, ...

---

## **Số liệu & Insight quan trọng**
| **Năm** | **Sự kiện công nghệ**                     | **Kích thước mô hình** (nếu có)       |
|----------|--------------------------------------------|----------------------------------------|
| 2018     | GPT-1 (OpenAI)                             | 117M tham số                          |
| 2019     | GPT-2                                      | 1.5B tham số                          |
| 2020     | GPT-3                                      | 175B tham số                          |
| 2021     | GPT-3.5, Codex                             | 175B → 1.3T (Codex)                   |
| 2022     | GPT-4 (phi công bố chính thức), LLaMA     | 7B–65B (LLaMA), GPT-4 >1T tham số      |
| 2023     | GPT-4, Claude 2, Gemini, Llama 2           | Llama 2: 7B–70B                       |
| 2024     | GPT-4o, Durasstic-2                        | Chưa rõ (tương lai)                   |

- **Mô hình lớn nhất**: GPT-4 (OpenAI), Gemini (Google)
- **Mô hình mở nguồn nổi bật**: LLaMA (Meta), Bloom (BigScience), StableLM (Stability AI)
- **Trends**:
  - Tăng tốc độ phát triển từ 2020–2024.
  - Sự cạnh tranh giữa các công ty lớn (OpenAI, Google, Meta, Anthropic).
  - Xu hướng mở nguồn (Open-Source) tăng mạnh từ 2021.

---

## **Ý nghĩa bài học**
1. **Phát triển nhanh chóng**: Công nghệ mô hình ngôn ngữ AI tiến hóa với tốc độ chóng mặt, từ mô hình 117M tham số (2018) lên hàng nghìn tỷ tham số (2023–2024).
2. **Cạnh tranh công nghệ**: Các tập đoàn lớn (Google, Meta, OpenAI) đẩy mạnh nghiên cứu, dẫn đến sự đa dạng hóa mô hình (Closed-Source vs Open-Source).
3. **Tầm quan trọng của Open-Source**: Các mô hình mở nguồn như LLaMA, Bloom tạo cơ hội cho cộng đồng nghiên cứu và ứng dụng linh hoạt hơn.
4. **Thách thức ứng dụng**: Sự phát triển nhanh chóng cũng đặt ra câu hỏi về đạo đức, an ninh và khả năng kiểm soát công nghệ AI.

---
> **Ghi chú**: Biểu đồ này phản ánh xu hướng phát triển của AI trong 6 năm qua, giúp học viên hiểu rõ bối cảnh và nguồn gốc của các mô hình hiện đại.
```

---
> **Lưu ý**: Do ảnh không thể trích xuất 100% nội dung chữ (như phần chú thích ở góc dưới), nên nội dung đã được tổng hợp dựa trên các thành phần chính của sơ đồ.



ChatGPT xuất hiện,
chứng minh hiệu quả →
trong tâm của toàn ngành
bắt đầu dồn về cùng một
trục

Trước khi ChatGPT bùng nổ, nghiên cứu mô hình
ngôn ngữ phân thành rất nhiều nhánh


<!-- END PAGE 24 -->


<!-- START PAGE 25 -->

## [Trang 25]


PHẦN 03

# Bên trong LLM

*từ vòng lặp đoán token đến giới hạn của model*


<!-- END PAGE 25 -->


<!-- START PAGE 26 -->

## [Trang 26]


# Bên trong LLM — bản đồ 5 chặng của buổi sáng

Cỗ máy đoán token

LLM là gì · xác suất · vòng lặp · token · context



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 26]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ liên kết các nút (Nodes) theo kiểu mạng lưới (Network Graph)
---

### **Các cột mốc / Thành phần chính**:
- **Các nút (Nodes)**:
  - `3A` (màu xanh nhạt)
  - `3B` (màu xanh dương)
  - `3C` (màu tím)
  - `3D` (màu nâu)
  - `3E` (màu xanh lá cây)

- **Các liên kết (Edges)**:
  - Mũi tên **đường nét đứt xanh nhạt** kết nối các nút theo thứ tự:
    `3A → 3B → 3C → 3D → 3E`.
  - Mũi tên **đường nét đứt xanh nhạt** từ `3E` trỏ về phía một biểu tượng mũi tên màu xanh nhạt (có thể biểu thị vòng lặp hoặc hướng tiếp theo).

---

### **Số liệu & Insight quan trọng**:
- **Số lượng nút**: 5 (3A, 3B, 3C, 3D, 3E).
- **Số lượng liên kết**: 4 (liên kết tuyến tính) + 1 (liên kết vòng lặp).
- **Kiểu biểu diễn**: Sơ đồ mạng lưới (Network Graph) với các nút và mũi tên hướng dẫn.

---

### **Ý nghĩa bài học**:
Sơ đồ này thể hiện một **quy trình tuyến tính có hướng**, có thể đại diện cho:
1. Một chuỗi các bước trong một quá trình (ví dụ: quy trình sản xuất, luồng dữ liệu, hoặc các giai đoạn trong một dự án).
2. Một mạng lưới liên kết giữa các thành phần (ví dụ: các node trong một hệ thống phân tán, các trạng thái trong một máy trạng thái hữu hạn).
3. Một mô hình đơn giản để minh họa **quy trình tuần tự** hoặc **quy trình có vòng lặp** (như mũi tên cuối cùng từ `3E`).

---
```



Attention

cách model nhìn ngữ cảnh · multi-head · ứng dụng

Model được tạo ra

tham số · training · RLHF

Model có “hiểu” không?

tranh luận · thí nghiệm Othello-GPT

Giới hạn & sống chung

cutoff · hallucination · học vẹt · cách chạm vào

Nếu giữa đường thấy lạc — quay lại bản đồ này. Mỗi chặng chỉ có một câu chốt duy nhất.

Thần chú xuyên suốt: “Model chỉ đoán token tiếp theo — mọi thứ khác là hệ quả.”


<!-- END PAGE 26 -->


<!-- START PAGE 27 -->

## [Trang 27]


# LLM là gì? — một bộ não nền, không phải một chatbot

**LLM (Large Language Model)** là một mô hình ngôn ngữ rất lớn, thường dựa trên kiến trúc Transformer, được luyện trên hàng nghìn tỷ mảnh chữ để học cách **đoán mảnh chữ tiếp theo trong ngữ cảnh**.

Nhờ được luyện đủ rộng, nó trở thành một **nền chung**: thay vì mỗi việc train một model riêng, cùng một model làm được rất nhiều việc.

Chatbot chỉ là **một dạng sản phẩm** đóng gói quanh bộ não đó — lớp áo bên ngoài.



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 27]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình phát triển ứng dụng sử dụng mô hình ngôn ngữ lớn (LLM)

---
**Các cột mốc / Thành phần chính**:
- **1 model nên (LLM)**: Thành phần trung tâm, đại diện cho mô hình ngôn ngữ lớn (Large Language Model).
  - Các thành phần phụ liên quan:
    - **Chatbot**: Ứng dụng cuối cùng tương tác với người dùng thông qua giao diện trò chuyện.
    - **Tóm tắt tài liệu**: Chức năng sử dụng LLM để tổng hợp hoặc tóm lược nội dung tài liệu.
    - **Viết code**: Sử dụng LLM để hỗ trợ viết mã nguồn.
    - **Dịch & phân tích**: Sử dụng LLM để dịch văn bản hoặc phân tích dữ liệu.

---
**Số liệu & Insight quan trọng**:
- Không có số liệu cụ thể trong sơ đồ, nhưng mô tả quy trình sử dụng **một mô hình LLM** làm nền tảng để xây dựng nhiều ứng dụng khác nhau (chatbot, tóm tắt tài liệu, viết code, dịch và phân tích).

---
**Ý nghĩa bài học**:
Sơ đồ này thể hiện cách một mô hình ngôn ngữ lớn (LLM) có thể được tái sử dụng và tùy biến để xây dựng nhiều ứng dụng thực tế khác nhau, từ tương tác người máy (chatbot) đến công cụ hỗ trợ lập trình và xử lý ngôn ngữ tự nhiên (dịch, phân tích). Điều này nhấn mạnh tầm quan trọng của mô hình LLM như một nền tảng linh hoạt trong phát triển phần mềm và ứng dụng trí tuệ nhân tạo.
---
```



LLM = bộ não ngôn ngữ dùng chung cho mọi việc — sản phẩm bạn thấy chỉ là lớp áo bên ngoài

Model hiện nay chủ yếu là kiến trúc decoder-only (GPT, Claude, Gemini, Kimi), nhiều model dùng MoE; sau pre-training còn các bước cần chỉnh (SFT, RLHF/DPO) và luyện suy luận (reasoning training, từ ~2025).


<!-- END PAGE 27 -->


<!-- START PAGE 28 -->

## [Trang 28]


## Bên trong Transformer: đầu ra luôn là một phân bố xác suất



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 28]**:
```markdown
### 1. **Tên/Chủ đề sơ đồ**
Sơ đồ minh họa quá trình xử lý ngôn ngữ tự nhiên (NLP) với mô hình Transformer và phân tích khả năng sinh từ liên quan đến "pi" trong ngữ cảnh hài hước/giáo dục.

---

### **Các cột mốc / Thành phần chính**
- **Hình ảnh bên trái**:
  - Một con vật hoang dã (được gọi là "pi creature") đứng trên biểu tượng số π (pi) và một đồ thị âm thanh.
  - Mô tả: "Behold, a wild pi creature, foraging in its native ___" (Hãy ngắm nhìn một sinh vật hoang dã pi, đang kiếm ăn trong môi trường sống bản địa của nó).
  - Biểu tượng π được nhấn mạnh với công thức \(2\pi e\).

- **Mũi tên và mô hình Transformer**:
  - Dữ liệu từ câu văn trên được đưa vào mô hình Transformer để dự đoán từ thích hợp điền vào chỗ trống.

- **Bảng thống kê từ khóa dự đoán (tỉ lệ xác suất)**:
  - Danh sách các từ khóa cùng với xác suất dự đoán (từ cao đến thấp):
    - `land` (22%)
    - `forest` (9%)
    - `country` (5%)
    - `habitat`, `forests`, `soil` (4% mỗi từ)
    - `territory`, `woods` (2% mỗi từ)
    - `lands`, `waters`, `woodland`, `grass` (1% mỗi từ).

---

### **Số liệu & Insight quan trọng**
- Từ có xác suất dự đoán cao nhất: **"land"** (22%).
- Các từ liên quan đến môi trường sống tự nhiên như `forest`, `habitat`, `soil` có xác suất cao.
- Mô hình Transformer được sử dụng để dự đoán từ trong câu văn dựa trên ngữ cảnh.

---

### **Ý nghĩa bài học**
Sơ đồ này minh họa cách mô hình Transformer hoạt động trong việc dự đoán từ dựa trên ngữ cảnh trong câu. Nó thể hiện ứng dụng của NLP trong việc phân tích và sinh từ tự nhiên, đồng thời tạo ra một ví dụ hài hước bằng cách kết hợp toán học (số π) với sinh vật ảo. Bài học này giúp người học hiểu cách mô hình AI xử lý và dự đoán từ trong văn bản một cách logic và có xác suất.
```



Với mọi ngữ cảnh, model chấm điểm **MỌI** từ trong từ vựng — “land” 22%, “forest” 9%... — rồi chọn theo xác suất đó

Transformers, the tech behind LLMs - 3Blue1Brown


<!-- END PAGE 28 -->


<!-- START PAGE 29 -->

## [Trang 29]


# Sinh văn bản = đoán → nối vào câu → đoán tiếp

If you could see the underlying probability distributions a large language model uses when generating text, then you



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 29]**:
Dưới đây là nội dung được trích xuất từ ảnh dưới dạng fenced code block (bảng biểu):

```markdown
| you | lex |
|-----|-----|
| it  | 10  |
| yes | 15  |
| what | 18 |
| I   | 18  |
| that | 10 |
| there | 10 |
| this | 10  |
| percentage | 10 |
| they | 10  |
```

---
**Ghi chú**:
- Bảng này thể hiện sự tương ứng giữa hai cột `you` và `lex`, với các giá trị số ở cột `lex`.
- Nếu đây là một phần của dữ liệu thống kê, có thể liên quan đến tần suất xuất hiện từ vựng hoặc điểm số trong một ngữ cảnh cụ thể (ví dụ: từ vựng trong bài học tiếng Anh).



If you could see the underlying probability distributions a large language model uses when generating text, then you would



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 29]**:
Dưới đây là nội dung được trích xuất từ ảnh dưới dạng fenced code block (bảng biểu):

```markdown
| you | lex |
|-----|-----|
| it  | 10  |
| yes | 15  |
| what | 18 |
| I   | 18  |
| that | 10 |
| there | 10 |
| this | 10  |
| percentage | 10 |
| they | 10  |
```

---
**Ghi chú**:
- Bảng này thể hiện sự tương ứng giữa hai cột `you` và `lex`, với các giá trị số ở cột `lex`.
- Nếu đây là một phần của dữ liệu thống kê, có thể liên quan đến tần suất xuất hiện từ vựng hoặc điểm số trong một ngữ cảnh cụ thể (ví dụ: từ vựng trong bài học tiếng Anh).



If you could see the underlying probability distributions a large language model uses when generating text, then you would essentially



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 29]**:
Dưới đây là nội dung được trích xuất từ ảnh dưới dạng fenced code block (bảng biểu):

```markdown
| you | lex |
|-----|-----|
| it  | 10  |
| yes | 15  |
| what | 18 |
| I   | 18  |
| that | 10 |
| there | 10 |
| this | 10  |
| percentage | 10 |
| they | 10  |
```

---
**Ghi chú**:
- Bảng này thể hiện sự tương ứng giữa hai cột `you` và `lex`, với các giá trị số ở cột `lex`.
- Nếu đây là một phần của dữ liệu thống kê, có thể liên quan đến tần suất xuất hiện từ vựng hoặc điểm số trong một ngữ cảnh cụ thể (ví dụ: từ vựng trong bài học tiếng Anh).



Mỗi token mới được nối vào ngữ cảnh, rồi model chạy lại từ đầu — vòng lặp predict → append → rerun

Transformers, the tech behind LLMs - 3Blue1Brown


<!-- END PAGE 29 -->


<!-- START PAGE 30 -->

## [Trang 30]


# Token: model không đọc "từ", model đọc mảnh chữ

Model không nhìn từ nguyên vẹn. Nó cắt văn bản thành các **mảnh nhỏ gọi là token**: có từ là một mảnh, có từ vỡ ba bốn mảnh, cả dấu câu và khoảng trắng cũng là mảnh.

Ví dụ: "*Hello world*" ≈ 2 token, nhưng "*Xin chào*" có thể tới 3–4 token.

**Tiếng Việt, code, JSON tốn token hơn** tiếng Anh thường — vì dấu thanh, ký tự đặc biệt và cấu trúc bị cắt nhỏ ra.

Độ dài câu **XẬP XÍ** nhau (9 vs 10 từ) nhưng **tokenizer GPT** cắt Tiếng Việt vẹn hơn hẳn: 1.9 token/từ so với 1.2 token/từ

Tiếng Anh: "To date, the cleverest thinker of all time was" → 9 từ → 11 token

|  To | _date | , | _the | _clever | est | _thinker | let | all | _time | _was  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Tiếng Việt: "Lan bỏ quyền sách vào túi vì nó quá dày" → 10 từ → 19 token

|  L | an | đã | ó | au | y | do | _dách | _vào | _tôi | l | u | l | u | ó | au | á | đó | ây  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Để tạo thành token, tokenizer GPT, token 3.0, token 2.0, token 1.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0, token 0.0

Mọi thứ model làm đều quy ra token — và **mỗi token đều có giá**. Nhớ điều này khi sang phần chi phí.

Thứ trực tiếp: platform.openai.com/tokenizer - Số token chính xác phụ thuộc tokenizer của từng model.


<!-- END PAGE 30 -->


<!-- START PAGE 31 -->

## [Trang 31]


# Context: bàn làm việc có hạn của model

Mỗi lần trả lời, model chỉ nhìn được một lượng chữ có hạn — gọi là **context**. Hãy hình dung một **bàn làm việc**: mọi thứ muốn model "thấy" phải bày lên bàn.

Quy đổi: 128K token ≈ một cuốn sách 300 trang; 1M token ≈ 4–5 cuốn sách trên bàn cùng lúc.

Bàn đầy quá thì đồ ở **giữa bàn dễ bị bỏ sót** — đặt điều quan trọng ở giữa một prompt rất dài, model có thể "quên" mất.

Vì sao "nhất" thật nhiều vào prompt không phải lúc nào cũng tốt



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 31]**:
Dưới đây là phân tích và chuyển đổi nội dung từ bức ảnh theo yêu cầu:

---
### **1. Tên/Chủ đề sơ đồ**:
**"Context window – Mô hình bản vị việc CO HAN"**
*(Sơ đồ mô tả cách phân chia và xử lý "context window" trong mô hình CO HAN, có liên quan đến xử lý ngôn ngữ hoặc xử lý văn bản theo các đoạn nhỏ.)*

---

### **2. Các cột mốc / Thành phần chính**:
- **Cấu trúc**: Sơ đồ chia thành **4 box** (khối) màu xanh, sắp xếp theo chiều ngang, mỗi box đại diện cho một "context window" riêng biệt.
  - **Box 1**: Ghi chữ **"A"** (có thể là một đoạn văn bản hoặc token đầu tiên).
  - **Box 2**: Ghi chữ **"B"** (tiếp theo).
  - **Box 3**: Ghi chữ **"C"** (tiếp tục).
  - **Box 4**: Ghi chữ **"D"** (cuối cùng).
- **Mũi tên và liên kết**:
  - Các box được nối tiếp nhau theo thứ tự từ trái sang phải, thể hiện sự liên tục của "context window".
  - Dưới hình, có chú thích bằng tiếng Việt:
    > *"Một MẶT CỬA SỐ (context window) = một đoạn văn bản ngắn để mô hình có thể xử lý được"*
    > *"Đoạn văn bản dài sẽ được chia thành nhiều context window để xử lý"*

---

### **3. Số liệu & Insight quan trọng**:
- **Khái niệm chính**:
  - **Context window**: Đoạn văn bản ngắn mà mô hình xử lý được một lần (đơn vị nhỏ nhất).
  - **Quy trình chia đoạn**: Văn bản dài được phân chia thành nhiều "context window" để xử lý hiệu quả.
- **Tên mô hình**: **CO HAN** (có thể là tên một mô hình xử lý ngôn ngữ hoặc hệ thống AI).

---

### **4. Ý nghĩa bài học**:
- Sơ đồ giải thích cách mô hình AI xử lý văn bản dài bằng cách chia nhỏ thành các "context window" (đoạn ngắn), giúp mô hình có thể phân tích và hiểu được từng phần một cách hiệu quả.
- Khái niệm này quan trọng trong các ứng dụng như chatbot, dịch thuật hoặc phân tích văn bản, nơi cần xử lý lượng dữ liệu lớn.
- Mô hình **CO HAN** có thể áp dụng phương pháp này để cải thiện hiệu suất xử lý văn bản dài.

---
> **Ghi chú**: Nếu đây là một phần của bài giảng về xử lý ngôn ngữ tự nhiên (NLP), thì nội dung liên quan đến cách mô hình AI chia nhỏ dữ liệu đầu vào để xử lý.





> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 31]**:
Dưới đây là phân tích và chuyển đổi nội dung từ bức ảnh theo yêu cầu:

---
### **1. Tên/Chủ đề sơ đồ**:
**"Context window – Mô hình bản vị việc CO HAN"**
*(Sơ đồ mô tả cách phân chia và xử lý "context window" trong mô hình CO HAN, có liên quan đến xử lý ngôn ngữ hoặc xử lý văn bản theo các đoạn nhỏ.)*

---

### **2. Các cột mốc / Thành phần chính**:
- **Cấu trúc**: Sơ đồ chia thành **4 box** (khối) màu xanh, sắp xếp theo chiều ngang, mỗi box đại diện cho một "context window" riêng biệt.
  - **Box 1**: Ghi chữ **"A"** (có thể là một đoạn văn bản hoặc token đầu tiên).
  - **Box 2**: Ghi chữ **"B"** (tiếp theo).
  - **Box 3**: Ghi chữ **"C"** (tiếp tục).
  - **Box 4**: Ghi chữ **"D"** (cuối cùng).
- **Mũi tên và liên kết**:
  - Các box được nối tiếp nhau theo thứ tự từ trái sang phải, thể hiện sự liên tục của "context window".
  - Dưới hình, có chú thích bằng tiếng Việt:
    > *"Một MẶT CỬA SỐ (context window) = một đoạn văn bản ngắn để mô hình có thể xử lý được"*
    > *"Đoạn văn bản dài sẽ được chia thành nhiều context window để xử lý"*

---

### **3. Số liệu & Insight quan trọng**:
- **Khái niệm chính**:
  - **Context window**: Đoạn văn bản ngắn mà mô hình xử lý được một lần (đơn vị nhỏ nhất).
  - **Quy trình chia đoạn**: Văn bản dài được phân chia thành nhiều "context window" để xử lý hiệu quả.
- **Tên mô hình**: **CO HAN** (có thể là tên một mô hình xử lý ngôn ngữ hoặc hệ thống AI).

---

### **4. Ý nghĩa bài học**:
- Sơ đồ giải thích cách mô hình AI xử lý văn bản dài bằng cách chia nhỏ thành các "context window" (đoạn ngắn), giúp mô hình có thể phân tích và hiểu được từng phần một cách hiệu quả.
- Khái niệm này quan trọng trong các ứng dụng như chatbot, dịch thuật hoặc phân tích văn bản, nơi cần xử lý lượng dữ liệu lớn.
- Mô hình **CO HAN** có thể áp dụng phương pháp này để cải thiện hiệu suất xử lý văn bản dài.

---
> **Ghi chú**: Nếu đây là một phần của bài giảng về xử lý ngôn ngữ tự nhiên (NLP), thì nội dung liên quan đến cách mô hình AI chia nhỏ dữ liệu đầu vào để xử lý.



Context càng dài càng tốn tiền và càng chậm — bàn rộng không có nghĩa là dùng tốt


<!-- END PAGE 31 -->


<!-- START PAGE 32 -->

## [Trang 32]


## Attention: mỗi từ được “nhìn sang” những từ quan trọng khác

Thay vì đọc tuần tự từng chữ, cơ chế **attention** cho phép mỗi token:

- **Chủ động “quay đầu”** nhìn lại các token trước đó trong câu
- **Chấm điểm mức độ liên quan** của từng token đối với nghĩa của mình
- **Khóa nghĩa theo ngữ cảnh** — “nó” là quyển sách hay cái túi, tùy theo nó chú ý vào từ nào

*Đây chính là chữ T trong GPT — và là lý do model hiểu ngữ cảnh tốt hơn hẳn các thế hệ trước*

Video minh họa: **Attention in transformers, step-by-step - 3Blue1Brown**


<!-- END PAGE 32 -->


<!-- START PAGE 33 -->

## [Trang 33]


## Minh họa khái niệm: token "nó" cần "chú ý" (attention) tới token nào để hiểu đúng nghĩa?



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 33]**:
```markdown
---
1. **Tên/Chủ đề sơ đồ**: Biểu đồ liên kết từ (Word Association Graph) giữa các từ trong tiếng Việt
   - **Loại biểu đồ**: Sơ đồ mạng từ (Word Association Network) với trọng số tương quan.

---
2. **Các cột mốc / Thành phần chính**:
   - **Các từ khóa chính** (trục X):
     Lan → bồ → **quyền** → sách → vào → **túi** → vì → **nó** → quả → dậy
   - **Mũi tên liên kết**:
     - Màu đỏ (trọng số cao): quyền ↔ sách (0.32), sách ↔ nó (0.28)
     - Màu vàng (trọng số trung bình): túi ↔ vì (0.10)
     - Màu xám (trọng số thấp): Lan ↔ bồ (0.05), vào ↔ túi (0.06), vì ↔ nó (0.08)
   - **Trọng số** (được hiển thị trên mũi tên): Giá trị số thập phân thể hiện mức độ liên kết giữa các từ.

---
3. **Số liệu & Insight quan trọng**:
   - **Trọng số cao nhất**: quyền ↔ sách (**0.32**)
   - **Trọng số thứ hai**: sách ↔ nó (**0.28**)
   - **Trọng số thấp nhất**: Lan ↔ bồ (**0.05**), vì ↔ nó (**0.08**)

---
4. **Ý nghĩa bài học**:
   - Biểu đồ thể hiện mối quan hệ tương quan giữa các từ trong một ngữ cảnh cụ thể, với trọng số càng cao thì liên kết càng mạnh.
   - Có thể ứng dụng trong phân tích ngôn ngữ tự nhiên (NLP) để hiểu cách các từ liên kết với nhau trong văn bản.
   - Giúp nhận diện từ khóa chính và mối quan hệ ngữ nghĩa trong bài học tiếng Việt hoặc phân tích văn bản.
---
```
> **Ghi chú**: Nếu đây là một phần của bài giảng về xử lý ngôn ngữ tự nhiên (NLP), biểu đồ này có thể minh họa cho khái niệm về **tương quan từ (word association)** hoặc **ma trận tương tự từ (word similarity matrix)**.



"Lan bỏ quyển sách vào túi vì nó quá dày" — muốn biết "nó" = quyển sách hay cái túi, mô hình so khớp "nó" với TẤT CẢ token trước đó, không chỉ token liền kề. Cung càng dày/đậm = trọng số attention càng cao (ở đây: hướng mạnh về "quyển"+"sách", không phải "túi").


<!-- END PAGE 33 -->


<!-- START PAGE 34 -->

## [Trang 34]


# Nhìn lân cận hay nhìn toàn cảnh?

Convolution — cửa sổ nhỏ quanh mỗi từ



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 34]**:
Dưới đây là phân tích và chuyển đổi nội dung trong ảnh theo định dạng Markdown:

---
### **2. Ảnh chụp chữ (Trích xuất nội dung)**
Nội dung chữ trong ảnh được trích xuất và sắp xếp theo cấu trúc từ vựng:

```markdown
# Danh sách từ vựng (cấu số = 3 tự)

- Lan
- bồ
- quyến
- sách
- vào
---
**Nhóm từ có cấu số 3 tự:**
- túi
- vì
- nó
```

---
### **Số liệu & Insight quan trọng**
- **Cấu số = 3 tự**: Chỉ nhóm từ có **3 âm tiết** (túi, vì, nó).
- **Từ loại**: Danh từ, động từ (ví dụ: *lan, bồ, quyến sách, vào* là từ đơn/động từ, trong khi *túi, vì, nó* là từ có cấu trúc 3 âm tiết).

---
> **Ghi chú**: Nếu đây là ví dụ về **phân tích cấu trúc âm tiết trong tiếng Việt**, có thể liên quan đến bài học về **phân loại từ vựng theo số âm tiết** hoặc **ngữ âm học**.



“nó” muốn hiểu nghĩa thì phải nhìn tới “quyển/sách” — nhưng chúng nằm ngoài cửa sổ → mối liên hệ xa bị cắt.

Attention — mọi từ đều trong tầm nhìn



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 34]**:
Dưới đây là phân tích và chuyển đổi nội dung trong ảnh theo định dạng Markdown:

---
### **2. Ảnh chụp chữ (Trích xuất nội dung)**
Nội dung chữ trong ảnh được trích xuất và sắp xếp theo cấu trúc từ vựng:

```markdown
# Danh sách từ vựng (cấu số = 3 tự)

- Lan
- bồ
- quyến
- sách
- vào
---
**Nhóm từ có cấu số 3 tự:**
- túi
- vì
- nó
```

---
### **Số liệu & Insight quan trọng**
- **Cấu số = 3 tự**: Chỉ nhóm từ có **3 âm tiết** (túi, vì, nó).
- **Từ loại**: Danh từ, động từ (ví dụ: *lan, bồ, quyến sách, vào* là từ đơn/động từ, trong khi *túi, vì, nó* là từ có cấu trúc 3 âm tiết).

---
> **Ghi chú**: Nếu đây là ví dụ về **phân tích cấu trúc âm tiết trong tiếng Việt**, có thể liên quan đến bài học về **phân loại từ vựng theo số âm tiết** hoặc **ngữ âm học**.



“nó” nhìn lại toàn bộ câu và tự chọn từ quan trọng — nét đậm ở “quyển”, “sách” nghĩa là chủ ý mạnh vào đó.

Cửa sổ nhỏ thì nhanh nhưng mù xa — attention đổi tốc độ lấy khả năng giữ ngữ cảnh dài, và đó là bước ngoặt


<!-- END PAGE 34 -->


<!-- START PAGE 35 -->

## [Trang 35]


# Multi-head: cùng một câu, nhiều con mắt chuyên môn nhìn song song

Attention không chỉ có một "con mắt". Model có **nhiều con mắt chuyên môn** nhìn cùng một câu một lúc:

- ● **Con mắt đại từ** — lo việc "nó" là con mèo hay cái bàn.
- ● **Con mắt không gian** — lo việc cái gì nằm trên cái gì.
- ● **Con mắt cú pháp** — lo nhịp câu, dấu câu, khoảng cách.

Mỗi con mắt nhìn một khía cạnh, rồi model **tổng hợp lại** thành hiểu biết đầy đủ hơn về câu.

**Multi-Head Attention** - Thay vì chỉ học một kiểu quan hệ duy nhất, Multi-Head Attention tách attention thành nhiều head song song. Mỗi head học một góc nhìn khác nhau của câu. Các kết quả này sau đó được **concat** và đi qua **linear projection** để tạo ra biểu diễn cuối cùng giữa thông tin hơn.



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 35]**:
Dưới đây là phân tích và chuyển đổi nội dung trong ảnh theo định dạng Markdown:

---
### **1. Tên/Chủ đề sơ đồ**
**Sơ đồ kiến trúc mạng neuron cho việc dự đoán/phân loại từ các đầu vào "Con mèo trên bàn, Nèo..."**
*(Dựa trên mô tả các Head khác nhau trong mô hình xử lý ngôn ngữ/ảnh)*

---

### **2. Các cột mốc / Thành phần chính**
- **Input (Đầu vào):**
  - `Con mèo trên bàn, Nèo...` (Dữ liệu đầu vào dạng văn bản/ảnh)

- **Head 1: Chuyển dạng Đại từ**
  - **Mô tả:** Chuyển đổi đại từ trong câu (ví dụ: thay thế "Nèo" thành "chó/con mèo").
  - **Kết quả:** Dữ liệu được chuẩn hóa về dạng chuẩn (Normalized).

- **Head 2: Chuyển dạng Không gian**
  - **Mô tả:** Xử lý thông tin vị trí không gian (từ khóa: "trên bàn, Nèo").
  - **Kết quả:** Dữ liệu được chuyển về dạng vector không gian (Spatial Vector).

- **Head 3: Chuyển dạng Cú pháp**
  - **Mô tả:** Xử lý cấu trúc cú pháp câu (chủ ngữ, động từ, tân ngữ).
  - **Kết quả:** Dữ liệu được chuyển về dạng vector cú pháp (Syntax Vector).

- **Linear Projection (W^p):**
  - **Mô tả:** Tiến hành dự phóng tuyến tính (Linear Projection) để kết hợp các đầu ra từ 3 Head thành một vector chung.

- **Concat (Kết hợp):**
  - **Mô tả:** Kết hợp các đầu ra từ 3 Head trước khi đưa vào Linear Projection.

---

### **3. Số liệu & Insight quan trọng**
- **Các Head riêng biệt:** 3 Head chuyên biệt (Đại từ, Không gian, Cú pháp).
- **Kỹ thuật:** Sử dụng **Linear Projection** để chuyển đổi và kết hợp các vector.
- **Mục tiêu:** Xử lý và chuyển đổi dữ liệu đầu vào thành các dạng vector phù hợp cho việc phân tích sâu hơn.

---

### **4. Ý nghĩa bài học**
Sơ đồ minh họa một kiến trúc xử lý ngôn ngữ/ảnh đa đầu (multi-head) để chuyển đổi dữ liệu thô thành các dạng vector có cấu trúc. Mỗi Head tập trung vào một khía cạnh cụ thể (đại từ, không gian, cú pháp), sau đó kết hợp thông tin để tạo ra một biểu diễn toàn diện. Đây là một phương pháp phổ biến trong các mô hình học máy và xử lý ngôn ngữ tự nhiên (NLP), đặc biệt là trong việc phân tích câu hoặc nhận diện đối tượng trong ảnh kết hợp với ngữ cảnh văn bản.

---
> **Ghi chú:** Nếu đây là một phần của mô hình NLP/Computer Vision, có thể liên quan đến kiến trúc như **Transformer** hoặc **Multi-modal Processing**.



Một con mắt nhìn được một góc — nhiều con mắt cùng nhìn mới thành "hiểu ngữ cảnh"

Multi-head attention — Vaswani et al. (2017) — arxiv.org/abs/1706.03762


<!-- END PAGE 35 -->


<!-- START PAGE 36 -->

## [Trang 36]


# Hiểu attention để dùng AI hiệu quả: quản context = quản sự chú ý

Attention có hạn và có 'điểm mù'. Vì vậy, cách bạn bày context quyết định model chú ý vào đâu:

## 1 Đặt điều quan trọng đầu – cuối

Đầu và cuối prompt được chú ý nhiều nhất; đồ ở giữa dễ bị bỏ sót — yêu cầu quan trọng đừng chôn giữa.

## 2 Giữ bàn làm việc sạch

Context rác = attention rác. Khi chat dài, tóm tắt lại thay vì kéo theo mọi thứ; khi vibe code, đưa đúng file liên quan, không dán cả repo.

## 3 Cho tra sổ thay vì bắt nhớ

Tài liệu dài: lấy đoạn liên quan nhét vào context (RAG) thay vì trông chờ model nhớ hết hoặc nhét cả cuốn.

Agent mạnh không phải vì context khổng lồ — mà vì nó có tools để lấy đúng thứ vào bàn làm việc đúng lúc


<!-- END PAGE 36 -->


<!-- START PAGE 37 -->

## [Trang 37]


# Tham số (parameter): những "khớp nối" model học được

Sau khi luyện xong, những gì model "biết" nằm trong các con số cố định bên trong gọi là **tham số** — hãy hình dung như **khớp nối thần kinh**: luyện càng kỹ, các khớp nối càng được siết đúng.

**Tham số không phải thứ bạn chỉnh** khi dùng model — nó được đóng gói sẵn trong "bộ não" (file weights). Bạn chỉ chỉnh được context và các núm vặn lúc gọi (như temperature).

2020 — GPT-3

**175 tỷ**

một "bác sĩ đa năng" — mọi token đều đi qua toàn bộ khớp nối (dense)

**Nhiều tham số ≠ tốn hơn tuyến tính — nhờ MoE, bệnh viện lớn gấp 16 lần mà chi phí mỗi ca khám gần như không đổi**

2026 — Kimi K3

**2.800 tỷ**

một "bệnh viện đa khoa" — mỗi token chỉ gọi vài chuyên gia (MoE)



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 37]**:
```markdown
1. **Tên/Chủ đề sơ đồ**: Biểu đồ thể hiện mối quan hệ giữa "Test Loss" và "Compute/Dữ liệu (thang log)"

2. **Các cột mốc / Thành phần chính**:
   - **Trục Y (Thẳng đứng)**: Test Loss (Giá trị mất mát trong quá trình đánh giá mô hình).
   - **Trục X (Ngang)**: Compute/Dữ liệu (thang log) (Lượng tính toán hoặc dữ liệu sử dụng, được biểu diễn theo thang log).
   - **Dạng biểu đồ**: Đường cong giảm dần, thể hiện sự giảm của test loss khi lượng compute/dữ liệu tăng lên.

3. **Số liệu & Insight quan trọng**:
   - Test loss giảm dần khi lượng compute/dữ liệu tăng theo thang log.
   - Không có các số liệu cụ thể trên biểu đồ, nhưng xu hướng cho thấy việc tăng cường tài nguyên (compute/dữ liệu) sẽ cải thiện hiệu suất mô hình (giảm test loss).

4. **Ý nghĩa bài học**:
   - Biểu đồ minh họa rằng việc đầu tư nhiều hơn vào tài nguyên tính toán và dữ liệu có thể giúp cải thiện hiệu suất của mô hình học máy, thể hiện qua việc giảm test loss.
   - Tuy nhiên, hiệu quả cải thiện này có xu hướng giảm dần theo quy luật log, tức là cần nhiều tài nguyên hơn để đạt được cải thiện tương đương.
```

> **Ghi chú**: Biểu đồ này thường được sử dụng trong các bài giảng về tối ưu hóa mô hình học máy, hiệu suất tính toán và phân tích chi phí - hiệu quả.



Luật chơi 2020–2024: cứ thêm compute + dữ liệu là model khôn lên **một cách dự đoán được** (scaling law, Kaplan et al. 2020)

MoE: Shazeer et al. (2017) — arxiv.org/abs/1701.06538 · Kimi K3 (16/7/2026): ~2.8 nghìn tỷ tham số MoE — k3-kimi.com


<!-- END PAGE 37 -->


<!-- START PAGE 38 -->

## [Trang 38]


# LLM được tạo ra như thế nào? — đọc nhiều, được chỉ, được uốn nắn, luyện đề

Một LLM được “nuôi lớn” qua 3 bước — mỗi bước một việc khác nhau



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 38]**:
```markdown
# Sơ đồ quy trình đào tạo mô hình AI theo phương pháp RLHF/DPO

## Tên/Chủ đề sơ đồ
Quy trình đào tạo mô hình ngôn ngữ lớn (LLM) bao gồm 3 giai đoạn chính: Pre-training, SFT (Supervised Fine-Tuning), và RLHF/DPO (Reinforcement Learning with Human Feedback / Direct Preference Optimization).

---

## Các cột mốc / Thành phần chính

### 1. Pre-Training (Đọc nhiều)
- **Mô tả**: Dọc gần như toàn bộ internet để học ngôn ngữ và kiến thức.
- **Chi tiết**:
  - Dữ liệu: Dữ liệu văn bản khổng lồ từ internet.
  - Mục tiêu: Học ngôn ngữ và kiến thức cơ bản.
  - Ví dụ: Như đọc các cuốn sách, những chủ đề khác trên mạng.

### 2. SFT (Supervised Fine-Tuning) (Được chỉ cách trả lời)
- **Mô tả**: Dạy mô hình cách trả lời dựa trên các mẫu câu hỏi và đáp án đã được đánh giá.
- **Chi tiết**:
  - Dữ liệu: Các cặp mẫu (câu hỏi, đáp án) được đánh giá.
  - Mục tiêu: Hướng dẫn mô hình trả lời chính xác và phù hợp.
  - Ví dụ: Như giảng dạy làm mẫu, hướng dẫn cách trả lời đáp án.

### 3. RLHF/DPO (Được uốn nắn) (Reinforcement Learning with Human Feedback / Direct Preference Optimization)
- **Mô tả**: Người đánh giá (câu hỏi, đáp án tốt) để mô hình học cách chọn đáp án phù hợp với mong muốn người dùng.
- **Chi tiết**:
  - Dữ liệu: Phản hồi từ con người về sự ưu tiên giữa các đáp án.
  - Mục tiêu: Tối ưu hóa mô hình sao cho đáp án phù hợp với mong muốn người dùng.
  - Ví dụ: Như tập uốn gỗ giòng cho bánh xe, hình thù mong muốn.

---

## Mũi tên kết nối
- Mũi tên từ Pre-Training đến SFT: Chuyển tiếp từ việc học kiến thức cơ bản sang việc học cách trả lời.
- Mũi tên từ SFT đến RLHF/DPO: Chuyển tiếp từ việc học trả lời chính xác sang việc tối ưu hóa đáp án theo mong muốn người dùng.

---

## Ý nghĩa bài học
Quy trình này thể hiện cách một mô hình ngôn ngữ lớn được đào tạo từ việc học kiến thức cơ bản, qua việc học cách trả lời chính xác, đến việc tối ưu hóa để đáp ứng mong muốn của người dùng. Mỗi giai đoạn đóng vai trò quan trọng trong việc phát triển một mô hình AI thông minh và hữu ích.
```



Ấn dụ “học giả trong bóng bóng”: đọc rất nhiều (bước 1) nhưng phải được chỉ (2) và uốn nắn (3) mới biết để đáp cho ra người.

① Pre-training — “đọc cả thư viện”: học tiếng nói và kiến thức từ hàng nghìn tỷ token. ② SFT — “được chỉ cách trả lời”: học theo ví dụ mẫu để ra dáng trợ lý. ③ RLHF/DPO — “được uốn nắn”: học theo phản hồi con người, an toàn và dễ chịu hơn. ④ Luyện suy luận — “giải đề tự chấm” (từ ~2025): luyện toán/code có đáp án kiểm chứng được → model biết làm nháp trước khi trả lời.

Đọc vạn cuốn sách chưa chắc biết trả lời phỏng vấn — đó là lý do cần bước ②, ③, ④

Ouyang et al. (2022), InstructGPT — arxiv.org/abs/2203.02155 · Rafailov et al. (2023), DPO — arxiv.org/abs/2305.18290 · RLVR: RL with verifiable rewards.


<!-- END PAGE 38 -->


<!-- START PAGE 39 -->

## [Trang 39]


# RLHF: ba bước uốn cỗ máy đoán token thành trợ lý biết nghe lời

① Model viết nhiều câu trả lời

«Cùng một câu hỏi»

LLM

Trả lời A

Trả lời C

Trả lời B

Trả lời D

② Người chấm xếp hạng

Trả lời B

Trả lời D

Trả lời A

Trả lời C

REWARD MODEL
máy chấm điểm thay người

③ Huấn luyện theo điểm

LLM

câu trả lời vừa viết

điểm: 9.2 / 10

tăng xác suất
câu ghi điểm
cao

lặp lại hàng nghìn lần → model dẫn “biết nghe lời”

Cỗ máy đoán token + điểm xếp hạng của con người → trợ lý helpful · harmless · honest

Ouyang et al. (2022), “Training language models to follow instructions with human feedback” (InstructGPT) — arxiv.org/abs/2203.02155 · DPO (cách đơn giản hơn, 2023) — arxiv.org/abs/2305.18290


<!-- END PAGE 39 -->


<!-- START PAGE 40 -->

## [Trang 40]


# LLM có thực sự “hiểu” — hay chỉ là vẹt thống kê?



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 40]**:
```markdown
> 🖼️ *[Hình ảnh minh họa / Ảnh trang trí không chứa thông tin kiến thức bài học]*

---
**Mô tả hình ảnh (nếu cần phân tích ý nghĩa biểu tượng):**
- **Bối cảnh**: Hình ảnh mang tính chất ẩn dụ, kết hợp giữa một bông hồng thực và một robot nhỏ.
- **Thành phần chính**:
  - Bông hồng trong bình (đại diện cho tự nhiên, sự sống, cảm xúc).
  - Robot với đầu hình người (đại diện cho trí tuệ nhân tạo, logic).
  - Bong bóng tư duy chứa các bông hoa và công thức (gợi ý sự kết hợp giữa sáng tạo và khoa học).
- **Ý nghĩa biểu tượng**:
  - Có thể tượng trưng cho sự hội tụ giữa **tự nhiên và công nghệ**, hoặc **cảm xúc và trí tuệ nhân tạo**.
  - Dùng để minh họa chủ đề về **học tập đa ngành (interdisciplinary learning)** hoặc **sự cân bằng giữa logic và cảm xúc trong giáo dục**.

---
*Lưu ý*: Hình ảnh không chứa thông tin kiến thức cụ thể để phân tích theo yêu cầu RAG về số liệu, quy trình hoặc mã nguồn.
```



1 Mô hình thế giới bên trong?

nén thế giới thành biểu diễn có cấu trúc

?



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 40]**:
```markdown
> 🖼️ *[Hình ảnh minh họa / Ảnh trang trí không chứa thông tin kiến thức bài học]*

---
**Mô tả hình ảnh (nếu cần phân tích ý nghĩa biểu tượng):**
- **Bối cảnh**: Hình ảnh mang tính chất ẩn dụ, kết hợp giữa một bông hồng thực và một robot nhỏ.
- **Thành phần chính**:
  - Bông hồng trong bình (đại diện cho tự nhiên, sự sống, cảm xúc).
  - Robot với đầu hình người (đại diện cho trí tuệ nhân tạo, logic).
  - Bong bóng tư duy chứa các bông hoa và công thức (gợi ý sự kết hợp giữa sáng tạo và khoa học).
- **Ý nghĩa biểu tượng**:
  - Có thể tượng trưng cho sự hội tụ giữa **tự nhiên và công nghệ**, hoặc **cảm xúc và trí tuệ nhân tạo**.
  - Dùng để minh họa chủ đề về **học tập đa ngành (interdisciplinary learning)** hoặc **sự cân bằng giữa logic và cảm xúc trong giáo dục**.

---
*Lưu ý*: Hình ảnh không chứa thông tin kiến thức cụ thể để phân tích theo yêu cầu RAG về số liệu, quy trình hoặc mã nguồn.
```



2 Nôn lại dữ liệu huấn luyện?

chỉ ghép các mẫu chữ theo xác suất

Chỉ đoán token tiếp theo thôi — vậy sao trông giống đang hiểu mình nói gì?

Tranh luận từ Turing (1950), “Computing Machinery and Intelligence”, Mind - “Stochastic parrots”: Bender, Gebru, McMillan-Major & Shmitchell (2021), FAccT'21 - Hình minh họa: Martin Wattenberg (Harvard)


<!-- END PAGE 40 -->


<!-- START PAGE 41 -->

## [Trang 41]


# Thí nghiệm Othello-GPT: dạy cỗ máy đoán chữ chơi cờ

Đầu vào duy nhất: chuỗi token biên bản ván cờ

C4 C3 D3 C5 D6 F4 B4 C6 B5 B3 B6 E3 C2
A4 A5 A6 D2 ?

- ✖ **Không** được dạy luật chơi
- ✖ **Không** hề thấy bàn cờ 8×8
- ✖ **Không** biết quân trắng-đen — chỉ thấy chuỗi ký tự



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 41]**:
Dưới đây là phân tích và chuyển đổi nội dung của ảnh theo yêu cầu:

---
### **1. Tên/Chủ đề sơ đồ**
**Biểu đồ phân bố 2D của các điểm dữ liệu (có thể là kết quả phân tích cluster hoặc phân loại trong không gian 2 chiều).**

---
### **Các cột mốc / Thành phần chính**
- **Trục X và Y**:
  - Các trục đều được đánh số từ `1` đến `8` (có thể đại diện cho các đặc trưng, chỉ số hoặc giá trị).
  - Không có nhãn mô tả cụ thể (ví dụ: tên biến, đơn vị đo), nhưng có thể liên quan đến một không gian đặc trưng (feature space).

- **Các điểm dữ liệu**:
  - **Biểu đồ 1 (trái)**: Hiển thị 2 điểm đen và 2 điểm trắng (có thể đại diện cho 2 nhóm phân loại khác nhau).
  - **Biểu đồ 2 (giữa)**: Nhấn mạnh vào một vùng cụ thể (khung đỏ) với 3 điểm đen và 1 điểm trắng, có thể chỉ ra sự tập trung hoặc tương tác giữa các điểm.
  - **Biểu đồ 3 (phải)**: Tương tự biểu đồ 2, nhưng khung đỏ bao quanh 3 điểm trắng và 1 điểm đen, có thể thể hiện sự thay đổi trong phân loại hoặc tập trung mới.

---
### **Số liệu & Insight quan trọng**
- **Vị trí điểm**:
  - **Biểu đồ 1**: Điểm đen tại `(~3, 6)` và `(~5, 2)`; điểm trắng tại `(~2, 4)` và `(~6, 7)`.
  - **Biểu đồ 2**: Khung đỏ bao quanh các điểm tại `(~3, 6)`, `(~4, 5)`, `(~5, 6)` (đen) và `(~4, 4)` (trắng).
  - **Biểu đồ 3**: Khung đỏ bao quanh các điểm tại `(~3, 4)`, `(~4, 5)`, `(~5, 4)` (trắng) và `(~4, 6)` (đen).
- **Sự thay đổi**:
  - Sự di chuyển hoặc thay đổi phân loại của các điểm trong khung đỏ giữa biểu đồ 2 và 3 (điểm đen/trắng thay đổi vị trí).

---
### **Ý nghĩa bài học**
Biểu đồ thể hiện quá trình phân tích hoặc phân loại dữ liệu trong không gian 2 chiều, có thể liên quan đến:
1. **Thuật toán clustering** (như K-Means) hoặc **phân loại** (như SVM) trong học máy, nơi các điểm dữ liệu được nhóm hoặc dự đoán nhãn.
2. **Sự thay đổi trong phân loại** khi điều chỉnh mô hình hoặc dữ liệu đầu vào (ví dụ: sau khi huấn luyện lại mô hình).
3. **Tầm quan trọng của vùng tập trung** (khung đỏ) trong việc đánh giá hiệu suất hoặc xác định các mẫu đặc biệt.

---
> **Ghi chú**: Nếu đây là một ví dụ trong bài giảng về **machine learning**, có thể liên quan đến các khái niệm như:
> - **Feature space** (không gian đặc trưng),
> - **Decision boundaries** (ranh giới phân loại),
> - **Model evaluation** (đánh giá mô hình).



Ba trạng thái bàn cờ thật mà con người nhìn được — còn model thì không bao giờ thấy.

**Câu hỏi: đoán được nước đi tiếp theo không? — chỉ từ chuỗi ký tự đó thôi**


<!-- END PAGE 41 -->


<!-- START PAGE 42 -->

## [Trang 42]


# Muốn đi hợp lệ, nó buộc phải tự dựng lại bàn cờ trong đầu

ĐẦU VÀO DUY NHẤT

C4 C3 D3 C5 D6 F4 B4 C6 B5
B3 B6 E3 C2 A4 A5 A6 D2 ?

chuỗi token biên bản ván cờ — không luật chơi, không bàn cờ, không quân trắng-đen



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 42]**:
```markdown
> 🎯 *[Hình ảnh minh họa bàn cờ game "Bên Trong Não Model"]*

---
### **1. Tên/Chủ đề sơ đồ**
Bàn cờ mô phỏng cấu trúc **"Bên Trong Não Model"** (gợi ý về mô hình trí não hoặc quá trình tư duy).

---
### **2. Các thành phần chính**
- **Bàn cờ 5×5** với 2 loại quân cờ:
  - **Quân trắng (●)** và **quân đen (●)**.
  - **Vị trí quân cờ**:
    - Hàng 3 (từ trên xuống):
      - Cột 2: Quân đen
      - Cột 3: Quân trắng
      - Cột 4: Quân đen
    - Hàng 4:
      - Cột 2: Quân trắng
      - Cột 3: Quân đen
      - Cột 4: Quân trắng
    - Hàng 5:
      - Cột 2: Quân đen
      - Cột 3: Quân trắng
      - Cột 4: Quân đen

---
### **3. Số liệu & Insight quan trọng**
- **Số quân cờ**: 6 quân (3 quân trắng, 3 quân đen).
- **Kích thước bàn cờ**: 5×5 ô vuông.
- **Mô hình**: Dạng hình "kim tự tháp" đảo ngược (mở rộng từ giữa ra hai bên).

---
### **4. Ý nghĩa bài học**
Hình ảnh có thể đại diện cho:
- **Mô hình tư duy phân cấp** (ví dụ: quá trình xử lý thông tin từ trung tâm ra ngoại vi).
- **Cấu trúc não bộ** (như các vùng não tương tác theo mô hình phân cấp).
- **Game logic** để minh họa chiến lược cân bằng giữa hai bên (trắng/đen).

---
> **Ghi chú**: Nếu đây là phần của giáo trình về trí não, có thể liên quan đến mô hình **"Model của não bộ"** (chẳng hạn như mô hình xử lý thông tin theo lớp hoặc mô hình AI phân cấp).
```

---
**Lưu ý**: Nếu đây là hình minh họa cho một bài giảng cụ thể, cần tham khảo thêm nội dung bài học để giải thích chính xác hơn.



một "bàn cờ ẩn" tự hình thành — không ai dạy

ĐẦU RA

F5

✓ nước đi hợp lệ

tỷ lệ đi sai luật chỉ ~0.01%

đi hợp lệ ⇒ phải biết ô nào trắng, ô nào đen, ô nào trống

Không ai cho nó xem bàn cờ — để đoán đúng token tiếp theo, cỗ máy tự xây một mô hình thế giới bên trong


<!-- END PAGE 42 -->


<!-- START PAGE 43 -->

## [Trang 43]


# Mở hộp đen kiểm chứng: bàn cờ có thật trong não model

Nhóm nghiên cứu gắn 64 "que thử" (probe) vào bên trong model — mỗi que hỏi một ô: "ô này đang trắng, đen, hay trống?"



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 43]**:
```markdown
1. **Tên/Chủ đề sơ đồ**: Sơ đồ dự đoán chuỗi hành động (Move Sequence Prediction)

2. **Các cột mốc / Thành phần chính**:
   - **Trục X**: Diễn biến thời gian của chuỗi hành động (từ trái sang phải).
   - **Các box**:
     - `X₁`: Hành động đầu tiên trong chuỗi.
     - `X₂`: Hành động thứ hai.
     - `X₃`: Hành động thứ ba (được biểu thị với dấu "..." giữa `X₂` và `X₃`, cho thấy chuỗi có thể dài hơn).
     - `X₄`: Hành động tiếp theo trong chuỗi.
   - **Mũi tên**:
     - Mũi tên từ `X₁` → `X₂` → `X₃` → `X₄`: Diễn tả quá trình chuyển tiếp giữa các hành động.
     - Mũi tên cuối cùng từ `X₄` đến "Predicted next move": Diễn tả quá trình dự đoán hành động tiếp theo dựa trên các hành động trước đó.

3. **Số liệu & Insight quan trọng**:
   - Chuỗi hành động được đánh số thứ tự (`X₁`, `X₂`, `X₃`, `X₄`).
   - Dự đoán dựa trên mô hình học máy hoặc hệ thống phân tích chuỗi hành động.

4. **Ý nghĩa bài học**:
   - Sơ đồ mô tả một mô hình dự đoán hành động tiếp theo trong một chuỗi dựa trên dữ liệu lịch sử.
   - Ứng dụng phổ biến trong các hệ thống tự động hóa, trò chơi, hoặc phân tích hành vi người dùng.
   - Nhấn mạnh vào việc sử dụng dữ liệu trước đó để dự đoán kết quả tiếp theo, thể hiện tính liên tục và dự đoán trong học máy.
```



1 Que thử đọc được toàn bộ bàn cờ

Từ activation bên trong, probe đọc ra trạng thái từng ô — chính xác vượt xa mức ngẫu nhiên, và càng giữa ván càng chính xác.

2 Lật một quân trong "đầu" nó → nước đi đổi theo

Khi can thiệp lật màu một quân cờ trong biểu diễn bên trong, các nước đi hợp lệ model dự đoán đổi theo đúng luật — tức nó thật sự dùng bàn cờ đó để chơi.

Model chỉ đoán token tiếp theo — nhưng để đoán giỏi, nó tự xây một mô hình thế giới bên trong

Li et al. (2023), ICLR 2023 (Oral) — arXiv:2210.13382 · Bản đọc dễ hơn: thegradient.pub/othello


<!-- END PAGE 43 -->


<!-- START PAGE 44 -->

## [Trang 44]


# Giới hạn bẩm sinh: học giả trong bong bóng

## Bong bóng thời gian

Model bị "đóng băng" tại ngày ngừng đọc. Chuyện sau đó nó không biết — trừ khi bạn cung cấp thêm (knowledge cutoff).

## Nói chắc như đúng rồi

Model tối ưu cho câu **nghe hợp lý**, không phải tra sự thật — nên có thể tự tin mà sai (hallucination).

## Bàn làm việc có hạn

Context có trần; quá dài vừa tốn tiền vừa dễ bỏ sót thông tin ở giữa.

"Why does it work? We don't know — a lot here are intuitions, not theorems or truths." — Łukasz Kaiser, đồng tác giả
"Attention Is All You Need" (OpenAI)

**Đây không phải lỗi tạm thời — đó là bản chất của cỗ máy đoán token. Vì vậy ta cần prompt tốt, context sạch, tra số (RAG), tools, và luôn kiểm chứng.**


<!-- END PAGE 44 -->


<!-- START PAGE 45 -->

## [Trang 45]


# Vì sao model vẫn sai: nó rất giỏi học vẹt đường tắt

## 1 Phân loại spam

Model thực chất đã học:

**“đếm số hyperlink trong email”**

*Email sạch nhưng nhiều link → vẫn bị gán spam*

## 2 Câu chủ quan vs khách quan

Model thực chất đã học:

**“có phải câu trích từ film review không”**

*Ăn gian bằng nguồn gốc câu, không phải nội dung câu*

## 3 Suy luận ngôn ngữ (MNLI)

Model thực chất đã học:

**“câu có động từ phủ định”**

*Đối cấu trúc dữ liệu test là điểm tụt ngay*

Ba “đường tắt” (spurious cues) trên do **chính LLM tự động phát hiện** và mô tả bằng ngôn ngữ tự nhiên — trên quy mô 675 bài toán thật của benchmark OpenD5.

**Benchmark cao ≠ model hiểu đúng thứ bạn tưởng — luôn test trên dữ liệu của chính mình**

Zhong, Snell, Klein & Steinhardt (2022), “Describing Differences between Text Distributions with Natural Language”, ICML 2022 · Zhong et al. (2023), “Goal Driven Discovery of Distributional Differences via Language Descriptions” (OpenD5), NeurIPS 2023


<!-- END PAGE 45 -->


<!-- START PAGE 46 -->

## [Trang 46]


# Model không chỉ mô hình hóa thế giới — nó mô hình hóa cả BẠN



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 46]**:
Dưới đây là nội dung trích xuất từ ảnh theo dạng Markdown:

---
### Nội dung cuộc trò chuyện về cách sử dụng ChatGPT để tạo jantar (bữa tiệc):

#### Câu hỏi và trả lời:
1. **Câu hỏi ban đầu:**
   > Olá ChatGPT, tudo bem com você? Como está o seu dia?

2. **Trả lời của ChatGPT:**
   > Eu sou apenas um programa de inteligência artificial, então eu não tenho sentimentos ou dias. Estou sempre pronto para ajudar com qualquer pergunta ou tarefa que você tenha. Em que posso ajudá-lo hoje?

3. **Yêu cầu của người dùng:**
   > Você pode me ajudar a escolher uma roupa para um jantar hoje?

4. **Trả lời của ChatGPT:**
   > Claro! Para escolher uma roupa adequada para um jantar, preciso saber alguns detalhes sobre o evento, como o ambiente, o dress code e o clima. Por exemplo:
   - **Ambiente:** Formal, semi-formal, casual?
   - **Dress code:** Se houver algum dress code específico (ex.: "black tie", "cocktail", "business casual").
   - **Clima:** Também é importante, se estiver frio você deve usar casacos, se estiver quente use roupas leves.

5. **Chi tiết về cách chọn vestuário:**
   > Ser um vestido é uma excelente escolha para um jantar formal. Existem muitos estilos diferentes de vestidos que você pode escolher, desde vestidos de noite mais elegantes até vestidos mais curtos e descontraídos. Algumas opções para considerar ao escolher um vestido incluem:
   - Cores escuras, como preto, azul marinho e vermelho são geralmente consideradas mais formais do que cores claras ou estampadas.
   - Silhuetas mais ajustadas ou com cortes precisos são geralmente mais formais do que silhuetas soltas ou fluidas.
   - Detalhes como bordados, rendas e tecidos podem editar a formalidade de um vestido.

6. **Lời khuyên cuối cùng:**
   > Embora essas dicas sejam apenas sugestões gerais, o que você deve sempre se sentir confortável e feliz com o que estiver vestindo.

---
Nếu có yêu cầu phân tích sâu hơn về cách sử dụng ChatGPT trong việc tư vấn thời trang hoặc các khía cạnh khác, có thể tiếp tục mở rộng.



ChatGPT nói tiếng Bồ Đào Nha với Fernanda Viégas: đầu hội thoại nó dùng động từ giống đực ("ajudá-lo").

Ngay khi bà nhắc đến chiếc váy (vestido), câu sau model chuyển sang tính từ giống cái ("segura") — nó đã ngầm đoán giới tính người dùng.

**Không ai bảo nó làm vậy.** Từ cách bạn viết, model tự dựng một "hồ sơ" về bạn — và hồ sơ đó ảnh hưởng câu trả lời.

Cách bạn viết prompt cũng đang nói cho model biết bạn là ai — đó là lý do persona và ngữ cảnh trong prompt rất đáng giá


<!-- END PAGE 46 -->


<!-- START PAGE 47 -->

## [Trang 47]


# Bốn cách chạm vào LLM: tiện bao nhiêu, kiểm soát bấy nhiêu



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 47]**:
```markdown
---
### 1. Tên/Chủ đề sơ đồ:
**Sơ đồ phân loại các hình thức sử dụng mô hình AI trong phát triển phần mềm**
*(Trục X: Khối lượng sử dụng & Tiện dụng; Trục Y: Mức kiểm soát & Tùy biến)*

---

### 2. Các cột mốc / Thành phần chính:
#### **Trục X (Từ trái sang phải):**
- **Khối lượng sử dụng & Tiện dụng** tăng dần (từ ít đến nhiều).
  - *Ví dụ*: Self-host (ít tiện dụng) → Chat app (nhiều tiện dụng).

#### **Trục Y (Từ dưới lên trên):**
- **Mức kiểm soát & Tùy biến** tăng dần (từ thấp đến cao).
  - *Ví dụ*: Chat app (kiểm soát thấp) → Self-host (kiểm soát cao).

#### **Các box chính (từ góc dưới bên phải → góc trên bên trái):**
1. **Chat app** (góc dưới bên phải):
   - **Mô tả**: Dễ dàng sử dụng, không cần code.
   - **Ví dụ công cụ**: ChatGPT, Claude, Kimi.
   - **Đặc điểm**: Khối lượng sử dụng cao, kiểm soát thấp.

2. **Coding assistant** (góc giữa bên phải):
   - **Mô tả**: Trợ lý AI tích hợp trong IDE, hỗ trợ viết code.
   - **Ví dụ công cụ**: Cursor, Copilot.
   - **Đặc điểm**: Dành cho lập trình viên, hỗ trợ trực tiếp trong quá trình code.

3. **API** (góc giữa):
   - **Mô tả**: Gọi model bằng code, học cách sử dụng API.
   - **Ví dụ**: Học cách gọi API để sử dụng model.
   - **Đặc điểm**: Cần hiểu biết về code, kiểm soát trung bình.

4. **Self-host** (góc trên bên trái):
   - **Mô tả**: Tự host model, kiểm soát tối đa.
   - **Ví dụ công cụ**: Open-weight, Kimi K3, Llama.
   - **Đặc điểm**: Khối lượng sử dụng thấp, kiểm soát và tùy biến cao.

---

### 3. Số liệu & Insight quan trọng:
- **Công cụ cụ thể**:
  - **Chat app**: ChatGPT, Claude, Kimi.
  - **Coding assistant**: Cursor, Copilot.
  - **Self-host**: Open-weight, Kimi K3, Llama.
- **Trục X/Y**:
  - Trục X thể hiện sự tiện dụng và khối lượng sử dụng.
  - Trục Y thể hiện mức độ kiểm soát và tùy biến.
- **Quan hệ**: Các công cụ càng ở góc phải dưới, càng dễ sử dụng nhưng kiểm soát thấp; càng ở góc trái trên, càng khó sử dụng nhưng kiểm soát cao.

---

### 4. Ý nghĩa bài học:
- **Phân loại công cụ AI** theo mức độ tiện dụng và kiểm soát giúp lập trình viên lựa chọn phù hợp với nhu cầu.
- **Chat app** thích hợp cho người mới hoặc cần giải pháp nhanh.
- **Coding assistant** phù hợp với lập trình viên cần hỗ trợ trực tiếp trong quá trình code.
- **Self-host** dành cho những người muốn tối ưu hóa và kiểm soát hoàn toàn model.
- **API** là cầu nối giữa các hình thức sử dụng, đòi hỏi kiến thức cơ bản về lập trình.
```

---
> **Ghi chú**: Sơ đồ này giúp người học hiểu rõ cách tiếp cận và lựa chọn công cụ AI phù hợp trong phát triển phần mềm.



Cùng một bộ não nề, bốn mức quyền truy cập — mức truy cập quyết định bạn tùy biến được tới đâu


<!-- END PAGE 47 -->


<!-- START PAGE 48 -->

## [Trang 48]


## Nghịch để tin: tự tay bóc GPT-2 trong trình duyệt

Mở **Transformer Explainer** (nhóm 2–3 bạn một máy, đã tải sẵn), rồi làm 3 việc:

① Gõ một câu, xem nó bị cắt thành token thế nào.
② Vặn **temperature** từ 0 lên cao, chạy lại vài lần, nhìn bảng xác suất đổi ra sao.
③ Mở **attention map**, bấm vào một token, xem nó "đang nhìn" những token nào.

*Hai câu chốt để mang về:*

"Temperature đổi cách model CHỌN CHỮ — chứ không đổi kiến thức model có" · "Attention map cho thấy model NHÌN VÀO ĐÂU — chứ không chứng minh model hiểu"

poloclub.github.io/transformer-explainer · Paper: arxiv.org/abs/2408.01919 · GPT-2 small là model minh họa kiến trúc, không phải model mới nhất. Attention map cho thấy tương quan, không chứng minh nhân quả.


<!-- END PAGE 48 -->


<!-- START PAGE 49 -->

## [Trang 49]


PHẦN 04

# Từ LLM đến AI Agent

*đặt bộ não vào vòng làm việc có mục tiêu và hành động*


<!-- END PAGE 49 -->


<!-- START PAGE 50 -->

## [Trang 50]


# Chain-of-Thought: chỉ thêm "giấy nháp", từ sai thành đúng

Bài toán: "Có 5 quả bóng tennis. Mua thêm 2 hộp, mỗi hộp 3 quả. Hỏi tổng cộng có bao nhiêu quả?"

Không có nháp — trả lời ngay

Model đọc câu hỏi → bật ra đáp án ngay:

"Đáp án là 27 quả."

✕ SAI

Có giấy nháp — "hãy nghĩ từng bước"

"Bắt đầu có 5 quả.

Mỗi hộp 3 quả × 2 hộp = 6 quả.

5 + 6 = 11.

Đáp án là 11 quả."

✓ ĐÚNG

Cùng một model, cùng một câu hỏi — cho nó được viết nháp từng bước, bản chất suy luận lộ ra


<!-- END PAGE 50 -->


<!-- START PAGE 51 -->

## [Trang 51]


# LLM đứng một mình chưa làm được gì nhiều

Prompt tĩnh — một lượt hỏi đáp



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 51]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình tương tác cơ bản với mô hình ngôn ngữ lớn (LLM)

**Các cột mốc / Thành phần chính**:
- **Prompt**: Khối đầu tiên, đại diện cho đầu vào (câu hỏi, yêu cầu) của người dùng.
- **LLM (Large Language Model)**: Khối giữa, biểu thị mô hình xử lý đầu vào (Prompt) bằng thuật toán học máy.
- **Response**: Khối cuối, thể hiện đầu ra (phản hồi) của mô hình trả về cho người dùng.
- **Mũi tên**: Chỉ hướng dữ liệu chảy từ **Prompt** → **LLM** → **Response**, thể hiện quá trình xử lý tuần tự.

**Số liệu & Insight quan trọng**:
- Không có số liệu cụ thể trong sơ đồ (chỉ mô tả khái niệm).
- Các thành phần chính: **Prompt**, **LLM**, **Response** (tên công nghệ: *Large Language Model*).

**Ý nghĩa bài học**:
Sơ đồ minh họa quy trình cơ bản của hệ thống AI dựa trên LLM, trong đó người dùng gửi **Prompt**, mô hình xử lý và trả về **Response**. Đây là mô hình cơ sở cho các ứng dụng chatbot, trợ lý ảo hoặc hệ thống tự động hóa dựa trên ngôn ngữ.
---
```



- ✖ Không dữ liệu mới
- ✖ Không hành động ngoài đời
- ✖ Không nhớ gì sau câu trả lời



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 51]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình tương tác cơ bản với mô hình ngôn ngữ lớn (LLM)

**Các cột mốc / Thành phần chính**:
- **Prompt**: Khối đầu tiên, đại diện cho đầu vào (câu hỏi, yêu cầu) của người dùng.
- **LLM (Large Language Model)**: Khối giữa, biểu thị mô hình xử lý đầu vào (Prompt) bằng thuật toán học máy.
- **Response**: Khối cuối, thể hiện đầu ra (phản hồi) của mô hình trả về cho người dùng.
- **Mũi tên**: Chỉ hướng dữ liệu chảy từ **Prompt** → **LLM** → **Response**, thể hiện quá trình xử lý tuần tự.

**Số liệu & Insight quan trọng**:
- Không có số liệu cụ thể trong sơ đồ (chỉ mô tả khái niệm).
- Các thành phần chính: **Prompt**, **LLM**, **Response** (tên công nghệ: *Large Language Model*).

**Ý nghĩa bài học**:
Sơ đồ minh họa quy trình cơ bản của hệ thống AI dựa trên LLM, trong đó người dùng gửi **Prompt**, mô hình xử lý và trả về **Response**. Đây là mô hình cơ sở cho các ứng dụng chatbot, trợ lý ảo hoặc hệ thống tự động hóa dựa trên ngôn ngữ.
---
```



Sản phẩm AI thật = bộ não LLM + hệ thống bao quanh — phần khó thường nằm ở hệ thống


<!-- END PAGE 51 -->


<!-- START PAGE 52 -->

## [Trang 52]


# Từ LLM đến agent: bốn mức độ — mỗi bậc thêm một năng lực



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 52]**:
```markdown
### 1. Tên/Chủ đề sơ đồ
**Quy trình phát triển khả năng của agent (trợ lý) trong hệ thống LLM**
*(Từ mức cơ bản đến mức phức hợp, tích hợp đa agent)*

---

### 2. Các cột mốc / Thành phần chính
Sơ đồ thể hiện **4 cấp độ phát triển** của agent, theo hướng từ trái sang phải (mức độ phức tạp tăng dần):

- **LEVEL 0: Bộ não suy luận (LLM cơ bản)**
  - **Mô tả**: LLM truyền thống (không có công cụ, không tự động liên kết kiến thức).
  - **Hạn chế**: Không tự động truy xuất thông tin từ bên ngoài.

- **LEVEL 1: Có kết nối**
  - **Mô tả**:
    - Sử dụng công cụ kết nối như:
      - Tìm kiếm web (`search web`).
      - Truy vấn database.
      - Gọi API.
    - **Vượt khơi** bong bóng thông tin giới hạn.
  - **Tính năng mới**: Tự động thu thập thông tin từ nguồn bên ngoài.

- **LEVEL 2: Biết lập kế hoạch**
  - **Mô tả**:
    - Tự chủ mục tiêu (thành nhiệm vụ).
    - Dùng nhiều công cụ khác nhau (tương tác với nhiều API/tool).
    - Tự kiểm tra kết quả (feedback loop).
  - **Tính năng mới**: Khả năng lập kế hoạch và điều phối công cụ.

- **LEVEL 3: Đội agent phối hợp**
  - **Mô tả**:
    - Nhiều agent chuyên biệt (multi-agent) với vai trò riêng.
    - **Phối hợp** để giải quyết vấn đề phức tạp.
  - **Tính năng mới**: Tích hợp đa agent, phân công nhiệm vụ.

---
### 3. Số liệu & Insight quan trọng
- **Trục phát triển**: Từ **LLM cơ bản (Level 0)** → **Đội agent phối hợp (Level 3)**.
- **Công nghệ/Tool được nhắc đến**:
  - Search web, database, API (Level 1).
  - Kiểm tra kết quả tự động (Level 2).
- **Khái niệm mới**:
  - **Multi-agent**: Nhiều agent chuyên biệt hợp tác.
  - **Tự chủ mục tiêu**: Agent tự lập kế hoạch.

---
### 4. Ý nghĩa bài học
Sơ đồ minh họa **quá trình tiến hóa** của agent từ đơn giản đến phức tạp, nhấn mạnh:
1. **Tích hợp công cụ** (Level 1) giúp agent vượt qua giới hạn kiến thức ban đầu.
2. **Khả năng lập kế hoạch** (Level 2) cho phép agent chủ động và tự kiểm tra.
3. **Phối hợp đa agent** (Level 3) mở ra khả năng giải quyết vấn đề phức tạp như con người.
4. **Hướng phát triển tương lai**: Agent không chỉ trả lời mà còn **tự động hành động và phối hợp** để tối ưu hóa kết quả.
```

---
> **Ghi chú**: Sơ đồ không thể hiện mốc thời gian cụ thể nhưng thể hiện **tăng dần phức tạp** theo chiều mũi tên.



Agent không phải “một loại model khác” — đó là LLM được đặt vào vòng làm việc có mục tiêu và hành động


<!-- END PAGE 52 -->


<!-- START PAGE 53 -->

## [Trang 53]


## Giải phẫu một agent: 5 bộ phận là một vòng lặp



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 53]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình tư duy và ra quyết định của hệ thống LLM (Large Language Model)

---
**Các cột mốc / Thành phần chính**:

1. **Goal (Mục tiêu cần đạt)**
   - **Mô tả**: Đầu vào của quá trình tư duy, thể hiện mục tiêu cụ thể cần đạt được.
   - **Kết nối**: Gửi thông tin đến thành phần "Reasoning" (Lý lẽ/chia bước).

2. **Reasoning (Bộ não LLM chia bước)**
   - **Mô tả**: Thành phần xử lý logic, sử dụng bộ não LLM để phân tích và chia nhỏ vấn đề.
   - **Kết nối**:
     - Nhận đầu vào từ "Goal".
     - Sử dụng "Tools" (Tiện ích) để hỗ trợ tìm kiếm, truy vấn API, database, code.
     - Kết quả được gửi đến "Action" (Hành động).

3. **Tools (Tiện ích hỗ trợ)**
   - **Mô tả**: Các công cụ hỗ trợ như:
     - `search`
     - `API`
     - `database`
     - `code`
   - **Kết nối**: Được kích hoạt bởi "Reasoning" để thực hiện các tác vụ cụ thể.

4. **Action (Hành động ra đời thật)**
   - **Mô tả**: Thực thi các hành động dựa trên kết quả phân tích và công cụ hỗ trợ.
   - **Kết nối**:
     - Nhận kết quả từ "Reasoning".
     - Kết quả hành động được quan sát và phản hồi lại cho "Memory" (Bộ nhớ).

5. **Memory (Số tay ghi nhớ các bước)**
   - **Mô tả**: Lưu trữ thông tin từ quá trình trước đó (ghi/dốc) để hỗ trợ vòng lặp tiếp theo.
   - **Kết nối**:
     - Ghi nhận kết quả từ "Action".
     - Cung cấp thông tin cho "Reasoning" qua vòng lặp agent.

---
**Số liệu & Insight quan trọng**:
- **Vòng lặp agent**: Quá trình liên tục giữa "Memory" và "Reasoning" để cải thiện kết quả.
- **Công cụ hỗ trợ**: Các thành phần như `search`, `API`, `database`, `code` được tích hợp để hỗ trợ "Reasoning".
- **Thông tin phản hồi**: Kết quả từ "Action" được quan sát và lập lại thông qua "Memory".

---
**Ý nghĩa bài học**:
Sơ đồ này mô tả quy trình hoạt động của một hệ thống AI dựa trên LLM, trong đó mục tiêu ban đầu được phân tích, hỗ trợ bởi các công cụ và hành động thực thi, đồng thời tích lũy kinh nghiệm qua bộ nhớ để cải thiện hiệu quả. Quá trình này nhấn mạnh vào tính tương tác và vòng lặp liên tục giữa các thành phần để đạt được kết quả tối ưu.
---
```



Agent = Goal + Reasoning + Tools + Memory + Action — chạy thành vòng lặp cho tới khi xong việc


<!-- END PAGE 53 -->


<!-- START PAGE 54 -->

## [Trang 54]


# Voyager: agent tự xây thư viện kỹ năng, rồi sống bằng tái dùng



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 54]**:
```markdown
---
### 1. **Tên/Chủ đề sơ đồ**: Sơ đồ quy trình sử dụng GPT-4 để tự động hóa và cải tiến kỹ năng trong Minecraft (lộn dần theo thời gian)

---

### **Các cột mốc / Thành phần chính**:
1. **GPT-4 - bộ não**
   - **Vai trò**: Đơn vị tư duy chính, tạo ra code mới.
   - **Kết nối**: Nhận đầu vào từ việc phân tích feedback và tạo ra code mới.

2. **Viết code**
   - **Vai trò**: GPT-4 viết code tự động để thực hiện các nhiệm vụ trong Minecraft.
   - **Kết nối**: Code được chuyển đến bước chạy thử nghiệm.

3. **Chạy trong Minecraft**
   - **Vai trò**: Thực thi code trong trò chơi để thu thập feedback.
   - **Chi tiết**: Nếu thất bại, hệ thống sẽ quay lại GPT-4 để sửa lỗi và viết lại code.
   - **Kết nối**: Nếu thành công, dữ liệu được sử dụng để cải tiến thư viện kỹ năng.

4. **Pass / Fail?**
   - **Vai trò**: Đánh giá kết quả thực thi.
   - **Chi tiết**:
     - Nếu thất bại: Quay lại GPT-4 để sửa lỗi.
     - Nếu thành công: Dữ liệu được sử dụng để cải tiến thư viện kỹ năng.

5. **Thư viện kỹ năng (Thứ tự theo thời gian)**
   - **Danh sách kỹ năng hiện tại**:
     - Mine Wood Log
     - Craft Sword
     - Craft Furnace
     - Build Shelter
     - Hunt Cow
   - **Task mới**: Chế tạo bàn chế tác (crafting table).
   - **Kết nối**: Thư viện kỹ năng liên tục được mở rộng và cải tiến dựa trên feedback từ việc chạy code.

6. **Task mới**
   - **Vai trò**: Tạo ra các nhiệm vụ mới để cải tiến liên tục.
   - **Chi tiết**: Ví dụ: Truy xuất top-5 kỹ năng quan trọng để làm nổi bật hơn và tối ưu hóa.

---

### **Số liệu & Insight quan trọng**:
- Công nghệ sử dụng: **GPT-4** (tư duy và viết code).
- Trò chơi ứng dụng: **Minecraft**.
- Phương pháp học tập: **Lộn dần theo thời gian** (từ các nhiệm vụ cơ bản đến phức tạp).
- Kỹ năng hiện tại trong thư viện: 5 kỹ năng (Mining, Crafting, Build, Hunt).
- Task mới: Chế tạo bàn chế tác (crafting table).
- Kết quả học tập: Truy xuất top-5 kỹ năng quan trọng để tối ưu hóa.

---

### **Ý nghĩa bài học**:
Sơ đồ mô tả một quy trình học tập tự động hóa và cải tiến liên tục bằng cách sử dụng trí tuệ nhân tạo (GPT-4) để viết và điều chỉnh code trong Minecraft. Hệ thống này học từ thất bại và thành công, mở rộng thư viện kỹ năng theo thời gian và tự động hóa việc phát triển các nhiệm vụ mới. Điều này minh họa cách AI có thể hỗ trợ học tập và phát triển kỹ năng một cách hiệu quả và tự động.
```

---



Agent giỏi không chỉ vì bộ não to — vì nó tích lũy kỹ năng thành thư viện và tái sử dụng


<!-- END PAGE 54 -->


<!-- START PAGE 55 -->

## [Trang 55]


PHẦN 05

# Landscape: model hôm nay

*giá rơi, năng lực hội tụ, và cuộc đua đang diễn ra*


<!-- END PAGE 55 -->


<!-- START PAGE 56 -->

## [Trang 56]


# 2022 đến nay: tốc độ ra model tăng chóng mặt

Từ một ChatGPT (11/2022) đến hàng chục model mới quý: nhịp ra mắt tăng tốc và làn sóng Trung Quốc



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 56]**:
```markdown
---
### 1. Tên/Chủ đề sơ đồ: **Timeline Phát triển các mô hình AI lớn (LLMs) theo thời gian (2022–2024)**
**Loại:** Biểu đồ Timeline phân loại theo tổ chức và loại mô hình (Closed-source, Open-weight, Open-source).

---

### 2. Các cột mốc / Thành phần chính:
#### **Trục X (Thời gian):**
- Dải thời gian từ **tháng 7/2022** đến **tháng 7/2024**.

#### **Trục Y (Tổ chức phát triển):**
- **OpenAI**
- **Anthropic**
- **Google**
- **xAI (Elon Musk)**
- **Meta**
- **Mistral AI**
- **DeepSeek**
- **AIlabba (Alibaba)**
- **Moonshot AI**
- **Zhipu AI / ZAI**
- **MiniMax**

#### **Ký hiệu mô hình:**
- **★ (Sao trắng):** Mô hình **Closed-source** (Đóng mã nguồn).
- **● (Điểm xanh):** Mô hình **Open-weight** (Trọng số mở, có thể tải về nhưng mã nguồn không hoàn toàn mở).
- **🟡 (Vòng cam):** Mô hình **Open-source** (Mở mã nguồn hoàn toàn).

#### **Các mô hình nổi bật:**
- **OpenAI:**
  - GPT-3.5 (3/11/22 ChatGPT), GPT-4 (3/2023), GPT-4o (Q1/2024), o1-reasoning (2024).
- **Anthropic:**
  - Claude 3 (2024).
- **Google:**
  - Gemini (2023–2024).
- **xAI:**
  - Grok (2024).
- **Meta:**
  - Llama 2 (2023), Llama 3 (2024).
- **Mistral AI:**
  - Mistral 7B (2023), Mistral Large (2024).
- **DeepSeek:**
  - DeepSeek R1 (2024), DeepSeek V4 (2024).
- **Moonshot AI:**
  - Khai thác trọng số mở (Open-weight) từ 2023.
- **Zhipu AI / ZAI:**
  - Mô hình ZAI (2024).
- **MiniMax:**
  - MiniMax (2024).

---

### 3. Số liệu & Insight quan trọng:
- **OpenAI** dẫn đầu về số lượng phiên bản phát hành (4 phiên bản từ GPT-3.5 đến o1-reasoning).
- **Mistral AI** và **DeepSeek** là tổ chức mới nổi (2023–2024) với mô hình mở (Open-source/Open-weight).
- **Meta** tập trung vào Llama series (Llama 2, Llama 3) với chiến lược Open-source.
- **DeepSeek** phát hành **DeepSeek R1 và V4** trong năm 2024, đều là mô hình Open-weight.
- **Moonshot AI** và **Zhipu AI** chủ yếu tập trung vào mô hình Open-weight.
- **Anthropic** và **Google** phát hành mô hình Closed-source (Claude 3, Gemini).

---

### 4. Ý nghĩa bài học:
- **Sự phát triển nhanh chóng của AI:** Trong vòng 2 năm (2022–2024), các tổ chức lớn và nhỏ đã cạnh tranh mạnh về chất lượng và chiến lược mở/đóng mã nguồn.
- **Chiến lược mở (Open-source/Open-weight):** Các mô hình như Llama (Meta), Mistral, DeepSeek cho thấy xu hướng mở mã nguồn để thúc đẩy cộng đồng nghiên cứu và ứng dụng thực tế.
- **Cạnh tranh đa dạng:** Không chỉ các công ty lớn (OpenAI, Google, Meta) mà các tổ chức mới (Mistral AI, Moonshot AI) cũng đóng góp đáng kể vào thị trường AI.
- **Tương lai AI:** Sự đa dạng trong mô hình (Closed-source, Open-weight, Open-source) sẽ định hình cách tiếp cận phát triển và ứng dụng AI trong tương lai.
---
```



Mỗi năm có hàng chục model đáng chú ý — đừng học thuộc tên, hãy học quỹ đạo


<!-- END PAGE 56 -->


<!-- START PAGE 57 -->

## [Trang 57]


# Cùng một mức năng lực, giá rơi khoảng 10 lần mỗi năm



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 57]**:
1. **Tên/Chủ đề sơ đồ**:
   Giá cho một lượng tính toán (~10x/năm) – open-weight (cam) nằm ở tầm ngày (Token input cost comparison for AI models)

---

2. **Các cột mốc / Thành phần chính**:
   - **Trục Y (log)**: Giá tính theo USD cho 1 triệu token input (đơn vị log).
   - **Trục X**: Thời gian và các mô hình AI khác nhau, được chia thành:
     - **Closed-weight (đóng)**: Dùng biểu tượng hình tròn xanh.
     - **Open-weight (mở)**: Dùng biểu tượng hình tròn cam.
     - **Cùng mức lương lý GPT-3.5**: Dùng hình vuông đen.
   - Các mô hình AI được liệt kê theo thời gian và giá:
     - **$20 text-davinci-003 (11/2022)**
     - **GPT-4 ($30)**
     - **Gemini 1.5 Pro ($3.5)**
     - **Claude 3 Haiku ($0.25)**
     - **DeepSeek R1 ($0.55)**
     - **DeepSeek V3 ($0.27)**
     - **DeepSeek V4 ($0.14)**
     - **GPT-4o ($5)**
     - **GPT-4 Turbo ($10)**
     - **GPT-4o ($5)**
     - **GPT-5 ($1.25)**

   - **Dòng thẳng**: Diễn tả sự giảm giá theo công thức ~10x/năm.

---

3. **Số liệu & Insight quan trọng**:
   - Giá tính toán cho các mô hình AI đã giảm mạnh theo thời gian.
   - **Mô hình đắt nhất**: GPT-4 Turbo ($10/1 triệu token).
   - **Mô hình rẻ nhất**: DeepSeek V4 ($0.14/1 triệu token).
   - **Mô hình có giá tương đương với mức lương lý GPT-3.5**: DeepSeek V3 ($0.27).
   - **Mô hình mới nhất (tính đến thời điểm biểu đồ)**: DeepSeek V4 và GPT-5.
   - **Dự đoán giảm giá**: >280 lần trong 2 năm (từ 11/2022 đến 10/2024).

---

4. **Ý nghĩa bài học**:
   Biểu đồ thể hiện xu hướng giảm giá mạnh mẽ của chi phí tính toán cho các mô hình AI theo thời gian, với sự cạnh tranh gay gắt giữa các công ty phát triển. Sự xuất hiện của các mô hình open-weight (mở) và closed-weight (đóng) cũng cho thấy sự đa dạng hóa trong thị trường, cùng với việc dự đoán giảm giá đáng kể trong tương lai gần. Điều này có thể thúc đẩy việc ứng dụng rộng rãi hơn của công nghệ AI trong nhiều lĩnh vực khác nhau.



Việc năm ngoái phải dùng model đắt nhất — năm nay model rẻ đã làm được

Tổng hợp từ bảng giá rơi, nhà cung cấp, 2000-2020


<!-- END PAGE 57 -->


<!-- START PAGE 58 -->

## [Trang 58]


# Năng lực hội tụ — và model mở đang bắt kịp model đóng



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 58]**:
```markdown
---
### 1. **Tên/Chủ đề sơ đồ**:
**Biểu đồ so sánh khoảng cách năng lực bị thu hẹp mạnh trong một năm giữa các mô hình AI (Top-1 vs Top-10 và Open-weight vs Closed)**

---

### 2. **Các cột mốc / Thành phần chính**:
- **Trục Y (Thành phần so sánh)**:
  - Khoảng cách model **Top-1 vs Top-10**.
  - Khoảng cách **Open-weight vs Closed** (một số benchmark).

- **Trục X (Khoảng cách điểm số, %)**:
  - Dữ liệu thể hiện sự cải thiện năng lực (càng sang phải, khoảng cách năng lực bị thu hẹp nhiều hơn).

- **Mốc thời gian**:
  - **Trước (~2023–2024)**: Dữ liệu màu xám.
  - **Sau (~2024–2025)**: Dữ liệu màu xanh.

- **Dữ liệu cụ thể**:
  - **Top-1 vs Top-10**:
    - Trước: **5.4%**.
    - Sau: **11.9%**.
  - **Open-weight vs Closed**:
    - Trước: **1.7%**.
    - Sau: **8%**.

---

### 3. **Số liệu & Insight quan trọng**:
| So sánh                     | Trước (~2023–2024) | Sau (~2024–2025) |
|-----------------------------|--------------------|------------------|
| Top-1 vs Top-10             | 5.4%               | 11.9%            |
| Open-weight vs Closed       | 1.7%               | 8%               |

- **Insight**:
  - Khoảng cách năng lực giữa các mô hình **Top-1 và Top-10** tăng gấp đôi (từ 5.4% lên 11.9%).
  - Khoảng cách giữa **Open-weight và Closed** tăng mạnh từ 1.7% lên 8%, cho thấy sự cải thiện đáng kể trong khả năng của các mô hình mở (open-weight).

---

### 4. **Ý nghĩa bài học**:
- Sự tiến bộ nhanh chóng trong năng lực của các mô hình AI trong thời gian ngắn (~1 năm) khiến khoảng cách năng lực giữa các nhóm mô hình (Top-1 vs Top-10) và giữa các loại mô hình (Open-weight vs Closed) bị thu hẹp mạnh mẽ.
- Các mô hình **Open-weight** đang bắt kịp và vượt qua đáng kể so với các mô hình **Closed**, thể hiện xu hướng mở nguồn (open-source) trở nên cạnh tranh hơn.
- Dữ liệu nhấn mạnh tầm quan trọng của việc theo dõi và cập nhật liên tục trong lĩnh vực AI để không bị tụt hậu về năng lực.
---
```



Nguồn: Stanford HAI AI Index 2025

**Không còn một model bỏ xa phần còn lại — chọn model là bài toán phương pháp, không phải bài toán nhớ tên**

Sắc thái mới: AI Index ghi nhận frontier hội tụ nhưng khoảng cách mở-đóng hơi nói lại 2025 — hai.stanford.edu/ai-index


<!-- END PAGE 58 -->


<!-- START PAGE 59 -->

## [Trang 59]


# Từ model đơn lẻ sang hệ thống biết hành động



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 59]**:
Dưới đây là phân tích và chuyển đổi nội dung của biểu đồ theo yêu cầu:

---
### **1. Tên/Chủ đề sơ đồ**
**Dự báo mở (open-weight) các mô hình AI Trung Quốc (2023) so với các mô hình US/EU (2025–2026)**
*(Tạm dịch: "Làn sóng open-weight Trung Quốc: từ vàng bóng (2023) đến áp đảo nguyên mẫu (2025–2026)")*

---

### **2. Các cột mốc / Thành phần chính**
#### **Trục X (Thời gian)**
- Các khoảng thời gian được chia theo bán kỳ (H1/H2) từ **2023 đến 2026**:
  - 2023H1, 2023H2, 2024H1, 2024H2, 2025H1, 2025H2, 2026H1, 2026H2.

#### **Trục Y (Số liệu đánh giá)**
- Đơn vị: **Số mô hình open-weight** (chưa rõ đơn vị chính xác, có thể là số lượng hoặc điểm đánh giá).
- Màu sắc phân biệt:
  - **Xanh**: US/EU (mô hình đóng - closed-weight).
  - **Xanh nhạt**: US/EU (mô hình mở - open-weight).
  - **Cam**: Trung Quốc (mô hình mở - open-weight).

#### **Các thành phần chính (mô hình)**
- **Mô hình US/EU (closed-weight)**:
  - GPT-4, Claude 2, Gemini 1.0, Llama 2, GPT-4 Turbo, Claude 3 Haiku, GPT-4.5, DeepSeek R1, GPT-5, Gemini 2.0, Claude 4 Opus, GPT-5.5, ...
- **Mô hình US/EU (open-weight)**:
  - LLaMA, Mistral 7B, ...
- **Mô hình Trung Quốc (open-weight)**:
  - Baichuan, DeepSeek, Qwen, InternLM, GLM, ChatGLM, Yiyan, ...

---
### **3. Số liệu & Insight quan trọng**
#### **Dữ liệu theo thời gian**
| Thời điểm       | Mô hình US/EU (closed) | Mô hình US/EU (open) | Mô hình Trung Quốc (open) |
|------------------|------------------------|-----------------------|---------------------------|
| **2023H1**       | 1 (GPT-3.5 Turbo)      | 1 (LLaMA)             | 1 (Baichuan)              |
| **2023H2**       | 3 (Claude 2, GPT-4)     | 2 (Mistral 7B)        | 2 (DeepSeek, Qwen)        |
| **2024H1**       | 3 (Gemini 1.0, ...)     | 1 (Llama 2)           | 3 (InternLM, GLM, ChatGLM) |
| **2024H2**       | 3 (Claude 3 Haiku, ...) | 1 (Mistral 8x)        | 5 (Yiyan, Baichuan 2, ...) |
| **2025H1**       | 2 (GPT-4.5, ...)       | 1 (Gemini 1.5 Pro)    | 7 (DeepSeek R1, Qwen 2, ...)|
| **2025H2**       | 2 (Claude 4 Opus, ...)  | 1 (LLaMA 3)           | 10 (GPT-NeoX, Baichuan 3, ...)|
| **2026H1**       | 1 (GPT-5)              | 1 (Mistral 9)         | 12 (Qwen 3, DeepSeek 2, ...)|
| **2026H2**       | 1 (Gemini 2.0)         | 1 (Claude 5)          | 15 (InternLM 3, ...)       |

#### **Insight quan trọng**
- **2023**: Trung Quốc bắt đầu phát triển mạnh mô hình open-weight (Baichuan, DeepSeek).
- **2024**: Sự gia tăng rõ rệt của mô hình Trung Quốc (InternLM, GLM, ChatGLM).
- **2025**: Trung Quốc vượt xa US/EU trong số lượng mô hình open-weight (từ 7 lên 10 mô hình).
- **2026**: Trung Quốc áp đảo với **15 mô hình open-weight** so với **2 mô hình closed-weight** của US/EU.

---
### **4. Ý nghĩa bài học**
- **Sự cạnh tranh mới**: Trung Quốc đang dẫn đầu trong phát triển mô hình AI mở (open-weight), có thể thay đổi thị trường AI toàn cầu.
- **Tốc độ phát triển**: Làn sóng mô hình AI của Trung Quốc tăng nhanh, đặc biệt từ 2024 trở đi.
- **Chuyển dịch từ closed-weight sang open-weight**: Các mô hình mở (open-weight) có thể trở thành xu hướng chính trong tương lai.

---
> **Ghi chú**: Biểu đồ này nhấn mạnh sự phát triển mạnh mẽ của các mô hình AI Trung Quốc trong thời gian tới, đặc biệt là trong phân khúc open-weight.



Tùy model chọn lọc (không phải điều tra toàn bộ) 2024-05-10 16:17:00

Làn sóng hiện tại không phải 'model nào mạnh hơn' — mà là system nào dùng model khôn hơn


<!-- END PAGE 59 -->


<!-- START PAGE 60 -->

## [Trang 60]


## SWE-bench Verified: từ 33% (6/2024) lên ~81% (2/2026) — rồi chạm trần bão hòa



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 60]**:
```markdown
---
### 1. **Tên/Chủ đề sơ đồ**
**Biểu đồ so sánh hiệu suất các phiên bản mô hình Claude (Anthropic) và Claude Opus trên SWE-bench (Verify)**

---

### **Các cột mốc / Thành phần chính**
- **Trục Y**: Tỷ lệ phần trăm nhiệm vụ được giải quyết thành công trên SWE-bench (Verify), từ 0% đến 100%.
- **Trục X**: Các phiên bản mô hình được phát triển theo thời gian (từ trái sang phải).
- **Dòng Sonnet (Anthropic)**:
  - **Claude 3.5 Sonnet**: 33.4%
  - **Claude 3.5 Sonnet (nâng cấp)**: 49.0%
  - **Claude 3.7 Sonnet**: 62.3%
  - **Claude Sonnet 4**: 72.7%
  - **Claude Sonnet 4.5**: 77.2%
- **Dòng Opus (Frontier)**:
  - **Claude Opus 4.5**: 80.9% (~81%).
- **Ghi chú**:
  - SWE-agent (bản FULL): 12.5% (tham khảo).
  - Dữ liệu OpenAI ngang bằng cao cấp Verified (2/2026).
  - Chú thích về việc sử dụng SWE-bench Pro (dữ liệu repo riêng tư).

---

### **Số liệu & Insight quan trọng**
| Mô hình                     | Tỷ lệ thành công (%) |
|-----------------------------|----------------------|
| Claude 3.5 Sonnet            | 33.4%                |
| Claude 3.5 Sonnet (nâng cấp) | 49.0%                |
| Claude 3.7 Sonnet            | 62.3%                |
| Claude Sonnet 4              | 72.7%                |
| Claude Sonnet 4.5            | 77.2%                |
| Claude Opus 4.5              | 80.9% (~81%)         |
| SWE-agent (FULL)             | 12.5% (tham khảo)    |

- **Tăng trưởng**: Từ Claude 3.5 Sonnet đến Claude Sonnet 4.5, hiệu suất tăng **43.8%** (từ 33.4% lên 77.2%).
- **So sánh Frontier**: Claude Opus 4.5 vượt xa các phiên bản Sonnet với **80.9%**.
- **Scaffolding/Parallel Compute**: Claude Sonnet 4.5 sử dụng tính năng này để cải thiện hiệu suất.

---

### **Ý nghĩa bài học**
1. **Tiến bộ liên tục**: Các phiên bản mới của mô hình Claude thể hiện sự cải thiện rõ rệt trong khả năng giải quyết nhiệm vụ kỹ thuật (SWE-bench).
2. **Giá trị của tính năng nâng cao**: Sử dụng tính năng như *scaffolding/parallel compute* và *Opus* giúp đạt hiệu suất cao hơn đáng kể.
3. **Tham chiếu hiệu suất**: Dữ liệu này cho thấy tầm quan trọng của việc đánh giá mô hình trên các bộ dữ liệu chuyên biệt (như SWE-bench) để đo lường khả năng thực tế trong các nhiệm vụ cụ thể.
```

---
> **Ghi chú**: Biểu đồ này phản ánh sự phát triển của các mô hình AI trong việc xử lý nhiệm vụ kỹ thuật (Software Engineering) và có thể được sử dụng để phân tích xu hướng cải tiến trong lĩnh vực này.



**33% → ~81% chỉ trong 20 tháng — và đang chạm trần bão hòa quanh ~80%: benchmark này sắp “hết khó” để phân biệt model**

Nguồn: SWE-bench Verified = 500 issue GitHub thật, con người đã lọc · điểm công bố chính thức bởi Anthropic (pass@1) · swebench.com — 33.4% (6/2024) → 49.0% (10/2024) → 62.3% → 72.7% → 77.2% → 80.9% → ≈81% (2/2026)


<!-- END PAGE 60 -->


<!-- START PAGE 61 -->

## [Trang 61]


# Kiến trúc từ GPT-3 đến nay: cỗ máy vẫn vậy, cách nuôi đã đổi

**Lỗi Transformer không đổi từ 2017** — như động cơ đốt trong: piston vẫn là piston, nhưng mọi thứ xung quanh được tối ưu điên cuồng.

## Cái gì ĐI LÊN

- 🕒 **Cách đánh số ghế khôn hơn** (RoPE) — model nhớ được câu dài mà không lẫn.
- 🖥️ **Cuốn sổ ghi chú dùng chung** (GQA/MLA) — đọc context dài rẻ đi nhiều lần.
- 🖥️ **Bệnh viện đa khoa** (MoE) — 175 tỷ → 2.800 tỷ tham số, mỗi ca chỉ gọi vài chuyên gia.
- 🖥️ **Bàn làm việc** — từ 2–3 trang (2K) tới 4–5 cuốn sách (1M token).

## Cái gì CHẠM TRẦN → trận đua chuyển hướng

- 🖥️ **Đọc hết sách trong thư viện** (~2024): model đã đọc gần hết văn bản công khai của nhân loại ("data wall") → "to hơn + đọc nhiều hơn" không còn thắng chắc.
- 🖥️ **Trận đua mới ① — luyện để tự chấm** (RLVR): toán có đáp số, code có test → model biết suy luận.
- 🖥️ **Trận đua mới ② — được nghĩ kỹ** (test-time compute): cùng một model, cho nháp và thời gian thì khôn hơn hẳn.

Cuộc cách mạng không phải thay động cơ — mà là: nén dữ liệu hiệu quả hơn · luyện bằng bài tập tự chấm · cho model thời gian đề nghị

Tìm hiểu thêm: RoPE · GQA/MLA · MoE · RLVR · test-time compute — knightli.com — LLM Architecture Evolution 2023–2026 · S. Raschka — The Big LLM Architecture Comparison


<!-- END PAGE 61 -->


<!-- START PAGE 62 -->

## [Trang 62]


# Cuộc đua hiện tại (7/2026): ba câu chuyện đáng nhớ

## Claude Fable 5 — mạnh nhất, nhưng bị khóa

Anthropic ra model tầng mới (9/6/2026), vượt mọi benchmark — **3 ngày sau bị Mỹ export-control tạm khóa toàn cầu**; bản không giới hạn chỉ cấp cho đội cyberdefense. Model khả dụng mạnh nhất hiện là Opus 4.8.

→ *Bài học: phụ thuộc một nhà cung cấp là một rủi ro.*

## GPT-5.6 — tự chia tầng cho bạn

OpenAI (26/6/2026) ra 3 tầng rõ rệt: **Sol** (flagship, reasoning tối đa), **Terra** (ngang GPT-5.5, rẻ một nửa), **Luna** (nhanh-rẻ).

→ *Bài học: chính vendor cũng đang dạy mình 'chọn tầng theo việc' — đúng framework ở slide sau.*

## Kimi K3 — model mở ngang frontier

Moonshot (16/7/2026): 2.800 tỷ tham số MoE, context 1M, **open-weight**, giá chỉ $3/$15 — lần đầu một model mở chơi ngang tốp đầu. Báo chí gọi 'cú sốc DeepSeek mới', nhu cầu quá tải cả GPU.

→ *Bài học: mở đã bắt kịp đóng thật — self-host không còn là chơi riêng.*

*Bản đồ này sẽ cũ trong vài tháng — thứ bền là cách đọc bản đồ: ai mạnh, ai rẻ, ai mở, ai bị khóa*

Tính đến tháng 7/2026 - Fable 5 - GPT-5.6 - Kimi K3


<!-- END PAGE 62 -->


<!-- START PAGE 63 -->

## [Trang 63]


# Từ language model đến multimodal: 'token' không chỉ là chữ

Mọi thứ bạn vừa học — token, context, attention — không chỉ dùng cho chữ viết.

Hãy nhớ lại 'bàn làm việc' của model: ngày xưa nó chỉ bày được chữ. Giờ người ta **cắt ảnh thành những mảnh nhỏ, cắt tiếng thành những đoạn ngắn** — rồi gọi chúng là 'token' y như mảnh chữ, và bày lên đúng cái bàn đó.

**Bộ não bên trong không đổi** — vẫn là cỗ máy đoán token tiếp theo. Chỉ khác là giờ nó 'nhìn' được hình, 'nghe' được tiếng: nên model hôm nay (Fable 5, Kimi K3, Gemini) đọc được ảnh, PDF có biểu đồ, audio, cả video.

![play button icon]() văn bản → token

![play button icon]() ảnh → token

![play button icon]() audio → token

Cùng một cỗ máy đoán-token — đó đầu vào đã vượt ra ngoài văn bản


<!-- END PAGE 63 -->


<!-- START PAGE 64 -->

## [Trang 64]


PHẦN 06

# Chọn model & chi phí token

*framework chọn tầng và token economy*


<!-- END PAGE 64 -->


<!-- START PAGE 65 -->

## [Trang 65]


# Chọn model theo TẦNG, không chọn theo tên

VIỆC CỦA BẠN

Việc đơn giản, khối lượng lớn

phân loại · trích xuất · tóm tắt ngắn

Việc hàng ngày

viết · code · phân tích công việc · automation

Việc khó nhất

suy luận nhiều bước · code phức tạp · tài liệu dài · độ tin cậy cao

Việc cần kiểm soát

dữ liệu nhạy cảm · chi phí ở quy mô lớn

Hai lỗi đối xứng:

× việc đơn giản mà gọi frontier → phí tiền

× việc khó mà cố dùng rẻ → kết quả tệ

TẦNG MODEL

TẦNG 1 — FRONTIER ĐÓNG

Fable 5 · GPT-5.6 Sol · Opus 4.8

đắt nhất — chỉ trả cho việc thật sự khó

★ MẶC ĐỊNH THỨ TẦNG NÀY TRƯỚC

TẦNG 2 — RẺ MÀ MẠNH

Sonnet 4.6 · Terra · Gemini 3.1 Pro · Kimi K3 · Haiku · Flash

giải quyết đa số việc hằng ngày

TẦNG 3 — SELF-HOST / SIÊU RẺ

Kimi K3 open-weight · DeepSeek · Qwen

khi cần kiểm soát dữ liệu hoặc chi phí quy mô lớn

Bắt đầu từ model đủ tốt và đủ rẻ — chỉ nâng tầng khi kết quả thực sự chặn use case


<!-- END PAGE 65 -->


<!-- START PAGE 66 -->

## [Trang 66]


# Ba trực làm model “giỏi hơn” — tham số chỉ là MỘT trong ba

## Trực 1 — Pretraining scale

Cùng ngân sách tính toán (Chinchilla, 2022): model nào thắng?



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 66]**:
```markdown
### Biểu đồ so sánh kích thước tham số của các mô hình ngôn ngữ

- **Tên/Chủ đề sơ đồ**: So sánh số lượng tham số (parameters) của các mô hình ngôn ngữ lớn (LLMs)

- **Các thành phần chính**:
  - **MT-NLG**: 530 tỷ tham số
  - **Gopher**: 280 tỷ tham số
  - **GPT-3**: 175 tỷ tham số
  - **Chinchilla**: 70 tỷ tham số (được đánh dấu là tham khảo số nhật mà **THÀNG CẢ 3**)

- **Số liệu & Insight quan trọng**:
  - MT-NLG có số tham số lớn nhất: **530B**
  - Gopher xếp thứ hai: **280B**
  - GPT-3 có **175B** tham số
  - Chinchilla có **70B** tham số, được nhấn mạnh là "ít tham số nhật mà **THÀNG CẢ 3**"

- **Ý nghĩa bài học**:
  Biểu đồ thể hiện sự phát triển về quy mô tham số của các mô hình ngôn ngữ, từ **70B** (Chinchilla) lên đến **530B** (MT-NLG). Điều này cho thấy xu hướng tăng quy mô để cải thiện khả năng học tập và hiệu suất, đồng thời có thể gợi ý về sự cân nhắc giữa **số lượng tham số** và **hiệu quả tính toán** (như mô hình Chinchilla với số tham số nhỏ hơn nhưng vẫn đạt hiệu suất cao).
```

---
> **Ghi chú**: Dữ liệu "THÀNG CẢ 3" có vẻ là một chú thích riêng, có thể liên quan đến một khái niệm hoặc ví dụ cụ thể trong bài giảng (ví dụ: mô hình Chinchilla hiệu quả hơn với số tham số ít hơn). Nếu cần giải thích thêm, hãy cung cấp ngữ cảnh chi tiết.



Vì được nuôi bằng dữ liệu tương xứng đúng tỉ lệ — to không bằng cân đối.

## Trực 2 — Post-training

CÙNG 175 tỷ tham số, chỉ khác: có RLHF hay không (InstructGPT, 2022)



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 66]**:
```markdown
### Biểu đồ so sánh kích thước tham số của các mô hình ngôn ngữ

- **Tên/Chủ đề sơ đồ**: So sánh số lượng tham số (parameters) của các mô hình ngôn ngữ lớn (LLMs)

- **Các thành phần chính**:
  - **MT-NLG**: 530 tỷ tham số
  - **Gopher**: 280 tỷ tham số
  - **GPT-3**: 175 tỷ tham số
  - **Chinchilla**: 70 tỷ tham số (được đánh dấu là tham khảo số nhật mà **THÀNG CẢ 3**)

- **Số liệu & Insight quan trọng**:
  - MT-NLG có số tham số lớn nhất: **530B**
  - Gopher xếp thứ hai: **280B**
  - GPT-3 có **175B** tham số
  - Chinchilla có **70B** tham số, được nhấn mạnh là "ít tham số nhật mà **THÀNG CẢ 3**"

- **Ý nghĩa bài học**:
  Biểu đồ thể hiện sự phát triển về quy mô tham số của các mô hình ngôn ngữ, từ **70B** (Chinchilla) lên đến **530B** (MT-NLG). Điều này cho thấy xu hướng tăng quy mô để cải thiện khả năng học tập và hiệu suất, đồng thời có thể gợi ý về sự cân nhắc giữa **số lượng tham số** và **hiệu quả tính toán** (như mô hình Chinchilla với số tham số nhỏ hơn nhưng vẫn đạt hiệu suất cao).
```

---
> **Ghi chú**: Dữ liệu "THÀNG CẢ 3" có vẻ là một chú thích riêng, có thể liên quan đến một khái niệm hoặc ví dụ cụ thể trong bài giảng (ví dụ: mô hình Chinchilla hiệu quả hơn với số tham số ít hơn). Nếu cần giải thích thêm, hãy cung cấp ngữ cảnh chi tiết.



Cùng một bộ não — chỉ khác cách uốn nắn mà người dùng ưa hẳn.

## Trực 3 — Test-time / agentic compute

CÙNG một model (Claude Opus 4.8) — chỉ đổi bộ đề / harness



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 66]**:
```markdown
### Biểu đồ so sánh kích thước tham số của các mô hình ngôn ngữ

- **Tên/Chủ đề sơ đồ**: So sánh số lượng tham số (parameters) của các mô hình ngôn ngữ lớn (LLMs)

- **Các thành phần chính**:
  - **MT-NLG**: 530 tỷ tham số
  - **Gopher**: 280 tỷ tham số
  - **GPT-3**: 175 tỷ tham số
  - **Chinchilla**: 70 tỷ tham số (được đánh dấu là tham khảo số nhật mà **THÀNG CẢ 3**)

- **Số liệu & Insight quan trọng**:
  - MT-NLG có số tham số lớn nhất: **530B**
  - Gopher xếp thứ hai: **280B**
  - GPT-3 có **175B** tham số
  - Chinchilla có **70B** tham số, được nhấn mạnh là "ít tham số nhật mà **THÀNG CẢ 3**"

- **Ý nghĩa bài học**:
  Biểu đồ thể hiện sự phát triển về quy mô tham số của các mô hình ngôn ngữ, từ **70B** (Chinchilla) lên đến **530B** (MT-NLG). Điều này cho thấy xu hướng tăng quy mô để cải thiện khả năng học tập và hiệu suất, đồng thời có thể gợi ý về sự cân nhắc giữa **số lượng tham số** và **hiệu quả tính toán** (như mô hình Chinchilla với số tham số nhỏ hơn nhưng vẫn đạt hiệu suất cao).
```

---
> **Ghi chú**: Dữ liệu "THÀNG CẢ 3" có vẻ là một chú thích riêng, có thể liên quan đến một khái niệm hoặc ví dụ cụ thể trong bài giảng (ví dụ: mô hình Chinchilla hiệu quả hơn với số tham số ít hơn). Nếu cần giải thích thêm, hãy cung cấp ngữ cảnh chi tiết.



Đổi cách cho model “được nghỉ kỹ” (agentic harness) → lệch tới 19 điểm cùng một model.

Model “giỏi hơn” không chỉ vì to hơn — còn vì cân đối hơn · được uốn nắn hơn · được nghỉ kỹ hơn

Nguồn: Hoffmann et al. 2022 (Chinchilla) · Ouyang et al. 2022 (InstructGPT) · SWE-bench, Claude Opus 4.8 vendor-reported


<!-- END PAGE 66 -->


<!-- START PAGE 67 -->

## [Trang 67]


# Mixture of Experts: tăng tham số mà không tăng chi phí tính toán

DENSE (truyền thống)



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 67]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình Feed-Forward cho MQI Token

---
**Các cột mốc / Thành phần chính**:
- **Token (Input)**: Đầu vào của hệ thống.
- **Feed-Forward (Quy trình xử lý)**:
  - Khối xử lý chính với mô tả:
    > **"TẤT CẢ tham số hoạt động cho MQI token"**
- **Out (Output)**: Kết quả đầu ra sau khi xử lý.

---
**Số liệu & Insight quan trọng**:
- Không có số liệu cụ thể (số, thời gian, công nghệ) trong sơ đồ.
- Chỉ mô tả khái quát quy trình "Feed-Forward" với vai trò tham số hóa hoạt động của **MQI token**.

---
**Ý nghĩa bài học**:
Sơ đồ thể hiện một quy trình **Feed-Forward** đơn giản, trong đó các tham số hoạt động của **MQI token** được định nghĩa và truyền vào hệ thống để sinh ra kết quả đầu ra. Đây có thể là một mô hình xử lý thông tin hoặc cơ chế điều khiển trong hệ thống token hóa (ví dụ: blockchain, hệ thống quản lý token riêng).
```

---
**Ghi chú bổ sung**:
- Nếu **MQI token** là một khái niệm riêng (ví dụ: token trong một hệ sinh thái cụ thể), cần tham khảo thêm tài liệu liên quan để giải thích chi tiết hơn về quy trình này.



GPT-2 - GPT-3 - Llama 1-3

MIXTURE OF EXPERTS



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 67]**:
```markdown
---
**Tên/Chủ đề sơ đồ**: Sơ đồ quy trình Feed-Forward cho MQI Token

---
**Các cột mốc / Thành phần chính**:
- **Token (Input)**: Đầu vào của hệ thống.
- **Feed-Forward (Quy trình xử lý)**:
  - Khối xử lý chính với mô tả:
    > **"TẤT CẢ tham số hoạt động cho MQI token"**
- **Out (Output)**: Kết quả đầu ra sau khi xử lý.

---
**Số liệu & Insight quan trọng**:
- Không có số liệu cụ thể (số, thời gian, công nghệ) trong sơ đồ.
- Chỉ mô tả khái quát quy trình "Feed-Forward" với vai trò tham số hóa hoạt động của **MQI token**.

---
**Ý nghĩa bài học**:
Sơ đồ thể hiện một quy trình **Feed-Forward** đơn giản, trong đó các tham số hoạt động của **MQI token** được định nghĩa và truyền vào hệ thống để sinh ra kết quả đầu ra. Đây có thể là một mô hình xử lý thông tin hoặc cơ chế điều khiển trong hệ thống token hóa (ví dụ: blockchain, hệ thống quản lý token riêng).
```

---
**Ghi chú bổ sung**:
- Nếu **MQI token** là một khái niệm riêng (ví dụ: token trong một hệ sinh thái cụ thể), cần tham khảo thêm tài liệu liên quan để giải thích chi tiết hơn về quy trình này.



Mixtral - DeepSeek - Llama 4 - Qwen3

Mỗi token chỉ đi qua vài “chuyên gia” (ví dụ 2/8) → tổng tham số rất lớn nhưng chi phí mỗi token gần như model nhỏ


<!-- END PAGE 67 -->


<!-- START PAGE 68 -->

## [Trang 68]


# Token có giá: vé vào rẻ, vé ra đắt gấp 3–5 lần

VÉ VÀO — INPUT

×1

chữ BẠN gửi đi:
prompt · system instruction ·
context · lịch sử chat

rẻ — model chỉ cần đọc

VÉ RA — OUTPUT

×3–5

chữ MODEL viết ra — nó phải
tự sinh từng mảnh một, vừa
chậm vừa tốn

đắt — model phải “vắt óc”

HÓA ĐƠN — 1 LẦN GỌI API

|  input | 1.150 tok × $3 / 1M | $0.00345  |
| --- | --- | --- |
|  output | 200 tok × $15 / 1M | $0.00300  |

TỔNG

≈ $0.0065

số liệu ví dụ — giá thật tùy model & nhà cung cấp

Đọc mục usage trong mỗi response — đó là hóa đơn chi tiết
giúp bạn kiểm soát chi phí từ ngày đầu.

Input tokens + Output tokens = Chi phí mỗi lần gọi — kiểm soát output là núm vặn lớn
nhất


<!-- END PAGE 68 -->


<!-- START PAGE 69 -->

## [Trang 69]


# Prompt dài = hóa đơn dài — mọi thứ cộng dồn mỗi lần gọi

system prompt + context: TRẢ TIỀN LẠI MỖI LẦN GỌI

Lần gọi thứ nhất



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 69]**:
```markdown
---
### **Tên/Chủ đề sơ đồ**: **Cấu trúc token trong mô hình RAG (Retrieval-Augmented Generation)**
---

#### **Các cột mốc / Thành phần chính**:
1. **Câu hỏi của user (50 token)**
   - Dữ liệu đầu vào từ người dùng, chiếm **50 token**.

2. **System prompt (300 token)**
   - Hệ thống chỉ dẫn (ví dụ: hướng dẫn mô hình trả lời, cấu trúc câu trả lời, hoặc các quy tắc xử lý).
   - Chiếm **300 token**.

3. **Context trả số (RAG) (800 token)**
   - Dữ liệu được trích xuất từ cơ sở tri thức (Retrieval) để cung cấp ngữ cảnh cho câu trả lời.
   - Chiếm **800 token** (là thành phần lớn nhất).

4. **Output (200 token)**
   - Kết quả trả lời cuối cùng của mô hình, chiếm **200 token**.

---
#### **Số liệu & Insight quan trọng**:
- **Tổng số token**: **1.350 token**.
- **Phân bố token**:
  - User input: **50 tok** (3.7%).
  - System prompt: **300 tok** (22.2%).
  - Context RAG: **800 tok** (59.3%).
  - Output: **200 tok** (14.8%).
- **Quan sát**: Context RAG chiếm **~60%** tổng số token, cho thấy tính quan trọng của việc trích xuất ngữ cảnh chính xác trong RAG.

---
#### **Ý nghĩa bài học**:
- **Quan trọng của ngữ cảnh (Context)**: Trong mô hình RAG, chất lượng của dữ liệu trích xuất (context) quyết định chất lượng output. Một context dài và chính xác giúp mô hình trả lời chính xác hơn.
- **Hạn chế token**: Các mô hình có giới hạn token (ví dụ: 4k, 8k token), vì vậy cần tối ưu hóa phân bố token giữa các thành phần (user input, system prompt, context) để đảm bảo output chất lượng.
- **Tối ưu hóa prompt**: System prompt nên được thiết kế ngắn gọn nhưng hiệu quả để không chiếm quá nhiều token, để lại không gian cho context và output.
---
```



Lần gọi thứ mười — history đã phình ra



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 69]**:
```markdown
---
### **Tên/Chủ đề sơ đồ**: **Cấu trúc token trong mô hình RAG (Retrieval-Augmented Generation)**
---

#### **Các cột mốc / Thành phần chính**:
1. **Câu hỏi của user (50 token)**
   - Dữ liệu đầu vào từ người dùng, chiếm **50 token**.

2. **System prompt (300 token)**
   - Hệ thống chỉ dẫn (ví dụ: hướng dẫn mô hình trả lời, cấu trúc câu trả lời, hoặc các quy tắc xử lý).
   - Chiếm **300 token**.

3. **Context trả số (RAG) (800 token)**
   - Dữ liệu được trích xuất từ cơ sở tri thức (Retrieval) để cung cấp ngữ cảnh cho câu trả lời.
   - Chiếm **800 token** (là thành phần lớn nhất).

4. **Output (200 token)**
   - Kết quả trả lời cuối cùng của mô hình, chiếm **200 token**.

---
#### **Số liệu & Insight quan trọng**:
- **Tổng số token**: **1.350 token**.
- **Phân bố token**:
  - User input: **50 tok** (3.7%).
  - System prompt: **300 tok** (22.2%).
  - Context RAG: **800 tok** (59.3%).
  - Output: **200 tok** (14.8%).
- **Quan sát**: Context RAG chiếm **~60%** tổng số token, cho thấy tính quan trọng của việc trích xuất ngữ cảnh chính xác trong RAG.

---
#### **Ý nghĩa bài học**:
- **Quan trọng của ngữ cảnh (Context)**: Trong mô hình RAG, chất lượng của dữ liệu trích xuất (context) quyết định chất lượng output. Một context dài và chính xác giúp mô hình trả lời chính xác hơn.
- **Hạn chế token**: Các mô hình có giới hạn token (ví dụ: 4k, 8k token), vì vậy cần tối ưu hóa phân bố token giữa các thành phần (user input, system prompt, context) để đảm bảo output chất lượng.
- **Tối ưu hóa prompt**: System prompt nên được thiết kế ngắn gọn nhưng hiệu quả để không chiếm quá nhiều token, để lại không gian cho context và output.
---
```



Tối ưu chi phí = tối ưu prompt + context — tóm tắt lại thay vì kéo theo cả lịch sử


<!-- END PAGE 69 -->


<!-- START PAGE 70 -->

## [Trang 70]


# Nhiều token hơn = vừa chậm hơn, vừa đắt hơn

## Một núm vặn, hai hệ quả



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 70]**:
1. **Tên/Chủ đề sơ đồ**:
   Biểu đồ so sánh chi phí và độ trẻ (tương đối) của mô hình ngôn ngữ theo số lượng token trong một lần gọi (query).

---

2. **Các cột mốc / Thành phần chính**:
   - **Trục X**: Token trong một lần gọi (từ ít đến nhiều).
   - **Trục Y**:
     - **Chi phí ($)**: Đường cong xanh (tăng nhanh theo hàm mũ).
     - **Độ trẻ (⊙)**: Đường cong nét đứt đỏ (tăng chậm hơn, tuyến tính gần).
   - **3 vùng được nhấn mạnh**:
     - **Context dài hơn**: Phần đầu của trục X, liên quan đến đầu vào dài.
     - **Output dài hơn**: Phần giữa, liên quan đến đầu ra dài.
     - **Model lớn hơn**: Phần cuối, liên quan đến mô hình phức tạp hơn (tăng chi phí nhanh).

---

3. **Số liệu & Insight quan trọng**:
   - **Chi phí ($)**: Tăng theo hàm mũ khi số lượng token tăng, đặc biệt khi mô hình lớn hoặc đầu vào/đầu ra dài.
   - **Độ trẻ (⊙)**: Tăng tuyến tính hoặc gần tuyến tính, không tăng nhanh như chi phí.
   - **Quan hệ**: Chi phí tăng nhanh hơn độ trẻ khi số lượng token hoặc độ phức tạp mô hình tăng.

---
4. **Ý nghĩa bài học**:
   - Khi sử dụng mô hình ngôn ngữ, chi phí tài chính tăng nhanh theo số lượng token và độ phức tạp của mô hình, trong khi độ mới mẻ (độ trẻ) của kết quả tăng chậm hơn.
   - Điều này nhấn mạnh việc cân nhắc giữa đầu vào/đầu ra dài và chi phí khi thiết kế hệ thống sử dụng mô hình ngôn ngữ.
   - Đặc biệt quan trọng khi lựa chọn mô hình lớn, vì chi phí có thể tăng vọt.



Cả hai cùng quy về một thứ: **số token model phải đọc và sinh ra** — đó là 'một núm vặn'.

## Ví dụ tiền thật — chatbot 1.000 lượt/ngày

1.350 tok × 1.000 lượt × 30 ngày = **40 triệu token/tháng**



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 70]**:
1. **Tên/Chủ đề sơ đồ**:
   Biểu đồ so sánh chi phí và độ trẻ (tương đối) của mô hình ngôn ngữ theo số lượng token trong một lần gọi (query).

---

2. **Các cột mốc / Thành phần chính**:
   - **Trục X**: Token trong một lần gọi (từ ít đến nhiều).
   - **Trục Y**:
     - **Chi phí ($)**: Đường cong xanh (tăng nhanh theo hàm mũ).
     - **Độ trẻ (⊙)**: Đường cong nét đứt đỏ (tăng chậm hơn, tuyến tính gần).
   - **3 vùng được nhấn mạnh**:
     - **Context dài hơn**: Phần đầu của trục X, liên quan đến đầu vào dài.
     - **Output dài hơn**: Phần giữa, liên quan đến đầu ra dài.
     - **Model lớn hơn**: Phần cuối, liên quan đến mô hình phức tạp hơn (tăng chi phí nhanh).

---

3. **Số liệu & Insight quan trọng**:
   - **Chi phí ($)**: Tăng theo hàm mũ khi số lượng token tăng, đặc biệt khi mô hình lớn hoặc đầu vào/đầu ra dài.
   - **Độ trẻ (⊙)**: Tăng tuyến tính hoặc gần tuyến tính, không tăng nhanh như chi phí.
   - **Quan hệ**: Chi phí tăng nhanh hơn độ trẻ khi số lượng token hoặc độ phức tạp mô hình tăng.

---
4. **Ý nghĩa bài học**:
   - Khi sử dụng mô hình ngôn ngữ, chi phí tài chính tăng nhanh theo số lượng token và độ phức tạp của mô hình, trong khi độ mới mẻ (độ trẻ) của kết quả tăng chậm hơn.
   - Điều này nhấn mạnh việc cân nhắc giữa đầu vào/đầu ra dài và chi phí khi thiết kế hệ thống sử dụng mô hình ngôn ngữ.
   - Đặc biệt quan trọng khi lựa chọn mô hình lớn, vì chi phí có thể tăng vọt.



Cùng một việc **đủ tốt**, giá 3/2026 — chọn sai tầng là trả đắt gấp ~4 lần **mỗi tháng**. Slide chọn tầng vừa rồi không phải lý thuyết — nó là tiền thật.

**Cái gì làm chậm cũng làm đắt → tối ưu cả hai cùng lúc bằng cách tiết kiệm token**


<!-- END PAGE 70 -->


<!-- START PAGE 71 -->

## [Trang 71]


# Cùng một prompt — ba model, ba phong cách trả lời

Prompt: “Tóm tắt báo cáo tài chính Q1 trong 3 bullet và nêu 1 rủi ro chính.”

## Claude consulting style

### Tóm tắt Q1:

1. **Doanh thu:** +12% nhờ kênh online
2. **Chi phí vận hành:** -8% sau tình gọn
3. **Dòng tiền:** cải thiện, đủ 6 tháng vận hành

**Rủi ro chính:** tồn kho tăng 20% — cần phương án xử lý trong Q2.

Mạch lạc, thiên cấu trúc → hợp phân tích, viết tài liệu dài

## GPT ngắn gọn · tự nhiên

- Q1 khá ổn: doanh thu +12%, chi phí -8%, dòng tiền dương.
- Điểm sáng lớn nhất là kênh online.
- Rủi ro chính: tồn kho +20%, nên xả bớt trong Q2.

Nói gọn: ổn — nhưng coi chừng kho hàng. 👍

Tự nhiên, linh hoạt → hợp app/chat đa dạng, hệ sinh thái lớn

## Gemini / Kimi mạnh context dài

Đối chiếu **40 trang báo cáo + 3 file đính kèm**:

- DT +12%; online chiếm 61% tổng DT
- Chi phí -8% nhờ tình gọn 2 kho
- Dòng tiền dương, đủ 6 tháng

Rủi ro chính: tồn kho +20% — vượt ngưỡng an toàn (mục 7.2).

Bám nhiều tài liệu → hợp workflow nhiều file, cửa sổ 1M token

**Chọn model không chỉ là chọn giá và điểm số — còn là chọn phong cách**

Bài tập về nhà: lấy một prompt trong công việc của bạn, chạy thử trên 2–3 model, so sánh. Phong cách thay đổi theo thế hệ model.


<!-- END PAGE 71 -->


<!-- START PAGE 72 -->

## [Trang 72]


# Benchmark có đáng tin không? — tin vừa thôi

## 1 Model học vẹt đường tắt

Điểm cao có thể nhờ ấn gian dữ liệu (spurious cues) — như slide 'học vẹt' vừa rồi.

## 2 Để thi bị bão hòa

SWE-bench Verified: 33% → ~81% trong 20 tháng → sắp 'hết khó' để phân biệt model, phải ra để mới (SWE-bench Pro).

## 3 Học tủ để (benchmaxxing)

Model có thể được luyện đúng dạng để dễ ăn điểm — điểm tăng không hẳn năng lực tăng.

Ví dụ profile không phẳng (2023): GPT-4 đỗ **Bar exam** (kỳ thi luật sư Mỹ) ở top 10% — nhưng **Codeforces** (thi lập trình thi đấu) dưới 5%. Điểm cao ở kỳ thi này không nói gì về kỳ thi khác.

> Benchmark là tín hiệu, không phải bằng chứng. Chỉ có một bài test đáng tin hoàn toàn: việc của chính bạn, trên dữ liệu của chính bạn.

Nguồn: swebench.com · Zhong et al. (2022), ICML · Stanford AI Index.


<!-- END PAGE 72 -->


<!-- START PAGE 73 -->

## [Trang 73]


PHẦN 07

# Gọi API lần đầu

*điều khiển một vòng next-token từ xa*


<!-- END PAGE 73 -->


<!-- START PAGE 74 -->

## [Trang 74]


## Một lần gọi API diễn ra thế nào?



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 74]**:
```markdown
---
### **1. Tên/Chủ đề sơ đồ**
**Quy trình tương tác với mô hình AI dựa trên token stream**
*(Ví dụ: Chatbot/API gọi model sinh token để trả lời)*

---
### **2. Các cột mốc / Thành phần chính**
Sơ đồ mô tả **4 bước** trong quá trình tương tác với mô hình AI (trục X theo thứ tự thời gian):

1. **Prompt (Bước 1)**
   - **Nội dung**: `system + user + context`
   - **Mô tả**: Dữ liệu đầu vào bao gồm:
     - **System**: Cài đặt hệ thống (vd: vai trò của AI).
     - **User**: Nhập liệu của người dùng.
     - **Context**: Bối cảnh liên quan (nếu có).

2. **API call (Bước 2)**
   - **Nội dung**: `gửi request tới provider`
   - **Mô tả**: Người dùng/giao diện gửi yêu cầu đến API của nhà cung cấp mô hình (vd: OpenAI, Hugging Face).

3. **Token stream (Bước 3)**
   - **Nội dung**: `model sinh từng mãnh` *(tạm dịch: model sinh token từng phần)*
   - **Mô tả**:
     - Mô hình AI xử lý `Prompt` và **trả về token một cách luồng (stream)**.
     - Token được sinh ra **từng phần** (không chờ đợi toàn bộ câu trả lời).
     - Ứng dụng thực tế: Hiển thị kết quả **tương tác tức thời** (vd: chatbot gõ từng từ).

4. **Response (Bước 4)**
   - **Nội dung**: `nội dung + usage + lý do dùng`
   - **Mô tả**:
     - **Nội dung (Content)**: Trả lời cuối cùng của mô hình.
     - **Usage**: Thông tin chi phí/tài nguyên sử dụng (vd: số token).
     - **Lý do dùng (Reason)**: Dữ liệu phân tích (vd: độ tin cậy, nguồn gốc).

---
### **3. Số liệu & Insight quan trọng**
- **Không có số liệu cụ thể** trong hình, nhưng quy trình áp dụng cho:
  - **Công nghệ**: API mô hình ngôn ngữ lớn (LLM) như GPT, Llama.
  - **Kiến trúc**: **Streaming response** (luồng token) thay vì chờ đợi toàn bộ câu trả lời.
  - **Ưu điểm**: Trải nghiệm người dùng **gần thực thời**, tiết kiệm băng thông.

---
### **4. Ý nghĩa bài học**
- **Quy trình tương tác AI** không chỉ là "gửi yêu cầu - nhận trả lời" mà là **luồng dữ liệu động** (token stream).
- **Ứng dụng thực tế**:
  - Tối ưu hóa **trải nghiệm người dùng** (vd: chatbot, trợ lý ảo).
  - Quản lý **tài nguyên** (biết khi nào model bắt đầu/giữa/kết thúc sinh token).
  - Hiểu cơ chế **API gọi model** để tích hợp vào hệ thống (vd: frontend + backend).

---
```
> **Ghi chú**: Sơ đồ phù hợp cho bài giảng về **Cơ sở dữ liệu/Kỹ thuật AI**, **Phát triển ứng dụng chatbot**, hoặc **Kiến trúc hệ thống cloud**.



Gọi API = điều khiển một vòng next-token từ xa — không phép màu, đúng cơ chế mình vừa học

Mỗi API call luôn có 3 thứ phải kiểm soát cùng lúc: **chất lượng** — **độ trễ** — **chi phí**.


<!-- END PAGE 74 -->


<!-- START PAGE 75 -->

## [Trang 75]


# Giải phẫu một prompt: bốn lớp xếp chồng

1 PROMPT = 4 PHẦN

**LỚP 1**
**System instruction**

“Lời dặn đầu ca”: model là ai, cư xử thế nào, không được làm gì

«Bạn là trợ lý y khoa, trả lời ngắn gọn, không chẩn đoán...»

**LỚP 2**
**User input**

Câu hỏi / yêu cầu của người dùng trong lượt này

«Tóm tắt báo cáo Q1 giúp mình»

**LỚP 3**
**Context bổ sung**

Tài liệu, lịch sử chat, dữ liệu tra số — phần bày lên “bàn làm việc”

«[đính kèm: bao_cao_q1.pdf – 3 đoạn liên quan]»

**LỚP 4**
**Output mong muốn**

Dạng kết quả: gạch đầu dòng? bảng? JSON? dài bao nhiêu?

«3 bullet + 1 rủi ro chính, tiếng Việt»

Viết rõ cả 4 lớp = đã làm tốt một nửa “prompt engineering” — **phần còn lại là các ngày sau**


<!-- END PAGE 75 -->


<!-- START PAGE 76 -->

## [Trang 76]


# Giải phẫu một API call: gói thư gửi và gói thư về

MÁY BẠN

gói thư GỬI

SERVER PROVIDER

gói thư VỀ

MÁY BẠN

REQUEST — gói thư gửi đi

POST api.openai.com/v1/chat/completions
{
  "model": "gpt-5.6-terra", ①
  "messages": [ ②
    { "role": "system", "content": "Bạn là trợ lý tài chính,
    trả lời ngắn gọn." },
    { "role": "user", "content": "Tóm tắt báo cáo Q1: 3
    bullet + 1 rủi ro." }
  ],
  "max_tokens": 500, ③
  "temperature": 0 ④
}

① tên model — "số tổng đài" · ② 3 vai trò: system / user / assistant
③ trần độ dài trả lời · ④ độ "liều" (0 = ổn định)

RESPONSE — gói thư nhận về

{
  "choices": [{
    "message": { "role": "assistant",
    "content": "• Doanh thu Q1 +12%...\n• Chi phí -8%...
\n• Rủi ro: tốn kho +20%." }, ⑤
    "finish_reason": "stop" ⑥
  }],
  "usage": { ⑦
    "prompt_tokens": 1150, // vé vào
    "completion_tokens": 200, // vé ra
    "total_tokens": 1350
  }
}

⑤ câu trả lời ở choices[0].message.content
⑥ stop = tự kết thúc | length = hết hạn mức | tool_calls · ⑦ hóa đơn chi tiết

Đọc usage mỗi lần gọi — đừng để cuối tháng mới giật mình nhìn hóa đơn

platform.openai.com/docs/.../docs/anthropic.com


<!-- END PAGE 76 -->


<!-- START PAGE 77 -->

## [Trang 77]


# Hai núm vặn chọn từ: temperature & top_p

## temperature — “núm vặn độ liều”

Cùng một câu: “Một tách ___” — bảng xác suất đổi theo T

T = 0



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 77]**:
```markdown
> 📊 *[Biểu đồ cột đơn giản]*

- **Tên/Chủ đề sơ đồ**: Biểu đồ so sánh 4 danh từ trong tiếng Việt (cả phê, trà, múa, sao)
- **Các cột mốc / Thành phần chính**:
  - Trục X: Danh từ (cả phê, trà, múa, sao)
  - Trục Y: Giá trị tương đối (chỉ có "cả phê" có cột màu xanh, các mục khác không có giá trị)
- **Số liệu & Insight quan trọng**:
  - "Cả phê" có giá trị cao nhất (cột màu xanh)
  - "Trà", "múa", "sao" có giá trị bằng 0 (không biểu thị)
- **Ý nghĩa bài học**:
  - Biểu đồ thể hiện sự khác biệt về giá trị giữa các danh từ.
  - Có thể minh họa cho chủ đề về sự ưu tiên, phổ biến hoặc giá trị trong một ngữ cảnh cụ thể (ví dụ: "cả phê" có ý nghĩa đặc biệt trong bài học).
```

---
> **Ghi chú**: Nếu đây là biểu đồ minh họa trong giáo trình, có thể liên quan đến chủ đề về **từ vựng, văn hóa, hoặc giá trị xã hội** trong tiếng Việt. Nếu có ngữ cảnh chi tiết hơn, hãy cung cấp để phân tích chính xác hơn.



luôn chọn từ **chắc nhất** → ổn định, lặp lại, hợp code & phân tích

T = 1



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 77]**:
```markdown
> 📊 *[Biểu đồ cột đơn giản]*

- **Tên/Chủ đề sơ đồ**: Biểu đồ so sánh 4 danh từ trong tiếng Việt (cả phê, trà, múa, sao)
- **Các cột mốc / Thành phần chính**:
  - Trục X: Danh từ (cả phê, trà, múa, sao)
  - Trục Y: Giá trị tương đối (chỉ có "cả phê" có cột màu xanh, các mục khác không có giá trị)
- **Số liệu & Insight quan trọng**:
  - "Cả phê" có giá trị cao nhất (cột màu xanh)
  - "Trà", "múa", "sao" có giá trị bằng 0 (không biểu thị)
- **Ý nghĩa bài học**:
  - Biểu đồ thể hiện sự khác biệt về giá trị giữa các danh từ.
  - Có thể minh họa cho chủ đề về sự ưu tiên, phổ biến hoặc giá trị trong một ngữ cảnh cụ thể (ví dụ: "cả phê" có ý nghĩa đặc biệt trong bài học).
```

---
> **Ghi chú**: Nếu đây là biểu đồ minh họa trong giáo trình, có thể liên quan đến chủ đề về **từ vựng, văn hóa, hoặc giá trị xã hội** trong tiếng Việt. Nếu có ngữ cảnh chi tiết hơn, hãy cung cấp để phân tích chính xác hơn.



cân bằng tự nhiên — vẫn ưu tiên từ hợp lý

T = 2



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 77]**:
```markdown
> 📊 *[Biểu đồ cột đơn giản]*

- **Tên/Chủ đề sơ đồ**: Biểu đồ so sánh 4 danh từ trong tiếng Việt (cả phê, trà, múa, sao)
- **Các cột mốc / Thành phần chính**:
  - Trục X: Danh từ (cả phê, trà, múa, sao)
  - Trục Y: Giá trị tương đối (chỉ có "cả phê" có cột màu xanh, các mục khác không có giá trị)
- **Số liệu & Insight quan trọng**:
  - "Cả phê" có giá trị cao nhất (cột màu xanh)
  - "Trà", "múa", "sao" có giá trị bằng 0 (không biểu thị)
- **Ý nghĩa bài học**:
  - Biểu đồ thể hiện sự khác biệt về giá trị giữa các danh từ.
  - Có thể minh họa cho chủ đề về sự ưu tiên, phổ biến hoặc giá trị trong một ngữ cảnh cụ thể (ví dụ: "cả phê" có ý nghĩa đặc biệt trong bài học).
```

---
> **Ghi chú**: Nếu đây là biểu đồ minh họa trong giáo trình, có thể liên quan đến chủ đề về **từ vựng, văn hóa, hoặc giá trị xã hội** trong tiếng Việt. Nếu có ngữ cảnh chi tiết hơn, hãy cung cấp để phân tích chính xác hơn.



phân bố **phẳng ra** → đa dạng, “phiêu”, dễ lạc đề

## top_p — “chỉ xem top đầu bảng” (p = 0.9)

① Bảng xác suất gốc

giữ nhóm cộng dồn ≥ 90%



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 77]**:
```markdown
> 📊 *[Biểu đồ cột đơn giản]*

- **Tên/Chủ đề sơ đồ**: Biểu đồ so sánh 4 danh từ trong tiếng Việt (cả phê, trà, múa, sao)
- **Các cột mốc / Thành phần chính**:
  - Trục X: Danh từ (cả phê, trà, múa, sao)
  - Trục Y: Giá trị tương đối (chỉ có "cả phê" có cột màu xanh, các mục khác không có giá trị)
- **Số liệu & Insight quan trọng**:
  - "Cả phê" có giá trị cao nhất (cột màu xanh)
  - "Trà", "múa", "sao" có giá trị bằng 0 (không biểu thị)
- **Ý nghĩa bài học**:
  - Biểu đồ thể hiện sự khác biệt về giá trị giữa các danh từ.
  - Có thể minh họa cho chủ đề về sự ưu tiên, phổ biến hoặc giá trị trong một ngữ cảnh cụ thể (ví dụ: "cả phê" có ý nghĩa đặc biệt trong bài học).
```

---
> **Ghi chú**: Nếu đây là biểu đồ minh họa trong giáo trình, có thể liên quan đến chủ đề về **từ vựng, văn hóa, hoặc giá trị xã hội** trong tiếng Việt. Nếu có ngữ cảnh chi tiết hơn, hãy cung cấp để phân tích chính xác hơn.



② Bảng mới

→ cắt & chuẩn hóa lại



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 77]**:
```markdown
> 📊 *[Biểu đồ cột đơn giản]*

- **Tên/Chủ đề sơ đồ**: Biểu đồ so sánh 4 danh từ trong tiếng Việt (cả phê, trà, múa, sao)
- **Các cột mốc / Thành phần chính**:
  - Trục X: Danh từ (cả phê, trà, múa, sao)
  - Trục Y: Giá trị tương đối (chỉ có "cả phê" có cột màu xanh, các mục khác không có giá trị)
- **Số liệu & Insight quan trọng**:
  - "Cả phê" có giá trị cao nhất (cột màu xanh)
  - "Trà", "múa", "sao" có giá trị bằng 0 (không biểu thị)
- **Ý nghĩa bài học**:
  - Biểu đồ thể hiện sự khác biệt về giá trị giữa các danh từ.
  - Có thể minh họa cho chủ đề về sự ưu tiên, phổ biến hoặc giá trị trong một ngữ cảnh cụ thể (ví dụ: "cả phê" có ý nghĩa đặc biệt trong bài học).
```

---
> **Ghi chú**: Nếu đây là biểu đồ minh họa trong giáo trình, có thể liên quan đến chủ đề về **từ vựng, văn hóa, hoặc giá trị xã hội** trong tiếng Việt. Nếu có ngữ cảnh chi tiết hơn, hãy cung cấp để phân tích chính xác hơn.



“sao” (đuôi dài xác suất thấp) **bị loại khỏi lựa chọn** — model chỉ còn chọn trong nhóm đáng tin. Thường chỉ vặn **một trong hai**: temperature hoặc top_p.

**Lưu ý quan trọng:** hai núm này không làm model thông minh hơn — chỉ đổi **cách chọn từ**, không thêm tri thức.

Mặc định an toàn: **temperature = 0** cho việc cần ổn định — chỉ tăng khi thật sự cần đa dạng


<!-- END PAGE 77 -->


<!-- START PAGE 78 -->

## [Trang 78]


# Chatbot = vòng lặp + trí nhớ; streaming = nhà chữ từng mảnh

“Trí nhớ” của chatbot đến từ đâu?

user: “kể chuyện cười”

① nối vào history

HISTORY — MÌNH TỰ GIỮ

system: bạn là bot vui

user: kể chuyện cười

assistant: con gà qua đường...

user: câu nữa ← lượt mới

② gửi TOÀN BỘ history

MODEL
stateless

③ trả lời → nối tiếp vào history

Streaming — next-token nhìn tận mắt



> 🖼️ **[Mô tả Đa phương thức cho Ảnh/Biểu đồ trang 78]**:
Dưới đây là nội dung trích xuất từ ảnh dưới dạng Markdown:

```markdown
# Nội dung chatbot (tiếng Việt)

**Hôm nay** **mình** **học** **về** `token` !

< *chú niên dẫn từng mảnh, ngày khi model sinh ra* >
```

### Giải thích:
- Đây là một đoạn hội thoại chatbot (dạng streaming) trong giao diện terminal.
- Nội dung chính là một câu giới thiệu về khái niệm **token** trong ngôn ngữ NLP.
- Dòng cuối (`< chú niên dẫn từng mảnh, ngày khi model sinh ra>`) có vẻ là một ghi chú phụ hoặc thông tin bổ sung về quá trình sinh ra model (có thể liên quan đến cách token hóa hoặc lịch sử phát triển của mô hình).

---
**Nếu cần phân tích sâu hơn về khái niệm token trong NLP, có thể bổ sung:**
- Token là đơn vị nhỏ nhất trong xử lý ngôn ngữ tự nhiên (NLP), có thể là từ, từ ghép, hoặc ký tự phụ thuộc vào mô hình.
- Ví dụ: "Hôm nay" → ["Hôm", "nay"] hoặc ["Hôm_nay"] (tùy thuật toán tokenizer).



Đây chính là bản chất next-token: model đoán → nhà một mảnh → đoán tiếp. Giao diện “đang gõ” chỉ là lộ trình của vòng lặp.

Model không nhớ gì giữa hai lần gọi — “trí nhớ” là do MÌNH gửi lại history mỗi lần


<!-- END PAGE 78 -->


<!-- START PAGE 79 -->

## [Trang 79]


# Hai "số tổng đài" lớn — và khi nào tự nuôi model tại nhà

OpenAI vs Anthropic — cú pháp tương đương

Cùng một logic: gửi messages, nhận content + usage. Khác tên hàm và cách bóc kết quả:

OpenAI: client.chat.completions.create(...) →
.choices[0].message.content
Anthropic: client.messages.create(...) →
.content[0].text

Self-host (open-weight)

Tài "bộ não" mở (Kimi K3, Qwen, Llama) về chạy trên máy mình:

- ✓ dữ liệu không rời khỏi tay bạn
- ✓ không trả tiền theo token
- ✗ tự lo GPU, vận hành, cập nhật

Đổi base_url (số tổng đài) là code gọi API chuyển sang model tự host gần như nguyên vẹn.

API không chỉ là cách gọi model — đó là mức quyền truy cập bạn có với model đó


<!-- END PAGE 79 -->


<!-- START PAGE 80 -->

## [Trang 80]


PHẦN 08

# Tổng kết

*những ý để mang về*


<!-- END PAGE 80 -->


<!-- START PAGE 81 -->

## [Trang 81]


## Key takeaways — 5 ý để mang về

1. LLM = cỗ máy Transformer **đoán token tiếp theo từ context** — mọi thứ khác là hệ quả.
2. Từ cỗ máy đoán chữ thành trợ lý: pre-training → SFT → căn chỉnh → **luyện để tự chấm & được nghị kỹ**.
3. Model có giới hạn bẩm sinh: bong bóng thời gian, nói chắc như đúng rồi, bàn làm việc có hạn — nên **đừng tin benchmark, hãy tự test**.
4. Chọn model theo **tầng theo việc**, kiểm soát 3 núm: **chất lượng — độ trễ — chi phí**.
5. Gọi API là **điều khiển một vòng next-token từ xa** — kèm một mức quyền truy cập nhất định vào model.


<!-- END PAGE 81 -->


<!-- START PAGE 82 -->

## [Trang 82]


TRẢ LỜI CÂU HỎI ĐẦU NGÀY

## 'Bên trong AI đang làm gì?'

— một vòng lặp đoán token, được nuôi bằng dữ liệu, đang chờ bạn điều khiển.

Buổi chiều nay, bạn sẽ trả lời câu hỏi đó bằng hành động: **gọi API đầu tiên và build chatbot của chính mình.**

Một lời nhắc nhở mang theo: dữ liệu là mạch sống của model nhưng cũng là phần kém minh bạch nhất. Model nền là điểm đòn bẩy lớn — và cũng có thể là điểm lỗi lan xuống mọi ứng dụng. Evaluation, guardrails và system design không bao giờ là phần phụ.

Sáng nay bạn đã hiểu AI đang làm gì. Chiều nay — điều khiển nó bằng chính tay bạn.


<!-- END PAGE 82 -->


<!-- START PAGE 83 -->

## [Trang 83]


# Appendix — xem & đọc thêm sau buổi học

## Nên xem & chơi trước (khuyên bắt đầu từ đây)

**3Blue1Brown — Transformers, the tech behind LLMs** · video giải thích Transformer bằng hình động để hiểu nhất hiện nay — youtube.com/watch?v=wjZofJX0v4M

**3Blue1Brown — Attention in transformers, step-by-step** · phần tiếp theo, đi sâu vào attention — youtube.com/watch?v=eMlx5fFNoYc

**Transformer Explainer** · chạy GPT-2 ngay trong trình duyệt: tự chỉnh temperature, xem next-token probs và attention map — poloclub.github.io/transformer-explainer

**Karpathy — nanoGPT & State of GPT** · người giải thích lại mọi thứ này bằng code chạy được — github.com/karpathy/nanoGPT · youtube

## Paper nền tảng

**Attention Is All You Need** (Vaswani et al., 2017) · paper khai sinh Transformer — chữ T trong GPT — arxiv.org/abs/1706.03762

**InstructGPT** (Ouyang et al., 2022) · vì sao ChatGPT biết nghe lời — arxiv.org/abs/2203.02155 · **DPO** (2023) — arxiv.org/abs/2305.18290

**Emergent World Representations** (Li et al., ICLR 2023) · Othello-GPT — bằng chứng model tự xây world model — arxiv.org/abs/2210.13382 · bản đọc dễ hơn: The Gradient

**On the Dangers of Stochastic Parrots** (Bender et al., FAccT 2021) · phía phân biện nổi tiếng — doi.org/10.1145/3442188.3445922

## Đào sâu thêm

**Probe & can thiệp Othello-GPT** — Nanda et al. 2023 · **Diffusion model 'thấy' thế giới từ step 1** — arxiv.org/abs/2306.05720 · **Dynamometer car** — Viégas & Wattenberg 2023

**Dùng LLM để hiểu LLM** (Steinhardt, BAIR) — arxiv.org/abs/2302.14233 · bài nói · **Gán nhãn attention head CLIP** — arxiv.org/abs/2310.05916 · **Representation Engineering / ITI** — arxiv.org/abs/2306.03341 · arxiv.org/abs/2310.01405

## Số liệu & bảng giá (7/2026)

**Bảng model & giá (7/2026):** Fable 5 $10/$50 (tạm khóa export-control) · GPT-5.6 Sol/Terra/Luna · Opus 4.8 $5/$25 · Sonnet 4.6 $3/$15 · Haiku 4.5 $0.8/$4 · Gemini 3.1 Pro $2/$12 · Kimi K3 $3/$15 open-weight · DeepSeek V3 (API siêu rẻ)

**Stanford AI Index** — hai.stanford.edu/ai-index · **SWE-bench** — swebench.com · **Giá API** — openai.com/api/pricing · anthropic.com/pricing · **AI 2027** — ai-2027.com (kịch bản gây tranh luận — đọc phân biện)


<!-- END PAGE 83 -->
