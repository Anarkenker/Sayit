from sayit.domain.models import Candidate, DetectedIntent, RewritePlan, RewriteRequest
from sayit.engines.ai.providers.ollama import OllamaProvider
from sayit.engines.ai.providers.openai_compat import OpenAICompatibleProvider
from sayit.infra.config import AppConfig


class ProviderUnavailableError(RuntimeError):
    """Raised when an AI provider cannot be used."""


class AIRewriteManager:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._providers = self._build_providers()

    def has_available_provider(self) -> bool:
        provider = self._resolve_default_provider()
        return provider is not None and provider.available()

    def configured_providers(self) -> dict[str, bool]:
        return {
            name: provider.available()
            for name, provider in self._providers.items()
        }

    def rewrite(
        self,
        request: RewriteRequest,
        detected: DetectedIntent,
        plan: RewritePlan,
    ) -> list[Candidate]:
        provider = self._resolve_default_provider()
        if provider is None or not provider.available():
            raise ProviderUnavailableError("No available AI provider configured.")
        try:
            return provider.rewrite(request, detected, plan)
        except Exception as exc:  # pragma: no cover - depends on provider runtime
            raise ProviderUnavailableError(str(exc)) from exc

    def _resolve_default_provider(self):
        default_name = self._config.provider.default
        return self._providers.get(default_name)

    def _build_providers(self) -> dict[str, object]:
        return {
            "openai": OpenAICompatibleProvider("openai", self._config.providers.get("openai")),
            "openrouter": OpenAICompatibleProvider("openrouter", self._config.providers.get("openrouter")),
            "ollama": OllamaProvider(self._config.providers.get("ollama")),
        }
