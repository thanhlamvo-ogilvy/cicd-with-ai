# Backend Security (OWASP)

> OWASP-aligned security requirements covering SQL injection, input validation, secret management, and sensitive data protection.

## SQL Injection Prevention

- ALL database queries MUST use SQLAlchemy ORM/Core with bound parameters
- String interpolation in SQL (f-strings, `.format()`, concatenation) is forbidden — code review MUST reject it

## Input Validation

- All user input MUST be validated through Pydantic schemas
- Raw `dict` or `**kwargs` from request data are forbidden — endpoint parameters MUST be typed Pydantic models

## Password & Secret Handling

- Passwords MUST be hashed with bcrypt via `passlib` — plain-text password storage is forbidden
- JWT secrets and API keys MUST be loaded from `settings` (pydantic-settings via `.env`) — hardcoded secrets are forbidden

## Dynamic Code Execution

- `eval()`, `exec()`, and all dynamic code execution are forbidden — Bandit will catch and CI will fail

## Error Responses

- Production error responses MUST NOT expose stack traces, database errors, or internal file paths
- Unhandled exceptions in production MUST return `{"detail": "Internal server error"}`

## Logs

- Logs MUST NOT contain passwords, tokens, API keys, or PII — see also [Backend Observability](../backend-observability/spec.md)
