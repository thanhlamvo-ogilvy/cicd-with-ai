# Backend Observability

> Structured logging, correlation IDs, log levels, and health check requirements for the backend.

## Logging

- ALL logging MUST use `structlog.get_logger(__name__)` — `print()` and stdlib `logging` are forbidden
- Log entries MUST use structured context binding, not string formatting:
  - ✅ `log.info("item_created", item_id=item.id)`
  - ❌ `log.info(f"item created: {item.id}")`
- Log levels:
  - `info` — normal business events (item created, request processed)
  - `warning` — recoverable issues
  - `error` — failures, with structured context

## Correlation IDs

- ALL log entries MUST include a correlation/request ID
- Middleware MUST inject a request ID and propagate it to all log entries within that request

## Sensitive Data in Logs

- Logs MUST NEVER contain passwords, tokens, API keys, or PII
- AI provider API calls MUST log only: `provider`, `model`, `token_count`, `latency` — NEVER request/response bodies

## Health Check

- The system MUST expose a health check endpoint at `GET /health` returning `200` with database connectivity status
