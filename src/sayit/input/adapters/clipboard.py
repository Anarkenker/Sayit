import os
import shutil
import subprocess
import sys

try:
    import pyperclip
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    pyperclip = None

from sayit.app.dto import NormalizedInput
from sayit.input.errors import ClipboardUnavailableError, EmptyInputError
from sayit.input.language import detect_language
from sayit.input.normalizer import extract_surface_facts


def _clipboard_commands() -> list[tuple[str, ...]]:
    if sys.platform == "darwin":
        return [("pbpaste",)]
    if sys.platform.startswith("linux"):
        return [
            ("wl-paste", "--no-newline"),
            ("xclip", "-selection", "clipboard", "-o"),
            ("xsel", "--clipboard", "--output"),
        ]
    if sys.platform.startswith("win"):
        return [
            ("pwsh", "-NoProfile", "-Command", "Get-Clipboard"),
            ("powershell", "-NoProfile", "-Command", "Get-Clipboard"),
            ("powershell.exe", "-NoProfile", "-Command", "Get-Clipboard"),
        ]
    return []


class ClipboardInputAdapter:
    def load(self) -> NormalizedInput:
        text = self._read_clipboard_text().strip()
        if not text:
            raise EmptyInputError("clipboard is empty")
        return NormalizedInput(
            raw_text=text,
            source="clipboard",
            inferred_language=detect_language(text),
            facts=extract_surface_facts(text),
        )

    def _read_clipboard_text(self) -> str:
        forwarded_clipboard_text = os.getenv("SAYIT_CLIPBOARD_TEXT")
        if forwarded_clipboard_text is not None:
            return forwarded_clipboard_text
        pyperclip_text = self._read_with_pyperclip()
        if pyperclip_text is not None:
            return pyperclip_text
        return self._read_with_native_command()

    def _read_with_pyperclip(self) -> str | None:
        if pyperclip is None:
            return None
        pyperclip_exception = getattr(pyperclip, "PyperclipException", RuntimeError)
        try:
            return pyperclip.paste()
        except pyperclip_exception:
            return None

    def _read_with_native_command(self) -> str:
        for command in _clipboard_commands():
            if shutil.which(command[0]) is None:
                continue
            try:
                completed = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except (OSError, subprocess.CalledProcessError):
                continue
            return completed.stdout
        raise ClipboardUnavailableError(
            "Clipboard is unavailable in this environment. "
            "Try piping text into sayit or pass it as an argument."
        )
