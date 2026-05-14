# Backend Testing Standards

## Purpose

Define testing patterns and requirements for the backend workspace, ensuring consistent test infrastructure, coverage targets, and quality standards across all backend tests.

## Requirements

### Requirement: Async test client with ASGITransport
All backend API tests SHALL use `httpx.AsyncClient` with `ASGITransport` — no real network calls.

#### Scenario: API test uses async client
- **WHEN** a test exercises an API endpoint
- **THEN** it MUST use the `client` fixture backed by `httpx.AsyncClient` with `ASGITransport`

### Requirement: In-memory SQLite for tests
Tests SHALL use in-memory SQLite (`aiosqlite`) with auto-created/dropped tables per test. No external services required.

#### Scenario: Test database isolation
- **WHEN** a test runs
- **THEN** it MUST use a fresh in-memory SQLite database with tables created before and dropped after the test

### Requirement: Async test marking
All async tests SHALL be decorated with `@pytest.mark.asyncio`.

#### Scenario: Async test marker
- **WHEN** a test function is `async def`
- **THEN** it MUST have the `@pytest.mark.asyncio` decorator

### Requirement: TDD compliance with AAA pattern
Tests SHALL follow the Arrange-Act-Assert pattern. Test names MUST describe the behavior and expected outcome.

#### Scenario: Test naming convention
- **WHEN** a new test is written
- **THEN** its name MUST follow the pattern `test_<action>_<expected_outcome>` (e.g., `test_create_item_returns_201_with_valid_payload`)

### Requirement: Positive and negative test coverage
Every new endpoint MUST have at least one positive test case (happy path) and one negative test case (error case).

#### Scenario: New endpoint test coverage
- **WHEN** a new API endpoint is added
- **THEN** the PR MUST include at least one test for a successful response and one test for an error response

### Requirement: Coverage target
Test suite SHALL target 80%+ code coverage.

#### Scenario: Coverage threshold
- **WHEN** `pytest --cov=app` is run
- **THEN** overall coverage MUST be at least 80%

### Requirement: No skipped tests without justification
Tests MUST NOT use `pytest.mark.skip` without a comment explaining why.

#### Scenario: Skip marker requires comment
- **WHEN** a test is marked with `@pytest.mark.skip`
- **THEN** it MUST include a `reason` parameter explaining why it is skipped

### Requirement: Deterministic tests
Tests MUST be deterministic — no flaky dependencies on time, network, or execution order.

#### Scenario: No external dependencies in unit tests
- **WHEN** a unit test runs
- **THEN** it MUST NOT make real network calls, depend on system time, or rely on test execution order
