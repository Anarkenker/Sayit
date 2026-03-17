# sayit

[中文](README.zh-CN.md) | English

`sayit` is an API-first CLI for rewriting short, blunt, or awkward messages into cleaner versions you can send.

It is not a chatbot and it is not a long-form writing assistant.

## Overview

`sayit` focuses on:

- short input
- short output
- explicit social intent
- controlled rewriting
- API-based generation

Typical inputs:

- `你这个怎么还没弄完`
- `这个价格太高了`
- `我今天不想去了`
- `你先把钱转我`
- `我这边要延期`

Typical outputs:

- `polite`
- `direct`
- `firm`
- `soft`

`sayit explain` still gives you:

- detected intent
- risk flags
- rewrite strategy

The rewrite path itself is API-only.

## Current MVP

- API-only rewrite generation
- local intent and risk detection for controlled prompting
- rule-driven planner
- `argv`, `stdin`, file, and clipboard input
- `pretty`, `plain`, and `json` output
- `explain` command
- OpenAI-compatible provider support
- Docker-first usage

## Recommended Usage: Docker

Build the image:

```bash
docker build -t sayit .
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Fill in your provider key:

```bash
OPENAI_API_KEY=your_real_key_here
OPENROUTER_API_KEY=
```

Run with direct input:

```bash
docker run --rm --env-file .env sayit "你这个怎么还没弄完"
```

Run with JSON output:

```bash
docker run --rm --env-file .env sayit "这个价格太高了" --json
```

Run `explain`:

```bash
docker run --rm --env-file .env sayit explain "你先把钱转我"
```

Run with stdin:

```bash
echo "这个价格太高了" | docker run --rm -i --env-file .env sayit --plain
```

Run with a mounted file:

```bash
docker run --rm --env-file .env -v "$PWD:/workspace" -w /workspace sayit draft.txt
```

Use Docker Compose:

```bash
docker compose run --rm sayit "你这个怎么还没弄完"
```

Notes:

- Docker is the recommended runtime path.
- `--clipboard` is less practical inside containers.
- If you use file input, mount the working directory.

## Alternative: Local Python Setup

If you still want to run it directly:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
sayit "你这个怎么还没弄完"
```

Or without installation:

```bash
PYTHONPATH=src python -m sayit "你这个怎么还没弄完"
```

## API Key Setup

Do not hardcode real API keys in source files or config files.

Recommended setup:

1. Put the real key in an environment variable.
2. Keep only the environment variable name in config.
3. Commit `.env.example`, never commit `.env`.

The app loads `.env` automatically at runtime when running outside Docker.  
Inside Docker, prefer `--env-file .env`.

The user config file lives at:

```text
~/.config/sayit/config.toml
```

It should store the environment variable name, not the secret itself:

```toml
[providers.openai]
base_url = "https://api.openai.com/v1"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"
```

## Quick Start

```bash
docker run --rm --env-file .env sayit "你这个怎么还没弄完"
docker run --rm --env-file .env sayit "这个价格太高了" --context bargain
docker run --rm --env-file .env sayit explain "我今天不想去了"
```

## Usage

### Direct Input

```bash
sayit "你这个怎么还没弄完"
```

### Clipboard

```bash
sayit --clipboard
```

### File Input

```bash
sayit draft.txt
```

### stdin

```bash
pbpaste | sayit
cat raw.txt | sayit --plain
```

### Explain Mode

```bash
sayit explain "你先把钱转我"
```

### Common Options

```bash
sayit "这个价格太高了" --context bargain
sayit "今天给我答复" --tone firm
sayit "我今天来不了" --context social --tone soft
sayit "这个事情要延期" --audience client
sayit "这个事情要延期" --mode ai
sayit "这个价格太高了" --json
```

## Commands

```bash
sayit "..."
sayit explain "..."
sayit config init
sayit config show
sayit providers list
sayit providers test
sayit rules list
```

## Output Formats

### `pretty`

Human-readable output with:

- original text
- intent
- risk flags
- candidate rewrites

### `plain`

Only outputs candidate texts.

```bash
sayit "你这个怎么还没弄完" --plain
```

### `json`

Useful for scripts or integrations.

```bash
sayit "这个价格太高了" --json
```

## Modes

### `ai`

- all rewrite candidates are generated through the provider
- requires provider config and runtime key
- recommended for normal usage

### `auto`

- currently resolves to the configured provider path
- kept mainly for CLI/config compatibility

## Project Structure

```text
src/sayit/
  cli.py
  main.py
  app/
  domain/
  engines/
  infra/
  input/
  output/
  rules/
tests/
Dockerfile
compose.yaml
```

## Development

Run tests:

```bash
pytest
```

List rules:

```bash
sayit rules list
```

Show provider status:

```bash
sayit providers list
sayit providers test
```

Initialize user config:

```bash
sayit config init
```

## Known Limitations

- Rewrite generation now requires an available provider.
- Chinese rule coverage is stronger than English support right now.
- `explain` is local analysis, while rewrite is provider-backed.
- Clipboard usage is less suitable inside Docker containers.

## Roadmap

- Expand rules for the six core intents
- Add English rule coverage and tests
- Add stable snapshot tests
- Strengthen fact-preservation and fabricated-reason checks
- Improve provider-specific error handling and integration coverage

## Open Source Notes

This repository now has the minimum structure for a first public release:

- clear README
- `.gitignore`
- `.env.example`
- basic CI
- Docker runtime

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
