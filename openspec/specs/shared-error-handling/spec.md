# Shared Error Handling

## Purpose

Define cross-cutting error handling and resilience patterns applicable to both backend and frontend workspaces, covering exception specificity, retry strategies, timeouts, and graceful degradation.

## Requirements

### Requirement: Specific exception handling
All `except`/`catch` blocks MUST handle specific error types. Bare `except:` and bare `catch` are forbidden.

#### Scenario: No bare except in Python
- **WHEN** an exception is caught in Python code
- **THEN** it MUST specify the exception type (e.g., `except ValueError:`) — never bare `except:`

#### Scenario: No bare catch in TypeScript
- **WHEN** an error is caught in TypeScript code
- **THEN** the catch block MUST handle specific error types or narrow with `instanceof`

### Requirement: No silent error swallowing
Caught errors MUST be logged, propagated, or handled explicitly. Empty catch blocks are forbidden.

#### Scenario: Catch block handles error
- **WHEN** an exception is caught
- **THEN** the catch block MUST log the error, re-raise it, or handle it with explicit recovery logic

### Requirement: Exponential backoff for retries
Retry logic MUST use exponential backoff with jitter. Tight retry loops are forbidden.

#### Scenario: External call retry with backoff
- **WHEN** a retryable external call fails
- **THEN** the retry MUST use exponential backoff with jitter — never fixed-interval tight loops

### Requirement: Explicit timeouts on external calls
All network, database, and external service calls MUST have explicit timeouts. Unbounded waits are forbidden.

#### Scenario: HTTP call with timeout
- **WHEN** an HTTP call is made to an external service
- **THEN** it MUST specify a timeout value

### Requirement: Graceful degradation
Services MUST degrade gracefully when dependencies are unavailable — use cached data or fallback behavior.

#### Scenario: Dependency unavailable
- **WHEN** an external dependency (API, database) is unavailable
- **THEN** the system MUST return a meaningful error or fallback response — never hang or crash

### Requirement: Domain exceptions mapped to HTTP errors
Backend services SHALL raise domain-specific exceptions. Routes MUST catch them and map to appropriate `HTTPException` responses.

#### Scenario: Service exception becomes HTTP error
- **WHEN** a service raises a domain exception (e.g., `ItemNotFoundError`)
- **THEN** the route handler MUST catch it and return the appropriate HTTP status (e.g., 404)
