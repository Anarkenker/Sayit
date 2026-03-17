# sayit

`sayit` is a Python CLI for rewriting short, awkward, blunt, or not-sendable messages into cleaner versions that you can copy and send.

It is not a chatbot and it is not a long-form writing assistant.

The product boundary is intentional:

- short input
- short output
- explicit social intent
- controlled rewrite instead of free generation

## What it does

Given input like:

- `你这个怎么还没弄完`
- `这个价格太高了`
- `我今天不想去了`
- `你先把钱转我`
- `我这边要延期`

`sayit` produces variants such as:

- polite
- direct
- firm
- soft

And `sayit explain` tells you:

- detected intent
- risk flags
- rewrite strategy

## Current MVP

- Chinese-first local rewrite engine
- intent detection and risk detection
- rule-driven planner
- YAML-based templates
- `argv`, `stdin`, file, and clipboard input
- `pretty`, `plain`, and `json` output
- `explain` command
- OpenAI-compatible provider scaffold
- `local`, `ai`, and `hybrid` modes

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Or install the local repo with `pipx`:

```bash
pipx install .
```

After install, the CLI is available as:

```bash
sayit "你这个怎么还没弄完"
```

If you do not install the package yet, you can still run it with:

```bash
PYTHONPATH=src python -m sayit "你这个怎么还没弄完"
```

## Where the API key should go

Do not hardcode API keys in source files.

The recommended setup is:

1. Put the real key in an environment variable.
2. Keep only the environment variable name in config.
3. Commit `.env.example`, never commit `.env`.

### Recommended for local development

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then fill in the key you need:

```bash
OPENAI_API_KEY=your_real_key_here
OPENROUTER_API_KEY=
```

`sayit` loads `.env` automatically at runtime.

### Recommended for production or CI

Use environment variables provided by your shell, CI, or hosting platform:

```bash
export OPENAI_API_KEY="your_real_key_here"
```

### Config file location

The config file lives at:

```text
~/.config/sayit/config.toml
```

Important:

- the config file should store `api_key_env = "OPENAI_API_KEY"`
- the config file should not store the secret itself

Default provider config is already wired like this:

```toml
[providers.openai]
base_url = "https://api.openai.com/v1"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"
```

## Quick start

### Local mode, no API required

```bash
sayit "你这个怎么还没弄完"
sayit "我今天不想去了" --tone soft
sayit explain "这个价格太高了"
```

### AI or hybrid mode

```bash
sayit "这个价格太高了" --mode ai
sayit "你这个怎么还没弄完" --mode hybrid
```

Default behavior:

- if no available provider is configured: `local`
- if a provider is available: `hybrid`

## Usage

### Direct input

```bash
sayit "你这个怎么还没弄完"
```

### Clipboard

```bash
sayit --clipboard
```

### File input

```bash
sayit draft.txt
```

### stdin

```bash
pbpaste | sayit
cat raw.txt | sayit --plain
```

### Explain mode

```bash
sayit explain "你先把钱转我"
```

### Common options

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

## Output formats

### pretty

Human-readable terminal output with:

- original text
- intent
- risk flags
- candidate rewrites

### plain

Only the candidate texts.

Useful for copy/paste or shell piping:

```bash
sayit "你这个怎么还没弄完" --plain
```

### json

Useful for scripts and other tools:

```bash
sayit "这个价格太高了" --json
```

## Modes

### local

- no API required
- fast and deterministic
- driven by local rules and templates

### ai

- all candidate generation goes through the provider
- better for more nuanced language
- requires provider config and runtime key

### hybrid

- local detector and planner first
- provider generates controlled candidates
- failures can fall back to local behavior

## Project structure

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

List available templates:

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

## Known limitations

- Chinese templates are much stronger than English support right now.
- AI mode is implemented, but provider behavior still needs broader real-world validation.
- The local engine is intentionally conservative and only covers a limited set of high-frequency intents.
- There is no GUI, chat history import, or auto-send integration.

## Roadmap

- Expand the template and ruleset for the six core intents
- Add English templates and tests
- Add stable snapshot tests for representative rewrite cases
- Add stronger fact-preservation and fabricated-reason checks
- Improve provider-specific error handling and integration coverage
- Publish to PyPI for `pipx install sayit`

## Open source readiness

Good enough for a first public repo:

- clear README
- `.gitignore`
- `.env.example`
- basic CI
- local MVP

Before the first public release, replace `REPLACE_ME` placeholders in:

- [pyproject.toml](/Users/macbookpro/Documents/code/Sayit/pyproject.toml)
- [.github/ISSUE_TEMPLATE/config.yml](/Users/macbookpro/Documents/code/Sayit/.github/ISSUE_TEMPLATE/config.yml)

Still worth adding before wider promotion:

- choose a license
- add more templates and rules
- improve English template coverage
- add snapshot tests for stable outputs
- add real provider integration tests
- add issue templates and contribution guide
- polish CLI help text and error messages

## Contributing

See [CONTRIBUTING.md](/Users/macbookpro/Documents/code/Sayit/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](/Users/macbookpro/Documents/code/Sayit/CHANGELOG.md).

## License

MIT. See [LICENSE](/Users/macbookpro/Documents/code/Sayit/LICENSE).

## Design principles

- controlled generation over free-form generation
- do not invent facts by default
- solve high-frequency short scenarios first
- explanations matter as much as output quality
