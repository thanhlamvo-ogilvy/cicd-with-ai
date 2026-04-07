# Code Review Instructions

## Overview
This document defines the review guidelines to apply when reviewing pull requests in this repository.

---

## Security

- Flag any hardcoded secrets, API keys, passwords, or tokens.
- Ensure all user-supplied input is validated before use (use Pydantic schemas, not raw dicts).
- Verify SQL queries use parameterised statements (SQLAlchemy ORM/Core only – no raw string interpolation).
- Check that passwords are hashed with a strong algorithm (bcrypt via `passlib`).
- JWT tokens must use a strong secret loaded from environment variables, never hardcoded.
- Ensure CORS origins are explicitly configured and not set to `*` in production.
- Identify any path traversal, SSRF, or injection risks.
- Flag dependencies with known CVEs.

---

## Code Quality

- All functions and classes must have type annotations (PEP 484 / PEP 526). Enforced by ruff `ANN` rules and mypy `--strict`.
- Follow PEP 8 naming conventions: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants. Enforced by ruff `N` rules.
- Use `async`/`await` consistently – never mix sync blocking calls inside async endpoints.
- Raise `HTTPException` for all API-layer errors; business-layer should raise plain Python exceptions.
- Database sessions must be obtained via the `get_db` dependency – never instantiated manually in routes.
- Avoid `select *`; always select specific columns or use the ORM model.
- Ensure pagination parameters (`skip`/`limit`) are validated and have sensible defaults.
- Service functions should be unit-testable without a live database (mock the session).
- Simplify code when possible — avoid unnecessary `else` after `return`, unnecessary variable assignments before `return`. Enforced by ruff `RET` and `SIM` rules.
- Verify that all library APIs used actually exist — flag non-existent function signatures.
- Ensure logic correctly handles edge cases (empty lists, `None` values, zero).
- Flag any code that duplicates existing utilities or services.

---

## FastAPI Best Practices

- Use `response_model` on every endpoint to control serialisation.
- Return `status_code=201` for `POST` creation endpoints.
- Return `status_code=204` for `DELETE` endpoints (no body).
- Use `Annotated` for dependency injection when multiple endpoints share the same dependency.
- Group related routes into APIRouter instances, not directly on the `app` object.
- Use lifespan context managers (not deprecated `on_event`) for startup/shutdown logic.
- Validate path/query parameters with `Field` constraints in Pydantic models or `Query`/`Path` helpers.

---

## Testing

- Every new endpoint must have at least one positive and one negative test case.
- Tests should use the async `httpx.AsyncClient` with the `ASGITransport` (no real network calls).
- Test fixtures must clean up their database state after each test.
- Do not skip tests with `pytest.mark.skip` without a comment explaining why.

---

## Error Handling & Logging

- Services should define domain-specific exceptions — routes map them to `HTTPException`.
- Never let raw Python exceptions leak to the client. All error responses must use `{"detail": "..."}`.
- Never expose internal details (stack traces, DB errors) in production responses.
- Use `structlog` with structured context — not `print()` or string-formatted logging.
- Never log sensitive data (passwords, tokens, PII).

---

## Schema & Code Organisation

- Follow the Base/Create/Update/Response schema pattern for every resource.
- Use `model_dump(exclude_unset=True)` for partial updates.
- Define `Annotated` dependency aliases — do not repeat `Depends(get_db)` inline.
- Check existing services before writing new logic — flag duplicates.

---

## Git & PR Hygiene

- Commit messages must follow the structured release notes format defined in `copilot-instructions.md` — title line with primary change, curly-brace section headers, present-tense action verb bullets ≤ 120 chars, no trailing periods.
- Each PR should be one logical change. Flag PRs that bundle unrelated changes.
- No co-authored-by trailers or generator attribution in commit messages.
