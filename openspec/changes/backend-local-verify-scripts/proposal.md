## Why

Developers currently have no local equivalent of the CI pipeline checks defined in `backend-ci.yml`, requiring them to push commits and wait for GitHub Actions feedback to discover lint, type, security, or test failures. Providing per-check scripts and a combined runner closes this feedback loop immediately.

## What Changes

- Add `scripts/verify-lint.sh` — runs `ruff check app/`
- Add `scripts/verify-format.sh` — runs `ruff format --check app/`
- Add `scripts/verify-types.sh` — runs `mypy app/ --strict`
- Add `scripts/verify-security.sh` — runs `bandit -r app/ -c pyproject.toml -ll`
- Add `scripts/verify-tests.sh` — runs `pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html`
- Add `scripts/verify-deps.sh` — runs `pip-audit --skip-editable --desc`
- Add `scripts/verify-all.sh` — runs all six scripts in order, reporting a pass/fail summary

## Capabilities

### New Capabilities
- `local-verify-scripts`: Shell scripts that mirror every CI job in `backend-ci.yml`, runnable individually or all at once from a developer's local machine

### Modified Capabilities
<!-- None -->

## Impact

- New files only — no existing code is modified
- Requires Python dev dependencies already installed (`pip install -e ".[dev]"`)
- All scripts must be run from the `backend/` directory (matching CI working directory)
