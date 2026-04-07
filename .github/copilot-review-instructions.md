# Code Review Instructions

## Overview
This document defines the review guidelines for pull requests. This is a monorepo — apply backend rules to `backend/` files and frontend rules to `frontend/` files. Shared rules (git, security) apply everywhere.

---

## Security (All Code)

- Flag any hardcoded secrets, API keys, passwords, or tokens.
- Ensure CORS origins are explicitly configured — never `*` in production.
- No `eval()`, `exec()`, or dynamic execution in any language.
- No path traversal, SSRF, or injection risks.
- Flag dependencies with known CVEs.
- Never expose internal details (stack traces, DB errors) in error responses.
- Never log sensitive data (passwords, tokens, PII).

---

## Backend (`backend/`) — Python / FastAPI

### Code Quality

- All functions and classes must have type annotations (PEP 484 / PEP 526). Enforced by ruff `ANN` and mypy `--strict`.
- Follow PEP 8 naming: `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants. Enforced by ruff `N`.
- Use `async`/`await` consistently — never mix sync blocking calls inside async endpoints.
- Raise `HTTPException` for API-layer errors; business-layer should raise plain Python exceptions.
- Database sessions must come from the `get_db` dependency — never instantiated manually.
- Simplify code — avoid unnecessary `else` after `return`, unnecessary assignments before `return`. Enforced by ruff `RET`/`SIM`.
- Verify that all library APIs used actually exist — flag non-existent function signatures.
- Flag any code that duplicates existing utilities or services.

### FastAPI

- Use `response_model` on every endpoint.
- Return `status_code=201` for POST creation, `status_code=204` for DELETE (no body).
- Use `Annotated` for dependency injection.
- Group routes into `APIRouter` instances.
- Validate parameters with `Field` constraints or `Query`/`Path` helpers.

### Testing

- Every new endpoint: at least one positive and one negative test.
- Tests use async `httpx.AsyncClient` with `ASGITransport`.
- Fixtures must clean up database state after each test.
- No `pytest.mark.skip` without an explanation.

### Error Handling & Logging

- Services define domain-specific exceptions — routes map to `HTTPException`.
- All error responses use `{"detail": "..."}` shape.
- Use `structlog` with structured context — not `print()` or string formatting.

### Schema & Organisation

- Follow Base/Create/Update/Response schema pattern.
- Use `model_dump(exclude_unset=True)` for partial updates.
- Define `Annotated` dependency aliases — no inline `Depends(get_db)` repetition.

---

## Frontend (`frontend/`) — React / TypeScript

### Code Quality

- TypeScript strict mode must be respected — no `@ts-ignore` or `any` without justification.
- All functions must have typed parameters and return values.
- Use `interface` for object shapes, `type` for unions/intersections.
- Prefer `unknown` over `any` — narrow with type guards.
- No unused locals or parameters (enforced by tsconfig).

### React

- Functional components only — no class components.
- Named exports for components (except `App.tsx`).
- One component per file, PascalCase file names matching component names.
- Props defined as `{ComponentName}Props` interface, destructured in signature.
- Components under ~150 lines — extract sub-components if larger.

### Hooks & State

- Custom hooks start with `use`, live in `src/hooks/`, return typed objects.
- Proper dependency arrays on `useEffect`, `useCallback`, `useMemo`.
- Use `useCallback` for functions passed as props.
- No direct state mutation — always return new objects/arrays.

### API & Error Handling

- All API calls through `src/services/api.ts` — no inline `fetch`.
- Check `response.ok` before parsing.
- User-friendly error messages — never raw error objects in UI.
- Async operations wrapped in try/catch.

### Naming

- Files: PascalCase for components, camelCase for hooks/services/types.
- Event handlers: `handle*` in component, `on*` in props.
- Constants: UPPER_SNAKE_CASE.

### Accessibility & Performance

- Interactive elements must be keyboard-accessible — use semantic HTML.
- Form inputs need labels or `aria-label`.
- Stable `key` props on list items — never array index if items reorder.
- Memoize with `useMemo`/`useCallback` where appropriate.

---

## Git & PR Hygiene

- Commit messages must follow the structured release notes format in `.github/copilot-instructions.md`.
- Each PR should be one logical change — flag PRs that bundle unrelated changes.
- No co-authored-by trailers or generator attribution.
