from sayit.domain.models import Candidate


class FakeAIRewriteManager:
    def has_available_provider(self) -> bool:
        return True

    def rewrite(self, request, detected, plan) -> list[Candidate]:
        labels = [tone.value for tone in plan.variant_tones]
        return [
            Candidate(label=label, text=f"{label}:{request.text}")
            for label in labels
        ]

    def provider_label(self) -> str:
        return "fake-ai"
