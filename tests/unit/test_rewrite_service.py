from sayit.app.services.rewrite_service import RewriteService
from sayit.domain.models import ModeType, RewriteRequest
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.rules import RuleRepository
from sayit.infra.config import AppConfig
from sayit.test_support import FakeAIRewriteManager


def test_rewrite_service_generates_three_ai_candidates() -> None:
    rules = RuleRepository()
    config = AppConfig()
    service = RewriteService(
        config=config,
        detector=LocalIntentDetector(rules),
        planner=RewritePlanner(),
        validator=CandidateValidator(),
        scorer=CandidateScorer(),
        ai_manager=FakeAIRewriteManager(),
    )

    result = service.rewrite(
        RewriteRequest(
            text="你这个怎么还没弄完",
            mode=ModeType.AI,
            language="zh",
            variants=3,
        )
    )

    assert result.detected_intent.primary.value == "follow_up"
    assert [candidate.label for candidate in result.candidates] == ["polite", "direct", "firm"]
    assert result.engine == "fake-ai"
