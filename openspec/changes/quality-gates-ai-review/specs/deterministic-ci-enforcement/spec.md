# Deterministic CI/CD Enforcement

## Purpose

Define automated, non-negotiable code quality checks that run in GitHub Actions before merge. These checks are deterministic (same input always produces same output) and cannot be overridden—they block merges on failure.

## ADDED Requirements

### Requirement: Ruff linting and formatting checks
The backend codebase MUST pass Ruff linting and formatting checks. No code formatted with Black or linted with Flake8 outside Ruff is acceptable.

#### Scenario: Ruff lint check passes
- **WHEN** `ruff check app/` is run in CI
- **THEN** all backend code in `app/` MUST pass without errors

#### Scenario: Ruff format check passes
- **WHEN** `ruff format --check .` is run in CI
- **THEN** all code MUST be formatted according to Ruff standards (developers can run `ruff format .` locally to auto-fix)

#### Scenario: Ruff check blocks merge
- **WHEN** a PR has ruff lint or format violations
- **THEN** the GitHub Actions workflow MUST fail and block merging until violations are fixed

### Requirement: Mypy strict type checking
The backend `app/` directory MUST pass Mypy with `--strict` mode enabled. All type errors MUST be resolved before merge.

#### Scenario: Mypy passes with strict mode
- **WHEN** `mypy app/ --strict` is run in CI
- **THEN** all type annotations MUST be correct and no `Any` types allowed without `# type: ignore` comments with justification

#### Scenario: Mypy blocks merge on type errors
- **WHEN** a PR contains type errors
- **THEN** the CI workflow MUST fail and block merging

#### Scenario: Type ignore comments require justification
- **WHEN** a developer uses `# type: ignore`
- **THEN** a brief comment MUST follow explaining why the type error cannot be fixed (e.g., `# type: ignore  # third-party library untyped`)

### Requirement: Bandit security scanning
The backend code MUST pass Bandit security scanning. High and critical security issues MUST block the merge.

#### Scenario: Bandit detects SQL injection
- **WHEN** code contains f-string SQL queries like `f"SELECT * FROM users WHERE id={id}"`
- **THEN** bandit MUST flag it with HIGH severity and CI MUST fail

#### Scenario: Bandit detects eval/exec
- **WHEN** code contains `eval()` or `exec()`
- **THEN** bandit MUST flag it with CRITICAL severity and CI MUST fail

#### Scenario: Bandit detects hardcoded secrets
- **WHEN** code contains hardcoded API keys or passwords
- **THEN** bandit MUST flag it with HIGH severity and CI MUST fail

#### Scenario: Bandit check blocks merge
- **WHEN** a PR has HIGH or CRITICAL bandit findings
- **THEN** the CI workflow MUST fail and block merging

### Requirement: Pytest test execution
All backend tests MUST pass before merge. The pytest suite MUST run with the following constraints:
- Use in-memory SQLite (aiosqlite)
- Use httpx.AsyncClient with ASGITransport (no real network calls)
- All tests must complete in <5 seconds total

#### Scenario: All tests pass
- **WHEN** `pytest` is run in CI
- **THEN** all tests MUST pass (exit code 0)

#### Scenario: Test failure blocks merge
- **WHEN** a test fails
- **THEN** the CI workflow MUST fail and block merging

#### Scenario: Deterministic test execution
- **WHEN** the same commit is tested multiple times
- **THEN** results MUST be identical (no flaky tests)

### Requirement: Code coverage threshold enforcement
Code coverage MUST be ≥80% measured on the `app/` directory. Coverage below 80% blocks the merge.

#### Scenario: Coverage report generated
- **WHEN** `pytest --cov=app --cov-report=term-missing` is run
- **THEN** a coverage report MUST be generated showing module-level coverage

#### Scenario: Coverage below threshold blocks merge
- **WHEN** overall coverage is <80%
- **THEN** the CI workflow MUST fail with a message indicating the coverage shortfall

#### Scenario: Coverage exclusions respected
- **WHEN** coverage is measured
- **THEN** migrations (alembic/), test files, and `__pycache__` directories MUST be excluded

### Requirement: Pip-audit dependency vulnerability scanning
All dependencies MUST be scanned for known CVEs. Vulnerable packages (CVSS ≥ 4.0) MUST block the merge.

#### Scenario: Pip-audit detects vulnerable dependency
- **WHEN** `pip-audit` is run against the installed packages
- **THEN** any dependency with a known CVE MUST be flagged

#### Scenario: Vulnerable dependency blocks merge
- **WHEN** a PR introduces or retains a dependency with a known CVE
- **THEN** the CI workflow MUST fail and block merging

#### Scenario: Ignoring vulnerabilities requires exception
- **WHEN** a CVE is deemed unavoidable (e.g., no patch available)
- **THEN** an exception MUST be documented in a `.pip-audit-ignore` file with justification

### Requirement: GitHub Actions workflow for backend CI
A GitHub Actions workflow (`backend-ci.yml`) MUST run on all PRs to `main`. The workflow MUST execute in parallel where possible and report results.

#### Scenario: Workflow triggers on PR
- **WHEN** a PR is opened or updated with commits to `backend/`
- **THEN** the backend-ci.yml workflow MUST trigger automatically

#### Scenario: All checks run in parallel
- **WHEN** the workflow runs
- **THEN** ruff, mypy, bandit, pytest, and pip-audit checks MUST run in parallel for speed

#### Scenario: Workflow reports comprehensive summary
- **WHEN** the workflow completes
- **THEN** the PR status check MUST show pass/fail for each job; clicking details reveals logs

### Requirement: Required status checks on main branch
GitHub Branch Protection MUST require all CI status checks to pass before merging to `main`.

#### Scenario: PR cannot merge without passing CI
- **WHEN** a PR has failing CI checks
- **THEN** the merge button MUST be disabled with a message indicating which checks must pass

