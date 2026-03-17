import json
import os

try:
    import httpx
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    httpx = None

from sayit.domain.models import Candidate, DetectedIntent, RewritePlan, RewriteRequest
from sayit.engines.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from sayit.infra.config import ProviderConfig


class OpenAICompatibleProvider:
    def __init__(self, name: str, config: ProviderConfig | None) -> None:
        self.name = name
        self._config = config

    def available(self) -> bool:
        if self._config is None:
            return False
        if self._config.api_key_env is None:
            return True
        return bool(os.getenv(self._config.api_key_env))

    def rewrite(
        self,
        request: RewriteRequest,
        detected: DetectedIntent,
        plan: RewritePlan,
    ) -> list[Candidate]:
        if httpx is None:
            raise RuntimeError("AI provider support requires the 'httpx' package.")
        if self._config is None:
            raise RuntimeError(f"Provider {self.name} is not configured.")

        headers = {"Content-Type": "application/json"}
        if self._config.api_key_env:
            api_key = os.getenv(self._config.api_key_env)
            if not api_key:
                raise RuntimeError(f"Missing env var: {self._config.api_key_env}")
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": self._config.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(request, detected, plan),
                },
            ],
            "temperature": 0.4,
            "response_format": {"type": "json_object"},
        }

        with httpx.Client(timeout=self._config.timeout_seconds) as client:
            response = client.post(
                f"{self._config.base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return [
            Candidate(label=item["label"], text=item["text"])
            for item in parsed.get("candidates", [])
        ]
