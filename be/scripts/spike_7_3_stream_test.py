import asyncio
import json
import uuid
import httpx

from app.database import get_db
from app.evaluation.eval_documents import ensure_eval_documents, EVAL_USER_ID
from app.main import app
from app.services.auth_service import create_access_token
from app.services.rag_service import ask
from app.services.session_service import create_session


async def main():
    print("=" * 60)
    print("1. SMOKE TEST DIRECT ask() (Used by evaluation & legacy callers)")
    print("=" * 60)
    async for db in get_db():
        docs = await ensure_eval_documents(db, {"b1-full.pdf"})
        doc_id = docs["b1-full.pdf"]
        res = await ask(db, doc_id, "Transformer ra đời vào năm nào?")
        print("ask() answer:", res.answer)
        print("ask() grounded:", res.grounded)
        print("ask() citations count:", len(res.citations))
        assert "2017" in res.answer
        assert len(res.citations) > 0

        session = await create_session(db, EVAL_USER_ID, doc_id, "Test 7.3 Beta Stream")
        session_id = str(session.id)
        token = create_access_token(EVAL_USER_ID)
        break

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver/api", timeout=60.0) as client:
        print("\n" + "=" * 60)
        print("2. TESTING JSON PATH (Default, Non-SSE)")
        print("=" * 60)
        resp_json = await client.post(
            f"/sessions/{session_id}/messages",
            headers=headers,
            json={"question": "Transformer ra đời vào năm nào?"},
        )
        print("HTTP Status:", resp_json.status_code)
        print("Content-Type:", resp_json.headers.get("content-type"))
        body = resp_json.json()
        print("Enveloped JSON Response:")
        print(f"  success: {body.get('success')}")
        print(f"  role: {body.get('data', {}).get('role')}")
        print(f"  content: {body.get('data', {}).get('content')}")
        print(f"  answer_id: {body.get('data', {}).get('answer_id')}")
        print(f"  citations: {body.get('data', {}).get('citations')}")
        assert resp_json.status_code == 200
        assert body.get("success") is True
        assert body.get("data", {}).get("content") is not None
        assert body.get("data", {}).get("answer_id") is not None

        # Create a fresh session for clean SSE first-turn test (no history)
        async for db in get_db():
            fresh_session = await create_session(db, EVAL_USER_ID, doc_id, "Fresh SSE 7.3")
            fresh_sid = str(fresh_session.id)
            break

        print("\n" + "=" * 60)
        print("3. TESTING SSE FIRST TURN (no history: retrieving -> generating -> token -> citation -> done)")
        print("=" * 60)
        sse_headers = {
            **headers,
            "Accept": "text/event-stream",
        }
        events_turn1 = []
        async with client.stream(
            "POST",
            f"/sessions/{fresh_sid}/messages?stream=1",
            headers=sse_headers,
            json={"question": "Transformer ra đời vào năm nào?"},
        ) as response:
            print("HTTP Status:", response.status_code)
            print("Content-Type:", response.headers.get("content-type"))
            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")

            current_event = None
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                if line.startswith("event:"):
                    current_event = line.split("event:", 1)[1].strip()
                elif line.startswith("data:") and current_event:
                    data_str = line.split("data:", 1)[1].strip()
                    data = json.loads(data_str)
                    events_turn1.append((current_event, data))
                    print(f"event: {current_event}\ndata: {json.dumps(data, ensure_ascii=False)}\n")
                    current_event = None

        turn1_names = [e[0] for e in events_turn1]
        print(f"Turn 1 Event sequence: {turn1_names}")
        stages_turn1 = [d["stage"] for e, d in events_turn1 if e == "status"]
        print(f"Turn 1 Stages: {stages_turn1}")
        assert stages_turn1 == ["retrieving", "generating"]
        token_delta = next(d["delta"] for e, d in events_turn1 if e == "token")
        print(f"Token delta: {repr(token_delta)}")
        assert not token_delta.strip().startswith("{\"segments\"")
        assert "2017" in token_delta

        done_turn1 = next(d for e, d in events_turn1 if e == "done")
        assert done_turn1.get("message_id") is not None
        assert done_turn1.get("answer_id") is not None

        print("\n" + "=" * 60)
        print("4. TESTING SSE FOLLOW-UP TURN (with history: contextualize -> retrieving -> generating -> token -> done)")
        print("=" * 60)
        events_turn2 = []
        async with client.stream(
            "POST",
            f"/sessions/{fresh_sid}/messages?stream=1",
            headers=sse_headers,
            json={"question": "Nó có điểm gì đặc biệt so với các mô hình trước đó?"},
        ) as response:
            current_event = None
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                if line.startswith("event:"):
                    current_event = line.split("event:", 1)[1].strip()
                elif line.startswith("data:") and current_event:
                    data_str = line.split("data:", 1)[1].strip()
                    data = json.loads(data_str)
                    events_turn2.append((current_event, data))
                    print(f"event: {current_event}\ndata: {json.dumps(data, ensure_ascii=False)}\n")
                    current_event = None

        turn2_names = [e[0] for e in events_turn2]
        print(f"Turn 2 Event sequence: {turn2_names}")
        stages_turn2 = [d["stage"] for e, d in events_turn2 if e == "status"]
        print(f"Turn 2 Stages: {stages_turn2}")
        assert stages_turn2 == ["contextualize", "retrieving", "generating"]

        print("\n" + "=" * 60)
        print("ALL 7.3 TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
