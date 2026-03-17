from sayit.domain.models import Candidate


def format_plain_candidates(candidates: list[Candidate]) -> str:
    return "\n".join(candidate.text for candidate in candidates)
