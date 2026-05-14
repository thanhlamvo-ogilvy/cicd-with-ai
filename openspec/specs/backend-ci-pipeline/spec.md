# Backend CI Pipeline

## Purpose

Define the CI pipeline configuration for the backend workspace, ensuring all quality gates (linting, type checking, security scanning, testing) run on every PR and block merge on failure.

## Requirements

### Requirement: Backend CI jobs run from backend directory
All backend CI jobs (ruff, mypy, bandit, pytest) SHALL execute with `working-directory: backend/` to ensure correct path resolution.

#### Scenario: CI job working directory
- **WHEN** a backend CI job executes
- **THEN** it MUST run from the `backend/` directory

### Requirement: Ruff lint and format check
CI SHALL run `ruff check .` and `ruff format --check .` on every PR to main. Violations MUST block merge.

#### Scenario: Ruff lint failure blocks merge
- **WHEN** `ruff check .` reports violations on a PR
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

#### Scenario: Ruff format failure blocks merge
- **WHEN** `ruff format --check .` reports formatting violations on a PR
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

### Requirement: Mypy strict type checking
CI SHALL run `mypy app/` with strict mode on every PR to main. Type errors MUST block merge.

#### Scenario: Mypy failure blocks merge
- **WHEN** `mypy app/` reports type errors on a PR
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

### Requirement: Bandit security scan
CI SHALL run `bandit -r app/ -c pyproject.toml` on every PR to main. Security findings MUST block merge.

#### Scenario: Bandit failure blocks merge
- **WHEN** `bandit -r app/ -c pyproject.toml` reports security findings on a PR
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

### Requirement: Pytest execution
CI SHALL run `pytest` on every PR to main. Test failures MUST block merge.

#### Scenario: Pytest failure blocks merge
- **WHEN** `pytest` reports test failures on a PR
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

### Requirement: All four checks required before merge
All four CI checks (ruff, mypy, bandit, pytest) MUST pass before a PR can be merged to main. At least one human approval is also required.

#### Scenario: Partial CI pass does not allow merge
- **WHEN** three of four CI checks pass but one fails
- **THEN** the PR MUST NOT be mergeable
