import json


def format_sse(event: str, data: dict) -> str:
    """Format a server-sent event string according to the SSE standard.

    Format:
        event: <event_name>\\n
        data: <json_string>\\n\\n
    """
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"
