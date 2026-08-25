import asyncio
import json
import uuid
import httpx

from app.database import get_db
from app.evaluation.eval_documents import ensure_eval_documents, EVAL_USER_ID
from app.main import app
from app.services.auth_service import create_access_token
from app.services.session_service import create_session


async def main():
    async for db in get_db():
        docs = await ensure_eval_documents(db, {"b1-full.pdf"})
        doc_id = docs["b1-full.pdf"]
        session = await create_session(db, EVAL_USER_ID, doc_id, "Test 7.2 SSE verification")
        session_id = str(session.id)
        token = create_access_token(EVAL_USER_ID)
        break

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver/api", timeout=60.0) as client:
        print("=" * 60)
        print("1. TESTING JSON PATH (Default, Non-SSE)")
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

        print("\n" + "=" * 60)
        print("2. TESTING SSE PATH (Accept: text/event-stream & stream=1)")
        print("=" * 60)
        sse_headers = {
            **headers,
            "Accept": "text/event-stream",
        }
        events_received = []
        async with client.stream(
            "POST",
            f"/sessions/{session_id}/messages?stream=1",
            headers=sse_headers,
            json={"question": "Kiến trúc Transformer gồm những thành phần chính nào?"},
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
                    events_received.append((current_event, data))
                    print(f"-> EVENT [{current_event}]: {data}")
                    current_event = None

        event_names = [e[0] for e in events_received]
        print(f"\nReceived event sequence: {event_names}")
        assert "status" in event_names
        assert "token" in event_names
        assert "done" in event_names
        done_data = next(d for e, d in events_received if e == "done")
        print(f"Done event payload: message_id={done_data.get('message_id')}, answer_id={done_data.get('answer_id')}")
        assert done_data.get("message_id") is not None
        assert done_data.get("answer_id") is not None

        print("\n" + "=" * 60)
        print("3. TESTING 404 ON SSE REQUEST (Should return HTTP 404 JSON, NOT SSE)")
        print("=" * 60)
        fake_session_id = str(uuid.uuid4())
        resp_404 = await client.post(
            f"/sessions/{fake_session_id}/messages?stream=1",
            headers=sse_headers,
            json={"question": "Test 404"},
        )
        print("HTTP Status:", resp_404.status_code)
        print("Content-Type:", resp_404.headers.get("content-type"))
        print("Response body:", resp_404.json())
        assert resp_404.status_code == 404
        assert "application/json" in resp_404.headers.get("content-type", "")

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
