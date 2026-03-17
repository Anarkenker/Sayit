from sayit.app.dto import ExplainResult
from sayit.domain.models import RewriteRequest
from sayit.domain.planner import RewritePlanner
from sayit.engines.local.detector import LocalIntentDetector


class ExplainService:
    def __init__(
        self,
        detector: LocalIntentDetector,
        planner: RewritePlanner,
    ) -> None:
        self._detector = detector
        self._planner = planner

    def explain(self, request: RewriteRequest) -> ExplainResult:
        detected = self._detector.detect(
            text=request.text,
            language=request.language or "zh",
            context=request.context,
        )
        plan = self._planner.build(request, detected)
        suggestions = [
            "如果结果不够稳，优先补充场景或对象。",
            "当原句很短时，建议显式指定 --context 或 --tone。",
        ]
        if detected.primary.value == "unknown":
            suggestions.insert(0, "这句话过短或语义不清，补充目标动作会更稳定。")
        return ExplainResult(
            original_text=request.text,
            detected_intent=detected,
            plan=plan,
            suggestions=suggestions,
        )
