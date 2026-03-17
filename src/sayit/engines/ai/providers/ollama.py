from sayit.engines.ai.providers.openai_compat import OpenAICompatibleProvider
from sayit.infra.config import ProviderConfig


class OllamaProvider(OpenAICompatibleProvider):
    def __init__(self, config: ProviderConfig | None) -> None:
        super().__init__("ollama", config)
