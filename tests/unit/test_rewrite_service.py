from sayit.app.services.rewrite_service import RewriteService
from sayit.domain.models import ModeType, RewriteRequest
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.ai.manager import AIRewriteManager
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.generator import LocalGenerator
from sayit.engines.local.templates import TemplateRepository
from sayit.infra.config import AppConfig


def test_rewrite_service_generates_three_local_candidates() -> None:
    templates = TemplateRepository()
    config = AppConfig()
    service = RewriteService(
        config=config,
        detector=LocalIntentDetector(templates),
        planner=RewritePlanner(),
        local_generator=LocalGenerator(templates),
        validator=CandidateValidator(),
        scorer=CandidateScorer(),
        ai_manager=AIRewriteManager(config),
    )

    result = service.rewrite(
        RewriteRequest(
            text="你这个怎么还没弄完",
            mode=ModeType.LOCAL,
            language="zh",
            variants=3,
        )
    )

    assert result.detected_intent.primary.value == "follow_up"
    assert [candidate.label for candidate in result.candidates] == ["polite", "direct", "firm"]
