# sayit

<p align="center">
  <img src="assets/logo-wordmark.svg" width="700" alt="sayit logo">
</p>

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml/badge.svg)](https://github.com/Anarkenker/Sayit/actions/workflows/ci.yml)
[![Docker First](https://img.shields.io/badge/Run%20with-Docker-2496ED?logo=docker&logoColor=white)](README.md#quick-start)
[![Status](https://img.shields.io/badge/Status-Alpha-orange)](README.md#project-status)

[中文](README.zh-CN.md) | English

`sayit` is a CLI tool focused on **improving message wording**. It takes **short messages that feel awkward, too blunt, too harsh, or not appropriate to send as-is**, and rewrites them into a few **safer, more natural, and more sendable** versions.

It is not a chatbot, and it is not a long-form writing assistant. It is closer to a tool for answering one narrow question: **how should I phrase this message so it sounds better before I send it?** The input should stay short, the output should stay short, the result should be easy to copy, and the tool should avoid inventing facts.

---

## What It Is Good For

`sayit` works well for situations like:

- following up without sounding too aggressive
- refusing, rescheduling, declining, or taking leave
- requesting, reminding, nudging, or apologizing
- negotiating, bargaining, or expressing dissatisfaction
- softening messages that sound too much like commands
- turning something rude or awkward into something more sendable

For example:

- `你这个怎么还没弄完`
- `你先把钱转我`
- `这个价格太高了`
- `我今天不想去了`

---

## What It Is Not For

`sayit` is meant to improve expression, not to help package bad intent. It is not a good fit for:

- generating long emails, articles, or full conversations
- inventing facts or making up excuses for the user
- dressing up threats, harassment, manipulation, deception, or responsibility-avoidance
- replacing the user's own judgment about accuracy or consequences

---

## Features

- built for **short-message rewriting**, not general writing
- generates several candidate versions with different tones
- performs a **local analysis and planning pass** before generation
- tries to reduce risks like sounding too harsh, too vague, or too commanding
- supports `argv`, `stdin`, file, and clipboard input
- supports `pretty`, `plain`, and `json` output
- runs through Docker by default to reduce local environment differences

---

## Quick Start

The first time you use it, run this in the project root:

```bash
git clone https://github.com/Anarkenker/sayit.git
cd sayit
./setup
# setup installs the sayit command and prepares .env
# open .env and replace OPENAI_API_KEY= with your own key
sayit "你这个怎么还没弄完"
```

If `sayit` is still not found right after `./setup`, open a new terminal once. In the uncommon cases where your shell needs a manual `PATH` update, `setup` prints the exact line for you.

More examples:

```bash
sayit "这个价格太高了"
sayit "这个价格太高了" --context bargain
sayit explain "我今天不想去了"
sayit "这个价格太高了" --json
echo "这个价格太高了" | sayit --plain
sayit draft.txt
```

---

## Command Reference

If you just want one place that lists the commands without searching through the whole README, use this section. `sayit "..."` is the most common entry point, and it is equivalent to explicitly writing `sayit rewrite "..."`. Beyond that, the project also exposes analysis commands, config commands, provider checks, and rule inspection. The list below covers the full set of commands most users will actually use:

```bash
# setup
./setup

# most common usage
sayit "你这个怎么还没弄完"
sayit rewrite "你这个怎么还没弄完"
sayit explain "我今天不想去了"

# input sources
sayit draft.txt
sayit --clipboard
echo "这个价格太高了" | sayit
echo "这个价格太高了" | sayit --plain

# common rewrite options
sayit "这个价格太高了" --context bargain
sayit "今天给我答复" --tone firm
sayit "我今天来不了" --context social --tone soft
sayit "这个事情要延期" --audience client
sayit "你这个怎么还没弄完" --variants 3
sayit "你这个怎么还没弄完" --mode auto
sayit "你这个怎么还没弄完" --mode ai
sayit "你这个怎么还没弄完" --language zh

# output formats
sayit "这个价格太高了" --plain
sayit "这个价格太高了" --json
sayit explain "你先把钱转我" --json

# config and inspection
sayit config init
sayit config show
sayit providers list
sayit providers test
sayit rules list
```

The most commonly used options are `--context`, `--tone`, `--audience`, `--variants`, `--mode`, `--language`, `--plain`, and `--json`. In practice, `--context` helps steer the situation, `--tone` helps steer the voice, `--plain` is useful for copy-paste, and `--json` is useful for scripts. `--plain` and `--json` cannot be used at the same time.

---

## Option Reference

If you see a lot of flags in the examples and want to know what each one actually does, this section is the short version. Most of `sayit`'s options fall into three groups: input source, rewrite control, and output format.

### Input-related

- `sayit "..."`: treat the command-line text itself as input. This is the most common path.
- `sayit draft.txt`: treat the file contents as input.
- `echo "..." | sayit`: the command before the pipe prints text first, and the pipe `|` passes that text directly into `sayit`. This is useful when an earlier shell command already produced the text you want to rewrite.
- `--clipboard`: read input from the clipboard. When you use the installed `sayit` shell command, the host launcher reads the clipboard before entering Docker and forwards the text into the container. If you run the Docker image directly yourself, prefer stdin or pass the text explicitly.

### Rewrite-related

- `--context`: tells the tool which situation the message belongs to. Examples include `work`, `social`, `bargain`, `email`, and `support`. This is especially useful when the sentence is short or ambiguous.
- `--tone`: requests a tone such as `polite`, `direct`, `firm`, or `soft`. If you do not set it, the tool will usually return several tones by default.
- `--audience`: tells the tool who the message is for, such as `client`, `boss`, `friend`, or `colleague`. This influences the style of the rewrite.
- `--variants`: controls how many candidate rewrites to return. The default is `3`.
- `--mode`: selects the runtime mode. In practice, `auto` and `ai` are the relevant values for most users, and the default is usually enough.
- `--language`: manually sets the language, for example `zh` or `en`. If you omit it, the tool tries to infer the language automatically.

### Output-related

- `--plain`: prints only the raw candidate texts, which is useful for copy-paste.
- `--json`: prints structured JSON, which is useful for scripts or programmatic integration.
- `explain`: does not rewrite the message; it analyzes it. It tells you the likely intent, the main risks, and the suggested rewrite strategy.

### Config and inspection commands

- `config init`: create the user config file.
- `config show`: display the current config.
- `providers list`: show which services are supported and which keys are currently configured.
- `providers test`: quickly check whether the current provider setup is usable.
- `rules list`: show the built-in local rules.

If you only want the practical subset for daily use, these are the ones worth remembering:

```bash
sayit "..."
sayit explain "..."
sayit "..." --context bargain
sayit "..." --tone polite
sayit "..." --plain
sayit "..." --json
```

---

## Examples

Input:

```bash
sayit "你这个怎么还没弄完"
```

Example output (actual results will vary depending on context and model):

```text
- Just wanted to check where this stands right now.
- Would it be possible to share the current status?
- Roughly how much longer do you think this will take?
```

Input:

```bash
sayit explain "你先把钱转我"
```

Example output:

```text
Intent: request
Risk: too blunt, may sound like a direct command
Strategy: keep the core ask, reduce the command tone, add politeness and buffer
```

---

## How To Run It

The repository provides one main bootstrap script at the root: `./setup`. It hides most of the Docker details needed for the first run and installs the `sayit` command into your shell environment. For most people, the normal flow is to run `./setup` once and then use `sayit` directly after that.

`sayit` is mainly aimed at macOS and common shell environments. On other platforms, you can still run it directly with Docker commands.

---

## Requirements

In the default setup, you need:

* Docker / Docker Desktop
* a working model-service API key
* a `.env` file in the project root

---

## Configuration

### `.env`

For most people, the only file you actually need to touch is the `.env` file in the project root. If that file does not exist yet, run `./setup` once and it will create it for you from `.env.example`. Your `.env` file should stay on your own machine and **must not be committed to GitHub**, because it may contain your own key.

If you are using official OpenAI, the usual setup is just one line: replace `OPENAI_API_KEY=` with your own key. You do not need to fill in a URL, and you do not need to edit anything under `src`; the default endpoint is already configured in the project. The most common version looks like this:

```env
OPENAI_API_KEY=your_api_key_here
```

There are a few small details worth getting right here: put the key directly after the `=`, do not wrap it in quotes, do not add extra spaces, and do not split it across multiple lines. Once you save the file, the simplest way to verify that it is correct is to run a normal command and see whether `sayit` returns a result:

```bash
sayit "你这个怎么还没弄完"
```

If this is your first time setting it up, the safest order is: run `./setup`, let it create `.env` and install the `sayit` command, open `.env` in a text editor, fill in `OPENAI_API_KEY=...`, save the file, then go back to the terminal and run `sayit "你这个怎么还没弄完"`. For most users, that is enough, and everything else in this section can wait.

### Using Another OpenAI-Compatible Service

If you are not using official OpenAI and want to connect another OpenAI-compatible service instead, then you need a few more fields. In that case, you are telling `sayit` which provider to use, which base URL to call, which model name to send, and which key to use. A typical `.env` looks like this:

```env
SAYIT_PROVIDER_DEFAULT=custom
SAYIT_CUSTOM_BASE_URL=https://your-provider.example.com/v1
SAYIT_CUSTOM_MODEL=your-model-name
SAYIT_CUSTOM_API_KEY=your_api_key_here
```

The two fields people mix up most often are `SAYIT_CUSTOM_BASE_URL` and `SAYIT_CUSTOM_MODEL`. The first is the API endpoint, and the second is the model name. You only need this section if you already know you are using another compatible service. Otherwise, you can ignore it completely and keep the setup to a single `OPENAI_API_KEY=...` line.

### User Config File

Besides `.env`, the project also supports a user config file at `~/.config/sayit/config.toml`. This is not required for the first run. It is there for people who want to save default behavior, such as a preferred language, number of variants, or output format.

If you do want to create it manually, run:

```bash
sayit config init
```

This creates:

```text
~/.config/sayit/config.toml
```

After that, you can inspect the currently active configuration with:

```bash
sayit config show
```

For most users, the first run does not require creating this file manually. In practice, `.env`, `./setup`, and `sayit` are enough. If your goal is simply to get the project running, focus on `.env` first and ignore `config.toml` until you actually need custom defaults.

A common config looks like this:

```toml
[defaults]
language = "zh"
mode = "auto"
context = "work"
tone = "polite"
variants = 3
preserve_facts = true

[output]
format = "pretty"
show_notes = true

[provider]
default = "openai"
timeout_seconds = 20
```

---

## Usage Guide

### 1) Rewrite a Single Message

```bash
sayit "你这个怎么还没弄完"
```

This is the most common usage. `sayit` returns a few alternative versions that are easier to send.

### 2) Rewrite With Context

```bash
sayit "这个价格太高了" --context bargain
```

Context helps the tool choose a more stable rewrite direction, such as negotiation, refusal, reminder, or follow-up.

### 3) Inspect the Local Analysis

```bash
sayit explain "我今天不想去了"
```

`explain` outputs the local analysis for the message, including:

* which intent it is closest to
* which risks are present
* which rewrite strategy is likely to fit

It is useful for debugging rules, checking the reasoning path, or understanding why a sentence was rewritten in a certain way.

### 4) Machine-Readable Output

```bash
sayit "这个价格太高了" --json
```

Useful for scripts and programmatic integration.

### 5) Plain Text Only

```bash
echo "这个价格太高了" | sayit --plain
```

Useful for shell pipelines or fast copy-paste.

### 6) Read Input From a File

```bash
sayit draft.txt
```

---

## Input and Output

### Input Sources

`sayit` supports multiple input sources:

* command-line arguments (`argv`)
* standard input (`stdin`)
* files
* clipboard

### Output Formats

It supports three output formats:

* `pretty`: default, for humans
* `plain`: raw candidate text only
* `json`: for scripts and programs

---

## How It Works

`sayit` currently generates rewrite candidates through a model service. Before the request is sent, it still performs a **local detection and planning pass** that helps:

* identify whether the message is closer to a follow-up, refusal, request, apology, negotiation, or complaint
* detect risks such as being too harsh, too vague, or too command-like
* give the generation step a more controlled direction

The local rule layer is not the final output itself. It exists to make the resulting candidates steadier and less dependent on fully free-form generation.

---

## Troubleshooting

### `Cannot connect to the Docker daemon`

This usually means Docker Desktop has not fully started yet. On macOS, `./setup` and `sayit` try to launch it and wait for it. If that still fails, open Docker Desktop manually and try again.

### `No available AI provider configured`

This usually means:

* `.env` is missing
* the key is wrong
* the key is currently unusable

Check whether the relevant `.env` entries are present and correctly formatted.

### Network Errors

This usually means your current network cannot reach the model service you are using. Check connectivity, proxy settings, or the availability of the service itself.

---

## Development

If you want to modify the code, the most direct path is to run tests, inspect provider status, and inspect the rule list.

Common commands:

```bash
pytest
PYTHONPATH=src python -m sayit providers list
PYTHONPATH=src python -m sayit providers test
PYTHONPATH=src python -m sayit rules list
```

The repository already includes:

* basic tests
* bilingual README files
* Dockerfile
* compose setup
* CI
* contribution docs
* license

That is enough to support public alpha-stage use and collaboration.

---

## Project Status

`sayit` is currently in **alpha**.
Interfaces, rules, output details, and configuration shape may still change.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Contributions are welcome, especially:

* bug fixes
* rule improvements
* documentation improvements
* platform compatibility improvements
* real-world usage examples
* provider-related improvements

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## License

See [LICENSE](LICENSE).
