from sayit.domain.models import ContextType, IntentType

MVP_INTENTS = [
    IntentType.FOLLOW_UP,
    IntentType.REFUSAL,
    IntentType.REQUEST,
    IntentType.APOLOGY,
    IntentType.NEGOTIATION,
    IntentType.COMPLAINT,
]

INTENT_DESCRIPTIONS: dict[IntentType, str] = {
    IntentType.FOLLOW_UP: "跟进或催进度，目标是推动对方给出状态或时间点。",
    IntentType.REFUSAL: "明确拒绝、无法参加或不接受某事。",
    IntentType.REQUEST: "提出请求、拜托处理或推动对方行动。",
    IntentType.APOLOGY: "道歉、解释、缓和影响。",
    IntentType.NEGOTIATION: "议价、协商条件、表达预算压力。",
    IntentType.COMPLAINT: "表达不满，但仍希望继续推进沟通。",
    IntentType.BOUNDARY: "设边界、拒绝不合理要求。",
    IntentType.CONFIRMATION: "确认安排、推进下一步。",
    IntentType.UNKNOWN: "语义不足，无法稳定判断意图。",
}

DEFAULT_CONTEXT_BY_INTENT: dict[IntentType, ContextType] = {
    IntentType.FOLLOW_UP: ContextType.WORK,
    IntentType.REFUSAL: ContextType.SOCIAL,
    IntentType.REQUEST: ContextType.WORK,
    IntentType.APOLOGY: ContextType.WORK,
    IntentType.NEGOTIATION: ContextType.BARGAIN,
    IntentType.COMPLAINT: ContextType.WORK,
    IntentType.BOUNDARY: ContextType.WORK,
    IntentType.CONFIRMATION: ContextType.WORK,
}
