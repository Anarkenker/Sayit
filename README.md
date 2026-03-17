# sayit

[中文](README.zh-CN.md) | English

`sayit` is a Python CLI for rewriting short, awkward, blunt, or not-sendable messages into cleaner versions you can copy and send.

It is not a chatbot and it is not a long-form writing assistant.

## Overview

The product boundary is intentional:

- short input
- short output
- explicit social intent
- controlled rewrite instead of free generation

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

`sayit explain` also tells you:

- detected intent
- risk flags
- rewrite strategy

## Current MVP

- Chinese-first local rewrite engine
- intent detection and risk detection
- rule-driven planner
- YAML-based template system
- `argv`, `stdin`, file, and clipboard input
- `pretty`, `plain`, and `json` output
- `explain` command
- OpenAI-compatible provider scaffolding
- `local`, `ai`, and `hybrid` modes

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

You can also install the local repo with `pipx`:

```bash
pipx install .
```

After install, you can run:

```bash
sayit "你这个怎么还没弄完"
```

If you have not installed the package yet, you can still run:

```bash
PYTHONPATH=src python -m sayit "你这个怎么还没弄完"
```

## Where the API Key Should Go

Do not hardcode real API keys in source files or config files.

Recommended setup:

1. Put the real key in an environment variable.
2. Keep only the environment variable name in config.
3. Commit `.env.example`, never commit `.env`.

### Local Development

Create a `.env` file:

```bash
cp .env.example .env
```

Then fill in the key you want to use:

```bash
OPENAI_API_KEY=your_real_key_here
OPENROUTER_API_KEY=
```

The app loads `.env` automatically at runtime.

### Production or CI

Use shell or platform environment variables instead:

```bash
export OPENAI_API_KEY="your_real_key_here"
```

### Config File Location

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

### Local Mode, No API Required

```bash
sayit "你这个怎么还没弄完"
sayit "我今天不想去了" --tone soft
sayit explain "这个价格太高了"
```

### AI or Hybrid Mode

```bash
sayit "这个价格太高了" --mode ai
sayit "你这个怎么还没弄完" --mode hybrid
```

Default behavior:

- if no provider is available, use `local`
- if a provider is available, default to `hybrid`

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
sayit templates list
```

## Output Formats

### `pretty`

Human-readable output with:

- original text
- intent
- risk flags
- candidate rewrites

### `plain`

Only outputs candidate texts, useful for copy/paste or shell piping.

```bash
sayit "你这个怎么还没弄完" --plain
```

### `json`

Useful for scripts or integrations.

```bash
sayit "这个价格太高了" --json
```

## Modes

### `local`

- no API required
- fast, deterministic, predictable
- driven by local rules and templates

### `ai`

- all candidate generation goes through the provider
- better for more nuanced rewrites
- requires provider config and runtime key

### `hybrid`

- local engine handles detector and planner first
- provider handles controlled generation
- can fall back to local behavior on provider failures

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
  templates/
tests/
```

## Development

Run tests:

```bash
pytest
```

List templates:

```bash
sayit templates list
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

- Chinese templates are much stronger than English support right now.
- AI mode is implemented, but still needs broader real-world validation.
- The local engine is intentionally conservative and only covers a limited set of high-frequency cases.
- There is no GUI, chat history import, or auto-send integration.

## Roadmap

- Expand the rules and templates for the six core intents
- Add English templates and tests
- Add stable snapshot tests
- Strengthen fact-preservation and fabricated-reason checks
- Improve provider-specific error handling and integration coverage
- Publish to PyPI for `pipx install sayit`

## Open Source Notes

This repository now has the minimum structure for a first public release:

- clear README
- `.gitignore`
- `.env.example`
- basic CI
- local MVP

Before the first public release, replace the repository placeholders in:

- `pyproject.toml`
- `.github/ISSUE_TEMPLATE/config.yml`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).

## Design Principles

- controlled generation over free-form generation
- do not invent facts by default
- solve high-frequency short scenarios first
- explanations matter as much as output quality
