from types import SimpleNamespace
import subprocess

import pytest

from sayit.input.adapters.clipboard import ClipboardInputAdapter
from sayit.input.errors import ClipboardUnavailableError, EmptyInputError


def test_clipboard_adapter_reads_with_native_command_when_pyperclip_fails(monkeypatch) -> None:
    class FakePyperclipException(RuntimeError):
        pass

    def failing_paste() -> str:
        raise FakePyperclipException("no clipboard backend")

    monkeypatch.setattr(
        "sayit.input.adapters.clipboard.pyperclip",
        SimpleNamespace(
            paste=failing_paste,
            PyperclipException=FakePyperclipException,
        ),
    )
    monkeypatch.setattr(
        "sayit.input.adapters.clipboard._clipboard_commands",
        lambda: [("pbpaste",)],
    )
    monkeypatch.setattr("sayit.input.adapters.clipboard.shutil.which", lambda _: "/usr/bin/pbpaste")
    monkeypatch.setattr(
        "sayit.input.adapters.clipboard.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, stdout="copied text\n", stderr=""),
    )

    normalized = ClipboardInputAdapter().load()

    assert normalized.raw_text == "copied text"
    assert normalized.source == "clipboard"
    assert normalized.inferred_language == "en"


def test_clipboard_adapter_prefers_forwarded_env_value(monkeypatch) -> None:
    monkeypatch.setenv("SAYIT_CLIPBOARD_TEXT", "来自宿主机的剪贴板")
    monkeypatch.setattr("sayit.input.adapters.clipboard.pyperclip", None)

    normalized = ClipboardInputAdapter().load()

    assert normalized.raw_text == "来自宿主机的剪贴板"
    assert normalized.source == "clipboard"
    assert normalized.inferred_language == "zh"


def test_clipboard_adapter_rejects_empty_clipboard(monkeypatch) -> None:
    monkeypatch.setattr(
        "sayit.input.adapters.clipboard.pyperclip",
        SimpleNamespace(paste=lambda: "   ", PyperclipException=RuntimeError),
    )

    with pytest.raises(EmptyInputError, match="clipboard is empty"):
        ClipboardInputAdapter().load()


def test_clipboard_adapter_reports_unavailable_clipboard(monkeypatch) -> None:
    monkeypatch.setattr("sayit.input.adapters.clipboard.pyperclip", None)
    monkeypatch.setattr(
        "sayit.input.adapters.clipboard._clipboard_commands",
        lambda: [("pbpaste",)],
    )
    monkeypatch.setattr("sayit.input.adapters.clipboard.shutil.which", lambda _: None)

    with pytest.raises(ClipboardUnavailableError, match="Clipboard is unavailable"):
        ClipboardInputAdapter().load()
