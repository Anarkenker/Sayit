from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from sayit.domain.models import ContextType, ModeType, RewriteRequest, ToneType
from sayit.engines.ai.manager import ProviderUnavailableError
from sayit.engines.local.rules import RuleRepository
from sayit.infra.config import load_config, provider_env_status, write_default_config
from sayit.input.adapters.argv import ArgvInputAdapter
from sayit.input.adapters.clipboard import ClipboardInputAdapter
from sayit.input.adapters.file import FileInputAdapter
from sayit.input.errors import InputResolutionError
from sayit.input.normalizer import normalize_text
from sayit.output.formatter import format_explain, format_rewrite
from sayit.runtime import build_services


MENU_ITEMS = [
    ("1", "Rewrite", "Rewrite a message into safer versions"),
    ("2", "Explain", "Inspect intent, risk, and rewrite strategy"),
    ("3", "Providers", "Inspect provider configuration"),
    ("4", "Rules", "Browse built-in local rules"),
    ("5", "Config", "Show or initialize local config"),
    ("0", "Quit", "Exit the TUI"),
]


def run_tui(console: Console | None = None) -> None:
    ui = console or Console()
    while True:
        ui.clear()
        _render_home(ui)
        choice = Prompt.ask(
            "Select an action",
            choices=[item[0] for item in MENU_ITEMS],
            default="1",
            console=ui,
        )
        if choice == "1":
            _run_rewrite_flow(ui)
        elif choice == "2":
            _run_explain_flow(ui)
        elif choice == "3":
            _run_providers_flow(ui)
        elif choice == "4":
            _run_rules_flow(ui)
        elif choice == "5":
            _run_config_flow(ui)
        else:
            ui.print("[bold cyan]Bye.[/bold cyan]")
            return


def _render_home(console: Console) -> None:
    table = Table(box=None, show_header=False, pad_edge=False)
    table.add_column(style="bold cyan", width=4)
    table.add_column(style="bold white", width=12)
    table.add_column(style="white")
    for key, label, description in MENU_ITEMS:
        table.add_row(key, label, description)

    console.print(
        Panel.fit(
            "[bold cyan]sayit[/bold cyan]\nRewrite short messages without leaving the terminal.",
            border_style="cyan",
        )
    )
    console.print(table)


def _run_rewrite_flow(console: Console) -> None:
    console.clear()
    console.print(Rule("[bold cyan]Rewrite[/bold cyan]"))

    text_or_path, clipboard = _prompt_input_source(console)
    context = _optional_enum(console, "Context", ContextType)
    tone = _optional_enum(console, "Tone", ToneType)
    audience = _optional_text(console, "Audience")
    variants = IntPrompt.ask("Variants", default=3, console=console)
    mode = ModeType(
        Prompt.ask(
            "Mode",
            choices=[mode.value for mode in ModeType],
            default=ModeType.AUTO.value,
            console=console,
        )
    )
    language = _optional_text(console, "Language")
    output_format = Prompt.ask(
        "Output format",
        choices=["pretty", "plain", "json"],
        default=_rewrite_default_output_format(),
        console=console,
    )

    try:
        normalized = _resolve_tui_input(text_or_path=text_or_path, clipboard=clipboard)
        request = RewriteRequest(
            text=normalize_text(normalized.raw_text),
            context=context,
            tone=tone,
            audience=audience,
            variants=variants,
            mode=mode,
            language=language or normalized.inferred_language,
            source=normalized.source,
        )
        rewrite_service, _ = build_services()
        result = rewrite_service.rewrite(request)
    except (InputResolutionError, ProviderUnavailableError) as exc:
        _show_message(console, "Error", str(exc), style="red")
        _pause(console)
        return

    _show_message(
        console,
        "Rewrite Result",
        format_rewrite(result, output_format=output_format, show_notes=True),
    )
    _pause(console)


def _run_explain_flow(console: Console) -> None:
    console.clear()
    console.print(Rule("[bold cyan]Explain[/bold cyan]"))

    text_or_path, clipboard = _prompt_input_source(console)
    context = _optional_enum(console, "Context", ContextType)
    tone = _optional_enum(console, "Tone", ToneType)
    audience = _optional_text(console, "Audience")
    mode = ModeType(
        Prompt.ask(
            "Mode",
            choices=[mode.value for mode in ModeType],
            default=ModeType.AUTO.value,
            console=console,
        )
    )
    language = _optional_text(console, "Language")
    output_format = Prompt.ask(
        "Output format",
        choices=["pretty", "json"],
        default="pretty",
        console=console,
    )

    try:
        normalized = _resolve_tui_input(text_or_path=text_or_path, clipboard=clipboard)
        request = RewriteRequest(
            text=normalize_text(normalized.raw_text),
            context=context,
            tone=tone,
            audience=audience,
            mode=mode,
            language=language or normalized.inferred_language,
            source=normalized.source,
        )
        _, explain_service = build_services()
        result = explain_service.explain(request)
    except InputResolutionError as exc:
        _show_message(console, "Error", str(exc), style="red")
        _pause(console)
        return

    _show_message(console, "Explain Result", format_explain(result, output_format=output_format))
    _pause(console)


def _run_providers_flow(console: Console) -> None:
    console.clear()
    console.print(Rule("[bold cyan]Providers[/bold cyan]"))

    action = Prompt.ask("Action", choices=["list", "test"], default="list", console=console)
    config = load_config()
    status = provider_env_status(config)

    if action == "list":
        lines = [f"default: {config.provider.default}", ""]
        for name, provider in config.providers.items():
            lines.append(
                f"- {name}: model={provider.model}, base_url={provider.base_url}, status={status[name]}"
            )
        body = "\n".join(lines)
    else:
        body = "\n".join(f"{name}: {provider_status}" for name, provider_status in status.items())

    _show_message(console, "Providers", body)
    _pause(console)


def _run_rules_flow(console: Console) -> None:
    console.clear()
    console.print(Rule("[bold cyan]Rules[/bold cyan]"))

    repo = RuleRepository()
    languages = repo.list_languages()
    default_language = "zh" if "zh" in languages else (languages[0] if languages else "zh")
    language = Prompt.ask(
        "Language",
        choices=languages or [default_language],
        default=default_language,
        console=console,
    )

    lines = [f"language: {language}", ""]
    for rule in repo.load_rules(language):
        lines.append(
            f"- {rule['id']}: intent={rule['intent']}, risk_flags={', '.join(rule.get('risk_flags', []))}"
        )
    if len(lines) == 2:
        lines.append("- no rules found")

    _show_message(console, "Rules", "\n".join(lines))
    _pause(console)


def _run_config_flow(console: Console) -> None:
    console.clear()
    console.print(Rule("[bold cyan]Config[/bold cyan]"))

    action = Prompt.ask("Action", choices=["show", "init"], default="show", console=console)
    if action == "show":
        config = load_config()
        _show_message(console, "Config", config.model_dump_json(indent=2))
        _pause(console)
        return

    force = Confirm.ask("Overwrite existing config if present", default=False, console=console)
    try:
        path = write_default_config(force=force)
    except FileExistsError as exc:
        _show_message(console, "Error", str(exc), style="red")
        _pause(console)
        return

    _show_message(console, "Config", f"Config written to {path}")
    _pause(console)


def _prompt_input_source(console: Console) -> tuple[str | None, bool]:
    clipboard = Confirm.ask("Use clipboard as input", default=False, console=console)
    if clipboard:
        return None, True
    return _required_text(console, "Text or file path"), False


def _resolve_tui_input(text_or_path: str | None, clipboard: bool):
    if clipboard:
        return ClipboardInputAdapter().load()

    if text_or_path:
        candidate_path = Path(text_or_path)
        if candidate_path.exists() and candidate_path.is_file():
            return FileInputAdapter().load(text_or_path)
        return ArgvInputAdapter().load(text_or_path)

    raise InputResolutionError("No input provided. Pass text, a file path, or use the clipboard.")


def _required_text(console: Console, label: str) -> str:
    while True:
        value = console.input(f"{label}: ").strip()
        if value:
            return value
        _show_message(console, "Error", f"{label} cannot be empty.", style="red")


def _optional_text(console: Console, label: str) -> str | None:
    value = console.input(f"{label} (optional): ").strip()
    return value or None


def _optional_enum(console: Console, label: str, enum_cls):
    values = [item.value for item in enum_cls]
    raw = console.input(f"{label} ({'/'.join(values)}; optional): ").strip()
    if not raw:
        return None
    if raw not in values:
        _show_message(console, "Error", f"Unsupported {label.lower()}: {raw}", style="red")
        return _optional_enum(console, label, enum_cls)
    return enum_cls(raw)


def _rewrite_default_output_format() -> str:
    output_format = load_config().output.format
    return output_format if output_format in {"pretty", "plain", "json"} else "pretty"


def _show_message(console: Console, title: str, body: str, style: str = "cyan") -> None:
    console.print(Panel(Text(body), title=title, border_style=style))


def _pause(console: Console) -> None:
    console.input("\nPress Enter to continue...")
