# Frontend Resilience

## Purpose

Define frontend error recovery and resilience patterns, covering retry strategies, loading states, error boundaries, offline detection, and SSE error handling.

## Requirements

### Requirement: Retry with exponential backoff
Failed API calls MUST be retried with exponential backoff. `AbortController` MUST be used to cancel on component unmount.

#### Scenario: API retry on failure
- **WHEN** an API call fails with a transient error
- **THEN** it MUST be retried with exponential backoff

#### Scenario: Cleanup on unmount
- **WHEN** a component unmounts during an active API call
- **THEN** the call MUST be cancelled via `AbortController` to prevent state updates on unmounted components

### Requirement: Loading states during async operations
All async operations MUST show loading states to the user.

#### Scenario: Fetch shows loading indicator
- **WHEN** an API call is in progress
- **THEN** the UI MUST display a loading indicator

### Requirement: User-friendly error states with retry
API errors MUST display user-friendly messages with retry actions. Raw error objects or stack traces MUST NOT be shown.

#### Scenario: Error with retry button
- **WHEN** an API call fails
- **THEN** the UI MUST show a user-friendly message (e.g., "Something went wrong. Try again.") with a retry button

### Requirement: React Error Boundaries
React Error Boundaries MUST be used to catch render errors in production and display fallback UIs.

#### Scenario: Render error caught
- **WHEN** a component throws during rendering
- **THEN** an Error Boundary MUST catch it and display a fallback UI — not a blank screen

### Requirement: Offline detection
The application MUST detect offline state using `navigator.onLine` and inform the user.

#### Scenario: Offline notification
- **WHEN** the browser goes offline
- **THEN** the UI MUST notify the user that they are offline

### Requirement: No empty catch blocks
All `catch` blocks MUST handle errors explicitly. Empty `catch {}` blocks are forbidden.

#### Scenario: Catch block with handling
- **WHEN** an error is caught in a try/catch
- **THEN** the catch block MUST log the error with context or handle it — never be empty

### Requirement: SSE error logging without PII
Malformed SSE data MUST be logged with event metadata (event type, stream position) — never the raw content (may contain PII).

#### Scenario: SSE parse error logging
- **WHEN** an SSE event fails to parse
- **THEN** the log MUST include event type and stream position — never the raw event content
