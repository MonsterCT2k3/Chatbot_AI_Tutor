# JudgeScore/_judge/score_faithfulness giờ sống ở rag_service.py —
# score_faithfulness không còn chỉ là công cụ đánh giá offline nữa, mà là
# guardrail thật chạy ngay trong ask() (Phase 5.5.7). Import lại ở đây (thay
# vì định nghĩa trùng) để relevance/correctness dùng chung đúng 1 hạ tầng
# judge — eval phụ thuộc production, không phải ngược lại.
from app.services.rag_service import JudgeScore, _judge, score_faithfulness  # noqa: F401 (score_faithfulness re-exported for callers of this module)

_RELEVANCE_SYSTEM_PROMPT = (
    "Bạn là giám khảo đánh giá mức độ liên quan (relevance) giữa câu hỏi và câu trả lời.\n"
    "Câu trả lời LIÊN QUAN là câu trả lời giải quyết đúng trọng tâm câu hỏi (kể cả khi câu trả lời là từ chối hợp lý vì thiếu thông tin).\n"
    "Câu trả lời KHÔNG liên quan là câu trả lời lạc đề, trả lời câu hỏi khác, hoặc né tránh không thực sự chạm vào điều được hỏi.\n"
    "Chấm điểm score từ 0.0 (hoàn toàn lạc đề) đến 1.0 (đi thẳng vào trọng tâm câu hỏi)."
)


async def score_relevance(question: str, answer: str) -> JudgeScore:
    user_prompt = f"<question>\n{question}\n</question>\n\n<answer>\n{answer}\n</answer>"
    return await _judge(_RELEVANCE_SYSTEM_PROMPT, user_prompt)


_CORRECTNESS_SYSTEM_PROMPT = (
    "Bạn là giám khảo so sánh 1 câu trả lời AI với đáp án tham chiếu (reference answer) đã biết là đúng.\n"
    "Chấm điểm score từ 0.0 (sai hoàn toàn, hoặc không đề cập tới ý chính của đáp án tham chiếu) "
    "đến 1.0 (khớp đúng ý chính, kể cả khi diễn đạt khác đi hoặc ngắn gọn hơn)."
)


async def score_correctness(answer: str, expected_answer_summary: str) -> JudgeScore:
    user_prompt = f"<reference_answer>\n{expected_answer_summary}\n</reference_answer>\n\n<answer>\n{answer}\n</answer>"
    return await _judge(_CORRECTNESS_SYSTEM_PROMPT, user_prompt)
