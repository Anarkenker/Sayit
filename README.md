# sayit

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-wordmark-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-wordmark.svg">
    <img src="assets/logo-wordmark.svg" width="700" alt="sayit logo">
  </picture>
</p>

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml/badge.svg)](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml)
[![Docker First](https://img.shields.io/badge/Run%20with-Docker-2496ED?logo=docker&logoColor=white)](README.md#quick-start)
[![Status](https://img.shields.io/badge/Status-Alpha-orange)](README.md#project-status)

[中文](README.zh-CN.md) | English

`sayit` rewrites short awkward, blunt, or overly harsh messages into safer, more natural versions that are easier to send. It is built for short-message rewriting, not long-form writing, and it aims to avoid inventing facts.

## Good For

- follow-ups, reminders, refusals, reschedules, and apologies
- bargaining, complaints, and sensitive requests
- softening messages that sound too direct or too much like commands
- examples: `你这个怎么还没弄完` `你先把钱转我` `这个价格太高了`

## Not For

- long emails, articles, or full conversations
- making up facts or excuses
- harassment, threats, manipulation, deception, or responsibility avoidance

## Features

- several rewrite candidates with different tones
- local intent and risk analysis before generation
- optional terminal UI via `sayit tui`
- `argv`, `stdin`, file, and clipboard input
- `pretty`, `plain`, and `json` output
- Docker-first setup

## Quick Start

```bash
git clone https://github.com/Anarkenker/sayit.git
cd sayit
./setup
# edit .env and set OPENAI_API_KEY=...
sayit "你这个怎么还没弄完"
```

If `sayit` is not found right after `./setup`, open a new terminal once. If your shell still needs a manual `PATH` update, `setup` prints the exact line.

Run:

```bash
sayit "这个价格太高了"
sayit "这个价格太高了" --context bargain
sayit explain "我今天不想去了"
sayit tui
sayit "这个价格太高了" --json
echo "这个价格太高了" | sayit --plain
sayit draft.txt
```

## Command Reference

```bash
# setup
./setup

# help
sayit --help
sayit rewrite --help
sayit explain --help
sayit tui --help
sayit config --help
sayit providers --help
sayit rules --help

# terminal UI
sayit tui

# rewrite (default subcommand)
sayit [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--variants 1-6] [--mode auto|ai] [--language TEXT] [--clipboard] [--plain|--json]
sayit rewrite [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--variants 1-6] [--mode auto|ai] [--language TEXT] [--clipboard] [--plain|--json]

# analysis
sayit explain [TEXT_OR_PATH] [--context work|social|email|bargain|support] [--tone polite|direct|firm|soft] [--audience TEXT] [--mode auto|ai] [--language TEXT] [--clipboard] [--json]

# config
sayit config init [--force]
sayit config show

# provider checks
sayit providers list
sayit providers test

# rule inspection
sayit rules list [--language TEXT]
```

## Option Reference

- `sayit "..."` behaves the same as `sayit rewrite "..."`.
- `sayit tui`: open the interactive terminal menu.
- `TEXT_OR_PATH`: raw text or a file path. Omit it to read from stdin, or use `--clipboard` to read from the clipboard.
- `--context`: `work` `social` `email` `bargain` `support`
- `--tone`: `polite` `direct` `firm` `soft`
- `--audience TEXT`: target audience.
- `--variants`: `1-6`, default `3`, `rewrite` only.
- `--mode`: `auto` `ai`, default `auto`.
- `--language TEXT`: manually set the language.
- `--plain`: print candidate texts only, `rewrite` only.
- `--json`: print JSON output.
- `--plain` and `--json` cannot be used together.
- `config init --force`: overwrite an existing config file.
- `rules list --language TEXT`: select rule language, default `zh`.
- `providers list`: list providers, models, base URLs, and env status.
- `providers test`: check whether the current provider setup is usable.

## Configuration

Default setup needs:

- Docker / Docker Desktop
- a working model-service API key
- a `.env` file in the project root

Official OpenAI:

```env
OPENAI_API_KEY=your_api_key_here
```

OpenAI-compatible provider:

```env
SAYIT_PROVIDER_DEFAULT=custom
SAYIT_CUSTOM_BASE_URL=https://your-provider.example.com/v1
SAYIT_CUSTOM_MODEL=your-model-name
SAYIT_CUSTOM_API_KEY=your_api_key_here
```

User config:

```bash
sayit config init
sayit config show
```

The user config file is `~/.config/sayit/config.toml`. Use it only when defaults such as language, variants, mode, or output format need to be persisted. Do not commit `.env`.

## How It Works

- `sayit` uses a model service to generate rewrite candidates.
- Before generation, it runs a local detection and planning pass to identify likely intent, risks, and a safer rewrite direction.

## Troubleshooting

- `Cannot connect to the Docker daemon`: start Docker Desktop and try again.
- `No available AI provider configured`: check `.env` and the configured API key.
- Network errors: check connectivity, proxy settings, or provider availability.

## Development

```bash
pytest
PYTHONPATH=src python -m sayit providers list
PYTHONPATH=src python -m sayit providers test
PYTHONPATH=src python -m sayit rules list
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution details.

## Project Status

`sayit` is currently in **alpha**. Interfaces, rules, output details, and configuration shape may still change.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

See [LICENSE](LICENSE).
