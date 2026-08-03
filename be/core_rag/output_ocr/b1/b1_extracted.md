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

![img-0.jpeg](img-0.jpeg)

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

![img-1.jpeg](img-1.jpeg)

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

![img-2.jpeg](img-2.jpeg)

2 lần mùa đông, cách tiếp cận chậm trễ

Từ model đơn lẻ sang system có khả năng hành động như agent


<!-- END PAGE 9 -->


<!-- START PAGE 10 -->

## [Trang 10]


# 1956: Dartmouth Workshop

![img-3.jpeg](img-3.jpeg)


<!-- END PAGE 10 -->


<!-- START PAGE 11 -->

## [Trang 11]


# 1969: Perceptrons

![img-4.jpeg](img-4.jpeg)

Các hướng đi lần lượt **chạm trần**:

- **Hướng symbolic** (dạy máy bằng luật/quy tắc): bắt đầu đuổi trước thế giới quá nhiều ngữ cảnh
- **Hướng Perceptron** (thay vì viết hết luật, mình có thể cho máy học từ ví dụ) cũng gặp vấn đề vì quá đơn giản


<!-- END PAGE 11 -->


<!-- START PAGE 12 -->

## [Trang 12]


# 1973: Báo cáo Lighthill — cú hích kết thúc kỳ lạc quan đầu

![img-5.jpeg](img-5.jpeg)

Chính phủ Anh nhờ James Lighthill đánh giá lại toàn ngành AI. Ông kết luận thẳng: **những gì AI làm được đi quá xa so với lời hứa.**

Nguồn tiền đổ vào AI ở Anh và Mỹ bị cắt mạnh → mở màn **mùa đông AI lần thứ nhất.**


<!-- END PAGE 12 -->


<!-- START PAGE 13 -->

## [Trang 13]


# Mùa đông AI lần 1: 1974-1980

![img-6.jpeg](img-6.jpeg)

Bài toán nhỏ — trông khá thông minh ✓

![img-7.jpeg](img-7.jpeg)

Ít nhanh, máy duyệt hết được → kết quả trông “thông minh”.

Thế giới thật — mỗi bước sinh ra quá nhiều nhánh

![img-8.jpeg](img-8.jpeg)

## BÙNG NỔ TỐ HỢP

![img-9.jpeg](img-9.jpeg)


<!-- END PAGE 13 -->


<!-- START PAGE 14 -->

## [Trang 14]


# 1980: Hệ chuyên gia (expert system)

![img-10.jpeg](img-10.jpeg)

Đặt lại vấn đề: 'Nếu AI chỉ giải thật tốt một loại bài toán chuyên môn hẹp thì sao?'

→ Sự ra đời của **expert systems**

AI đổi chiến lược: thôi theo đuổi trí tuệ tổng quát và **tập trung giải thật tốt một miền hẹp** bằng cách mã hóa tri thức chuyên gia thành luật


<!-- END PAGE 14 -->


<!-- START PAGE 15 -->

## [Trang 15]


## Mùa đông AI lần 2

![img-11.jpeg](img-11.jpeg)

Expert systems từng tạo ra giá trị thật, nhưng càng mở rộng thì càng lộ trần: tri thức phải nhập bằng tay, luật càng nhiều càng khó cập nhật, và hệ thống khó đứng vững trước ngoại lệ mới.

→ Mùa đông AI lần 2


<!-- END PAGE 15 -->


<!-- START PAGE 16 -->

## [Trang 16]


# Sự ra đời của Deep Learning

![img-12.jpeg](img-12.jpeg)

Sau mùa đông lần hai, câu hỏi của cả ngành đổi hẳn:
"Nếu không thể viết hết trí thức thế giới vào máy, thì có thể để máy tự học nó từ dữ liệu không?"


<!-- END PAGE 16 -->


<!-- START PAGE 17 -->

## [Trang 17]


## 2009: Fei-Fei Li và ImageNet — cuộc cách mạng của dữ liệu

![img-13.jpeg](img-13.jpeg)


<!-- END PAGE 17 -->


<!-- START PAGE 18 -->

## [Trang 18]


# Deep Learning khác Machine Learning truyền thống ở chỗ nào?

## Machine Learning

![img-14.jpeg](img-14.jpeg)

## Deep Learning

![img-15.jpeg](img-15.jpeg)

Không cần con người thiết kế đặc trưng bằng tay — mạng sâu TỰ học đặc trưng từ dữ liệu thô, từ đơn giản đến phức tạp


<!-- END PAGE 18 -->


<!-- START PAGE 19 -->

## [Trang 19]


# 2012: AlexNet

![img-16.jpeg](img-16.jpeg)

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)

## ImageNet: **AlexNet chiến thắng ở ImageNet Large Scale Visual Recognition Challenge**

![img-19.jpeg](img-19.jpeg)

- **ImageNet** cho mô hình ăn một lượng dữ liệu chưa từng có ở thời điểm đó.
- **Kiến trúc sâu** cho phép học dần từ cạnh, hình, bộ phận, rồi đến đối tượng.
- **GPU** cung cấp đủ năng lực tính toán để quá trình huấn luyện trở nên khả thi.


<!-- END PAGE 19 -->


<!-- START PAGE 20 -->

## [Trang 20]


# 2016: AlphaGo

![img-20.jpeg](img-20.jpeg)

![img-21.jpeg](img-21.jpeg)

## AlphaGo và nước đi số 37

Ban đầu nó học từ khoảng 150.000 ván cờ của chuyên gia con người để có trực giác khởi đầu

→ Tạo ra nhiều bản sao của AlphaGo và để chúng **tự chơi với chính mình** hàng triệu lần

→ Hệ thống không chỉ học từ những gì con người đã biết, mà còn **tự mở rộng không gian chiến lược** bằng cách **khám phá những nước đi chưa từng được thử** trước đó.


<!-- END PAGE 20 -->


<!-- START PAGE 21 -->

## [Trang 21]


# Nút thắt của RNN: đọc hết rồi mới nói — từng bước một

![img-22.jpeg](img-22.jpeg)

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

![img-23.jpeg](img-23.jpeg)

**Transformer** là bước ngoặt vì nó cho mô hình hiểu ngôn ngữ theo cách linh hoạt hơn: **mỗi từ có thể nhìn sang những từ quan trọng khác** trong cả câu, thay vì chỉ đi tuần tự từng bước → trở thành nền móng kỹ thuật cho GPT, BERT và toàn bộ làn sóng LLM sau đó.


<!-- END PAGE 22 -->


<!-- START PAGE 23 -->

## [Trang 23]


# 2022: ChatGPT

![img-24.jpeg](img-24.jpeg)

## ChatGPT xuất hiện như một trải nghiệm đại chúng

Lần đầu tiên rất đông người dùng phổ thông có thể trực tiếp chạm vào một mô hình ngôn ngữ mạnh, thông qua một giao diện đơn giản đến mức ai cũng hiểu cách dùng


<!-- END PAGE 23 -->


<!-- START PAGE 24 -->

## [Trang 24]


![img-25.jpeg](img-25.jpeg)

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

![img-26.jpeg](img-26.jpeg)

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

![img-27.jpeg](img-27.jpeg)

LLM = bộ não ngôn ngữ dùng chung cho mọi việc — sản phẩm bạn thấy chỉ là lớp áo bên ngoài

Model hiện nay chủ yếu là kiến trúc decoder-only (GPT, Claude, Gemini, Kimi), nhiều model dùng MoE; sau pre-training còn các bước cần chỉnh (SFT, RLHF/DPO) và luyện suy luận (reasoning training, từ ~2025).


<!-- END PAGE 27 -->


<!-- START PAGE 28 -->

## [Trang 28]


## Bên trong Transformer: đầu ra luôn là một phân bố xác suất

![img-28.jpeg](img-28.jpeg)

Với mọi ngữ cảnh, model chấm điểm **MỌI** từ trong từ vựng — “land” 22%, “forest” 9%... — rồi chọn theo xác suất đó

Transformers, the tech behind LLMs - 3Blue1Brown


<!-- END PAGE 28 -->


<!-- START PAGE 29 -->

## [Trang 29]


# Sinh văn bản = đoán → nối vào câu → đoán tiếp

If you could see the underlying probability distributions a large language model uses when generating text, then you

![img-29.jpeg](img-29.jpeg)

If you could see the underlying probability distributions a large language model uses when generating text, then you would

![img-30.jpeg](img-30.jpeg)

If you could see the underlying probability distributions a large language model uses when generating text, then you would essentially

![img-31.jpeg](img-31.jpeg)

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

![img-32.jpeg](img-32.jpeg)

![img-33.jpeg](img-33.jpeg)

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

![img-34.jpeg](img-34.jpeg)

"Lan bỏ quyển sách vào túi vì nó quá dày" — muốn biết "nó" = quyển sách hay cái túi, mô hình so khớp "nó" với TẤT CẢ token trước đó, không chỉ token liền kề. Cung càng dày/đậm = trọng số attention càng cao (ở đây: hướng mạnh về "quyển"+"sách", không phải "túi").


<!-- END PAGE 33 -->


<!-- START PAGE 34 -->

## [Trang 34]


# Nhìn lân cận hay nhìn toàn cảnh?

Convolution — cửa sổ nhỏ quanh mỗi từ

![img-35.jpeg](img-35.jpeg)

“nó” muốn hiểu nghĩa thì phải nhìn tới “quyển/sách” — nhưng chúng nằm ngoài cửa sổ → mối liên hệ xa bị cắt.

Attention — mọi từ đều trong tầm nhìn

![img-36.jpeg](img-36.jpeg)

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

![img-37.jpeg](img-37.jpeg)

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

![img-38.jpeg](img-38.jpeg)

Luật chơi 2020–2024: cứ thêm compute + dữ liệu là model khôn lên **một cách dự đoán được** (scaling law, Kaplan et al. 2020)

MoE: Shazeer et al. (2017) — arxiv.org/abs/1701.06538 · Kimi K3 (16/7/2026): ~2.8 nghìn tỷ tham số MoE — k3-kimi.com


<!-- END PAGE 37 -->


<!-- START PAGE 38 -->

## [Trang 38]


# LLM được tạo ra như thế nào? — đọc nhiều, được chỉ, được uốn nắn, luyện đề

Một LLM được “nuôi lớn” qua 3 bước — mỗi bước một việc khác nhau

![img-39.jpeg](img-39.jpeg)

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

![img-40.jpeg](img-40.jpeg)

1 Mô hình thế giới bên trong?

nén thế giới thành biểu diễn có cấu trúc

?

![img-41.jpeg](img-41.jpeg)

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

![img-42.jpeg](img-42.jpeg)

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

![img-43.jpeg](img-43.jpeg)

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

![img-44.jpeg](img-44.jpeg)

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

![img-45.jpeg](img-45.jpeg)

ChatGPT nói tiếng Bồ Đào Nha với Fernanda Viégas: đầu hội thoại nó dùng động từ giống đực ("ajudá-lo").

Ngay khi bà nhắc đến chiếc váy (vestido), câu sau model chuyển sang tính từ giống cái ("segura") — nó đã ngầm đoán giới tính người dùng.

**Không ai bảo nó làm vậy.** Từ cách bạn viết, model tự dựng một "hồ sơ" về bạn — và hồ sơ đó ảnh hưởng câu trả lời.

Cách bạn viết prompt cũng đang nói cho model biết bạn là ai — đó là lý do persona và ngữ cảnh trong prompt rất đáng giá


<!-- END PAGE 46 -->


<!-- START PAGE 47 -->

## [Trang 47]


# Bốn cách chạm vào LLM: tiện bao nhiêu, kiểm soát bấy nhiêu

![img-46.jpeg](img-46.jpeg)

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

![img-47.jpeg](img-47.jpeg)

- ✖ Không dữ liệu mới
- ✖ Không hành động ngoài đời
- ✖ Không nhớ gì sau câu trả lời

![img-48.jpeg](img-48.jpeg)

Sản phẩm AI thật = bộ não LLM + hệ thống bao quanh — phần khó thường nằm ở hệ thống


<!-- END PAGE 51 -->


<!-- START PAGE 52 -->

## [Trang 52]


# Từ LLM đến agent: bốn mức độ — mỗi bậc thêm một năng lực

![img-49.jpeg](img-49.jpeg)

Agent không phải “một loại model khác” — đó là LLM được đặt vào vòng làm việc có mục tiêu và hành động


<!-- END PAGE 52 -->


<!-- START PAGE 53 -->

## [Trang 53]


## Giải phẫu một agent: 5 bộ phận là một vòng lặp

![img-50.jpeg](img-50.jpeg)

Agent = Goal + Reasoning + Tools + Memory + Action — chạy thành vòng lặp cho tới khi xong việc


<!-- END PAGE 53 -->


<!-- START PAGE 54 -->

## [Trang 54]


# Voyager: agent tự xây thư viện kỹ năng, rồi sống bằng tái dùng

![img-51.jpeg](img-51.jpeg)

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

![img-52.jpeg](img-52.jpeg)

Mỗi năm có hàng chục model đáng chú ý — đừng học thuộc tên, hãy học quỹ đạo


<!-- END PAGE 56 -->


<!-- START PAGE 57 -->

## [Trang 57]


# Cùng một mức năng lực, giá rơi khoảng 10 lần mỗi năm

![img-53.jpeg](img-53.jpeg)

Việc năm ngoái phải dùng model đắt nhất — năm nay model rẻ đã làm được

Tổng hợp từ bảng giá rơi, nhà cung cấp, 2000-2020


<!-- END PAGE 57 -->


<!-- START PAGE 58 -->

## [Trang 58]


# Năng lực hội tụ — và model mở đang bắt kịp model đóng

![img-54.jpeg](img-54.jpeg)

Nguồn: Stanford HAI AI Index 2025

**Không còn một model bỏ xa phần còn lại — chọn model là bài toán phương pháp, không phải bài toán nhớ tên**

Sắc thái mới: AI Index ghi nhận frontier hội tụ nhưng khoảng cách mở-đóng hơi nói lại 2025 — hai.stanford.edu/ai-index


<!-- END PAGE 58 -->


<!-- START PAGE 59 -->

## [Trang 59]


# Từ model đơn lẻ sang hệ thống biết hành động

![img-55.jpeg](img-55.jpeg)

Tùy model chọn lọc (không phải điều tra toàn bộ) 2024-05-10 16:17:00

Làn sóng hiện tại không phải 'model nào mạnh hơn' — mà là system nào dùng model khôn hơn


<!-- END PAGE 59 -->


<!-- START PAGE 60 -->

## [Trang 60]


## SWE-bench Verified: từ 33% (6/2024) lên ~81% (2/2026) — rồi chạm trần bão hòa

![img-56.jpeg](img-56.jpeg)

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

![img-57.jpeg](img-57.jpeg)

Vì được nuôi bằng dữ liệu tương xứng đúng tỉ lệ — to không bằng cân đối.

## Trực 2 — Post-training

CÙNG 175 tỷ tham số, chỉ khác: có RLHF hay không (InstructGPT, 2022)

![img-58.jpeg](img-58.jpeg)

Cùng một bộ não — chỉ khác cách uốn nắn mà người dùng ưa hẳn.

## Trực 3 — Test-time / agentic compute

CÙNG một model (Claude Opus 4.8) — chỉ đổi bộ đề / harness

![img-59.jpeg](img-59.jpeg)

Đổi cách cho model “được nghỉ kỹ” (agentic harness) → lệch tới 19 điểm cùng một model.

Model “giỏi hơn” không chỉ vì to hơn — còn vì cân đối hơn · được uốn nắn hơn · được nghỉ kỹ hơn

Nguồn: Hoffmann et al. 2022 (Chinchilla) · Ouyang et al. 2022 (InstructGPT) · SWE-bench, Claude Opus 4.8 vendor-reported


<!-- END PAGE 66 -->


<!-- START PAGE 67 -->

## [Trang 67]


# Mixture of Experts: tăng tham số mà không tăng chi phí tính toán

DENSE (truyền thống)

![img-60.jpeg](img-60.jpeg)

GPT-2 - GPT-3 - Llama 1-3

MIXTURE OF EXPERTS

![img-61.jpeg](img-61.jpeg)

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

![img-62.jpeg](img-62.jpeg)

Lần gọi thứ mười — history đã phình ra

![img-63.jpeg](img-63.jpeg)

Tối ưu chi phí = tối ưu prompt + context — tóm tắt lại thay vì kéo theo cả lịch sử


<!-- END PAGE 69 -->


<!-- START PAGE 70 -->

## [Trang 70]


# Nhiều token hơn = vừa chậm hơn, vừa đắt hơn

## Một núm vặn, hai hệ quả

![img-64.jpeg](img-64.jpeg)

Cả hai cùng quy về một thứ: **số token model phải đọc và sinh ra** — đó là 'một núm vặn'.

## Ví dụ tiền thật — chatbot 1.000 lượt/ngày

1.350 tok × 1.000 lượt × 30 ngày = **40 triệu token/tháng**

![img-65.jpeg](img-65.jpeg)

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

![img-66.jpeg](img-66.jpeg)

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

![img-67.jpeg](img-67.jpeg)

luôn chọn từ **chắc nhất** → ổn định, lặp lại, hợp code & phân tích

T = 1

![img-68.jpeg](img-68.jpeg)

cân bằng tự nhiên — vẫn ưu tiên từ hợp lý

T = 2

![img-69.jpeg](img-69.jpeg)

phân bố **phẳng ra** → đa dạng, “phiêu”, dễ lạc đề

## top_p — “chỉ xem top đầu bảng” (p = 0.9)

① Bảng xác suất gốc

giữ nhóm cộng dồn ≥ 90%

![img-70.jpeg](img-70.jpeg)

② Bảng mới

→ cắt & chuẩn hóa lại

![img-71.jpeg](img-71.jpeg)

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

![img-72.jpeg](img-72.jpeg)

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
