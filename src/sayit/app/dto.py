from pydantic import BaseModel, Field

from sayit.domain.models import DetectedIntent, RewritePlan


class NormalizedInput(BaseModel):
    raw_text: str
    source: str
    inferred_language: str = "zh"
    path: str | None = None
    facts: dict[str, list[str]] = Field(default_factory=dict)


class ExplainResult(BaseModel):
    original_text: str
    detected_intent: DetectedIntent
    plan: RewritePlan
    suggestions: list[str] = Field(default_factory=list)
