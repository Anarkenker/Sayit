from sayit.app.services.explain_service import ExplainService
from sayit.app.services.rewrite_service import RewriteService
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.ai.manager import AIRewriteManager
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.rules import RuleRepository
from sayit.infra.config import load_config


def build_services() -> tuple[RewriteService, ExplainService]:
    config = load_config()
    rules = RuleRepository()
    detector = LocalIntentDetector(rules)
    planner = RewritePlanner()
    rewrite_service = RewriteService(
        config=config,
        detector=detector,
        planner=planner,
        validator=CandidateValidator(),
        scorer=CandidateScorer(),
        ai_manager=AIRewriteManager(config),
    )
    explain_service = ExplainService(detector=detector, planner=planner)
    return rewrite_service, explain_service
