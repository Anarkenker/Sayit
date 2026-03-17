import json


def format_json_payload(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
