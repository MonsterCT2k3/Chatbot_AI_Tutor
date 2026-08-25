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
    async for db in get_db():
        docs = await ensure_eval_documents(db, {"b1-full.pdf"})
        doc_id = str(docs["b1-full.pdf"])
        token = create_access_token(str(EVAL_USER_ID))
        session = await create_session(db, EVAL_USER_ID, docs["b1-full.pdf"], "Test 7.6 Delete Ask")
        session_id = str(session.id)
        break

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver/api", timeout=60.0) as client:
        print("=" * 60)
        print("1. VERIFY POST /api/documents/{id}/ask IS 404 (DEAD)")
        print("=" * 60)
        resp_dead_ask = await client.post(
            f"/documents/{doc_id}/ask",
            headers=headers,
            json={"question": "Transformer ra đời vào năm nào?"},
        )
        print("HTTP Status:", resp_dead_ask.status_code)
        print("Response body:", resp_dead_ask.json())
        assert resp_dead_ask.status_code == 404
        assert resp_dead_ask.status_code != 200

        print("\n" + "=" * 60)
        print("2. VERIFY OPENAPI SCHEMA (/openapi.json)")
        print("=" * 60)
        openapi_resp = await client.get("/../openapi.json")
        openapi = openapi_resp.json()
        paths = openapi.get("paths", {})
        ask_paths = [p for p in paths if p.rstrip("/").endswith("/ask")]
        feedback_paths = [p for p in paths if "feedback" in p]
        print("Paths ending with /ask:", ask_paths)
        print("Paths containing feedback:", feedback_paths)
        assert len(ask_paths) == 0, f"Found unexpected /ask paths in openapi: {ask_paths}"
        assert len(feedback_paths) > 0, "Missing feedback path in openapi"

        print("\n" + "=" * 60)
        print("3. VERIFY SESSION MESSAGE (JSON & SSE) + GET ANSWER_ID")
        print("=" * 60)
        resp_msg = await client.post(
            f"/sessions/{session_id}/messages",
            headers=headers,
            json={"question": "Transformer ra đời vào năm nào?"},
        )
        print("Session Message HTTP Status:", resp_msg.status_code)
        msg_body = resp_msg.json()
        print("Envelope data:", msg_body.get("data", {}))
        assert resp_msg.status_code == 200
        answer_id = msg_body["data"]["answer_id"]
        assert answer_id is not None
        print("Got answer_id for feedback test:", answer_id)

        print("\n" + "=" * 60)
        print("4. VERIFY FEEDBACK ROUTE IS ALIVE (HTTP 204)")
        print("=" * 60)
        feedback_resp = await client.post(
            f"/documents/{doc_id}/ask/{answer_id}/feedback",
            headers=headers,
            json={"is_positive": True, "reason": "Great answer"},
        )
        print("Feedback HTTP Status:", feedback_resp.status_code)
        assert feedback_resp.status_code == 204

        print("\n" + "=" * 60)
        print("5. VERIFY DIRECT ask() FOR EVAL / OFFLINE CALLERS")
        print("=" * 60)
        async for db in get_db():
            res = await ask(db, uuid.UUID(doc_id), "Transformer ra đời vào năm nào?")
            print("Direct ask() answer:", res.answer)
            print("Direct ask() grounded:", res.grounded)
            print("Direct ask() call_group_id:", res.call_group_id)
            assert "2017" in res.answer
            assert res.grounded is True
            break

        print("\n" + "=" * 60)
        print("ALL 7.6 TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
