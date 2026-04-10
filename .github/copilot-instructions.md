# Copilot Instructions

> Informed by: Clean Code, SOLID, TDD, Test Pyramid, Working Effectively with Legacy Code,
> Continuous Delivery, Google Engineering Practices, Release It!, OWASP Top 10, 12-Factor App,
> WCAG 2.1 AA, REST API Design, Site Reliability Engineering, Team Topologies

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

## Clean Code Principles (Uncle Bob)

These apply to **all code** in every language:

- **Intention-revealing names** — variables, functions, and classes must clearly communicate their purpose. No abbreviations or single-letter names outside tiny scopes.
- **Small functions that do one thing** — each function should have a single responsibility. If you need a comment to explain a block, extract it into a named function.
- **DRY (Don't Repeat Yourself)** — no unnecessary duplication. Extract shared logic into utilities or services.
- **No dead code** — remove unused variables, imports, functions, and debugging artifacts before committing.
- **No code smells** — long methods (>30 lines), deep nesting (>3 levels), god classes, and feature envy must be refactored.
- **Boy Scout Rule** — leave the code cleaner than you found it.

## SOLID Principles (Uncle Bob)

All code — backend and frontend — must follow SOLID:

- **S — Single Responsibility**: each class/module/component has one reason to change. A route handles HTTP, a service handles business logic, a component renders UI.
- **O — Open/Closed**: code should be extendable without modifying existing code. Use abstractions (e.g., `AIProvider` base class, React composition).
- **L — Liskov Substitution**: subtypes must be interchangeable with base types. Any `AIProvider` implementation must honour the `stream_chat` contract.
- **I — Interface Segregation**: no forced dependency on unused interfaces. Keep props interfaces focused; split large service classes.
- **D — Dependency Inversion**: depend on abstractions, not concretions. Inject dependencies (FastAPI `Depends`, React props/context) — never hardcode them.

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

- **Design for testability** — inject dependencies, isolate side effects, prefer pure functions.
- **TDD cycle** — Red → Green → Refactor. Write a failing test first, make it pass, then clean up.
- **Test Pyramid** — many unit tests (base), fewer integration tests (middle), minimal E2E tests (top).
- **Beyoncé Rule** — if you liked it, you should have put a test on it. Untested code is untrustworthy code.
- Edge cases must be handled: nulls, empty inputs, boundary values, zero.
- No race conditions or concurrency issues — especially in async code.
- Tests must be deterministic, isolated, and fast — no shared mutable state between tests.
- Mock external services at integration boundaries, not internal implementation details.

## Error Handling & Resilience

- No bare `catch` / `except` blocks — always handle specific error types or re-raise.
- Never swallow errors silently — log, propagate, or handle explicitly.
- Use circuit breakers for calls to external services to prevent cascade failures.
- Retries must use exponential backoff with jitter — never retry in a tight loop.
- Set explicit timeouts on all network calls, database queries, and external integrations.
- Use bulkhead patterns to isolate failures and prevent one bad component from taking down the system.
- Degrade gracefully — return cached data or a sensible fallback when a dependency is unavailable.
- Route unprocessable messages to dead letter queues for later inspection.

## API Design

- Follow RESTful conventions — use nouns for resources, HTTP verbs for actions, proper status codes.
- Version APIs explicitly (URL path `/v1/` or header) — never break existing clients silently.
- Validate request schemas at the boundary — reject malformed input early with clear error messages.
- Support pagination for all list endpoints (`limit`/`offset` or cursor-based).
- Implement rate limiting to protect services from abuse and ensure fair usage.
- Design mutating endpoints to be idempotent where possible — safe to retry on failure.
- Use a consistent error response format across all endpoints (e.g., `{ "error": { "code", "message", "details" } }`).
- Maintain OpenAPI/Swagger documentation — auto-generate from code where possible.

## Database & Data Integrity

- Migrations must be safe, reversible, and backward-compatible — no destructive changes without a migration plan.
- Add indexes for columns used in `WHERE`, `JOIN`, and `ORDER BY` — verify with query plans.
- Eliminate N+1 query patterns — use eager loading, joins, or batch fetching.
- Wrap multi-step mutations in transactions — ensure atomicity and rollback on failure.
- Understand and choose the right consistency model (strong vs. eventual) for each use case.
- Schema changes must not cause data loss — add columns as nullable, backfill, then enforce constraints.
- Encrypt sensitive data at rest and in transit — use application-level encryption for PII where appropriate.

## Security (Cross-Cutting)

- Never hardcode secrets, API keys, passwords, or tokens — load from environment variables or a secrets manager.
- Rotate secrets on a defined schedule and immediately on suspected compromise.
- User input must always be validated and sanitized before use — defend against OWASP Top 10 (injection, XSS, CSRF, SSRF, broken auth, etc.).
- Authentication/authorization checks must be in place for protected endpoints — follow least privilege principle.
- Never use `eval()`, `exec()`, or similar dynamic execution in any language.
- Set security headers: CORS (explicit origins, never `*` in production), CSP, HSTS, X-Content-Type-Options.
- Dependencies must be free of known vulnerabilities — scan before adding and on a regular schedule.
- No path traversal, SSRF, or injection vulnerabilities.
- Never expose internal details (stack traces, DB errors, file paths) in production error responses.
- Never log sensitive data: passwords, tokens, secrets, PII.
- Apply least privilege to service accounts, IAM roles, and database credentials.

## Data Privacy & Compliance

- Identify and classify PII — handle it with appropriate safeguards throughout the data lifecycle.
- Collect only necessary data and obtain explicit user consent where required.
- Support right to deletion (GDPR/CCPA) — ensure PII can be purged on request.
- Define and enforce data retention policies — do not keep data longer than necessary.
- Exclude PII from logs, error messages, and monitoring dashboards.
- Encrypt PII at rest and in transit — use field-level encryption where appropriate.
- Review third-party data sharing agreements — never send PII to external services without authorization.

## Performance (Cross-Cutting)

- No N+1 queries or unnecessary loops — profile and optimize hot paths.
- Large data sets must be handled efficiently (pagination, streaming, virtual scrolling).
- No memory or resource leaks — clean up connections, file handles, and subscriptions.
- Caching must be considered where appropriate — define clear invalidation strategies (TTL, event-based, write-through).
- Use lazy loading for non-critical resources — defer expensive operations until needed.
- Define SLAs/SLOs for critical paths — measure and alert on latency, throughput, and error rate.
- Run load tests before major releases — validate that the system handles expected traffic.
- Minimize bundle size and network payloads — compress, tree-shake, and code-split.

## Accessibility (a11y)

- Use semantic HTML elements (`nav`, `main`, `article`, `button`) — avoid `div`/`span` soup.
- Provide meaningful `alt` text for all images — decorative images use `alt=""`.
- All interactive elements must be keyboard-navigable — no mouse-only interactions.
- Manage focus correctly — set focus on route changes, modals, and dynamic content updates.
- Meet WCAG 2.1 AA color contrast ratios (4.5:1 for text, 3:1 for large text/UI components).
- Use ARIA attributes only when semantic HTML is insufficient — prefer native elements.
- Test with screen readers (VoiceOver, NVDA) as part of the development workflow.
- Every form input must have an associated `<label>` — never rely on placeholder text alone.

## Internationalization (i18n)

- No hardcoded user-facing strings — extract all text to translation files or i18n keys.
- Use locale-aware formatting for dates, numbers, currencies, and units.
- Support RTL (right-to-left) layouts — use logical CSS properties (`margin-inline-start` over `margin-left`).
- Encode all text as UTF-8 — never assume ASCII.
- Handle pluralization rules correctly — different languages have different plural forms.
- Allow for text expansion (translations can be 30–50% longer) — avoid fixed-width layouts for text.
- Store and transmit timestamps in UTC — convert to local timezone only at display time.

## Deployment (Cross-Cutting)

- Follow 12-Factor App principles — config in env vars, stateless processes, disposable containers, port binding.
- Infrastructure as Code (IaC) — all infrastructure must be defined in version-controlled templates (Terraform, Bicep, CloudFormation).
- Adopt GitOps — deployments triggered by merges to a deployment branch, not manual steps.
- Database migrations must be safe and reversible — run migrations separately from application deploys.
- Feature flags should be used for risky rollouts — decouple deployment from release.
- Logging and monitoring must be added for new code paths.
- Rollback plan must be considered for every deployment.
- Environments (dev, staging, prod) must be as similar as possible — minimize "works on my machine" issues.

## Release Strategy

- Verify release readiness — all CI checks pass, documentation updated, stakeholders notified.
- Use safe release patterns: feature flags, blue-green deployments, canary releases, or rolling updates.
- Never release on Fridays or before holidays without an on-call plan.
- Rollback procedures must be tested and documented — know how to revert within minutes.
- Monitor key metrics (error rate, latency, resource usage) closely after every release.
- Tag releases in git — maintain a CHANGELOG linking releases to their changes.

## Observability

- Use structured logging (JSON) — include timestamp, level, service name, and request context.
- Follow standard log levels: DEBUG for dev, INFO for normal operations, WARN for recoverable issues, ERROR for failures.
- Attach correlation IDs to every request — propagate across service boundaries for distributed tracing.
- Track RED metrics (Rate, Errors, Duration) for services and USE metrics (Utilization, Saturation, Errors) for resources.
- Implement distributed tracing (OpenTelemetry) — trace requests across service boundaries.
- Set up actionable alerts — alert on symptoms (error rate spike), not causes. Include runbook links in alert notifications.
- Maintain runbooks for common operational scenarios — keep them up to date.

## Dependency Management

- Justify every new dependency — prefer standard library or existing deps over adding new ones.
- Pin dependency versions in lockfiles — ensure reproducible builds across environments.
- Check licenses before adding dependencies — ensure compatibility with project licensing.
- Run vulnerability scans (Dependabot, Snyk, `pip-audit`) on every CI run.
- Review transitive dependencies — a small direct dep can pull in a large attack surface.
- Update dependencies regularly — small, frequent updates are safer than large, infrequent ones.

## Cost & Resource Efficiency

- Cloud resource usage must be proportional to actual needs — avoid over-provisioning.
- Use auto-scaling where possible — scale down during low-traffic periods.
- Clean up unused resources: orphaned disks, idle load balancers, unattached IPs, stale environments.
- Tag cloud resources with team, project, and environment for cost attribution.
- Include cost impact estimates in PRs that add or change infrastructure.

## Developer Experience (DX)

- README must enable a new contributor to run the project locally in under 5 minutes.
- Support single-command local development (`docker compose up`, `make dev`, or equivalent).
- New team member onboarding should be documented — link to architecture docs, key contacts, and conventions.
- Use PR templates to ensure consistent descriptions, testing notes, and review checklists.
- Maintain a CONTRIBUTING.md with guidelines for code style, branching, testing, and submitting PRs.

## Architecture & Design

- Changes must fit existing architecture — don't introduce patterns that conflict with the layered structure.
- Respect service boundaries — a change should not reach across service/module boundaries without justification.
- No tight coupling or broken abstractions — components should be replaceable.
- API contracts must be backward-compatible or properly versioned.
- PRs should contain a single logical change — flag PRs doing too many things.
- Create an ADR (Architecture Decision Record) for significant architectural decisions — record context, decision, and consequences.

## Documentation & Communication

- PR descriptions must explain *what* changed and *why*.
- Public APIs or config changes must be documented.
- Breaking changes must be clearly called out — update CHANGELOG and notify consumers.
- Maintain a CHANGELOG that links releases to their changes.
- Create runbooks for operational procedures — deployments, incident response, data recovery.
- Keep architecture diagrams up to date — they should reflect the current system, not the original design.

## AI Context & Token Efficiency

### Context Files
- Root `.github/copilot-instructions.md` must stay in sync with project-level conventions.
- Workspace-level `copilot-instructions.md` files updated when local patterns/APIs change.

### Token-Saving Structure
- Context files use structured formats (lists, headers) over verbose prose.
- Context is layered (shared → workspace-specific) so AI loads only what it needs.
- Use references instead of duplicating content across docs.

### AI Ignore Rules
- Large auto-generated files (lockfiles, migrations, bundles) should be excluded from AI indexing via `.gitignore` or ignore files.
- Generated code, vendor directories, and data files should not be indexed.

### Discoverability
- Directory naming must be clear and consistent.
- Self-documenting code reduces need for AI to ask clarifying questions.

### Prompt Cache Friendliness
- Stable context (project info, conventions) separated from volatile content.
- No unnecessary churn in context files that would invalidate prompt caches.

## AI Persona Roles

When generating or modifying code, the AI agent must adopt the persona matching the workspace context. Personas are activated based on the file path being edited — not announced in comments or output.

| Context | Persona | Expertise | Activates When |
|---------|---------|-----------|----------------|
| `backend/` | **Senior Python/FastAPI Engineer** | Python 3.12, async/await, SQLAlchemy 2.0, Pydantic v2, OWASP security, structlog, pytest | Editing files under `backend/` |
| `frontend/` | **Senior React/TypeScript Engineer** | React 19, TypeScript strict mode, Vite, accessibility (WCAG 2.1 AA), modern CSS, Vitest, Playwright | Editing files under `frontend/` |
| Root / CI / Docker | **Senior DevOps/Platform Engineer** | GitHub Actions, Docker, CI/CD pipelines, 12-Factor App, infrastructure-as-code, shell scripting | Editing root-level files, `.github/`, `docker-compose.yml`, `Dockerfile` |
| Cross-cutting | **Senior Full-Stack Engineer** | All of the above — used when a change spans multiple workspaces | Editing files in both `backend/` and `frontend/` in the same task |

Rules:
- Apply the persona's constraints silently — do not mention the role in generated code or comments.
- When a task spans workspaces, use the cross-cutting persona but still follow each workspace's specific rules.
- Persona expertise areas define the knowledge base for code review, suggestions, and error diagnosis.

## CI/CD (Continuous Delivery)

The `ai-review.yml` workflow runs on PRs to `main` (backend CI jobs run from the `backend/` directory):

1. Ruff lint + format check
2. Mypy type check
3. Bandit security scan
4. Pytest
5. Requests code review automatically
6. Posts a summary comment

All checks (1–4) are required to pass before merge. Every commit that passes CI must be potentially deployable. Review guidelines are in `.github/copilot-review-instructions.md`.
