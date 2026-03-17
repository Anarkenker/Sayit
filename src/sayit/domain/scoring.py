from sayit.domain.models import Candidate, DetectedIntent, RewritePlan, ToneType


class CandidateScorer:
    def rank(
        self,
        detected: DetectedIntent,
        plan: RewritePlan,
        candidates: list[Candidate],
        requested_tone: ToneType | None,
    ) -> list[Candidate]:
        ranked: list[Candidate] = []
        for index, candidate in enumerate(candidates):
            score = 1.0
            if requested_tone and candidate.label == requested_tone.value:
                score += 0.35
            elif candidate.label in [tone.value for tone in plan.variant_tones]:
                score += 0.15

            length = len(candidate.text)
            if 12 <= length <= 42:
                score += 0.15
            elif length > 68:
                score -= 0.1

            score -= 0.18 * len(candidate.notes)
            score -= index * 0.02

            ranked.append(candidate.model_copy(update={"score": round(score, 3)}))

        return sorted(ranked, key=lambda candidate: candidate.score or 0.0, reverse=True)
