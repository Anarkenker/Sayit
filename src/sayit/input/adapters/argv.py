from sayit.app.dto import NormalizedInput
from sayit.input.language import detect_language
from sayit.input.normalizer import extract_surface_facts


class ArgvInputAdapter:
    def load(self, raw_text: str) -> NormalizedInput:
        text = raw_text.strip()
        return NormalizedInput(
            raw_text=text,
            source="argv",
            inferred_language=detect_language(text),
            facts=extract_surface_facts(text),
        )
