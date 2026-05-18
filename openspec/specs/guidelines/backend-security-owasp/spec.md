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

### Requirement: Secrets from environment configuration

JWT secrets and API keys MUST come from `settings` (pydantic-settings loaded from `.env`). Hardcoded secrets and insecure default values are forbidden. If a required secret is absent from the environment, the application MUST fail to start with a descriptive error message.

#### Scenario: Secret not hardcoded
- **WHEN** a secret (JWT key, API key) is used in code
- **THEN** it MUST be loaded from `settings` via environment variables — never hardcoded in source

#### Scenario: Missing secret causes startup failure
- **WHEN** a required secret (e.g., `SECRET_KEY`) is not set in the environment
- **THEN** the application MUST raise a `ValueError` at startup with a message identifying the missing variable

#### Scenario: Insecure default rejected by linter
- **WHEN** a settings field is defined with a default value that matches a known insecure pattern (e.g., `"change-me"`, `"secret"`)
- **THEN** Ruff S105 MUST flag it and CI MUST fail

## Dynamic Code Execution

- `eval()`, `exec()`, and all dynamic code execution are forbidden — Bandit will catch and CI will fail

## Error Responses

- Production error responses MUST NOT expose stack traces, database errors, or internal file paths
- Unhandled exceptions in production MUST return `{"detail": "Internal server error"}`

## Logs

- Logs MUST NOT contain passwords, tokens, API keys, or PII — see also [Backend Observability](../backend-observability/spec.md)
