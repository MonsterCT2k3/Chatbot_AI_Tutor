import asyncio
import json
import uuid
from unittest.mock import AsyncMock, patch
import httpx

from app.database import get_db
from app.evaluation.eval_documents import ensure_eval_documents, EVAL_USER_ID
from app.main import app
from app.models.message import ChatMessage
from app.services.auth_service import create_access_token
from app.services.rag_service import (
    FAITHFULNESS_THRESHOLD,
    REFUSAL_SENTENCE,
    AnswerResult,
    JudgeScore,
    TokenUsage,
    ask,
)
from app.services.session_service import create_session


async def run_sse_request(client, session_id, token, question):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    events = []
    async with client.stream(
        "POST",
        f"/sessions/{session_id}/messages?stream=1",
        headers=headers,
        json={"question": question},
    ) as response:
        assert response.status_code == 200
        current_event = None
        async for line in response.aiter_lines():
            if not line.strip():
                continue
            if line.startswith("event:"):
                current_event = line.split("event:", 1)[1].strip()
            elif line.startswith("data:") and current_event:
                data_str = line.split("data:", 1)[1].strip()
                data = json.loads(data_str)
                events.append((current_event, data))
                current_event = None
    return events


async def main():
    async for db in get_db():
        docs = await ensure_eval_documents(db, {"b1-full.pdf"})
        doc_id = docs["b1-full.pdf"]
        break

    token = create_access_token(EVAL_USER_ID)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver/api", timeout=60.0) as client:
        # ============================================================
        # 1. LIVE GROUNDED TEST (Without Mock)
        # ============================================================
        print("=" * 60)
        print("1. LIVE GROUNDED TEST (Real LLM, no mock)")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Live Grounded 7.4")
            live_sid = str(s.id)
            break

        live_events = await run_sse_request(client, live_sid, token, "Transformer ra đời vào năm nào?")
        live_event_names = [e[0] for e in live_events]
        print(f"Live SSE event sequence: {live_event_names}")
        assert "replace" not in live_event_names
        assert live_event_names == ["status", "status", "token", "citation", "done"]
        token_delta = next(d["delta"] for e, d in live_events if e == "token")
        print(f"Live Token Delta: {token_delta}")
        assert "2017" in token_delta
        print("-> Live Grounded Test PASSED (No replace event emitted)!\n")

        # ============================================================
        # 2. MOCK TEST A: Judge 1 >= 0.7 (Grounded -> No replace)
        # ============================================================
        print("=" * 60)
        print("2. MOCK TEST A: Judge 1 >= 0.7 (Grounded)")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Mock Grounded")
            sid_a = str(s.id)
            break

        with patch(
            "app.services.rag_service.score_faithfulness",
            new=AsyncMock(return_value=(JudgeScore(score=0.95, reasoning="Good"), TokenUsage())),
        ):
            events_a = await run_sse_request(client, sid_a, token, "Transformer ra đời năm nào?")
            names_a = [e[0] for e in events_a]
            print(f"Events: {names_a}")
            assert "replace" not in names_a
            assert "token" in names_a
            assert "done" in names_a
            print("-> Mock Test A PASSED!\n")

        # ============================================================
        # 3. MOCK TEST B: Judge 1 = 0.4 (Fail), Retry Judge = 0.9 (Success)
        # ============================================================
        print("=" * 60)
        print("3. MOCK TEST B: Judge 1 = 0.4 (Fail), Retry Judge = 0.9 (Success)")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Mock Retry OK")
            sid_b = str(s.id)
            break

        judge_side_effects = [
            (JudgeScore(score=0.4, reasoning="Ungrounded draft"), TokenUsage()),
            (JudgeScore(score=0.9, reasoning="Retry grounded"), TokenUsage()),
        ]

        with patch(
            "app.services.rag_service.score_faithfulness",
            new=AsyncMock(side_effect=judge_side_effects),
        ):
            events_b = await run_sse_request(client, sid_b, token, "Transformer ra đời năm nào?")
            names_b = [e[0] for e in events_b]
            print(f"Events: {names_b}")
            assert names_b.count("replace") == 1
            assert names_b.count("token") == 1
            replace_payload = next(d for e, d in events_b if e == "replace")
            token_payload = next(d for e, d in events_b if e == "token")
            done_payload = next(d for e, d in events_b if e == "done")
            print(f"Draft token: {token_payload['delta'][:40]}...")
            print(f"Replace content: {replace_payload['content'][:40]}...")
            assert replace_payload["content"] != token_payload["delta"]
            assert len(replace_payload["citations"]) > 0
            assert done_payload["citations"] == replace_payload["citations"]

            # Verify DB contains final message
            async for db in get_db():
                msg = await db.get(ChatMessage, uuid.UUID(done_payload["message_id"]))
                assert msg.content == replace_payload["content"]
                break

            print("-> Mock Test B PASSED!\n")

        # ============================================================
        # 4. MOCK TEST C: Judge 1 = 0.4, Retry Judge = 0.4 (Fail -> Refusal)
        # ============================================================
        print("=" * 60)
        print("4. MOCK TEST C: Judge 1 = 0.4, Retry Judge = 0.4 (Both Fail -> Refusal)")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Mock Double Fail")
            sid_c = str(s.id)
            break

        double_fail_side_effects = [
            (JudgeScore(score=0.4, reasoning="Draft ungrounded"), TokenUsage()),
            (JudgeScore(score=0.4, reasoning="Retry still ungrounded"), TokenUsage()),
        ]

        with patch(
            "app.services.rag_service.score_faithfulness",
            new=AsyncMock(side_effect=double_fail_side_effects),
        ):
            events_c = await run_sse_request(client, sid_c, token, "Transformer ra đời năm nào?")
            names_c = [e[0] for e in events_c]
            print(f"Events: {names_c}")
            assert names_c.count("replace") == 1
            assert names_c.count("token") == 1
            replace_payload = next(d for e, d in events_c if e == "replace")
            done_payload = next(d for e, d in events_c if e == "done")
            print(f"Replace content: {replace_payload['content']}")
            print(f"Replace citations: {replace_payload['citations']}")
            assert replace_payload["content"] == REFUSAL_SENTENCE
            assert replace_payload["citations"] == []
            assert done_payload["citations"] == []
            print("-> Mock Test C PASSED!\n")

        # ============================================================
        # 5. MOCK TEST D: Output Moderation Flagged (Fail -> Refusal)
        # ============================================================
        print("=" * 60)
        print("5. MOCK TEST D: Output Moderation Flagged (Flagged -> Refusal)")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Mock Output Mod")
            sid_d = str(s.id)
            break

        async def mock_mod(text):
            # Flag output, allow input
            if text == "Transformer ra đời năm nào?":
                return False
            return True

        with patch("app.services.rag_service.moderate_text", new=AsyncMock(side_effect=mock_mod)):
            events_d = await run_sse_request(client, sid_d, token, "Transformer ra đời năm nào?")
            names_d = [e[0] for e in events_d]
            print(f"Events: {names_d}")
            assert names_d.count("replace") == 1
            replace_payload = next(d for e, d in events_d if e == "replace")
            print(f"Replace content: {replace_payload['content']}")
            assert replace_payload["content"] == REFUSAL_SENTENCE
            assert replace_payload["citations"] == []
            print("-> Mock Test D PASSED!\n")

        # ============================================================
        # 6. MOCK TEST E: Input Moderation Flagged
        # ============================================================
        print("=" * 60)
        print("6. MOCK TEST E: Input Moderation Flagged")
        print("=" * 60)
        async for db in get_db():
            s = await create_session(db, EVAL_USER_ID, doc_id, "Mock Input Mod")
            sid_e = str(s.id)
            break

        with patch("app.services.rag_service.moderate_text", new=AsyncMock(return_value=True)):
            events_e = await run_sse_request(client, sid_e, token, "Bad input prompt")
            names_e = [e[0] for e in events_e]
            print(f"Events: {names_e}")
            assert "replace" not in names_e
            assert "citation" not in names_e
            assert names_e == ["token", "done"]
            token_payload = next(d for e, d in events_e if e == "token")
            assert token_payload["delta"] == REFUSAL_SENTENCE
            print("-> Mock Test E PASSED!\n")

        # ============================================================
        # 7. DIRECT ask() TEST WITH MOCK (Ensures ask() returns final)
        # ============================================================
        print("=" * 60)
        print("7. DIRECT ask() WITH MOCK (Verify ask() returns final answer, not draft)")
        print("=" * 60)
        async for db in get_db():
            with patch(
                "app.services.rag_service.score_faithfulness",
                new=AsyncMock(side_effect=double_fail_side_effects),
            ):
                res = await ask(db, doc_id, "Transformer ra đời năm nào?")
                print(f"Direct ask() result: {res.answer}")
                assert res.answer == REFUSAL_SENTENCE
                assert res.grounded is False
            break
        print("-> Direct ask() with mock PASSED!\n")

        print("=" * 60)
        print("ALL 7.4 TESTS (LIVE & MOCKS) PASSED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
