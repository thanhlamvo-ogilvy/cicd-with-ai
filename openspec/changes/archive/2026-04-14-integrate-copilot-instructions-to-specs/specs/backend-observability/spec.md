## ADDED Requirements

### Requirement: Structured logging with structlog
All backend logging MUST use `structlog.get_logger(__name__)`. Direct use of `print()` or stdlib `logging` is forbidden.

#### Scenario: Logger instantiation
- **WHEN** a module needs to log
- **THEN** it MUST use `structlog.get_logger(__name__)`

### Requirement: Structured context binding
Log entries MUST use structured context binding, not string formatting.

#### Scenario: Structured log entry
- **WHEN** a business event is logged
- **THEN** it MUST use `log.info("event_name", key=value)` format — not `log.info(f"event: {value}")`

### Requirement: Correct log levels
Log levels MUST follow: `info` for business events, `warning` for recoverable issues, `error` for failures.

#### Scenario: Business event logged at info level
- **WHEN** a normal business operation completes (e.g., item created)
- **THEN** it MUST be logged at `info` level

#### Scenario: Failure logged at error level
- **WHEN** an operation fails
- **THEN** it MUST be logged at `error` level with structured context

### Requirement: Correlation IDs in log entries
All log entries MUST include a correlation/request ID. Middleware SHALL inject request IDs.

#### Scenario: Request ID propagation
- **WHEN** an API request is processed
- **THEN** all log entries for that request MUST include the same correlation ID

### Requirement: Health check endpoint
The system SHALL expose a health check endpoint at `/health` with dependency checks (database connectivity).

#### Scenario: Health endpoint returns status
- **WHEN** a GET request is made to `/health`
- **THEN** it MUST return a 200 response with database connectivity status

### Requirement: No sensitive data in logs
Logs MUST NOT contain passwords, tokens, API keys, or PII. AI provider API calls MUST NOT log request/response bodies.

#### Scenario: AI provider call logging
- **WHEN** an AI provider API call is logged
- **THEN** the log MUST include only provider name, model, token count, and latency — never request/response bodies
