# Shared Error Handling

> Cross-cutting error handling and resilience patterns for all workspaces.

## Exception Handling

- MUST handle specific exception types — bare `except:` (Python) and untyped `catch` (TypeScript) are forbidden
- NEVER swallow errors silently — every caught error MUST be logged, re-raised, or explicitly recovered from; empty catch blocks are forbidden

## Retries & Timeouts

- Retry logic MUST use exponential backoff with jitter — tight fixed-interval loops are forbidden
- ALL network, database, and external service calls MUST have explicit timeouts — unbounded waits are forbidden

## Resilience

- Services MUST degrade gracefully when dependencies are unavailable — return cached data or a meaningful fallback response; never hang or crash

## Backend: Domain Exceptions → HTTP Errors

- Services MUST raise domain-specific exceptions (e.g., `ItemNotFoundError`)
- Route handlers MUST catch domain exceptions and map them to the appropriate `HTTPException` (e.g., 404)

### Requirement: Domain exception naming convention

All domain-specific exception classes MUST follow PEP 8 naming: class names SHALL end with the `Error` suffix (e.g., `AppError`, `ConversationNotFoundError`). The `Exception` suffix is forbidden for custom domain exceptions. Ruff N818 enforces this convention.

#### Scenario: Exception class name ends with Error
- **WHEN** a new domain exception is defined
- **THEN** its class name MUST end with `Error` (e.g., `class ItemNotFoundError(AppError)`)

#### Scenario: Ruff N818 catches wrong naming
- **WHEN** an exception class is named with a suffix other than `Error` (e.g., `AppException`, `ItemNotFoundExc`)
- **THEN** Ruff rule N818 MUST flag it and CI MUST fail

#### Scenario: Existing usages updated on rename
- **WHEN** an exception class is renamed to comply with the `Error` suffix convention
- **THEN** all `except`, `raise`, and `import` usages across the codebase MUST be updated to the new name
