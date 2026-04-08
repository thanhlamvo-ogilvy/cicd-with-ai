# Code Review Instructions

> Informed by: Clean Code (Uncle Bob), TDD (Kent Beck), Test Pyramid (Martin Fowler),
> Working Effectively with Legacy Code (Michael Feathers), Continuous Delivery (Farley & Humble),
> Google Engineering Practices, OWASP Top 10, WCAG 2.1, 12-Factor App

## Overview

This document defines the review guidelines for pull requests. This is a monorepo — apply backend rules to `backend/` files and frontend rules to `frontend/` files. Shared rules apply everywhere. Every checklist item is actionable: reviewers should verify each applicable item before approving.

---

## 1. Code Quality (Clean Code)

- [ ] **Intention-revealing names** — variables, functions, and classes clearly communicate purpose. No abbreviations or single-letter names outside tiny scopes.
- [ ] **Small functions that do one thing** — each function has a single responsibility. If a comment is needed to explain a block, it should be extracted into a named function.
- [ ] **DRY** — no unnecessary duplication. Shared logic extracted into utilities or services.
- [ ] **No dead code** — unused variables, imports, functions, and debugging artifacts removed.
- [ ] **No code smells** — methods ≤ 30 lines, nesting ≤ 3 levels, no god classes or feature envy.
- [ ] **Boy Scout Rule** — code left cleaner than found.
- [ ] **Readability** — code reads top-to-bottom without jumping around. Guard clauses preferred over deep nesting.
- [ ] **Consistent style** — formatting matches project linters (ruff for Python, ESLint/Prettier for TypeScript).

## 2. SOLID Principles

- [ ] **Single Responsibility** — each class/module/component has one reason to change. Routes handle HTTP; services handle business logic; components render UI.
- [ ] **Open/Closed** — code is extendable without modifying existing code. Use abstractions (`AIProvider` base class, React composition).
- [ ] **Liskov Substitution** — subtypes are interchangeable with base types. Any `AIProvider` implementation honours the `stream_chat` contract.
- [ ] **Interface Segregation** — no forced dependency on unused interfaces. Props interfaces are focused; large service classes are split.
- [ ] **Dependency Inversion** — depend on abstractions, not concretions. Dependencies injected (FastAPI `Depends`, React props/context) — never hardcoded.

## 3. Version Control

### Commit Standards

- [ ] Commit messages follow the structured release notes format defined in `.github/copilot-instructions.md`.
- [ ] Title line leads with the most newsworthy change; ends with `& more…` if multi-topic; no trailing period.
- [ ] Changes grouped under curly-brace headers (`{Backend}`, `{Frontend}`, `{CI}`, `{Docs}`, `{Dependencies}`).
- [ ] Bullet points start with present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); ≤ 120 chars; no periods.
- [ ] If no dependency updates, includes literal `(No dependency updates.)`.
- [ ] No co-authored-by trailers or generator attribution in commit messages.

> **NOTE:** This project uses a custom commit format — **not** Conventional Commits. See `.github/copilot-instructions.md` for the full specification.

### Branching Strategy

- [ ] No direct commits to `main` — all changes via feature branch + PR.
- [ ] PR contains a single logical change — flag PRs that bundle unrelated changes.
- [ ] Branch name is descriptive (`feat/add-login`, `fix/null-avatar`).
- [ ] Every commit is potentially deployable (Continuous Delivery).

## 4. Testability & Testing

### Design for Testability

- [ ] New code has seams for testing — dependencies are injectable, not hardcoded.
- [ ] Side effects (I/O, network, time) are isolated behind abstractions that can be mocked.
- [ ] Pure functions preferred where possible — easier to test deterministically.

### TDD Compliance

- [ ] Tests accompany new features — no feature code merged without corresponding tests.
- [ ] Tests written for bug fixes that reproduce the bug before the fix.
- [ ] Test names describe the behaviour being verified, not implementation details.

### Test Pyramid

- [ ] Unit tests form the base — fast, isolated, high coverage.
- [ ] Integration tests verify component interactions (API ↔ DB, frontend ↔ API).
- [ ] E2E tests used sparingly for critical user flows only.
- [ ] No test duplication across pyramid levels.

### The Beyoncé Rule

- [ ] "If you liked it, you should have put a test on it." — any behaviour the team relies on must have a test. If it breaks and there's no test, it's the author's fault.

### Backend Testing

- [ ] Every new endpoint has at least one positive and one negative test.
- [ ] Tests use async `httpx.AsyncClient` with `ASGITransport`.
- [ ] Fixtures clean up database state after each test.
- [ ] No `pytest.mark.skip` without an explanation.
- [ ] Edge cases tested: empty inputs, missing fields, invalid types, boundary values.

### Frontend Testing

- [ ] Components have unit tests for rendering and user interactions.
- [ ] Custom hooks tested in isolation with `renderHook`.
- [ ] API service functions tested with mocked fetch/responses.
- [ ] No snapshot tests unless explicitly justified — prefer assertion-based tests.

## 5. Error Handling & Resilience

### Backend Error Handling

- [ ] Services define domain-specific exceptions — routes map them to `HTTPException`.
- [ ] All error responses use `{"detail": "..."}` shape.
- [ ] Use `structlog` with structured context — not `print()` or string formatting.
- [ ] Errors never swallowed silently — every `except` block logs or re-raises.
- [ ] `HTTPException` used only at the API layer; business logic raises plain Python exceptions.

### Frontend Error Handling

- [ ] All API calls go through `src/services/api.ts` — no inline `fetch`.
- [ ] `response.ok` checked before parsing response body.
- [ ] User-friendly error messages displayed — never raw error objects in UI.
- [ ] Async operations wrapped in `try/catch`.
- [ ] Error boundaries used for component tree crash isolation.

### Resilience Patterns

- [ ] External service calls have timeouts configured.
- [ ] Retry logic uses exponential backoff with jitter — no tight retry loops.
- [ ] Circuit breaker pattern considered for frequently failing dependencies.
- [ ] Graceful degradation — features degrade rather than crash when dependencies are unavailable.
- [ ] No race conditions or concurrency issues — especially in async code.

## 6. API Design

- [ ] RESTful conventions followed — proper HTTP verbs, plural resource nouns, correct status codes.
- [ ] API versioning strategy in place for breaking changes (`/v1/`, `/v2/`).
- [ ] Pagination implemented for list endpoints — never unbounded result sets.
- [ ] Request/response schemas documented and validated.
- [ ] Idempotent operations where appropriate (PUT, DELETE).
- [ ] Consistent error response format across all endpoints.

### Backend API (FastAPI)

- [ ] `response_model` set on every endpoint.
- [ ] `status_code=201` for POST creation, `status_code=204` for DELETE (no body).
- [ ] `Annotated` used for dependency injection.
- [ ] Routes grouped into `APIRouter` instances.
- [ ] Parameters validated with `Field` constraints or `Query`/`Path` helpers.
- [ ] Request bodies validated with Pydantic models — no raw `dict` parsing.

## 7. Database & Data Integrity

- [ ] Migrations are safe and reversible — no destructive changes without a migration plan.
- [ ] Indexes added for columns used in WHERE, JOIN, and ORDER BY clauses.
- [ ] Foreign keys and constraints enforce referential integrity at the DB level.
- [ ] Transactions used for multi-step operations — no partial writes on failure.
- [ ] Database sessions come from the `get_db` dependency — never instantiated manually.
- [ ] Sensitive data encrypted at rest where required.
- [ ] No raw SQL concatenation — use parameterised queries or ORM exclusively.
- [ ] Schema changes are backward-compatible with running application code (expand-contract pattern).

## 8. Security (OWASP)

- [ ] No hardcoded secrets, API keys, passwords, or tokens — load from environment variables.
- [ ] User input validated and sanitised before use — both client and server side.
- [ ] Authentication/authorisation checks in place for protected endpoints.
- [ ] No `eval()`, `exec()`, or dynamic code execution in any language.
- [ ] CORS origins explicitly configured — never `*` in production.
- [ ] Dependencies free of known CVEs — flag any with vulnerabilities.
- [ ] No path traversal, SSRF, or injection risks (SQL, command, template).
- [ ] Internal details (stack traces, DB errors, file paths) never exposed in production error responses.
- [ ] Sensitive data (passwords, tokens, PII) never logged.
- [ ] HTTPS enforced for all external communication.
- [ ] Rate limiting applied to authentication and public-facing endpoints.
- [ ] CSRF protection enabled for state-changing requests where applicable.
- [ ] Security headers set: `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`.
- [ ] File uploads validated for type, size, and content — never trust client-provided MIME types.

## 9. Data Privacy & Compliance

- [ ] PII identified, documented, and minimised — only collect what's necessary.
- [ ] Data retention policies implemented — no indefinite storage of personal data.
- [ ] User consent obtained before collecting or processing personal data.
- [ ] Data deletion/anonymisation mechanisms exist for user data removal requests.
- [ ] Sensitive fields masked in logs and error messages.
- [ ] Data access audited — who accessed what and when.
- [ ] Third-party data sharing documented and compliant with privacy policies.

## 10. Performance

### Backend Performance

- [ ] No N+1 queries — use eager loading or batch queries.
- [ ] Large data sets handled with pagination or streaming — no unbounded queries.
- [ ] Caching used where appropriate (response caching, query result caching).
- [ ] No memory or resource leaks — connections, file handles, and sessions properly closed.
- [ ] Expensive operations offloaded to background tasks where possible.
- [ ] Database queries use `EXPLAIN` analysis for complex joins.

### Frontend Performance

- [ ] `useMemo` and `useCallback` applied where re-renders are expensive.
- [ ] Stable `key` props on list items — never array index if items can reorder.
- [ ] Lazy loading used for routes and heavy components (`React.lazy`, `Suspense`).
- [ ] Images optimised — proper sizing, formats, and lazy loading.
- [ ] Bundle size monitored — flag large new dependencies.
- [ ] No unnecessary re-renders — verify with React DevTools Profiler.

## 11. Accessibility (a11y)

- [ ] Semantic HTML used — `<button>`, `<nav>`, `<main>`, `<section>`, `<article>` over generic `<div>`/`<span>`.
- [ ] All interactive elements keyboard-accessible — focus order logical, no keyboard traps.
- [ ] Form inputs have associated `<label>` elements or `aria-label`/`aria-labelledby`.
- [ ] Images have meaningful `alt` text (or `alt=""` for decorative images).
- [ ] Colour contrast meets WCAG AA (4.5:1 for normal text, 3:1 for large text).
- [ ] Focus indicators visible — never `outline: none` without a custom alternative.
- [ ] ARIA roles, states, and properties used correctly — no ARIA is better than bad ARIA.
- [ ] Dynamic content changes announced to screen readers (`aria-live`, `role="status"`).
- [ ] Touch targets ≥ 44×44px for mobile interfaces.
- [ ] Error messages programmatically associated with form fields (`aria-describedby`).

## 12. Internationalization (i18n)

- [ ] No user-facing hardcoded strings — text extracted to translation files or constants.
- [ ] Date, time, number, and currency formatting uses locale-aware APIs (`Intl.*`).
- [ ] Timestamps stored and transmitted in UTC — converted to local time only at display.
- [ ] RTL (right-to-left) layout support considered — use logical CSS properties (`margin-inline-start` over `margin-left`).
- [ ] Text expansion accommodated — UI doesn't break with longer translated strings (~30-40% expansion).
- [ ] Pluralisation rules handled correctly — not just appending "s".
- [ ] Character encoding is UTF-8 throughout the stack.

## 13. Deployment & CI

### CI Pipeline

- [ ] All CI checks pass: ruff lint + format, mypy type check, bandit security scan, pytest.
- [ ] CI pipeline defined in `ai-review.yml` — changes to CI reviewed carefully.
- [ ] No CI steps skipped or disabled without documented justification.
- [ ] CI runs in under 10 minutes — flag slow tests or builds.

### 12-Factor Compliance

- [ ] Config stored in environment variables — not in code.
- [ ] Dependencies explicitly declared and isolated.
- [ ] Stateless processes — no local state between requests.
- [ ] Port binding — app is self-contained, binds its own port.
- [ ] Dev/prod parity — minimise gaps between environments.

### Infrastructure as Code / GitOps

- [ ] Infrastructure changes defined in code (Terraform, Docker Compose, etc.) — no manual config.
- [ ] `docker-compose.yml` changes reviewed for security and resource implications.
- [ ] Environment-specific config separated from application code.

## 14. Release Strategy

### Release Readiness

- [ ] Feature complete — all acceptance criteria met.
- [ ] No known critical bugs — all blockers resolved.
- [ ] Documentation updated (API docs, README, CHANGELOG).
- [ ] Stakeholders notified of breaking changes.

### Safe Release Patterns

- [ ] Feature flags used for risky rollouts — new features can be toggled without redeployment.
- [ ] Canary/blue-green deployment considered for high-risk changes.
- [ ] Database migrations run independently of application deployment (expand-contract).

### Rollback & Recovery

- [ ] Rollback plan documented — how to revert if something goes wrong.
- [ ] Database migrations are reversible.
- [ ] Monitoring and alerting in place to detect issues post-deploy.

## 15. Observability

### Structured Logging

- [ ] Use `structlog` (backend) with structured key-value context — not `print()` or string formatting.
- [ ] Log levels used correctly: `DEBUG` for dev, `INFO` for flow, `WARNING` for recoverable issues, `ERROR` for failures.
- [ ] Correlation IDs propagated across service boundaries for request tracing.
- [ ] No sensitive data in logs (passwords, tokens, PII).

### Metrics

- [ ] Key business and operational metrics exposed (request count, latency, error rate).
- [ ] Custom metrics added for new features where appropriate.
- [ ] Metrics follow naming conventions (e.g., `http_requests_total`, `db_query_duration_seconds`).

### Distributed Tracing

- [ ] Trace context propagated across API boundaries.
- [ ] Spans created for significant operations (DB queries, external calls).
- [ ] Trace IDs included in error responses for debugging.

### Alerting

- [ ] Alerts defined for new failure modes introduced by the change.
- [ ] Alert thresholds are actionable — no alert fatigue from noisy alerts.
- [ ] Runbook linked for each alert — responders know what to do.

## 16. Dependency Management

- [ ] New dependencies justified — no dependency added for trivial functionality.
- [ ] Versions pinned in `requirements.txt` / `package.json` — no floating ranges for production.
- [ ] Licence compatible with project licence — flag GPL/AGPL in permissive-licence projects.
- [ ] Vulnerability scanning run on new/updated dependencies (bandit, `npm audit`).
- [ ] Dependency tree checked for bloat — flag transitive dependencies that are excessively large.
- [ ] Lock files (`package-lock.json`, etc.) committed and reviewed for unexpected changes.

## 17. Cost & Resource Efficiency

- [ ] Resource usage proportional to workload — no over-provisioning.
- [ ] Auto-scaling configured where applicable — resources scale down when idle.
- [ ] Temporary resources (files, containers, cloud resources) cleaned up after use.
- [ ] Cost tags applied to cloud resources for allocation tracking.
- [ ] Expensive operations (large queries, file processing) bounded and monitored.
- [ ] Caching and CDN used to reduce redundant computation and bandwidth.

## 18. Developer Experience (DX)

- [ ] README updated if setup steps, commands, or config changed.
- [ ] Local development works with a single command (`docker compose up`, `npm run dev`).
- [ ] New environment variables documented in `.env.example` or README.
- [ ] Error messages helpful for developers — include context, not just "something went wrong".
- [ ] PR template followed — description explains *what* and *why*.
- [ ] Onboarding friction minimised — new contributors can get started quickly.

## 19. Architecture & Design

- [ ] Changes fit existing architecture — no patterns that conflict with the layered structure.
- [ ] No tight coupling or broken abstractions — components are replaceable.
- [ ] API contracts backward-compatible or properly versioned.
- [ ] ADR (Architecture Decision Record) created for significant architectural decisions.
- [ ] Service boundaries respected — no cross-service direct DB access.
- [ ] Shared code extracted to a common location — no copy-paste across workspaces.
- [ ] Verify all library APIs used actually exist — flag non-existent function signatures.
- [ ] Flag any code that duplicates existing utilities or services.

## 20. Documentation & Communication

- [ ] PR description explains *what* changed and *why*.
- [ ] Public APIs documented — endpoint, parameters, response shape, error codes.
- [ ] Breaking changes clearly called out in PR description and CHANGELOG.
- [ ] Config changes documented — new env vars, feature flags, permissions.
- [ ] Runbooks updated for operational changes.
- [ ] Inline code comments used only where *why* isn't obvious — no restating what the code does.

## 21. AI Context & Token Efficiency

### Context Files

- [ ] Root `.github/copilot-instructions.md` stays in sync with project-level conventions.
- [ ] Workspace-level `copilot-instructions.md` files updated when local patterns/APIs change.
- [ ] `.github/copilot-review-instructions.md` updated if review standards change.

### Token-Saving Structure

- [ ] Context files use structured formats (lists, headers) over verbose prose.
- [ ] Context layered (shared → workspace-specific) so AI loads only what it needs.
- [ ] References used instead of duplicating content across docs.

### AI Ignore Rules

- [ ] Large auto-generated files (lockfiles, migrations, bundles) excluded from AI indexing.
- [ ] Generated code, vendor directories, and data files not indexed.

### Discoverability

- [ ] Directory naming clear and consistent.
- [ ] Self-documenting code reduces need for AI to ask clarifying questions.

### Prompt Cache Friendliness

- [ ] Stable context (project info, conventions) separated from volatile content.
- [ ] No unnecessary churn in context files that would invalidate prompt caches.

---

## Backend-Specific Standards (`backend/`)

### Code Quality

- [ ] All functions and classes have type annotations (PEP 484 / PEP 526). Enforced by ruff `ANN` and mypy `--strict`.
- [ ] PEP 8 naming: `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants. Enforced by ruff `N`.
- [ ] `async`/`await` used consistently — never mix sync blocking calls inside async endpoints.
- [ ] Code simplified — no unnecessary `else` after `return`, no unnecessary assignments before `return`. Enforced by ruff `RET`/`SIM`.

### FastAPI Patterns

- [ ] `response_model` set on every endpoint.
- [ ] `status_code=201` for POST creation, `status_code=204` for DELETE (no body).
- [ ] `Annotated` used for dependency injection.
- [ ] Routes grouped into `APIRouter` instances.
- [ ] Parameters validated with `Field` constraints or `Query`/`Path` helpers.
- [ ] `HTTPException` raised only at the API layer; business logic raises plain Python exceptions.

### Schema Design

- [ ] Follow Base/Create/Update/Response schema pattern.
- [ ] `model_dump(exclude_unset=True)` used for partial updates.
- [ ] `Annotated` dependency aliases defined — no inline `Depends(get_db)` repetition.

### Dependency Injection

- [ ] Database sessions come from the `get_db` dependency — never instantiated manually.
- [ ] Dependencies injected via `Annotated[Type, Depends(...)]` — no direct instantiation in route functions.

---

## Frontend-Specific Standards (`frontend/`)

### TypeScript

- [ ] TypeScript strict mode respected — no `@ts-ignore` or `any` without justification.
- [ ] All functions have typed parameters and return values.
- [ ] `interface` used for object shapes, `type` for unions/intersections.
- [ ] `unknown` preferred over `any` — narrow with type guards.
- [ ] No unused locals or parameters (enforced by tsconfig).

### React Patterns

- [ ] Functional components only — no class components.
- [ ] Named exports for components (except `App.tsx`).
- [ ] One component per file, PascalCase file names matching component names.
- [ ] Props defined as `{ComponentName}Props` interface, destructured in signature.
- [ ] Components under ~150 lines — extract sub-components if larger.

### Hooks & State

- [ ] Custom hooks start with `use`, live in `src/hooks/`, return typed objects.
- [ ] Proper dependency arrays on `useEffect`, `useCallback`, `useMemo`.
- [ ] `useCallback` used for functions passed as props.
- [ ] No direct state mutation — always return new objects/arrays.

### Naming Conventions

- [ ] Files: PascalCase for components, camelCase for hooks/services/types.
- [ ] Event handlers: `handle*` in component, `on*` in props.
- [ ] Constants: `UPPER_SNAKE_CASE`.

---

## Quick Reference

| # | Section | Key Question |
|---|---------|-------------|
| 1 | Code Quality | Is the code clean, readable, and free of smells? |
| 2 | SOLID Principles | Does the design follow SOLID? |
| 3 | Version Control | Do commits and branches follow standards? |
| 4 | Testability & Testing | Are there sufficient, well-structured tests? |
| 5 | Error Handling | Are errors handled gracefully with resilience? |
| 6 | API Design | Is the API RESTful, consistent, and documented? |
| 7 | Database | Are migrations safe and queries efficient? |
| 8 | Security | Are OWASP Top 10 risks mitigated? |
| 9 | Data Privacy | Is PII protected and compliance maintained? |
| 10 | Performance | Are there N+1 queries, leaks, or unnecessary re-renders? |
| 11 | Accessibility | Does the UI meet WCAG AA standards? |
| 12 | Internationalization | Is the app locale-aware and translation-ready? |
| 13 | Deployment & CI | Do all CI checks pass? Is the build 12-factor? |
| 14 | Release Strategy | Is there a rollback plan and safe release pattern? |
| 15 | Observability | Are logging, metrics, tracing, and alerts in place? |
| 16 | Dependencies | Are deps justified, pinned, licensed, and secure? |
| 17 | Cost Efficiency | Are resources proportional and cleaned up? |
| 18 | Developer Experience | Can a new contributor get started easily? |
| 19 | Architecture | Does the change fit the existing architecture? |
| 20 | Documentation | Is the change documented and communicated? |
| 21 | AI Context | Are context files updated and token-efficient? |
