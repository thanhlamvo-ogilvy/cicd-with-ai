<!--
Purpose: Shared coding standards, Git workflow, CI/CD practices, and AI persona rules.
Scope: All workspaces (root, backend/, frontend/).
Key: Git commit format is mandatory; personas guide AI behavior per file path.
Workspace-specific: Backend and frontend files override/extend these standards.
-->

# Copilot Instructions

## Project Structure

This is a monorepo with two workspaces. Each has its own coding standards:

- **`backend/`** — Python FastAPI API → see [`backend/copilot-instructions.md`](../backend/copilot-instructions.md)
- **`frontend/`** — React 19 + TypeScript + Vite UI → see [`frontend/copilot-instructions.md`](../frontend/copilot-instructions.md)

When working in a specific workspace, follow that workspace's instructions. This file covers shared, cross-workspace standards.

## Quick Start

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload        # http://localhost:8000

# Frontend
cd frontend
npm install
npm run dev                          # http://localhost:5173

# Docker (both)
docker compose up --build
```

## Clean Code Principles

Apply to **all code** in every language. Key rules:
- Intention-revealing names; single-letter names forbidden outside tiny scopes
- Small functions (≤30 lines), single responsibility, DRY, no dead code
- Guard clauses over nesting; refactor nested code >3 levels
- Boy Scout Rule — leave code cleaner than found

See [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) for detailed guidance.

## SOLID Principles

**S** — Single Responsibility: one reason to change (routes=HTTP, services=logic, components=UI)  
**O** — Open/Closed: extend via abstraction, not modification (e.g., `AIProvider` ABC)  
**L** — Liskov Substitution: subtypes interchangeable (honor contracts like `stream_chat`)  
**I** — Interface Segregation: focused interfaces/props (split if >5–6 items)  
**D** — Dependency Inversion: depend on abstractions; inject dependencies (never hardcode)

Workspace-specific guidance: backend/copilot-instructions.md, frontend/copilot-instructions.md

## Version Control & Git Workflow

- Never commit directly to `main` — always create a feature branch and open a PR.
- Use descriptive branch prefixes: `feat/`, `fix/`, `hotfix/`, `release/`.
- Keep branches short-lived — merge or close within days, not weeks.
- Keep PRs focused — one logical change per PR.
- All CI checks (ruff, mypy, bandit, pytest) must pass before merge. At least one human approval is required.
- Every commit must be potentially deployable (Continuous Delivery).
- Use SemVer (MAJOR.MINOR.PATCH) for API versioning — bump MAJOR for breaking changes.
- Rebase or squash-merge to keep history clean and bisectable.

## Git Commit Message Format

All commit messages must follow this structured release notes format:

```
[Primary Change Description]; [Secondary Changes] & more…

{PackageName}
- [Action verb] [concise description of change ≤ 120 chars]
- [Action verb] [another change description]

{AnotherPackage}
- [Action verb] [change description]

(No dependency updates.)
```

**Rules:**
1. **Title line** — Lead with the most newsworthy change; end with `& more…` if multi-topic; no trailing period
2. **Group changes** under curly-brace headers (`{PkgName}`) — common buckets: `{Dependencies}`, `{Backend}`, `{Frontend}`, `{CI}`, `{Docs}`
3. **Bullet points** — Start with present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); keep ≤ 120 characters; no periods
4. **Dependencies** — If no dependency updates, include literal line `(No dependency updates.)` after last section
5. **No attribution tags** — Never add co-authored-by trailers or generator attribution

## Testability & Testing

- **TDD cycle**: Red → Green → Refactor. Write failing test first.
- **Test Pyramid**: Many unit tests (base), fewer integration tests (middle), minimal E2E tests (top).
- **Beyoncé Rule**: "If you liked it, put a test on it." Untested code is untrustworthy.
- **Deterministic**: No flaky dependencies on time, network, or order.
- **Isolated**: Each test independent; no shared mutable state.
- **Fast**: Unit tests < 1s; integration tests < 5s.
- Edge cases: nulls, empty inputs, boundary values, zero.
- Mock external services at integration boundaries only.

## Error Handling & Resilience

- No bare `catch`/`except` — always handle specific error types or re-raise.
- Never swallow errors silently — log, propagate, or handle explicitly.
- Circuit breakers: fail fast on repeated external service failures.
- Retries: exponential backoff with jitter; never tight loops.
- Timeouts: explicit on all network, DB, and external calls.
- Bulkhead pattern: isolate failures; prevent cascade failures.
- Graceful degradation: use cached data or fallback when dependency unavailable.

## API Design

- RESTful: nouns for resources, HTTP verbs for actions, correct status codes
- Versioning: explicit (`/v1/` path or header), never silent breaking changes
- Validation: reject malformed input at boundary with clear messages
- Pagination: all list endpoints use `limit`/`offset` or cursor
- Rate limiting: protect endpoints from abuse
- Idempotent mutations: safe to retry
- Consistent error format: `{"detail": "message"}`
- Documentation: auto-generate OpenAPI/Swagger from code

## Database & Data Integrity

See workspace-specific files for implementation details:
- Migrations: safe, reversible, backward-compatible
- Indexes: on WHERE, JOIN, ORDER BY columns
- N+1 patterns: use eager loading, joins, batch fetching
- Transactions: wrap multi-step operations
- Schema changes: backward-compatible (expand-contract pattern)
- PII: encrypt at rest and in transit

## Security (Cross-Cutting)

- No hardcoded secrets (use env vars or secrets manager); rotate on schedule
- Validate & sanitize all user input; defend against OWASP Top 10
- Auth/authz checks on protected endpoints; follow least privilege
- Never use `eval()`, `exec()`, dynamic code execution
- Security headers: CORS (explicit origins, never `*`), CSP, HSTS, X-Content-Type-Options
- Dependencies: free of known CVEs; scan before adding
- No path traversal, SSRF, injection vulnerabilities
- Never expose internal details (stack traces, DB errors, paths) in prod errors
- Never log: passwords, tokens, secrets, PII

OWASP enforcement: see workspace-specific files

## Data Privacy & Compliance

- Identify & classify PII; handle with safeguards throughout lifecycle
- Collect only necessary data; obtain explicit consent
- Support right to deletion (GDPR/CCPA); enable purge on request
- Data retention policies: do not keep longer than necessary
- Exclude PII from logs, errors, monitoring dashboards
- Encrypt PII at rest and in transit
- Review third-party data sharing agreements before authorization

## Performance (Cross-Cutting)

- No N+1 queries; no unnecessary loops; profile hot paths
- Large data sets: use pagination, streaming, virtual scrolling
- No resource leaks: clean up connections, file handles, subscriptions
- Caching: define clear invalidation (TTL, event-based, write-through)
- Lazy loading: defer expensive operations until needed
- SLAs/SLOs: measure latency, throughput, error rate; alert on breaches
- Load tests: validate system handles expected traffic before release
- Bundle size: compress, tree-shake, code-split

## Accessibility (a11y)

- Semantic HTML (`nav`, `main`, `button`); avoid `div`/`span` soup
- Meaningful `alt` text for images (decorative: `alt=""`)
- Keyboard-navigable interactive elements; no mouse-only interactions
- Manage focus: set on route changes, modals, dynamic content
- Color contrast: WCAG 2.1 AA (4.5:1 text, 3:1 large text)
- ARIA only when semantic HTML insufficient; prefer native elements
- Screen reader testing (VoiceOver, NVDA) in dev workflow
- Form inputs: associated `<label>` (never rely on placeholder alone)

## Internationalization (i18n)

- No hardcoded strings; extract to translation files or i18n keys
- Locale-aware formatting: dates, numbers, currencies, units
- RTL support: use logical CSS (`margin-inline-start` over `margin-left`)
- UTF-8 encoding (never ASCII)
- Pluralization: handle language-specific plural forms
- Text expansion: allow 30–50% longer translations; avoid fixed-width text layouts
- Timestamps: store/transmit UTC; convert to local TZ only at display

## Deployment (Cross-Cutting)

- 12-Factor App: env vars for config, stateless processes, disposable containers, port binding
- IaC: all infrastructure in version-controlled templates (Terraform, Bicep, CloudFormation)
- GitOps: deployments triggered by merges, not manual steps
- Migrations: safe, reversible, run separately from app deploy
- Feature flags: use for risky rollouts; decouple deployment from release
- Logging & monitoring: add for new code paths
- Rollback plan: consider for every deployment
- Parity: dev/staging/prod as similar as possible

## Release Strategy

- Verify readiness: CI passes, docs updated, stakeholders notified
- Safe patterns: feature flags, blue-green, canary, rolling updates
- Never release Fridays/holidays without on-call plan
- Rollback: tested, documented, revert within minutes
- Monitor: error rate, latency, resource usage post-release
- Tag releases; maintain CHANGELOG linking changes

## Observability

- Structured logging (JSON): timestamp, level, service, request context
- Log levels: DEBUG (dev), INFO (normal), WARN (recoverable), ERROR (failures)
- Correlation IDs: propagate across service boundaries for tracing
- RED metrics: Rate, Errors, Duration (services)
- USE metrics: Utilization, Saturation, Errors (resources)
- Distributed tracing: OpenTelemetry across boundaries
- Actionable alerts: on symptoms (error spike), not causes; include runbooks
- Runbooks: documented, up-to-date operational procedures

## Dependency Management

- Justify every new dep; prefer stdlib or existing deps
- Pin versions in lockfiles; ensure reproducible builds
- Check licenses; ensure compatibility
- Vulnerability scans: Dependabot, Snyk, `pip-audit` on every CI run
- Review transitive deps; small deps can pull large attack surfaces
- Update regularly: small, frequent updates safer than large, infrequent

## Cost & Resource Efficiency

- Cloud resources proportional to needs; avoid over-provisioning
- Auto-scaling: scale down during low-traffic periods
- Clean up unused: orphaned disks, idle load balancers, stale environments
- Tag resources: team, project, environment for cost attribution
- Cost impact estimates in PRs that change infrastructure

## Developer Experience (DX)

- README: new contributors run locally in <5 minutes
- Single-command dev: `docker compose up` or equivalent
- Onboarding docs: architecture, key contacts, conventions
- PR templates: consistent descriptions, testing notes, checklists
- CONTRIBUTING.md: code style, branching, testing, submitting PRs

## Architecture & Design

- Fit existing architecture; no conflicting patterns
- Respect service boundaries; no cross-service access without justification
- No tight coupling; components replaceable
- API contracts: backward-compatible or properly versioned
- PRs: single logical change; flag multi-topic PRs
- ADRs: significant architectural decisions (context, decision, consequences)

## Documentation & Communication

- PR descriptions: explain *what* and *why*
- Public APIs/config changes: documented
- Breaking changes: clearly called out; update CHANGELOG, notify consumers
- CHANGELOG: link releases to changes
- Runbooks: deployments, incident response, data recovery
- Architecture diagrams: current, not original design

## AI Context & Token Efficiency

- Structured formats (lists, headers) save tokens; minimize prose
- Layered context: shared (root) → workspace-specific
- Use references, not duplication across docs
- Exclude auto-generated files from AI indexing
- Self-documenting code reduces AI context needs

## AI Persona Roles

| Context | Persona | Stack |
|---------|---------|-------|
| `backend/` | Senior Python/FastAPI Engineer | Python 3.12, FastAPI, SQLAlchemy, Pydantic, pytest, structlog |
| `frontend/` | Senior React/TypeScript Engineer | React 19, TypeScript, Vite, Vitest, Playwright |
| Root/.github/Docker | Senior DevOps/Platform Engineer | GitHub Actions, Docker, 12-Factor App, IaC |
| Cross-workspace | Senior Full-Stack Engineer | All domains |

Apply constraints silently. Follow workspace-specific rules.

## CI/CD (Continuous Delivery)

The `ai-review.yml` workflow runs on PRs to `main` (backend CI jobs run from the `backend/` directory):

1. Ruff lint + format check
2. Mypy type check
3. Bandit security scan
4. Pytest
5. Requests code review automatically
6. Posts a summary comment

All checks (1–4) are required to pass before merge. Every commit that passes CI must be potentially deployable. Review guidelines are in `.github/copilot-review-instructions.md`.
