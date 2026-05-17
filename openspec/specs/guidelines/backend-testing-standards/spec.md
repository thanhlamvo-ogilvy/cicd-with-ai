# Backend Testing Standards

> Testing patterns and requirements ensuring consistent test infrastructure, coverage, and quality.

## Test Infrastructure

- All API tests MUST use `httpx.AsyncClient` with `ASGITransport` — no real network calls
- Tests MUST use in-memory SQLite (`aiosqlite`) with tables auto-created before and dropped after each test — no external services required
- All `async def` test functions MUST be decorated with `@pytest.mark.asyncio`

## Test Structure

- Tests MUST follow the Arrange-Act-Assert (AAA) pattern
- Test names MUST follow `test_<action>_<expected_outcome>` (e.g., `test_create_item_returns_201_with_valid_payload`)
- Every new endpoint MUST have at least one positive (happy path) and one negative (error case) test

## Coverage & Quality

- Target: 80%+ code coverage (`pytest --cov=app`)
- Tests MUST be deterministic — no flaky dependencies on system time, network state, or execution order
- `@pytest.mark.skip` MUST include a `reason` parameter explaining why the test is skipped
