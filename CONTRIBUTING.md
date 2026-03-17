# Contributing to sayit

Thanks for contributing.

## Before you start

- Keep `sayit` focused on short, sendable message rewrites.
- Prefer controlled behavior over clever but unstable behavior.
- Do not add features that turn the project into a chatbot or general writing assistant.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Optional provider setup:

```bash
cp .env.example .env
```

Then fill in any provider keys you want to test locally.

## Development workflow

1. Make a focused change.
2. Add or update tests.
3. Run `pytest`.
4. If you change templates or rules, test with at least one real CLI example.

## Project structure

- `src/sayit/domain/`: core models, planner, validators, scoring
- `src/sayit/engines/local/`: local rule and template engine
- `src/sayit/engines/ai/`: provider abstraction and AI path
- `src/sayit/templates/`: YAML rules and rewrite templates
- `tests/`: unit and integration tests

## Contribution guidelines

- Keep inputs and outputs short.
- Preserve user facts by default.
- Avoid fabricated reasons, dates, or promises.
- Prefer explicit templates and rules over hidden heuristics when behavior must be stable.
- If adding a new intent or tone rule, update both templates and tests.

## Pull requests

Please include:

- what changed
- why it changed
- sample input/output before and after
- any known limits or follow-up work

Small, focused pull requests are easier to review and merge.
