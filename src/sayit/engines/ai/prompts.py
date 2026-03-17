from sayit.domain.models import DetectedIntent, RewritePlan, RewriteRequest

SYSTEM_PROMPT = """You rewrite short user messages into concise sendable alternatives.

Rules:
- preserve the user's intent
- do not invent facts, reasons, dates, or commitments
- keep the output short and directly sendable
- return strict JSON only
"""


def build_user_prompt(
    request: RewriteRequest,
    detected: DetectedIntent,
    plan: RewritePlan,
) -> str:
    return f"""
Input text: {request.text}
Language: {request.language or "zh"}
Intent: {detected.primary.value}
Risk flags: {[risk.value for risk in detected.risk_flags]}
Requested tone: {request.tone.value if request.tone else "auto"}
Variant tones: {[tone.value for tone in plan.variant_tones]}
Constraints: {plan.constraints}
Style moves: {plan.style_moves}

Return JSON with fields:
- intent
- risk_flags
- candidates: array of objects with label and text
""".strip()
