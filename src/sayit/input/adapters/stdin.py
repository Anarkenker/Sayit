import sys

from sayit.app.dto import NormalizedInput
from sayit.input.language import detect_language
from sayit.input.normalizer import extract_surface_facts


class StdinInputAdapter:
    def load(self) -> NormalizedInput:
        text = sys.stdin.read().strip()
        if not text:
            raise ValueError("stdin is empty")
        return NormalizedInput(
            raw_text=text,
            source="stdin",
            inferred_language=detect_language(text),
            facts=extract_surface_facts(text),
        )
