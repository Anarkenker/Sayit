from pathlib import Path

import typer
from rich.console import Console

from sayit.domain.models import ContextType, ModeType, RewriteRequest, ToneType
from sayit.engines.ai.manager import ProviderUnavailableError
from sayit.engines.local.rules import RuleRepository
from sayit.infra.config import (
    load_config,
    provider_env_status,
    write_default_config,
)
from sayit.input.adapters.argv import ArgvInputAdapter
from sayit.input.adapters.clipboard import ClipboardInputAdapter
from sayit.input.adapters.file import FileInputAdapter
from sayit.input.adapters.stdin import StdinInputAdapter
from sayit.input.errors import InputResolutionError
from sayit.input.normalizer import normalize_text
from sayit.output.formatter import format_explain, format_rewrite
from sayit.runtime import build_services
from sayit.tui import run_tui

app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=False,
    add_completion=False,
    help="Rewrite short messages into more sendable versions.",
)
config_app = typer.Typer(help="Config commands.")
providers_app = typer.Typer(help="Provider commands.")
rules_app = typer.Typer(help="Rule commands.")

app.add_typer(config_app, name="config")
app.add_typer(providers_app, name="providers")
app.add_typer(rules_app, name="rules")

console = Console()
error_console = Console(stderr=True)
KNOWN_COMMANDS = {"rewrite", "explain", "config", "providers", "rules", "tui"}


def normalize_argv(argv: list[str]) -> list[str]:
    if not argv:
        return ["rewrite"]
    first = argv[0]
    if first in KNOWN_COMMANDS or first in {"-h", "--help"}:
        return argv
    return ["rewrite", *argv]


@app.callback()
def main() -> None:
    """Command group entrypoint."""


@app.command()
def tui() -> None:
    run_tui(console=console)


@app.command("rewrite")
def rewrite_command(
    text_or_path: str | None = typer.Argument(None, help="Raw text or a file path."),
    context: ContextType | None = typer.Option(None, "--context"),
    tone: ToneType | None = typer.Option(None, "--tone"),
    audience: str | None = typer.Option(None, "--audience"),
    variants: int = typer.Option(3, "--variants", min=1, max=6),
    mode: ModeType = typer.Option(ModeType.AUTO, "--mode"),
    language: str | None = typer.Option(None, "--language"),
    clipboard: bool = typer.Option(False, "--clipboard", help="Read from clipboard."),
    plain: bool = typer.Option(False, "--plain", help="Only print candidates."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output."),
) -> None:
    if plain and json_output:
        raise typer.BadParameter("Choose only one of --plain or --json.")

    normalized = _resolve_input(text_or_path=text_or_path, clipboard=clipboard)
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

    try:
        result = rewrite_service.rewrite(request)
    except ProviderUnavailableError as exc:
        error_console.print(str(exc))
        raise typer.Exit(code=2) from exc

    output_format = "json" if json_output else "plain" if plain else load_config().output.format
    console.print(format_rewrite(result, output_format=output_format, show_notes=True))


@app.command()
def explain(
    text_or_path: str | None = typer.Argument(None, help="Raw text or a file path."),
    context: ContextType | None = typer.Option(None, "--context"),
    tone: ToneType | None = typer.Option(None, "--tone"),
    audience: str | None = typer.Option(None, "--audience"),
    mode: ModeType = typer.Option(ModeType.AUTO, "--mode"),
    language: str | None = typer.Option(None, "--language"),
    clipboard: bool = typer.Option(False, "--clipboard"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    normalized = _resolve_input(text_or_path=text_or_path, clipboard=clipboard)
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
    output_format = "json" if json_output else "pretty"
    console.print(format_explain(result, output_format=output_format))


@config_app.command("init")
def config_init(
    force: bool = typer.Option(False, "--force", help="Overwrite existing config."),
) -> None:
    path = write_default_config(force=force)
    console.print(f"Config written to {path}")


@config_app.command("show")
def config_show() -> None:
    config = load_config()
    console.print(config.model_dump_json(indent=2))


@providers_app.command("list")
def providers_list() -> None:
    config = load_config()
    status = provider_env_status(config)
    lines = [f"default: {config.provider.default}", ""]
    for name, provider in config.providers.items():
        lines.append(
            f"- {name}: model={provider.model}, base_url={provider.base_url}, status={status[name]}"
        )
    console.print("\n".join(lines))


@providers_app.command("test")
def providers_test() -> None:
    config = load_config()
    status = provider_env_status(config)
    failed = False
    for name, provider_status in status.items():
        console.print(f"{name}: {provider_status}")
        if provider_status.startswith("missing"):
            failed = True
    raise typer.Exit(code=1 if failed else 0)


@rules_app.command("list")
def rules_list(
    language: str = typer.Option("zh", "--language"),
) -> None:
    rules = RuleRepository()
    lines = [f"language: {language}", ""]
    for rule in rules.load_rules(language):
        lines.append(
            f"- {rule['id']}: intent={rule['intent']}, risk_flags={', '.join(rule.get('risk_flags', []))}"
        )
    console.print("\n".join(lines))


def _resolve_input(text_or_path: str | None, clipboard: bool):
    try:
        if clipboard:
            return ClipboardInputAdapter().load()

        if text_or_path:
            candidate_path = Path(text_or_path)
            if candidate_path.exists() and candidate_path.is_file():
                return FileInputAdapter().load(text_or_path)
            return ArgvInputAdapter().load(text_or_path)

        if not typer.get_text_stream("stdin").isatty():
            return StdinInputAdapter().load()
    except InputResolutionError as exc:
        error_console.print(str(exc))
        raise typer.Exit(code=2) from exc

    error_console.print("No input provided. Pass text, a file path, stdin, or --clipboard.")
    raise typer.Exit(code=2)
