# Local Verify Scripts

## Purpose

Developers need to run the same CI checks locally before pushing, catching issues fast without waiting for GitHub Actions. The `backend/scripts/verify-*.sh` suite mirrors each CI job, allowing offline verification and rapid iteration.

## Requirements

### Requirement: Individual verify scripts exist for each CI job
The system SHALL provide one executable shell script per CI job defined in `backend-ci.yml`, located at `backend/scripts/verify-<job>.sh`.

#### Scenario: Lint script mirrors ruff-lint job
- **WHEN** developer runs `backend/scripts/verify-lint.sh`
- **THEN** the script executes `ruff check app/` from the `backend/` directory and exits 0 on success, non-zero on lint errors

#### Scenario: Format script mirrors ruff-format job
- **WHEN** developer runs `backend/scripts/verify-format.sh`
- **THEN** the script executes `ruff format --check app/` from the `backend/` directory and exits 0 on success, non-zero on formatting violations

#### Scenario: Types script mirrors mypy job
- **WHEN** developer runs `backend/scripts/verify-types.sh`
- **THEN** the script executes `mypy app/ --strict` from the `backend/` directory and exits 0 on success, non-zero on type errors

#### Scenario: Security script mirrors bandit job
- **WHEN** developer runs `backend/scripts/verify-security.sh`
- **THEN** the script executes `bandit -r app/ -c pyproject.toml -ll` from the `backend/` directory and exits 0 when no HIGH/CRITICAL issues are found, non-zero otherwise

#### Scenario: Tests script mirrors pytest job
- **WHEN** developer runs `backend/scripts/verify-tests.sh`
- **THEN** the script executes `pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html` from the `backend/` directory and exits 0 on all tests passing, non-zero on any failure

#### Scenario: Deps script mirrors pip-audit job
- **WHEN** developer runs `backend/scripts/verify-deps.sh`
- **THEN** the script runs `pip-audit --skip-editable --desc` from the `backend/` directory and exits 0 when no vulnerabilities are found, non-zero when high-severity CVEs are detected

### Requirement: Scripts are executable from any working directory
Each individual script SHALL resolve the `backend/` directory relative to the script's own location, not the caller's working directory.

#### Scenario: Script called from repo root
- **WHEN** developer runs `./backend/scripts/verify-lint.sh` from the repo root
- **THEN** the script correctly runs `ruff check app/` inside `backend/` and exits with the appropriate code

#### Scenario: Script called from backend directory
- **WHEN** developer runs `./scripts/verify-lint.sh` from inside `backend/`
- **THEN** the script correctly runs `ruff check app/` inside `backend/` and exits with the appropriate code

### Requirement: Combined verify-all script runs all checks and summarises results
The system SHALL provide `backend/scripts/verify-all.sh` that runs all six individual verify scripts sequentially and prints a pass/fail summary.

#### Scenario: All checks pass
- **WHEN** developer runs `backend/scripts/verify-all.sh` and all six checks succeed
- **THEN** the script prints a summary showing each check as PASSED and exits 0

#### Scenario: One or more checks fail
- **WHEN** developer runs `backend/scripts/verify-all.sh` and at least one check fails
- **THEN** the script continues running remaining checks, prints a summary showing which checks PASSED and which FAILED, and exits 1

#### Scenario: Failed check name is visible in summary
- **WHEN** `verify-all.sh` completes with at least one failure
- **THEN** the printed summary explicitly names each failing check so the developer knows exactly what to fix

### Requirement: Scripts have a source-tracing header comment
Each script SHALL include a comment block at the top identifying the corresponding CI job in `backend-ci.yml`.

#### Scenario: Header present in individual script
- **WHEN** developer opens any `verify-<job>.sh` file
- **THEN** the first non-shebang lines identify the CI job name (e.g., `# CI job: ruff-lint`) and the workflow file (`# Source: .github/workflows/backend-ci.yml`)

### Requirement: Scripts are marked executable
All scripts in `backend/scripts/` SHALL have the executable bit set (`chmod +x`).

#### Scenario: Script is directly invocable
- **WHEN** developer runs `./backend/scripts/verify-lint.sh` without `bash` prefix
- **THEN** the OS executes the script without a "Permission denied" error
