## 1. Directory Setup

- [x] 1.1 Create `backend/scripts/` directory

## 2. Individual Verify Scripts

- [x] 2.1 Create `backend/scripts/verify-lint.sh` — runs `ruff check app/` (mirrors `ruff-lint` CI job)
- [x] 2.2 Create `backend/scripts/verify-format.sh` — runs `ruff format --check app/` (mirrors `ruff-format` CI job)
- [x] 2.3 Create `backend/scripts/verify-types.sh` — runs `mypy app/ --strict` (mirrors `mypy` CI job)
- [x] 2.4 Create `backend/scripts/verify-security.sh` — runs `bandit -r app/ -c pyproject.toml -ll` (mirrors `bandit` CI job)
- [x] 2.5 Create `backend/scripts/verify-tests.sh` — runs `pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html` (mirrors `pytest` CI job)
- [x] 2.6 Create `backend/scripts/verify-deps.sh` — runs `pip-audit --skip-editable --desc` with two-call pattern (mirrors `pip-audit` CI job)

## 3. Combined Script

- [x] 3.1 Create `backend/scripts/verify-all.sh` — calls all six individual scripts sequentially, collects exit codes, prints named pass/fail summary, exits 1 if any check failed

## 4. Script Compliance

- [x] 4.1 Add shebang (`#!/usr/bin/env bash`) and source-tracing header comment to every script
- [x] 4.2 Add `set -euo pipefail` to each individual script (fast-fail on errors within the script)
- [x] 4.3 Use `SCRIPT_DIR` / `cd` pattern in each script so it runs correctly from any working directory
- [x] 4.4 Mark all scripts executable with `chmod +x backend/scripts/*.sh`

## 5. Verification

- [x] 5.1 Run `./backend/scripts/verify-lint.sh` from repo root — confirm it exits 0 on a clean codebase
- [x] 5.2 Run `./backend/scripts/verify-format.sh` from repo root — confirm it exits 0
- [x] 5.3 Run `./backend/scripts/verify-types.sh` from repo root — confirm it exits 0
- [x] 5.4 Run `./backend/scripts/verify-security.sh` from repo root — confirm it exits 0
- [x] 5.5 Run `./backend/scripts/verify-tests.sh` from repo root — confirm tests pass
- [x] 5.6 Run `./backend/scripts/verify-deps.sh` from repo root — confirm it exits 0
- [x] 5.7 Run `./backend/scripts/verify-all.sh` from repo root — confirm all-pass summary and exit 0
