from sayit.domain.models import (
    Candidate,
    DetectedIntent,
    ModeType,
    RewriteRequest,
    RewriteResult,
)
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.ai.manager import AIRewriteManager, ProviderUnavailableError
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.generator import LocalGenerator
from sayit.infra.config import AppConfig


class RewriteService:
    def __init__(
        self,
        config: AppConfig,
        detector: LocalIntentDetector,
        planner: RewritePlanner,
        local_generator: LocalGenerator,
        validator: CandidateValidator,
        scorer: CandidateScorer,
        ai_manager: AIRewriteManager,
    ) -> None:
        self._config = config
        self._detector = detector
        self._planner = planner
        self._local_generator = local_generator
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
        resolved_mode = self._resolve_mode(request.mode)

        candidates: list[Candidate]
        engine = resolved_mode.value

        if resolved_mode == ModeType.LOCAL:
            candidates = self._local_generator.generate(request, plan)
        elif resolved_mode == ModeType.AI:
            candidates = self._ai_manager.rewrite(request, detected, plan)
        else:
            try:
                candidates = self._ai_manager.rewrite(request, detected, plan)
                engine = "hybrid"
            except ProviderUnavailableError:
                candidates = self._local_generator.generate(request, plan)
                engine = "hybrid(local-fallback)"

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
            engine=engine,
        )

    def _resolve_mode(self, mode: ModeType) -> ModeType:
        if mode != ModeType.AUTO:
            return mode
        if self._ai_manager.has_available_provider():
            return ModeType.HYBRID
        return ModeType.LOCAL

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
