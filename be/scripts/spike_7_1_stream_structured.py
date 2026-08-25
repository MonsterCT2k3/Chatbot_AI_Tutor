import asyncio
import json
import time

from app.config import settings
from app.services.rag_service import StructuredAnswer, _SYSTEM_PROMPT, _groq_client

# Section 2 Prompt — cô lập Groq, không DB, không OpenAI, không rerank
MESSAGES = [
    {"role": "system", "content": _SYSTEM_PROMPT},
    {
        "role": "user",
        "content": (
            "<context>\n"
            "[Trang 22]\n"
            "Transformer ra đời năm 2017.\n\n"
            "[Trang 39]\n"
            "RLHF gồm 3 bước: model viết nhiều câu trả lời; người chấm xếp hạng; huấn luyện theo điểm.\n"
            "</context>\n\n"
            "<question>\n"
            "Transformer ra đời vào năm nào?\n"
            "</question>"
        ),
    },
]


async def run_spike():
    # 3.1 Đối chứng (đường production)
    t0 = time.perf_counter()
    try:
        baseline_resp = await _groq_client.beta.chat.completions.parse(
            model=settings.GROQ_CHAT_MODEL,
            messages=MESSAGES,
            response_format=StructuredAnswer,
        )
        t_baseline_ms = (time.perf_counter() - t0) * 1000
        baseline_parsed: StructuredAnswer = baseline_resp.choices[0].message.parsed
    except Exception as exc:
        print(f"BASELINE FAILED: {type(exc).__name__}: {str(exc)[:500]}")
        print("CHOICE=B")
        print("T_BASELINE_MS=null")
        print("T_FIRST_DELTA_MS=null")
        print("T_STREAM_FULL_MS=null")
        print("SEGMENTS=[]")
        print("STREAM_HAS_TEXT_DELTAS=false")
        print("PARSE_STREAM_OK=false")
        print(f"ERROR={type(exc).__name__}: {str(exc)[:200]}")
        return

    # 3.2 — parse(..., stream=True) rồi beta.stream (họ parse). Không gọi create() nếu bước 2 được.
    parse_kw_err = None
    try:
        await _groq_client.beta.chat.completions.parse(
            model=settings.GROQ_CHAT_MODEL,
            messages=MESSAGES,
            response_format=StructuredAnswer,
            stream=True,
        )
        parse_kw_ok = True
    except Exception as exc:
        parse_kw_ok = False
        parse_kw_err = f"{type(exc).__name__}: {str(exc)[:200]}"

    t0 = time.perf_counter()
    t_first_delta_ms = None
    t_stream_full_ms = None
    deltas = []
    beta_stream_parsed = None
    beta_stream_err = None
    try:
        async with _groq_client.beta.chat.completions.stream(
            model=settings.GROQ_CHAT_MODEL,
            messages=MESSAGES,
            response_format=StructuredAnswer,
        ) as stream:
            async for event in stream:
                now = time.perf_counter()
                piece = None
                if event.type == "chunk" and event.chunk.choices:
                    piece = event.chunk.choices[0].delta.content
                elif event.type == "content.delta":
                    piece = event.delta
                if piece:
                    if t_first_delta_ms is None:
                        t_first_delta_ms = (now - t0) * 1000
                    deltas.append(piece)
            final_completion = await stream.get_final_completion()
            beta_stream_parsed = final_completion.choices[0].message.parsed
        t_stream_full_ms = (time.perf_counter() - t0) * 1000
    except Exception as exc:
        t_stream_full_ms = (time.perf_counter() - t0) * 1000
        beta_stream_err = f"{type(exc).__name__}: {str(exc)[:200]}"

    jsonish = lambda s: str(s).lstrip().startswith(("{", "["))
    stream_has_text_deltas = any(d and not jsonish(d) for d in deltas)

    segs = getattr(beta_stream_parsed, "segments", None) or []
    has_ok_page = any(getattr(seg, "page_number", None) in (22, 39) for seg in segs)
    parse_stream_ok = beta_stream_parsed is not None  # bước 2 — họ parse

    if parse_stream_ok and t_first_delta_ms is not None and has_ok_page:
        choice = "A"
        chosen_parsed = beta_stream_parsed
    else:
        # Không thử C (create) khi đã có kết luận A/B từ bước 2. Fail bước 2 → B.
        choice = "B"
        chosen_parsed = baseline_parsed

    segments_json = json.dumps(
        [{"text": seg.text, "page_number": seg.page_number} for seg in chosen_parsed.segments],
        ensure_ascii=False,
    )
    error_str = parse_kw_err or beta_stream_err or "none"

    print(f"CHOICE={choice}")
    print(f"T_BASELINE_MS={t_baseline_ms:.1f}")
    print(f"T_FIRST_DELTA_MS={f'{t_first_delta_ms:.1f}' if t_first_delta_ms is not None else 'null'}")
    print(f"T_STREAM_FULL_MS={f'{t_stream_full_ms:.1f}' if t_stream_full_ms is not None else 'null'}")
    print(f"SEGMENTS={segments_json}")
    print(f"STREAM_HAS_TEXT_DELTAS={'true' if stream_has_text_deltas else 'false'}")
    print(f"PARSE_STREAM_OK={'true' if parse_stream_ok else 'false'}")
    print(f"ERROR={error_str}")
    print(f"PARSE_KWARG_STREAM_OK={'true' if parse_kw_ok else 'false'}")


if __name__ == "__main__":
    asyncio.run(run_spike())
