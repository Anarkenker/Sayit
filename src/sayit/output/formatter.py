import json

from sayit.app.dto import ExplainResult
from sayit.domain.intents import INTENT_DESCRIPTIONS
from sayit.domain.models import RewriteResult
from sayit.domain.risks import RISK_DESCRIPTIONS
from sayit.output.json_formatter import format_json_payload
from sayit.output.plain_formatter import format_plain_candidates


def format_rewrite(result: RewriteResult, output_format: str, show_notes: bool = True) -> str:
    if output_format == "json":
        return format_json_payload(result.model_dump(mode="json"))
    if output_format == "plain":
        return format_plain_candidates(result.candidates)
    return _format_pretty_rewrite(result, show_notes=show_notes)


def format_explain(result: ExplainResult, output_format: str) -> str:
    if output_format == "json":
        return format_json_payload(result.model_dump(mode="json"))

    lines = [
        "Original:",
        result.original_text,
        "",
        "Intent:",
        f"- {result.detected_intent.primary.value}: {INTENT_DESCRIPTIONS[result.detected_intent.primary]}",
        f"- confidence: {result.detected_intent.confidence:.2f}",
        "",
        "Risk:",
    ]
    for risk in result.detected_intent.risk_flags:
        lines.append(f"- {risk.value}: {RISK_DESCRIPTIONS[risk]}")
    lines.extend(["", "Plan:"])
    lines.append(f"- audience: {result.plan.audience}")
    lines.append(f"- context: {result.plan.context.value if result.plan.context else 'unknown'}")
    for move in result.plan.style_moves:
        lines.append(f"- {move}")
    lines.extend(["", "Suggestions:"])
    for suggestion in result.suggestions:
        lines.append(f"- {suggestion}")
    return "\n".join(lines)


def _format_pretty_rewrite(result: RewriteResult, show_notes: bool) -> str:
    lines = [
        "Original:",
        result.original_text,
        "",
        "Intent:",
        f"- {result.detected_intent.primary.value}",
        "",
        "Risk:",
    ]
    if result.detected_intent.risk_flags:
        for risk in result.detected_intent.risk_flags:
            lines.append(f"- {risk.value}")
    else:
        lines.append("- none")

    lines.extend(["", "Candidates:"])
    for candidate in result.candidates:
        lines.append(f"{candidate.label.capitalize()}:")
        lines.append(candidate.text)
        if show_notes and candidate.notes:
            lines.extend([f"- note: {note}" for note in candidate.notes])
        lines.append("")

    lines.append(f"Engine: {result.engine}")
    return "\n".join(lines).strip()
