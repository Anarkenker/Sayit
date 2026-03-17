from typer.testing import CliRunner

from sayit.cli import app, normalize_argv

runner = CliRunner()


def test_cli_rewrite_plain_output() -> None:
    result = runner.invoke(app, normalize_argv(["你这个怎么还没弄完", "--plain"]))

    assert result.exit_code == 0
    assert "想跟你确认一下这件事目前的进度" in result.stdout


def test_cli_explain_output() -> None:
    result = runner.invoke(app, normalize_argv(["explain", "这个价格太高了"]))

    assert result.exit_code == 0
    assert "negotiation" in result.stdout


def test_cli_json_output() -> None:
    result = runner.invoke(app, normalize_argv(["你这个怎么还没弄完", "--json"]))

    assert result.exit_code == 0
    assert '"detected_intent"' in result.stdout
    assert '"follow_up"' in result.stdout
