# Contributing to sayit

Thanks for contributing.

## Before you start

- Keep `sayit` focused on short, sendable message rewrites.
- Prefer controlled behavior over clever but unstable behavior.
- Do not add features that turn the project into a chatbot or general writing assistant.

## Local setup

Recommended runtime:

```bash
docker build -t sayit .
docker run --rm --env-file .env sayit "你这个怎么还没弄完"
```

Alternative Python setup:

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
4. If you change rules or provider behavior, test with at least one real CLI example.

## Project structure

- `src/sayit/domain/`: core models, planner, validators, scoring
- `src/sayit/engines/local/`: local rule-based intent detection
- `src/sayit/engines/ai/`: provider abstraction and AI path
- `src/sayit/rules/`: YAML rules for local analysis
- `tests/`: unit and integration tests

## Contribution guidelines

- Keep inputs and outputs short.
- Preserve user facts by default.
- Avoid fabricated reasons, dates, or promises.
- Prefer explicit rules and validations over hidden heuristics when behavior must be stable.
- If adding or changing a rule, update both rules and tests.

## Pull requests

Please include:

- what changed
- why it changed
- sample input/output before and after
- any known limits or follow-up work

Small, focused pull requests are easier to review and merge.
