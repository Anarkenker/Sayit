import re

from sayit.domain.intents import DEFAULT_CONTEXT_BY_INTENT
from sayit.domain.models import (
    ContextType,
    DetectedIntent,
    IntentType,
    RewritePlan,
    RewriteRequest,
    RiskFlag,
    ToneType,
)


STYLE_MOVES_BY_RISK: dict[RiskFlag, list[str]] = {
    RiskFlag.ACCUSATORY: ["去掉责备式开头", "保留推进意图", "给对方回应空间"],
    RiskFlag.TOO_BLUNT: ["缓和开头", "减少命令感"],
    RiskFlag.TOO_WEAK: ["保持立场清晰", "避免过度道歉"],
    RiskFlag.TOO_VAGUE: ["补齐目标动作", "让对方知道下一步"],
    RiskFlag.COMMANDING: ["改为合作式请求", "保留核心诉求"],
    RiskFlag.LACKS_BUFFER: ["增加缓冲语", "让语气更可发送"],
    RiskFlag.LACKS_TIMEPOINT: ["尽量要求明确时间点", "避免空泛跟进"],
    RiskFlag.LACKS_COLLABORATION: ["加入配合姿态", "减少对立感"],
}


class RewritePlanner:
    def build(self, request: RewriteRequest, detected: DetectedIntent) -> RewritePlan:
        context = request.context or self._infer_context(request.text, detected.primary)
        audience = request.audience or self._infer_audience(request.text, context)
        variant_tones = self._resolve_variant_tones(request.tone, request.variants, detected.primary)
        constraints = self._collect_constraints(request.text, detected.primary, request.preserve_facts)
        style_moves = self._collect_style_moves(detected, detected.primary)
        return RewritePlan(
            intent=detected.primary,
            target_tone=request.tone,
            variant_tones=variant_tones,
            audience=audience,
            context=context,
            constraints=constraints,
            style_moves=style_moves,
        )

    def _infer_context(self, text: str, intent: IntentType) -> ContextType | None:
        lower = text.lower()
        if any(token in lower for token in ("报价", "价格", "预算", "discount", "quote")):
            return ContextType.BARGAIN
        if any(token in lower for token in ("客户", "client", "邮件", "email")):
            return ContextType.EMAIL
        if any(token in lower for token in ("朋友", "聚会", "吃饭", "约")):
            return ContextType.SOCIAL
        return DEFAULT_CONTEXT_BY_INTENT.get(intent)

    def _infer_audience(self, text: str, context: ContextType | None) -> str:
        lower = text.lower()
        if any(token in lower for token in ("老板", "领导", "boss")):
            return "boss"
        if any(token in lower for token in ("客户", "client")):
            return "client"
        if context == ContextType.SOCIAL:
            return "friend"
        return "colleague"

    def _resolve_variant_tones(
        self,
        requested_tone: ToneType | None,
        variants: int,
        intent: IntentType,
    ) -> list[ToneType]:
        base_order = [ToneType.POLITE, ToneType.DIRECT, ToneType.FIRM, ToneType.SOFT]
        if intent in (IntentType.REFUSAL, IntentType.APOLOGY):
            base_order = [ToneType.SOFT, ToneType.POLITE, ToneType.DIRECT, ToneType.FIRM]
        if requested_tone:
            order = [requested_tone, *[tone for tone in base_order if tone != requested_tone]]
        else:
            order = base_order
        return order[:variants]

    def _collect_constraints(
        self,
        text: str,
        intent: IntentType,
        preserve_facts: bool,
    ) -> list[str]:
        constraints: list[str] = []
        if preserve_facts:
            if re.search(r"\d", text):
                constraints.append("保留数字、金额和日期信息")
            if re.search(r"https?://", text):
                constraints.append("保留链接")
        if intent == IntentType.FOLLOW_UP:
            constraints.extend(["保留催进度意图", "避免指责"])
        elif intent == IntentType.REFUSAL:
            constraints.extend(["保留拒绝立场", "不要过度解释"])
        elif intent == IntentType.REQUEST:
            constraints.extend(["保留请求动作", "减少命令感"])
        elif intent == IntentType.APOLOGY:
            constraints.extend(["承认影响", "避免虚构理由"])
        elif intent == IntentType.NEGOTIATION:
            constraints.extend(["保留预算压力", "争取谈判空间"])
        elif intent == IntentType.COMPLAINT:
            constraints.extend(["表达问题", "保留继续合作空间"])
        return constraints

    def _collect_style_moves(
        self,
        detected: DetectedIntent,
        intent: IntentType,
    ) -> list[str]:
        style_moves: list[str] = []
        for risk in detected.risk_flags:
            style_moves.extend(STYLE_MOVES_BY_RISK.get(risk, []))
        if intent == IntentType.FOLLOW_UP:
            style_moves.extend(["增加确认语气", "尽量引导对方给出下一步"])
        elif intent == IntentType.REFUSAL:
            style_moves.extend(["表达清楚但不过分生硬", "结尾留出余地"])
        elif intent == IntentType.REQUEST:
            style_moves.extend(["开头先缓冲", "结尾保留礼貌请求"])
        elif intent == IntentType.APOLOGY:
            style_moves.extend(["先承认影响", "再给出处理方式"])
        elif intent == IntentType.NEGOTIATION:
            style_moves.extend(["先说明预算压力", "再提出调整空间"])
        elif intent == IntentType.COMPLAINT:
            style_moves.extend(["先陈述问题", "避免升级冲突"])
        return list(dict.fromkeys(style_moves))
