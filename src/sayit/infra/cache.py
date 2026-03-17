from pathlib import Path


def default_cache_dir() -> Path:
    return Path.home() / ".cache" / "sayit"
