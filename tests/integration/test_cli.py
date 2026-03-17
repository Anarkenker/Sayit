from sayit.app.services.explain_service import ExplainService
from sayit.app.services.rewrite_service import RewriteService
from typer.testing import CliRunner

from sayit.cli import app, normalize_argv
from sayit.domain.planner import RewritePlanner
from sayit.domain.scoring import CandidateScorer
from sayit.domain.validators import CandidateValidator
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.rules import RuleRepository
from sayit.infra.config import AppConfig
from sayit.test_support import FakeAIRewriteManager

runner = CliRunner()


def _fake_build_services() -> tuple[RewriteService, ExplainService]:
    detector = LocalIntentDetector(RuleRepository())
    planner = RewritePlanner()
    return (
        RewriteService(
            config=AppConfig(),
            detector=detector,
            planner=planner,
            validator=CandidateValidator(),
            scorer=CandidateScorer(),
            ai_manager=FakeAIRewriteManager(),
        ),
        ExplainService(detector=detector, planner=planner),
    )


def test_cli_rewrite_plain_output(monkeypatch) -> None:
    monkeypatch.setattr("sayit.cli.build_services", _fake_build_services)
    result = runner.invoke(app, normalize_argv(["你这个怎么还没弄完", "--plain"]))

    assert result.exit_code == 0
    assert "polite:你这个怎么还没弄完" in result.stdout


def test_cli_explain_output() -> None:
    result = runner.invoke(app, normalize_argv(["explain", "这个价格太高了"]))

    assert result.exit_code == 0
    assert "negotiation" in result.stdout


def test_cli_json_output(monkeypatch) -> None:
    monkeypatch.setattr("sayit.cli.build_services", _fake_build_services)
    result = runner.invoke(app, normalize_argv(["你这个怎么还没弄完", "--json"]))

    assert result.exit_code == 0
    assert '"detected_intent"' in result.stdout
    assert '"follow_up"' in result.stdout
    assert '"fake-ai"' in result.stdout
