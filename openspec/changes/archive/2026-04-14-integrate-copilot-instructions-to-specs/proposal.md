## Why

The three `copilot-instructions.md` files (root, backend, frontend) contain extensive coding standards covering ~20+ domains (security, testing, API design, performance, observability, etc.), but only a small subset has been formalized into the OpenSpec `specs/` system. The existing 7 specs cover AI chat PII, persona roles, coding standards quick-ref, frontend CI/linting/testing — leaving major domains like backend CI, security (OWASP), error handling, API design, database integrity, observability, and deployment without formal specs. This gap means the spec system cannot serve as the authoritative, verifiable source of truth for project standards.

## What Changes

- Create new specs for each major coding standard domain not yet covered by an existing spec
- Organize specs into logical capability groups mirroring the copilot-instructions structure
- Cover both shared (root) standards and workspace-specific (backend, frontend) standards
- Ensure each spec captures verifiable requirements (not just guidelines) that can drive implementation tasks

## Capabilities

### New Capabilities
- `backend-ci-pipeline`: Backend CI pipeline configuration (ruff, mypy, bandit, pytest jobs and enforcement rules)
- `backend-testing-standards`: Backend testing patterns (async test client, fixtures, TDD, coverage targets, test naming)
- `backend-api-design`: Backend API conventions (versioning, pagination, error format, status codes, idempotency)
- `backend-security-owasp`: Backend OWASP security enforcement (SQL injection prevention, input validation, auth patterns)
- `backend-observability`: Backend observability standards (structlog, correlation IDs, RED metrics, health checks)
- `backend-schema-design`: Backend Pydantic schema patterns (Base/Create/Update/Response, partial updates, validation)
- `shared-error-handling`: Cross-cutting error handling and resilience patterns (circuit breakers, retries, timeouts, graceful degradation)
- `shared-git-workflow`: Git workflow and commit message format standards (branch naming, PR rules, commit format)
- `shared-dependency-management`: Dependency management rules (justification, pinning, vulnerability scanning, license checks)
- `frontend-security`: Frontend security standards (XSS prevention, token storage, CSP, CSRF protection)
- `frontend-accessibility`: Frontend accessibility requirements (semantic HTML, keyboard nav, WCAG AA contrast, ARIA, screen reader)
- `frontend-resilience`: Frontend error recovery and resilience patterns (retry, abort controller, error boundaries, offline detection)

### Modified Capabilities
- `coding-standards-quick-ref`: Update to reference newly created specs as the authoritative source for each domain

## Impact

- **Specs directory**: 12 new spec files under `openspec/specs/`
- **Existing specs**: Minor update to `coding-standards-quick-ref` to cross-reference new specs
- **No code changes**: This change only formalizes existing documented standards into specs
- **Source files**: `copilot-instructions.md` files remain unchanged — specs are derived from them, not replacing them
