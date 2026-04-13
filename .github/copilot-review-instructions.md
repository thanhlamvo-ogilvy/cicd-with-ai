<!--
PR review checklist for code quality, standards compliance, and safety.
For detailed guidance on principles, see `.github/copilot-instructions.md` (shared), `backend/copilot-instructions.md`, `frontend/copilot-instructions.md` (workspace-specific).
-->

# Code Review Instructions

Review checklist for pull requests. Apply backend rules to `backend/`, frontend rules to `frontend/`, shared rules everywhere.

---

## 1. Code Quality

See: Clean Code principles in `.github/copilot-instructions.md`

- [ ] Intention-revealing names — variables, functions, classes clearly communicate purpose
- [ ] Small functions that do one thing (single responsibility)
- [ ] DRY — no unnecessary duplication
- [ ] No dead code — remove unused variables, imports, functions
- [ ] No code smells (methods ≤ 30 lines, nesting ≤ 3 levels)
- [ ] Boy Scout Rule — code left cleaner than found
- [ ] Readability — guard clauses preferred over nesting
- [ ] Consistent style — matches ruff (Python) / ESLint + Prettier (TypeScript)

## 2. SOLID Principles

See: SOLID definitions in `.github/copilot-instructions.md` (root), `backend/copilot-instructions.md`, `frontend/copilot-instructions.md` (workspace-specific)

- [ ] **SRP**: Single responsibility — routes/components handle one thing
- [ ] **OCP**: Open/Closed — use abstractions, composition; don't modify existing code
- [ ] **LSP**: Liskov Substitution — subtypes interchangeable with base types
- [ ] **ISP**: Interface Segregation — focused interfaces; split if >5-6 props/params
- [ ] **DIP**: Dependency Inversion — depend on abstractions; inject dependencies

## 3. Version Control

### Commit Standards

See: Full specification in `.github/copilot-instructions.md` (Git Commit Message Format section)

- [ ] Structured release notes format: title + grouped changes (`{Backend}`, `{Frontend}`, etc.) + bullets with action verbs
- [ ] Title is newsworthy; ends with `& more…` if multi-topic; no trailing period
- [ ] Bullets ≤ 120 chars; present-tense verbs (`Add`, `Fix`, `Refactor`); no periods
- [ ] If no dependency updates, includes literal `(No dependency updates.)`
- [ ] No co-authored-by or generator attribution

### Branching Strategy

- [ ] No direct commits to `main` — feature branch + PR
- [ ] PR single logical change — flag bundled unrelated changes
- [ ] Branch name descriptive (`feat/...`, `fix/...`)
- [ ] Every commit potentially deployable (Continuous Delivery)

## 4. Testability & Testing

See: TDD, Test Pyramid, Beyoncé Rule in workspace-specific instruction files

### Design for Testability

- [ ] Dependencies injectable; side effects isolated behind abstractions
- [ ] Pure functions preferred

### TDD & Coverage

- [ ] Tests accompany new features (no feature without test)
- [ ] Bug fix tests reproduce the bug first
- [ ] Test names describe behaviour
- [ ] Target coverage: 80%+

### Backend Testing

- [ ] Every new endpoint has positive + negative tests
- [ ] Tests use async `httpx.AsyncClient` with `ASGITransport`
- [ ] Fixtures clean up DB state after each test
- [ ] No `pytest.mark.skip` without explanation
- [ ] Edge cases tested: empty, missing fields, invalid types, boundaries

### Frontend Testing

- [ ] Components have unit tests for rendering + interactions
- [ ] Custom hooks tested in isolation with `renderHook`
- [ ] API service functions tested with mocked fetch
- [ ] Assertion-based tests preferred over snapshots

## 5. Error Handling & Resilience

See: Error Handling sections in workspace-specific instructions

### Backend

- [ ] Services define domain-specific exceptions; routes map to `HTTPException`
- [ ] Error responses use `{"detail": "..."}` shape
- [ ] Use `structlog` with context (not `print()` or string formatting)
- [ ] Errors never swallowed; every `except` logs or re-raises

### Frontend

- [ ] All API calls through `src/services/api.ts`
- [ ] `response.ok` checked before parsing
- [ ] User-friendly error messages in UI
- [ ] Async operations wrapped in try/catch
- [ ] Error boundaries for render error isolation

### Resilience Patterns

- [ ] External calls have timeouts
- [ ] Retry logic: exponential backoff with jitter
- [ ] Circuit breaker for frequently failing dependencies
- [ ] Graceful degradation — features degrade, don't crash
- [ ] No race conditions or concurrency issues

## 6. API Design

- [ ] RESTful conventions: proper verbs, plural nouns, correct status codes
- [ ] API versioning for breaking changes (`/v1/`, `/v2/`)
- [ ] Pagination on list endpoints (never unbounded results)
- [ ] Consistent error response format: `{"detail": "message"}`
- [ ] Idempotent operations (PUT, DELETE)

### Backend (FastAPI)

- [ ] `response_model` on every endpoint
- [ ] Status codes: 201 (POST creation), 204 (DELETE no body)
- [ ] `Annotated` for dependency injection
- [ ] Routes grouped in `APIRouter`
- [ ] Request bodies validated with Pydantic (no raw `dict`)

## 7. Database & Data Integrity

See: Database & Data Integrity in `backend/copilot-instructions.md`

- [ ] Migrations safe + reversible (no destructive changes without plan)
- [ ] Indexes on WHERE, JOIN, ORDER BY columns
- [ ] Foreign keys enforce referential integrity
- [ ] Transactions wrap multi-step operations
- [ ] DB sessions from `get_db` dependency
- [ ] Sensitive data encrypted at rest
- [ ] No raw SQL concatenation; parameterised queries or ORM only
- [ ] Schema changes backward-compatible (expand-contract)

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

- [ ] PII identified, documented, minimised
- [ ] Data retention policies enforced
- [ ] User consent obtained before collection
- [ ] Deletion/anonymisation mechanisms for requests
- [ ] Sensitive fields masked in logs/errors
- [ ] Data access audited
- [ ] Third-party sharing documented, compliant

## 10. Performance

See: Performance sections in workspace-specific instructions

### Backend

- [ ] No N+1 queries (use eager loading, batch queries)
- [ ] Large data sets paginated or streamed
- [ ] Caching where appropriate
- [ ] No resource leaks (connections, file handles closed)
- [ ] Expensive operations offloaded to background tasks
- [ ] Complex queries analysed with `EXPLAIN`

### Frontend

- [ ] `useMemo` + `useCallback` for expensive re-renders
- [ ] Stable `key` props on lists (never array index)
- [ ] Lazy loading for routes + heavy components
- [ ] Images optimised (sizing, formats, lazy loading)
- [ ] Bundle size monitored (flag large new deps)
- [ ] No unnecessary re-renders (verify with React DevTools)

## 11. Accessibility (a11y)

See: Accessibility section in `frontend/copilot-instructions.md`

- [ ] Semantic HTML (`<button>`, `<nav>`, `<main>`, not `<div>`)
- [ ] All interactive elements keyboard-accessible
- [ ] Form inputs have associated `<label>` or `aria-label`
- [ ] Images have meaningful `alt` text (or `alt=""` for decorative)
- [ ] Color contrast: WCAG AA (4.5:1 normal, 3:1 large text)
- [ ] Focus indicators visible
- [ ] ARIA used correctly (no ARIA better than bad ARIA)
- [ ] Dynamic content announced to screen readers
- [ ] Touch targets ≥ 44×44px
- [ ] Error messages tied to form fields (`aria-describedby`)

## 12. Internationalization (i18n)

See: i18n sections in workspace-specific instructions

- [ ] No hardcoded user-facing strings (externalize to translation files)
- [ ] Date/time/number/currency formatting locale-aware (`Intl.*`)
- [ ] Timestamps UTC; converted to local time at display
- [ ] RTL support considered (logical CSS props)
- [ ] Text expansion accommodated (~30-40% for translations)
- [ ] Pluralization handled correctly
- [ ] UTF-8 encoding throughout

## 13. Deployment & CI

### CI Pipeline

- [ ] All CI checks pass: ruff, mypy, bandit, pytest
- [ ] No CI steps skipped without documented justification
- [ ] Build completes in <10 min

### 12-Factor App

- [ ] Config in environment variables (not code)
- [ ] Dependencies explicitly declared + isolated
- [ ] Stateless processes
- [ ] Self-contained app, binds own port
- [ ] Dev/prod parity minimised

### Infrastructure as Code

- [ ] Infrastructure changes in code (Terraform, Docker, etc)
- [ ] `docker-compose.yml` changes reviewed
- [ ] Environment-specific config separated from app

## 14. Release Strategy

### Readiness

- [ ] Feature complete
- [ ] No critical bugs
- [ ] Docs updated (API docs, README, CHANGELOG)
- [ ] Stakeholders notified of breaking changes

### Safe Patterns

- [ ] Feature flags for risky rollouts
- [ ] Canary/blue-green deployment considered
- [ ] DB migrations independent of app deployment

### Rollback & Recovery

- [ ] Rollback plan documented
- [ ] DB migrations reversible
- [ ] Monitoring + alerting post-deploy

## 15. Observability

### Logging

- [ ] Structured logging (backend: `structlog`; key-value context)
- [ ] Log levels correct: DEBUG (dev), INFO (flow), WARNING (recoverable), ERROR (failures)
- [ ] Correlation IDs propagate across boundaries
- [ ] No sensitive data in logs

### Metrics & Tracing

- [ ] Business + operational metrics exposed
- [ ] Trace context propagated across APIs
- [ ] Spans created for significant operations

### Alerts

- [ ] Alerts for new failure modes
- [ ] Actionable thresholds (no fatigue)
- [ ] Runbook linked to each alert

## 16. Dependencies

- [ ] New deps justified (no trivial additions)
- [ ] Versions pinned in lock files
- [ ] Licenses compatible with project
- [ ] Vulnerability scanning on new/updated deps
- [ ] No transitive dependency bloat
- [ ] Lock files committed + reviewed

## 17. Cost & Efficiency

- [ ] Resource usage proportional to workload
- [ ] Auto-scaling configured (resources scale down idle)
- [ ] Temp resources cleaned up
- [ ] Cost tags applied to cloud resources
- [ ] Expensive operations bounded + monitored
- [ ] Caching + CDN reduce redundancy

## 18. Developer Experience (DX)

- [ ] README updated (setup, config changes)
- [ ] Local dev works with one command (`docker compose up`)
- [ ] New env vars documented
- [ ] Error messages helpful (context, not just "something wrong")
- [ ] PR template followed (what + why)
- [ ] Onboarding friction minimised

## 19. Architecture & Design

See: Architecture sections in workspace-specific instructions

- [ ] Changes fit existing architecture
- [ ] No tight coupling or broken abstractions
- [ ] API contracts backward-compatible or versioned
- [ ] ADR created for significant decisions
- [ ] Service boundaries respected
- [ ] Shared code in common location
- [ ] Verify APIs used exist (no non-existent signatures)
- [ ] No code duplication across utilities/services

## 20. Documentation & Communication

- [ ] PR description explains what + why
- [ ] Public APIs documented (endpoint, params, response, errors)
- [ ] Breaking changes called out (PR + CHANGELOG)
- [ ] Config changes documented (new env vars, feature flags, perms)
- [ ] Runbooks updated (operational changes)
- [ ] Inline comments explain *why*, not *what*

## 21. AI Context & Token Efficiency

- [ ] Root `.github/copilot-instructions.md` in sync with conventions
- [ ] Workspace `copilot-instructions.md` updated with pattern/API changes
- [ ] Structured formats (lists, headers) over wordy prose
- [ ] References used, not duplication
- [ ] Auto-generated files excluded from indexing
- [ ] Self-documenting code reduces AI context needs

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
