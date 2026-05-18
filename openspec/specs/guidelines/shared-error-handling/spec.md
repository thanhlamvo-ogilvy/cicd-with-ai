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
