## Why

Code quality and security vulnerabilities often slip through manual review. Without automated enforcement, engineering standards become aspirational rather than enforceable, leading to inconsistent architectures, potential security breaches (SQL injection, PII logging), and slower PR turnaround times. This change establishes a two-layer quality gate system that catches deterministic issues (formatting, type errors, security smells) early via CI/CD, while using AI to review architectural patterns and business logic—reducing manual reviewer burden and preventing avoidable rework.

## What Changes

- **Commit Standards Enforcement**: Branch protection rules block commits that don't follow `feat/`, `fix/`, `hotfix/`, or `release/` prefixes. Commit message format is validated via commitlint with rejection of Co-authored-by trailers.
- **Deterministic CI/CD Pipeline**: GitHub Actions workflows enforce ruff (lint + format), mypy (strict type checking), bandit (security scanning), pip-audit (dependency vulnerability scanning), and pytest with ≥80% code coverage before merge.
- **AI PR Review Agent**: Codium AI PR Agent runs on every PR, configured with project-specific guidelines to catch architectural violations (thin routes, correct schemas, proper error handling, security patterns) without noise from formatting issues.
- **Configuration as Code**: `.pr_agent.toml` centralizes AI reviewer rules, `.github/workflows/` contains CI definitions, and Husky pre-commit hooks enable local feedback before push.
- **New `.pr_agent.toml`**: Project-specific AI review constraints injected into the LLM system prompt.

## Capabilities

### New Capabilities

- `git-commit-standards`: Enforce branch naming (feat/fix/hotfix/release), commit message format ({PackageName} prefix, ≤10 line body), and reject Co-authored-by trailers via commitlint + Husky + GitHub Branch Protection.
- `deterministic-ci-enforcement`: Automated linting, type checking, security scanning, and dependency vulnerability detection. Blocks merges on failure. Covers ruff, mypy, bandit, pip-audit, pytest with coverage thresholds.
- `ai-pr-review`: AI-powered pull request review focusing on architecture, business logic, error handling, security patterns, and API design. Configured via `.pr_agent.toml` with project guidelines.
- `dependency-security-scanning`: Automated CVE detection via pip-audit to prevent vulnerable dependencies from entering the codebase.

### Modified Capabilities

- `backend-testing-standards`: Extends with pytest configuration, coverage thresholds (≥80%), and enforcement via CI/CD. Tests must use httpx.AsyncClient with ASGITransport and aiosqlite (no external calls).
- `backend-security-owasp`: Extends with Bandit integration and explicit SQL injection prevention enforcement in AI review rules.
- `backend-observability`: Extends with structlog enforcement in AI review rules (reject print(), demand structlog.get_logger()).

## Impact

- **Affected Code/Directories**: `.github/workflows/` (new CI pipelines), `pyproject.toml` (ruff/mypy config), `.pre-commit-config.yaml` (Husky), `backend/`, `frontend/` (inherit CI checks).
- **Affected APIs**: All new endpoints must pass schema validation and pagination checks. No breaking changes to existing APIs.
- **Affected Dependencies**: New: commitlint, Husky, ruff (if not present), mypy (if not present), bandit, pip-audit, pytest-cov. AI review uses Claude 3.5 Sonnet or GPT-4o (configured via API key).
- **Affected Systems**: GitHub Actions CI/CD system, local pre-commit hook system, GitHub Branch Protection settings, PR review workflow.
- **Breaking Changes**: None. New enforcement is additive—existing code may need refactoring to comply, but no API or system interfaces change.

