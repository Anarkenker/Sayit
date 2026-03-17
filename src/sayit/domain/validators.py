import re

from sayit.domain.models import RiskFlag

COMMON_EXCUSES = [
    "身体不舒服",
    "临时有事",
    "家里有事",
    "网络有问题",
    "突然有个会",
]


class CandidateValidator:
    def validate(
        self,
        original_text: str,
        candidate_text: str,
        preserve_facts: bool,
        risk_flags: list[RiskFlag],
    ) -> list[str]:
        issues: list[str] = []
        if len(candidate_text) > 88:
            issues.append("too_long")

        if preserve_facts and self._introduces_new_numbers(original_text, candidate_text):
            issues.append(RiskFlag.FACT_DRIFT.value)

        if preserve_facts and self._fabricates_reason(original_text, candidate_text):
            issues.append(RiskFlag.FABRICATED_REASON.value)

        if RiskFlag.ACCUSATORY in risk_flags and re.search(r"(怎么还|怎么又|你这边到底)", candidate_text):
            issues.append("still_accusatory")

        if RiskFlag.COMMANDING in risk_flags and re.search(r"^(马上|立刻|必须|赶紧)", candidate_text):
            issues.append("still_commanding")

        return issues

    def _introduces_new_numbers(self, original_text: str, candidate_text: str) -> bool:
        original_numbers = set(re.findall(r"\d+(?:\.\d+)?", original_text))
        candidate_numbers = set(re.findall(r"\d+(?:\.\d+)?", candidate_text))
        return bool(candidate_numbers - original_numbers)

    def _fabricates_reason(self, original_text: str, candidate_text: str) -> bool:
        if any(token in original_text for token in COMMON_EXCUSES):
            return False
        return any(token in candidate_text for token in COMMON_EXCUSES)
