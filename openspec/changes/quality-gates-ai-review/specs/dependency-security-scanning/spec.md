# Dependency Security Scanning

## Purpose

Define requirements for automated CVE (Common Vulnerabilities and Exposures) detection in project dependencies to prevent vulnerable packages from entering the codebase.

## ADDED Requirements

### Requirement: Pip-audit vulnerability scanning
All Python dependencies MUST be scanned for known CVEs via pip-audit. Vulnerabilities with CVSS score ≥4.0 MUST block the merge.

#### Scenario: Pip-audit runs in CI
- **WHEN** `pip-audit` is executed in the CI pipeline
- **THEN** it MUST scan all installed packages and report any CVEs

#### Scenario: CVE detected blocks merge
- **WHEN** a dependency has a known CVE with CVSS ≥4.0
- **THEN** the CI workflow MUST fail with a clear message listing affected packages and CVE details

#### Scenario: Low-severity CVE allowed with justification
- **WHEN** a dependency has a known CVE with CVSS <4.0
- **THEN** it MAY be allowed if documented in `.pip-audit-ignore` with justification

### Requirement: Ignore file for exceptions
A `.pip-audit-ignore` file MAY exist to document approved exceptions for vulnerabilities that are unavoidable or mitigated.

#### Scenario: Ignore file format
- **WHEN** a CVE is deemed acceptable
- **THEN** an entry MUST be added to `.pip-audit-ignore` with the CVE ID and justification (e.g., "No patch available; impact mitigated by X")

#### Scenario: Ignored CVE still tracked
- **WHEN** an ignored CVE is encountered
- **THEN** pip-audit MUST report it but NOT fail CI (informational only)

### Requirement: Dependency updates reviewed for security
Before merging a dependency update (major, minor, or patch), the PR MUST include pip-audit results showing the update resolves or introduces CVEs.

#### Scenario: Dependency update includes security note
- **WHEN** a PR updates a dependency
- **THEN** the commit message or PR description MUST note any security impact (e.g., "Updates lodash to patch CVE-2024-XXXX")

#### Scenario: No new vulnerabilities introduced
- **WHEN** a dependency version is updated
- **THEN** pip-audit MUST confirm no new CVEs are introduced

### Requirement: Transitive dependency scanning
Pip-audit MUST scan transitive (indirect) dependencies, not just direct dependencies.

#### Scenario: Transitive CVE detected
- **WHEN** a direct dependency has a transitive dependency with a CVE
- **THEN** pip-audit MUST report it with the full dependency chain

#### Scenario: Transitive CVE blocks merge
- **WHEN** a transitive CVE with CVSS ≥4.0 is detected
- **THEN** the CI workflow MUST fail unless the CVE is ignored

### Requirement: Regular dependency audits
Pip-audit MUST run on every PR and commit to main to catch new CVEs in existing locked versions.

#### Scenario: Scheduled audit workflow
- **WHEN** changes are merged to main
- **THEN** pip-audit MUST run in CI

#### Scenario: New CVE in locked dependency detected
- **WHEN** a CVE is announced for a currently-locked dependency version
- **THEN** the next PR or scheduled audit MUST detect it and recommend an upgrade

### Requirement: Audit results reporting
Pip-audit results MUST be reported in a human-readable format with links to CVE details.

#### Scenario: CVE report includes details
- **WHEN** a CVE is found
- **THEN** the report MUST include package name, version, CVE ID, CVSS score, and a link to NVD (National Vulnerability Database)

#### Scenario: Report suggests remediation
- **WHEN** a CVE is found
- **THEN** the report MUST suggest the minimum version to upgrade to (if available)

### Requirement: No vulnerable development-only dependencies
Dev dependencies (pytest, ruff, mypy) MUST also be scanned. Vulnerable dev tools can be exploited during CI/CD.

#### Scenario: Dev dependency CVE detected
- **WHEN** a dev dependency has a known CVE
- **THEN** pip-audit MUST flag it and CI MUST fail if CVSS ≥4.0

