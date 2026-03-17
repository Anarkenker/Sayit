from sayit.domain.models import RiskFlag
from sayit.domain.validators import CandidateValidator


def test_validator_flags_new_numbers_as_fact_drift() -> None:
    validator = CandidateValidator()

    issues = validator.validate(
        original_text="明天给我回复",
        candidate_text="明天下午 3 点前给我回复",
        preserve_facts=True,
        risk_flags=[],
    )

    assert RiskFlag.FACT_DRIFT.value in issues


def test_validator_flags_fabricated_reason() -> None:
    validator = CandidateValidator()

    issues = validator.validate(
        original_text="我今天不想去了",
        candidate_text="我今天身体不舒服，先不去了。",
        preserve_facts=True,
        risk_flags=[],
    )

    assert RiskFlag.FABRICATED_REASON.value in issues
