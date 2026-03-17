from sayit.cli import normalize_argv


def test_normalize_argv_inserts_rewrite_command() -> None:
    assert normalize_argv(["你好"]) == ["rewrite", "你好"]


def test_normalize_argv_keeps_known_commands() -> None:
    assert normalize_argv(["explain", "你好"]) == ["explain", "你好"]
