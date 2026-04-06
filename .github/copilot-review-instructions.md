# Copilot Code Review Instructions

## Overview
This document defines the review guidelines that GitHub Copilot should apply when reviewing pull requests in this repository.

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

## AI-Generated Code Risks

- Check for hallucinated library APIs or non-existent function signatures.
- Verify that auto-generated logic correctly handles edge cases (empty lists, `None` values, zero).
- Ensure AI-generated code follows the same conventions as the rest of the codebase.
- Flag any generated code that duplicates existing utilities or services.
- Confirm that AI-generated tests actually test the stated behaviour (not vacuous assertions).

---

## Code Quality

- All functions and classes must have type annotations (PEP 484 / PEP 526).
- Use `async`/`await` consistently – never mix sync blocking calls inside async endpoints.
- Raise `HTTPException` for all API-layer errors; business-layer should raise plain Python exceptions.
- Database sessions must be obtained via the `get_db` dependency – never instantiated manually in routes.
- Avoid `select *`; always select specific columns or use the ORM model.
- Ensure pagination parameters (`skip`/`limit`) are validated and have sensible defaults.
- Service functions should be unit-testable without a live database (mock the session).

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
