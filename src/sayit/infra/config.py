import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False

from sayit.domain.models import ContextType, ModeType, ToneType


class DefaultsConfig(BaseModel):
    language: str = "zh"
    mode: ModeType = ModeType.AUTO
    context: ContextType = ContextType.WORK
    tone: ToneType = ToneType.POLITE
    variants: int = 3
    preserve_facts: bool = True


class OutputConfig(BaseModel):
    format: str = "pretty"
    show_notes: bool = True


class ProviderConfig(BaseModel):
    base_url: str
    model: str
    api_key_env: str | None = None
    timeout_seconds: float = 20.0


class ProviderSettings(BaseModel):
    default: str = "openai"
    timeout_seconds: float = 20.0


class AppConfig(BaseModel):
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    provider: ProviderSettings = Field(default_factory=ProviderSettings)
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)


DEFAULT_CONFIG_TOML = """[defaults]
language = "zh"
mode = "auto"
context = "work"
tone = "polite"
variants = 3
preserve_facts = true

[output]
format = "pretty"
show_notes = true

[provider]
default = "openai"
timeout_seconds = 20

[providers.openai]
base_url = "https://api.openai.com/v1"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"

[providers.openrouter]
base_url = "https://openrouter.ai/api/v1"
model = "openai/gpt-4.1-mini"
api_key_env = "OPENROUTER_API_KEY"

[providers.ollama]
base_url = "http://localhost:11434/v1"
model = "qwen2.5:7b"
"""


def config_path() -> Path:
    return Path.home() / ".config" / "sayit" / "config.toml"


def load_config() -> AppConfig:
    load_dotenv()
    path = config_path()
    if not path.exists():
        config = AppConfig(
            providers={
                "openai": ProviderConfig(
                    base_url="https://api.openai.com/v1",
                    model="gpt-4.1-mini",
                    api_key_env="OPENAI_API_KEY",
                ),
                "openrouter": ProviderConfig(
                    base_url="https://openrouter.ai/api/v1",
                    model="openai/gpt-4.1-mini",
                    api_key_env="OPENROUTER_API_KEY",
                ),
                "ollama": ProviderConfig(
                    base_url="http://localhost:11434/v1",
                    model="qwen2.5:7b",
                    api_key_env=None,
                ),
            }
        )
    else:
        with path.open("rb") as file:
            data = tomllib.load(file)
        config = AppConfig.model_validate(data)

    if config.provider.timeout_seconds:
        for provider in config.providers.values():
            provider.timeout_seconds = config.provider.timeout_seconds

    custom_base_url = os.getenv("SAYIT_CUSTOM_BASE_URL")
    custom_model = os.getenv("SAYIT_CUSTOM_MODEL")
    if custom_base_url and custom_model:
        config.providers["custom"] = ProviderConfig(
            base_url=custom_base_url,
            model=custom_model,
            api_key_env="SAYIT_CUSTOM_API_KEY",
            timeout_seconds=config.provider.timeout_seconds,
        )

    if provider_default := os.getenv("SAYIT_PROVIDER_DEFAULT"):
        config.provider.default = provider_default
    return config


def write_default_config(force: bool = False) -> Path:
    path = config_path()
    if path.exists() and not force:
        raise FileExistsError(f"Config already exists at {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DEFAULT_CONFIG_TOML, encoding="utf-8")
    return path


def provider_env_status(config: AppConfig) -> dict[str, str]:
    status: dict[str, str] = {}
    for name, provider in config.providers.items():
        if provider.api_key_env is None:
            status[name] = "ready"
        elif os.getenv(provider.api_key_env):
            status[name] = f"ready ({provider.api_key_env})"
        else:
            status[name] = f"missing {provider.api_key_env}"
    return status
