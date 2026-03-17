import sys

from sayit.cli import app, normalize_argv


def run() -> None:
    sys.argv = [sys.argv[0], *normalize_argv(sys.argv[1:])]
    app()
