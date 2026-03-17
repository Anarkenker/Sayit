from sayit.domain.models import IntentType, RiskFlag
from sayit.engines.local.detector import LocalIntentDetector
from sayit.engines.local.rules import RuleRepository


def test_detector_recognizes_follow_up_and_risks() -> None:
    detector = LocalIntentDetector(RuleRepository())

    detected = detector.detect("你这个怎么还没弄完")

    assert detected.primary == IntentType.FOLLOW_UP
    assert RiskFlag.ACCUSATORY in detected.risk_flags
    assert RiskFlag.TOO_BLUNT in detected.risk_flags
