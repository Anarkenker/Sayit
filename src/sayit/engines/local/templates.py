from functools import lru_cache
from importlib import resources

import yaml


class TemplateRepository:
    def load_rules(self, language: str) -> list[dict]:
        resource = resources.files("sayit").joinpath("templates", "rules", f"{language}.yaml")
        with resource.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []

    def load_intent_templates(self, language: str, intent: str) -> dict:
        resource = resources.files("sayit").joinpath("templates", language, "intents", f"{intent}.yaml")
        with resource.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @lru_cache(maxsize=8)
    def list_intents(self, language: str) -> list[str]:
        intents_dir = resources.files("sayit").joinpath("templates", language, "intents")
        return sorted(
            path.name.removesuffix(".yaml")
            for path in intents_dir.iterdir()
            if path.name.endswith(".yaml")
        )
