## ADDED Requirements

### Requirement: Justify new dependencies
Every new dependency MUST be justified. Prefer stdlib or existing dependencies over adding new ones.

#### Scenario: New dependency justification
- **WHEN** a PR adds a new dependency
- **THEN** the PR description MUST explain why it is needed and why existing deps or stdlib cannot suffice

### Requirement: Pin versions in lockfiles
All dependencies MUST be pinned in lockfiles (`package-lock.json`, `pyproject.toml` constraints) for reproducible builds.

#### Scenario: Lockfile committed
- **WHEN** a dependency is added or updated
- **THEN** the lockfile MUST be updated and committed in the same PR

### Requirement: License compatibility
Dependency licenses MUST be compatible with the project. License checks MUST be performed before adding.

#### Scenario: License check on new dep
- **WHEN** a new dependency is being evaluated
- **THEN** its license MUST be checked for compatibility before adding

### Requirement: Vulnerability scanning in CI
CI MUST run vulnerability scanning (`pip-audit` for Python, `npm audit` for frontend) on every PR.

#### Scenario: Vulnerable dependency blocks merge
- **WHEN** a vulnerability scan finds known CVEs in dependencies
- **THEN** the CI check MUST fail and the PR MUST NOT be mergeable

### Requirement: Regular dependency updates
Dependencies MUST be updated regularly — small, frequent updates are preferred over large, infrequent ones.

#### Scenario: Dependabot or equivalent enabled
- **WHEN** the repository is configured
- **THEN** automated dependency update tooling (Dependabot, Snyk, or equivalent) MUST be enabled
