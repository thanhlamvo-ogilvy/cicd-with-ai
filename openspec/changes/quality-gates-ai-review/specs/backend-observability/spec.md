# Backend Observability - Delta

## MODIFIED Requirements

### Requirement: Structured logging with structlog (enforced by AI review)
All backend logging MUST use `structlog.get_logger(__name__)`. Direct use of `print()` or stdlib `logging` is forbidden and MUST be flagged by AI PR review.

#### Scenario: Logger instantiation
- **WHEN** a module needs to log
- **THEN** it MUST use `structlog.get_logger(__name__)`

#### Scenario: AI detects print() or stdlib logging
- **WHEN** a PR contains `print()` or `import logging` + `logging.getLogger()`
- **THEN** the AI PR agent MUST comment requesting replacement with structlog

#### Scenario: Stdlib logging flagged
- **WHEN** code uses the stdlib `logging` module
- **THEN** the AI MUST suggest refactoring to structlog

### Requirement: No sensitive data in logs (enforced by AI review with AI provider specific rules)
Logs MUST NOT contain passwords, tokens, secrets, API keys, or PII. AI provider API calls MUST NOT log request/response bodies. The AI PR agent MUST specifically check for logging of AI provider interactions.

#### Scenario: AI provider call logging
- **WHEN** an AI provider API call is logged
- **THEN** the log MUST include only provider name, model, token count, and latency — never request/response bodies

#### Scenario: AI detects chat message logging
- **WHEN** a PR logs AI provider request/response bodies (e.g., `log.info(f"response: {response.choices[0].message.content}")`)
- **THEN** the AI PR agent MUST request changes with guidance: "Do not log AI provider request/response bodies; log only metadata (provider, model, tokens, latency)"

#### Scenario: User message content not logged
- **WHEN** user-provided messages or chat content are processed
- **THEN** logs MUST NOT include the message content; only log metadata (message ID, timestamp, result)

