from enum import Enum

from pydantic import BaseModel, Field


class ModeType(str, Enum):
    AUTO = "auto"
    LOCAL = "local"
    AI = "ai"
    HYBRID = "hybrid"


class ToneType(str, Enum):
    POLITE = "polite"
    DIRECT = "direct"
    FIRM = "firm"
    SOFT = "soft"


class ContextType(str, Enum):
    WORK = "work"
    SOCIAL = "social"
    EMAIL = "email"
    BARGAIN = "bargain"
    SUPPORT = "support"


class IntentType(str, Enum):
    FOLLOW_UP = "follow_up"
    REFUSAL = "refusal"
    REQUEST = "request"
    APOLOGY = "apology"
    NEGOTIATION = "negotiation"
    COMPLAINT = "complaint"
    BOUNDARY = "boundary"
    CONFIRMATION = "confirmation"
    UNKNOWN = "unknown"


class RiskFlag(str, Enum):
    ACCUSATORY = "accusatory"
    TOO_BLUNT = "too_blunt"
    TOO_WEAK = "too_weak"
    TOO_VAGUE = "too_vague"
    COMMANDING = "commanding"
    LACKS_BUFFER = "lacks_buffer"
    LACKS_TIMEPOINT = "lacks_timepoint"
    LACKS_COLLABORATION = "lacks_collaboration"
    FACT_DRIFT = "fact_drift"
    FABRICATED_REASON = "fabricated_reason"


class RewriteRequest(BaseModel):
    text: str
    context: ContextType | None = None
    tone: ToneType | None = None
    audience: str | None = None
    variants: int = Field(default=3, ge=1, le=6)
    mode: ModeType = ModeType.AUTO
    preserve_facts: bool = True
    language: str | None = None
    source: str | None = None


class DetectedIntent(BaseModel):
    primary: IntentType
    secondary: list[IntentType] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    risk_flags: list[RiskFlag] = Field(default_factory=list)


class RewritePlan(BaseModel):
    intent: IntentType
    target_tone: ToneType | None = None
    variant_tones: list[ToneType] = Field(default_factory=list)
    audience: str
    context: ContextType | None = None
    constraints: list[str] = Field(default_factory=list)
    style_moves: list[str] = Field(default_factory=list)


class Candidate(BaseModel):
    label: str
    text: str
    notes: list[str] = Field(default_factory=list)
    score: float | None = None


class RewriteResult(BaseModel):
    original_text: str
    detected_intent: DetectedIntent
    plan: RewritePlan
    candidates: list[Candidate]
    engine: str = "local"
