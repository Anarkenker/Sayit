from typing import Protocol

from sayit.domain.models import Candidate, DetectedIntent, RewritePlan, RewriteRequest


class BaseProvider(Protocol):
    name: str

    def available(self) -> bool:
        ...

    def rewrite(
        self,
        request: RewriteRequest,
        detected: DetectedIntent,
        plan: RewritePlan,
    ) -> list[Candidate]:
        ...
