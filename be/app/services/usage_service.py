import logging
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.ai_usage import AICallLog, AIUsageLog, AnswerFeedback

logger = logging.getLogger(__name__)


class QuotaExceededError(Exception):
    # Lỗi NGHIỆP VỤ, không phải lỗi kỹ thuật — người dùng cần biết CHÍNH XÁC
    # lý do bị chặn và khi nào dùng lại được (khác hẳn guardrail an toàn ở
    # 5.6.1/5.6.2/5.6.4, nơi cố ý giấu lý do để tránh gợi ý cách né). Ở đây
    # không có gì để "né": hết lượt là hết lượt.
    def __init__(self, used: int, limit: int):
        self.used = used
        self.limit = limit
        super().__init__(f"Bạn đã dùng hết {limit} câu hỏi trong ngày hôm nay (đã dùng {used}). Vui lòng quay lại vào ngày mai.")


def _start_of_day_utc() -> datetime:
    # Mốc reset quota: 00:00 UTC. Chọn UTC (không phải giờ VN) để khớp với
    # created_at do Postgres ghi bằng now() — tránh lệch múi giờ làm quota reset
    # sai thời điểm. Nếu sau này cần reset theo giờ VN, đổi ở ĐÚNG 1 chỗ này.
    now = datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def _start_of_month_utc() -> datetime:
    return _start_of_day_utc().replace(day=1)


async def count_questions_today(db: AsyncSession, user_id: uuid.UUID) -> int:
    stmt = (
        select(func.count())
        .select_from(AIUsageLog)
        .where(AIUsageLog.user_id == user_id, AIUsageLog.created_at >= _start_of_day_utc())
    )
    return await db.scalar(stmt) or 0


async def check_daily_quota(db: AsyncSession, user_id: uuid.UUID) -> None:
    # Raise thay vì trả về bool: gọi sai (quên kiểm tra giá trị trả về) sẽ âm
    # thầm bỏ qua quota — với 1 guardrail chi phí thì im lặng thất bại là kiểu
    # lỗi tệ nhất.
    used = await count_questions_today(db, user_id)
    if used >= settings.DAILY_QUESTION_LIMIT:
        raise QuotaExceededError(used=used, limit=settings.DAILY_QUESTION_LIMIT)


# 5.6.7 — giá công bố tại thời điểm code (2026), USD / 1 triệu token, tách
# input/output vì 2 loại chênh lệch giá đáng kể (gpt-4o-mini: output đắt gấp 4
# lần input). Model không có trong bảng (VD model mới, gõ sai tên) mặc định
# (0.0, 0.0) — fail-open về phía "không tính phí" thay vì raise, vì đây là
# guardrail QUAN SÁT chi phí, không phải guardrail chặn tính năng chính.
_PRICING_USD_PER_1M_TOKENS: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    # Groq free tier hiện tại = $0 thật. Nếu sau này nâng cấp Dev Tier trả phí
    # (xem sự cố hết quota TPD ở 5.6.5), CẬP NHẬT giá thật vào đây — nếu không
    # cost_usd sẽ báo sai (thấp hơn thực tế).
    "openai/gpt-oss-120b": (0.0, 0.0),
}


def estimate_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    input_price, output_price = _PRICING_USD_PER_1M_TOKENS.get(model, (0.0, 0.0))
    return (prompt_tokens * input_price + completion_tokens * output_price) / 1_000_000


async def log_ai_usage(
    db: AsyncSession,
    user_id: uuid.UUID,
    *,
    id: uuid.UUID | None = None,
    document_id: uuid.UUID | None = None,
    blocked_reason: str | None = None,
    grounded: bool | None = None,
    faithfulness_score: float | None = None,
    retried: bool | None = None,
    total_tokens: int = 0,
    estimated_cost_usd: float = 0.0,
) -> None:
    # `id` optional: khi truyền vào (từ AnswerResult.call_group_id, 5.6.9), dòng
    # ai_usage_log này dùng ĐÚNG id đã gắn cho các dòng ai_call_log của cùng
    # lượt gọi — cho phép liên kết mềm giữa dòng GỘP và các dòng CHI TIẾT mà
    # không cần FK cứng (xem comment ở AICallLog). Không truyền → để DB tự sinh
    # (server_default) như trước 5.6.9, không phá vỡ caller cũ nào.
    kwargs = {}
    if id is not None:
        kwargs["id"] = id
    db.add(
        AIUsageLog(
            user_id=user_id,
            document_id=document_id,
            blocked_reason=blocked_reason,
            grounded=grounded,
            faithfulness_score=faithfulness_score,
            retried=retried,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            **kwargs,
        )
    )
    await db.commit()


# 5.6.9 — nội dung prompt/response đôi khi khá dài (context RAG có thể vài
# nghìn ký tự) — cắt bớt để log phục vụ ĐÚNG mục đích debug (xem đủ để hiểu
# chuyện gì xảy ra) mà không nhân bản toàn bộ tài liệu vào mọi dòng log.
MAX_LOGGED_TEXT_LENGTH = 4000


def _truncate(text: str | None) -> str | None:
    if text is None or len(text) <= MAX_LOGGED_TEXT_LENGTH:
        return text
    return text[:MAX_LOGGED_TEXT_LENGTH] + f"... [cắt bớt, gốc {len(text)} ký tự]"


async def log_ai_call(
    db: AsyncSession,
    call_group_id: uuid.UUID,
    *,
    call_type: str,
    model: str | None,
    latency_ms: float,
    prompt: str | None = None,
    response: str | None = None,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    estimated_cost_usd: float = 0.0,
    prompt_version: str | None = None,
) -> None:
    db.add(
        AICallLog(
            call_group_id=call_group_id,
            call_type=call_type,
            model=model,
            prompt=_truncate(prompt),
            response=_truncate(response),
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=estimated_cost_usd,
            prompt_version=prompt_version,
        )
    )
    await db.commit()


async def cost_this_month(db: AsyncSession, user_id: uuid.UUID) -> float:
    stmt = (
        select(func.coalesce(func.sum(AIUsageLog.estimated_cost_usd), 0.0))
        .where(AIUsageLog.user_id == user_id, AIUsageLog.created_at >= _start_of_month_utc())
    )
    return await db.scalar(stmt) or 0.0


# Ngưỡng CẢNH BÁO, không phải ngưỡng CHẶN — khác hẳn 5.6.6 (quota câu hỏi/ngày,
# vượt là raise). 5.6.7 chỉ "cảnh báo khi gần chạm ngưỡng đã đặt" đúng theo kế
# hoạch gốc — chặn cứng theo $ sẽ trùng lặp với 5.6.6 (vốn đã chặn theo số
# lượt) mà không có lợi ích rõ ràng, và dễ chặn oan nếu 1 vài câu hỏi tình cờ
# tốn nhiều token hơn (context dài, phải retry) dù số LƯỢT vẫn còn trong hạn.
COST_WARNING_RATIO = 0.8


async def check_cost_budget(db: AsyncSession, user_id: uuid.UUID) -> None:
    used = await cost_this_month(db, user_id)
    if used >= settings.MONTHLY_COST_BUDGET_USD * COST_WARNING_RATIO:
        logger.warning(
            "user %s đã dùng $%.4f / $%.2f ngân sách AI tháng này (%.0f%%)",
            user_id,
            used,
            settings.MONTHLY_COST_BUDGET_USD,
            100 * used / settings.MONTHLY_COST_BUDGET_USD,
        )


# 5.6.8 — Circuit breaker: khác 5.6.6/5.6.7 ở 2 điểm mấu chốt. (1) TOÀN HỆ
# THỐNG, không theo từng user — mục tiêu là bảo vệ CẢ HỆ THỐNG khỏi 1 bug (VD
# vòng lặp gọi API) hoặc tấn công phối hợp nhiều tài khoản, không phải giới
# hạn hành vi của 1 user đơn lẻ. (2) CỬA SỔ RẤT NGẮN (vài phút, không phải
# ngày/tháng) để bắt được TĂNG ĐỘT BIẾN — 1 spike có thể vẫn nằm dưới quota
# ngày/tháng của từng user riêng lẻ (VD 10 user cùng bị 1 bug gọi lặp, mỗi
# user chỉ mới dùng vài % quota ngày của họ) nhưng vẫn là dấu hiệu bất thường
# rõ ràng khi nhìn TỔNG toàn hệ thống trong vài phút.
class CircuitBreakerOpenError(Exception):
    def __init__(self, requests: int, cost: float, window_minutes: int):
        self.requests = requests
        self.cost = cost
        super().__init__(
            f"Hệ thống phát hiện lượng truy cập bất thường ({requests} lượt / "
            f"${cost:.4f} trong {window_minutes} phút gần nhất) và đang tạm khóa "
            "tính năng hỏi đáp để bảo vệ hệ thống. Vui lòng thử lại sau ít phút."
        )


# Ngưỡng thật đọc từ settings (CIRCUIT_BREAKER_*) — xem lý luận chọn số đầy đủ
# ở comment cạnh các setting đó trong app/config.py. Chưa có traffic production
# thật để hiệu chỉnh, đặt theo suy luận từ quy mô đã biết (DAILY_QUESTION_LIMIT,
# chi phí đo thật ở 5.6.7) — CẦN TINH CHỈNH LẠI khi có traffic thật.


def _window_start(minutes: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=minutes)


async def requests_in_window(db: AsyncSession, minutes: int) -> int:
    stmt = select(func.count()).select_from(AIUsageLog).where(AIUsageLog.created_at >= _window_start(minutes))
    return await db.scalar(stmt) or 0


async def cost_in_window(db: AsyncSession, minutes: int) -> float:
    stmt = (
        select(func.coalesce(func.sum(AIUsageLog.estimated_cost_usd), 0.0))
        .where(AIUsageLog.created_at >= _window_start(minutes))
    )
    return await db.scalar(stmt) or 0.0


async def check_circuit_breaker(db: AsyncSession) -> None:
    # Không lưu trạng thái "đã trip" riêng (không có bảng/cờ "đang khóa") —
    # TỰ SUY RA từ chính ai_usage_log mỗi lần gọi: nếu cửa sổ N phút gần nhất
    # vẫn đang vượt ngưỡng thì vẫn khóa, hễ traffic hạ xuống dưới ngưỡng thì tự
    # mở lại ngay, không cần cơ chế reset thủ công. Đơn giản hơn 1 state machine
    # open/half-open/closed đầy đủ — đánh đổi: có thể "rung" (flap) ở sát ngưỡng
    # thay vì có độ trễ ổn định (cooldown cố định), chấp nhận được ở quy mô này.
    window_minutes = settings.CIRCUIT_BREAKER_WINDOW_MINUTES
    requests = await requests_in_window(db, window_minutes)
    cost = await cost_in_window(db, window_minutes)
    if requests >= settings.CIRCUIT_BREAKER_MAX_REQUESTS or cost >= settings.CIRCUIT_BREAKER_MAX_COST_USD:
        logger.error(
            "CIRCUIT BREAKER TRIP: %d requests / $%.4f trong %d phút gần nhất (ngưỡng: %d requests / $%.2f)",
            requests,
            cost,
            window_minutes,
            settings.CIRCUIT_BREAKER_MAX_REQUESTS,
            settings.CIRCUIT_BREAKER_MAX_COST_USD,
        )
        raise CircuitBreakerOpenError(requests=requests, cost=cost, window_minutes=window_minutes)


# 5.6.10 — 5.6.9 đã LOG prompt_version vào từng dòng ai_call_log, nhưng log
# suông không tự thành "so sánh được" — đây là năng lực THỰC SỰ còn thiếu:
# gộp chất lượng/chi phí THẬT theo từng version, dùng để trả lời "version mới
# có tốt hơn version cũ không" bằng số liệu, không phải cảm tính khi đổi rule.
async def compare_prompt_versions(db: AsyncSession) -> list[dict]:
    # prompt_version được gắn vào TỪNG dòng ai_call_log (generation, judge, có
    # thể x2 nếu retry) của CÙNG 1 lượt ask() — phải lấy DISTINCT (call_group_id,
    # prompt_version) trước khi join, nếu không 1 lượt có 4 dòng call_log sẽ bị
    # đếm/join 4 LẦN vào ai_usage_log, làm sai lệch mọi con số gộp bên dưới.
    call_groups = (
        select(AICallLog.call_group_id, AICallLog.prompt_version)
        .distinct()
        .where(AICallLog.prompt_version.is_not(None))
        .subquery()
    )
    # 5.6.12 — OUTER join thêm answer_feedback: không phải câu hỏi nào cũng có
    # feedback, INNER join sẽ ÂM THẦM LÀM MẤT mọi câu chưa được đánh giá khỏi
    # thống kê (kể cả các cột không liên quan gì tới feedback như avg_faithfulness).
    # ai_usage_log 1-1 với call_groups (đã distinct) và answer_feedback 1-đến-0-
    # hoặc-1 với ai_usage_log (nhờ UniqueConstraint) — nên outer join này KHÔNG
    # làm nhân bản dòng, khác hẳn rủi ro ở chính join ai_call_log→ai_usage_log
    # phía trên (lý do phải distinct call_groups trước).
    stmt = (
        select(
            call_groups.c.prompt_version,
            func.count().label("n_questions"),
            func.avg(AIUsageLog.faithfulness_score).label("avg_faithfulness"),
            func.avg(case((AIUsageLog.grounded.is_(True), 1.0), else_=0.0)).label("grounded_rate"),
            func.avg(case((AIUsageLog.retried.is_(True), 1.0), else_=0.0)).label("retry_rate"),
            func.avg(AIUsageLog.estimated_cost_usd).label("avg_cost_usd"),
            func.sum(case((AnswerFeedback.is_positive.is_(True), 1), else_=0)).label("n_thumbs_up"),
            func.sum(case((AnswerFeedback.is_positive.is_(False), 1), else_=0)).label("n_thumbs_down"),
        )
        .select_from(call_groups)
        .join(AIUsageLog, AIUsageLog.id == call_groups.c.call_group_id)
        .outerjoin(AnswerFeedback, AnswerFeedback.ai_usage_log_id == AIUsageLog.id)
        .group_by(call_groups.c.prompt_version)
        .order_by(call_groups.c.prompt_version)
    )
    rows = (await db.execute(stmt)).all()
    return [dict(row._mapping) for row in rows]


class FeedbackTargetNotFoundError(Exception):
    # Cùng 1 lỗi cho "answer_id không tồn tại" VÀ "answer_id tồn tại nhưng của
    # user khác" — không tiết lộ sự khác biệt đó (tránh dò được answer_id của
    # người khác bằng cách thử-sai), nhất quán với cách get_owned_document đã
    # xử lý document not-found vs not-owned ở các phase trước.
    def __init__(self, ai_usage_log_id: uuid.UUID):
        super().__init__(f"Không tìm thấy câu trả lời {ai_usage_log_id} thuộc về bạn để đánh giá.")


async def submit_feedback(
    db: AsyncSession,
    ai_usage_log_id: uuid.UUID,
    user_id: uuid.UUID,
    *,
    is_positive: bool,
    reason: str | None = None,
) -> AnswerFeedback:
    owner_id = await db.scalar(select(AIUsageLog.user_id).where(AIUsageLog.id == ai_usage_log_id))
    if owner_id is None or owner_id != user_id:
        raise FeedbackTargetNotFoundError(ai_usage_log_id)

    # Upsert thủ công (đọc rồi quyết định insert/update) thay vì INSERT ...
    # ON CONFLICT: đơn giản hơn, dễ đọc hơn cho 1 bảng nhỏ, không cần lo race
    # condition ở quy mô hiện tại (1 user tự bấm 👍/👎 cho câu trả lời của
    # chính họ, không có kịch bản 2 request ghi đồng thời cùng 1 dòng thật sự).
    existing = await db.scalar(
        select(AnswerFeedback).where(
            AnswerFeedback.ai_usage_log_id == ai_usage_log_id, AnswerFeedback.user_id == user_id
        )
    )
    if existing is not None:
        existing.is_positive = is_positive
        existing.reason = reason
        feedback = existing
    else:
        feedback = AnswerFeedback(
            ai_usage_log_id=ai_usage_log_id, user_id=user_id, is_positive=is_positive, reason=reason
        )
        db.add(feedback)

    await db.commit()
    await db.refresh(feedback)
    return feedback
