# Backend CI Pipeline

> CI pipeline requirements for the backend workspace — all quality gates run on every PR and block merge on failure.

## Quality Gates

All four checks MUST pass before a PR can be merged to `main`. At least one human approval is also required.

| Check | Command | Blocks merge? |
|---|---|---|
| Lint | `ruff check .` | Yes |
| Format | `ruff format --check .` | Yes |
| Types | `mypy app/` (strict) | Yes |
| Security | `bandit -r app/ -c pyproject.toml` | Yes |
| Tests | `pytest` | Yes |

## Configuration

- All backend CI jobs MUST run with `working-directory: backend/` for correct path resolution
- Partial passes do not allow merge — ALL four checks must be green
