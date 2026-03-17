REWRITE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string"},
        "risk_flags": {"type": "array", "items": {"type": "string"}},
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["label", "text"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["intent", "risk_flags", "candidates"],
    "additionalProperties": False,
}
