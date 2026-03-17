from pathlib import Path

from sayit.app.dto import NormalizedInput
from sayit.input.language import detect_language
from sayit.input.normalizer import extract_surface_facts


class FileInputAdapter:
    def load(self, path: str) -> NormalizedInput:
        file_path = Path(path)
        text = file_path.read_text(encoding="utf-8").strip()
        return NormalizedInput(
            raw_text=text,
            source="file",
            inferred_language=detect_language(text),
            path=str(file_path),
            facts=extract_surface_facts(text),
        )
