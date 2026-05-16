# Backend Testing Standards - Delta

## MODIFIED Requirements

### Requirement: Coverage target
Test suite SHALL target 80%+ code coverage as a merge-blocking requirement in CI/CD.

#### Scenario: Coverage threshold
- **WHEN** `pytest --cov=app --cov-report=term-missing` is run in CI
- **THEN** overall coverage MUST be at least 80% and CI MUST fail if below this threshold

#### Scenario: Coverage exclusions respected
- **WHEN** coverage is measured
- **THEN** migrations (alembic/), test files, and `__pycache__` directories MUST be excluded from the coverage report

### Requirement: CI/CD enforcement of tests
All tests MUST pass and coverage MUST meet the 80% threshold before a PR can be merged. GitHub Branch Protection MUST require this status check.

#### Scenario: Test failure blocks merge
- **WHEN** any test fails in the CI pipeline
- **THEN** the GitHub status check MUST fail and merging MUST be blocked

#### Scenario: Coverage below threshold blocks merge
- **WHEN** code coverage falls below 80%
- **THEN** the GitHub status check MUST fail with a message indicating the shortfall

#### Scenario: Coverage report in PR
- **WHEN** a PR is evaluated
- **THEN** the coverage report MUST be visible in the CI logs (percentage + file-by-file breakdown)

