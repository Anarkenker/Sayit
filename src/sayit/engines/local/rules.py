from functools import lru_cache
from importlib import resources

import yaml


class RuleRepository:
    def load_rules(self, language: str) -> list[dict]:
        resource = resources.files("sayit").joinpath("rules", f"{language}.yaml")
        if not resource.is_file():
            return []
        with resource.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []

    @lru_cache(maxsize=8)
    def list_languages(self) -> list[str]:
        rules_dir = resources.files("sayit").joinpath("rules")
        return sorted(
            path.name.removesuffix(".yaml")
            for path in rules_dir.iterdir()
            if path.name.endswith(".yaml")
        )
