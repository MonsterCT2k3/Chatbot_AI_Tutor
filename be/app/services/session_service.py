from collections.abc import AsyncGenerator
from datetime import datetime, timezone
import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import ChatMessage, MessageCitation
from app.models.session import ChatSession
from app.schemas.message import ANSWER_ID_METADATA_KEY
from app.services.document_service import DocumentNotFoundError, ensure_document_ready, get_owned_document
from app.services.rag_service import AnswerResult, Citation, ask_events, contextualize_question
from app.services.usage_service import (
    check_circuit_breaker,
    check_cost_budget,
    check_daily_quota,
    log_ai_usage,
)


class SessionNotFoundError(Exception):
    pass


# Khớp server_default của chat_sessions.title — so sánh đúng chuỗi này thì
# mới được phép ghi đè bằng câu hỏi đầu (user đã đặt tên thì không đụng).
DEFAULT_SESSION_TITLE = "New chat"
AUTO_TITLE_MAX_LEN = 60
# 6.8 gộp vào 6.7: cửa sổ đưa vào rewrite, không tóm tắt.
CONTEXTUALIZE_MAX_MESSAGES = 10


def auto_title_from_question(question: str, max_len: int = AUTO_TITLE_MAX_LEN) -> str:
    text = " ".join(question.split())
    if not text:
        return DEFAULT_SESSION_TITLE
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut or text[:max_len]


async def get_owned_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> ChatSession:
    # Lọc theo id VÀ user_id trong CÙNG 1 query — bản sao chính xác của
    # document_service.get_owned_document. Nhờ vậy "session không tồn tại" và
    # "session của người khác" cùng ném 1 lỗi, router biến cả hai thành CÙNG
    # một 404: kẻ tấn công không thể dò xem session_id nào có thật bằng cách
    # thử hàng loạt UUID rồi so sánh mã lỗi trả về.
    session = await db.scalar(
        select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user_id)
    )
    if session is None:
        raise SessionNotFoundError()
    return session


async def create_session(
    db: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID, title: str | None = None
) -> ChatSession:
    # Phải kiểm tra tài liệu có thuộc về CHÍNH user này không, không chỉ là
    # "tài liệu có tồn tại không". Bỏ bước này thì user A tạo được session trỏ
    # vào tài liệu của user B, rồi chat với nội dung tài liệu đó — lỗ hổng đọc
    # trộm dữ liệu, dù mọi endpoint session phía sau đều kiểm tra quyền đúng.
    # Ném thẳng DocumentNotFoundError để router trả 404 giống hệt trường hợp
    # tài liệu không tồn tại (cùng lý do chống dò như trên).
    await get_owned_document(db, document_id, user_id)

    # title=None: SQLAlchemy tự bỏ cột khỏi INSERT vì cột có server_default
    # -> DB điền "New chat". Đã kiểm chứng bằng log SQL ở 6.1.
    session = ChatSession(user_id=user_id, document_id=document_id, title=title)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def list_sessions(
    db: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID | None = None
) -> list[ChatSession]:
    # Sắp theo updated_at: session vừa có tin nhắn mới phải nổi lên đầu. Điều
    # này CHỈ đúng nếu 6.5 chủ động "chạm" vào dòng session mỗi khi lưu tin
    # nhắn (mục ④ kế hoạch) — thêm dòng vào chat_messages KHÔNG tự làm
    # updated_at đổi, dù DB có trigger, vì trigger chỉ bắn khi chính dòng
    # session bị UPDATE.
    query = select(ChatSession).where(ChatSession.user_id == user_id)
    if document_id is not None:
        query = query.where(ChatSession.document_id == document_id)
    result = await db.scalars(query.order_by(ChatSession.updated_at.desc()))
    return list(result.all())


async def rename_session(
    db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID, title: str
) -> ChatSession:
    session = await get_owned_session(db, session_id, user_id)
    session.title = title
    await db.commit()
    await db.refresh(session)
    return session


async def list_messages(
    db: AsyncSession,
    session_id: uuid.UUID,
    user_id: uuid.UUID,
    *,
    limit: int,
    before: datetime | None = None,
) -> tuple[list[ChatMessage], dict[uuid.UUID, list[MessageCitation]], bool]:
    """Lịch sử hội thoại, phân trang LÙI về quá khứ.

    Trả về (tin nhắn TĂNG dần theo thời gian, citations gom theo message_id,
    còn trang cũ hơn hay không).
    """
    await get_owned_session(db, session_id, user_id)

    query = select(ChatMessage).where(ChatMessage.session_id == session_id)
    if before is not None:
        # Client có thể gửi mốc thời gian KHÔNG kèm timezone. created_at trong
        # DB là TIMESTAMPTZ, so sánh với giá trị naive sẽ được Postgres diễn
        # giải theo timezone của phiên — tức lệch giờ một cách âm thầm. Coi
        # giá trị thiếu timezone là UTC để so sánh luôn xác định.
        if before.tzinfo is None:
            before = before.replace(tzinfo=timezone.utc)
        query = query.where(ChatMessage.created_at < before)

    # Lấy DƯ 1 dòng để biết còn trang cũ hơn hay không, thay vì chạy thêm 1
    # truy vấn COUNT. Nếu không biết điều này thì chỉ còn 2 lựa chọn đều tệ:
    # luôn trả next_cursor (client bấm "xem thêm" rồi nhận trang RỖNG), hoặc
    # đếm toàn bộ lịch sử mỗi lần phân trang.
    #
    # Sắp GIẢM dần vì phân trang đi LÙI (mới nhất trước), khớp đúng index
    # idx_messages_session (session_id, created_at).
    rows = list(
        (await db.scalars(query.order_by(ChatMessage.created_at.desc()).limit(limit + 1))).all()
    )
    has_more = len(rows) > limit
    rows = rows[:limit]

    # Hợp đồng ở schema (6.1): messages trả ra phải TĂNG dần — đúng thứ tự
    # hiển thị. Truy vấn buộc phải giảm dần, nên đảo lại ở đây.
    rows.reverse()

    # 1 truy vấn cho TẤT CẢ citations, không phải mỗi tin nhắn một truy vấn.
    # Lấy từng cái sẽ thành N+1: trang 50 tin nhắn tốn 51 lượt đi DB.
    citations: dict[uuid.UUID, list[MessageCitation]] = {}
    if rows:
        found = await db.scalars(
            select(MessageCitation)
            .where(MessageCitation.message_id.in_([m.id for m in rows]))
            .order_by(MessageCitation.page_number)
        )
        for citation in found:
            citations.setdefault(citation.message_id, []).append(citation)

    return rows, citations, has_more


async def save_user_message(db: AsyncSession, session: ChatSession, content: str) -> ChatMessage:
    # Commit RIÊNG, trước mọi lệnh gọi LLM. now() của Postgres đóng băng từ
    # lúc transaction bắt đầu tới lúc commit — hai INSERT trong CÙNG
    # transaction nhận created_at GIỐNG HỆT (đã đo trên DB thật). Commit ở
    # đây còn giữ được câu hỏi nếu ask() ném exception sau đó.
    message = ChatMessage(session_id=session.id, role="user", content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def save_assistant_message(
    db: AsyncSession,
    session: ChatSession,
    content: str,
    *,
    citations: list[Citation] | None = None,
    ai_usage_log_id: uuid.UUID | None = None,
) -> ChatMessage:
    # Transaction riêng so với save_user_message (6.4). 6.6: bắc cầu sang
    # ai_usage_log qua JSONB — 👍/👎 vẫn FK cứng tới bảng đó, không đổi sang
    # chat_messages.id. Lưu str(uuid) vì JSONB đọc lại ra str, không phải UUID.
    metadata = {}
    if ai_usage_log_id is not None:
        metadata[ANSWER_ID_METADATA_KEY] = str(ai_usage_log_id)
    message = ChatMessage(
        session_id=session.id, role="assistant", content=content, metadata_=metadata
    )
    db.add(message)
    await db.flush()
    for citation in citations or []:
        db.add(
            MessageCitation(
                message_id=message.id,
                document_id=session.document_id,
                chunk_id=citation.chunk_id,
                page_number=citation.page_number,
                snippet=citation.snippet,
            )
        )
    await db.commit()
    await db.refresh(message)
    return message


async def touch_session(db: AsyncSession, session: ChatSession, *, title: str | None = None) -> None:
    # Thêm dòng chat_messages KHÔNG chạy trigger updated_at (trigger chỉ bắn
    # khi chính dòng session bị UPDATE). SET title kể cả khi không đổi tên —
    # Postgres vẫn coi là UPDATE, trigger chạy. SQLAlchemy bỏ qua UPDATE nếu
    # gán attribute Python không dirty, nên phải đi qua update() tường minh.
    await db.execute(
        update(ChatSession)
        .where(ChatSession.id == session.id)
        .values(title=title if title is not None else session.title)
    )
    await db.commit()
    await db.refresh(session)


async def recent_messages_for_contextualize(
    db: AsyncSession, session_id: uuid.UUID, *, limit: int = CONTEXTUALIZE_MAX_MESSAGES
) -> list[ChatMessage]:
    rows = list(
        (
            await db.scalars(
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.desc())
                .limit(limit)
            )
        ).all()
    )
    rows.reverse()
    return rows


async def send_message_events(
    db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID, question: str
) -> AsyncGenerator[tuple[str, dict], None]:
    session = await get_owned_session(db, session_id, user_id)
    document = await get_owned_document(db, session.document_id, user_id)
    ensure_document_ready(document)

    # History TRƯỚC khi save — nếu load sau, câu vừa gửi nằm trong history.
    history = await recent_messages_for_contextualize(db, session.id)

    await save_user_message(db, session, question)
    auto_title = auto_title_from_question(question) if session.title == DEFAULT_SESSION_TITLE else None
    await touch_session(db, session, title=auto_title)

    call_group_id = uuid.uuid4()
    retrieve_question = question

    # Kiểm tra quota & breaker trước khi gọi LLM
    await check_circuit_breaker(db)
    await check_daily_quota(db, user_id)

    if history:
        yield ("status", {"stage": "contextualize"})
        retrieve_question = await contextualize_question(
            history, question, db=db, call_group_id=call_group_id
        )

    draft_answer: str | None = None
    draft_citations: list[Citation] = []
    result: AnswerResult | None = None

    async for event, payload in ask_events(
        db,
        session.document_id,
        question,
        retrieve_question=retrieve_question,
        call_group_id=call_group_id,
    ):
        if event == "status":
            yield (event, payload)
        elif event == "generated":
            draft_answer = payload["answer"]
            draft_citations = payload["citations"]
            yield ("token", {"delta": draft_answer})
            for c in draft_citations:
                yield (
                    "citation",
                    {
                        "page_number": c.page_number,
                        "chunk_id": str(c.chunk_id) if c.chunk_id else None,
                        "snippet": c.snippet,
                    },
                )
        elif event == "result":
            result = payload

    if result is None:
        raise RuntimeError("ask_events completed without yielding a result")

    def _serialize_citation(c: Citation | MessageCitation) -> dict:
        return {
            "page_number": c.page_number,
            "chunk_id": str(c.chunk_id) if c.chunk_id else None,
            "snippet": c.snippet,
        }

    # Input moderation flagged: không có event "generated", nên emit token từ chối ở đây
    if draft_answer is None:
        yield ("token", {"delta": result.answer})
    else:
        final_answer = result.answer
        final_citations = result.citations
        if final_answer != draft_answer:
            yield (
                "replace",
                {
                    "content": final_answer,
                    "citations": [_serialize_citation(c) for c in final_citations],
                },
            )

    # 5.6.9 / 6.6: Ghi ai_usage_log giống ask_for_user để liên kết answer_id với chi phí/đánh giá
    await log_ai_usage(
        db,
        user_id,
        id=result.call_group_id,
        document_id=session.document_id,
        blocked_reason=result.blocked_reason,
        grounded=result.grounded,
        faithfulness_score=result.faithfulness_score,
        retried=result.retried,
        total_tokens=result.total_tokens,
        estimated_cost_usd=result.estimated_cost_usd,
    )
    await check_cost_budget(db, user_id)

    assistant = await save_assistant_message(
        db,
        session,
        result.answer,
        citations=result.citations,
        ai_usage_log_id=result.call_group_id,
    )
    await touch_session(db, session)

    saved_citations = list(
        (
            await db.scalars(
                select(MessageCitation)
                .where(MessageCitation.message_id == assistant.id)
                .order_by(MessageCitation.page_number)
            )
        ).all()
    )

    final_citations_payload = [_serialize_citation(c) for c in saved_citations]

    yield (
        "done",
        {
            "message_id": str(assistant.id),
            "answer_id": str(result.call_group_id) if result.call_group_id else None,
            "citations": final_citations_payload,
        },
    )


async def send_message(
    db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID, question: str
) -> tuple[ChatMessage, list[MessageCitation]]:
    done_payload = None
    async for event, payload in send_message_events(db, session_id, user_id, question):
        if event == "done":
            done_payload = payload

    if done_payload is None:
        raise RuntimeError("send_message_events completed without a 'done' event")

    message_id = uuid.UUID(done_payload["message_id"])
    assistant = await db.scalar(select(ChatMessage).where(ChatMessage.id == message_id))
    citations = list(
        (
            await db.scalars(
                select(MessageCitation)
                .where(MessageCitation.message_id == message_id)
                .order_by(MessageCitation.page_number)
            )
        ).all()
    )
    return assistant, citations


async def delete_session(db: AsyncSession, session_id: uuid.UUID, user_id: uuid.UUID) -> None:
    # Không cần tự xoá chat_messages/message_citations: FK của chúng đều là
    # ON DELETE CASCADE (đã kiểm chứng trên DB thật ở 6.1), Postgres tự dọn.
    session = await get_owned_session(db, session_id, user_id)
    await db.delete(session)
    await db.commit()
