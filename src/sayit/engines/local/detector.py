import re
from collections import Counter, defaultdict

from sayit.domain.models import ContextType, DetectedIntent, IntentType, RiskFlag
from sayit.engines.local.templates import TemplateRepository


class LocalIntentDetector:
    def __init__(self, templates: TemplateRepository) -> None:
        self._templates = templates

    def detect(
        self,
        text: str,
        language: str = "zh",
        context: ContextType | None = None,
    ) -> DetectedIntent:
        rules = self._templates.load_rules(language)
        intent_scores: defaultdict[IntentType, float] = defaultdict(float)
        risk_counter: Counter[RiskFlag] = Counter()
        matched_rules = 0

        for rule in rules:
            patterns = rule.get("patterns", [])
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                intent = IntentType(rule["intent"])
                intent_scores[intent] += float(rule.get("weight", 1.0))
                for item in rule.get("risk_flags", []):
                    risk_counter[RiskFlag(item)] += 1
                matched_rules += 1

        primary = self._pick_primary_intent(intent_scores, text)
        if primary == IntentType.UNKNOWN:
            risk_counter[RiskFlag.TOO_VAGUE] += 1

        if primary == IntentType.FOLLOW_UP and not re.search(r"(今天|明天|尽快|本周|这周|时间点)", text):
            risk_counter[RiskFlag.LACKS_TIMEPOINT] += 1
        if primary in (IntentType.FOLLOW_UP, IntentType.REQUEST, IntentType.COMPLAINT):
            risk_counter[RiskFlag.LACKS_BUFFER] += 1
        if primary in (IntentType.FOLLOW_UP, IntentType.REQUEST, IntentType.COMPLAINT):
            risk_counter[RiskFlag.LACKS_COLLABORATION] += 1

        if re.search(r"(马上|立刻|赶紧|先把.*转我)", text):
            risk_counter[RiskFlag.COMMANDING] += 1
        if re.search(r"(怎么还|怎么又|你这边到底)", text):
            risk_counter[RiskFlag.ACCUSATORY] += 1
            risk_counter[RiskFlag.TOO_BLUNT] += 1
        if len(text.strip()) <= 4:
            risk_counter[RiskFlag.TOO_VAGUE] += 1

        top_score = max(intent_scores.values(), default=0.0)
        secondary = [
            intent
            for intent, score in intent_scores.items()
            if intent != primary and top_score and score >= top_score * 0.65
        ]
        confidence = min(0.45 + 0.12 * matched_rules + 0.08 * top_score, 0.97)
        if primary == IntentType.UNKNOWN:
            confidence = 0.28
        if context == ContextType.BARGAIN and primary == IntentType.UNKNOWN:
            primary = IntentType.NEGOTIATION
            confidence = 0.52

        ordered_risks = [
            flag
            for flag, _count in risk_counter.most_common()
        ]
        return DetectedIntent(
            primary=primary,
            secondary=secondary[:2],
            confidence=round(confidence, 3),
            risk_flags=ordered_risks,
        )

    def _pick_primary_intent(
        self,
        scores: dict[IntentType, float],
        text: str,
    ) -> IntentType:
        if scores:
            return max(scores.items(), key=lambda item: item[1])[0]
        stripped = text.strip()
        if any(token in stripped for token in ("抱歉", "不好意思")):
            return IntentType.APOLOGY
        if any(token in stripped for token in ("太贵", "价格", "预算")):
            return IntentType.NEGOTIATION
        if any(token in stripped for token in ("不去", "来不了", "不想去")):
            return IntentType.REFUSAL
        if any(token in stripped for token in ("麻烦", "请", "帮我")):
            return IntentType.REQUEST
        return IntentType.UNKNOWN
