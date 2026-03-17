try:
    import pyperclip
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    pyperclip = None

from sayit.app.dto import NormalizedInput
from sayit.input.language import detect_language
from sayit.input.normalizer import extract_surface_facts


class ClipboardInputAdapter:
    def load(self) -> NormalizedInput:
        if pyperclip is None:
            raise RuntimeError("Clipboard support requires the 'pyperclip' package.")
        text = pyperclip.paste().strip()
        if not text:
            raise ValueError("clipboard is empty")
        return NormalizedInput(
            raw_text=text,
            source="clipboard",
            inferred_language=detect_language(text),
            facts=extract_surface_facts(text),
        )
