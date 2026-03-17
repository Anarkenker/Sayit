from sayit.domain.models import (
    Candidate,
    DetectedIntent,
    RewriteRequest,
    RewriteResult,
)
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.ai.manager import AIRewriteManager, ProviderUnavailableError
from sayit.engines.local.detector import LocalIntentDetector
from sayit.infra.config import AppConfig


class RewriteService:
    def __init__(
        self,
        config: AppConfig,
        detector: LocalIntentDetector,
        planner: RewritePlanner,
        validator: CandidateValidator,
        scorer: CandidateScorer,
        ai_manager: AIRewriteManager,
    ) -> None:
        self._config = config
        self._detector = detector
        self._planner = planner
        self._validator = validator
        self._scorer = scorer
        self._ai_manager = ai_manager

    def rewrite(self, request: RewriteRequest) -> RewriteResult:
        detected = self._detector.detect(
            text=request.text,
            language=request.language or self._config.defaults.language,
            context=request.context,
        )
        plan = self._planner.build(request, detected)
        candidates = self._ai_manager.rewrite(request, detected, plan)

        validated = self._apply_validation(
            original_text=request.text,
            detected=detected,
            candidates=candidates,
            preserve_facts=request.preserve_facts,
        )
        ranked = self._scorer.rank(
            detected=detected,
            plan=plan,
            candidates=validated,
            requested_tone=request.tone,
        )
        return RewriteResult(
            original_text=request.text,
            detected_intent=detected,
            plan=plan,
            candidates=ranked[: request.variants],
            engine=self._ai_manager.provider_label(),
        )

    def _apply_validation(
        self,
        original_text: str,
        detected: DetectedIntent,
        candidates: list[Candidate],
        preserve_facts: bool,
    ) -> list[Candidate]:
        validated: list[Candidate] = []
        for candidate in candidates:
            issues = self._validator.validate(
                original_text=original_text,
                candidate_text=candidate.text,
                preserve_facts=preserve_facts,
                risk_flags=detected.risk_flags,
            )
            validated.append(
                candidate.model_copy(
                    update={
                        "notes": [*candidate.notes, *issues],
                    }
                )
            )
        return validated
