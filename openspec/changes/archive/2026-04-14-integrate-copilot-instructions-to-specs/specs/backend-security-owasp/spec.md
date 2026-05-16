## ADDED Requirements

### Requirement: SQL injection prevention via ORM
All SQL queries MUST use SQLAlchemy ORM/Core with bound parameters. String interpolation (f-strings, `.format()`) in SQL is forbidden.

#### Scenario: SQL query uses parameterized statements
- **WHEN** a database query is constructed
- **THEN** it MUST use SQLAlchemy ORM/Core methods — never f-strings or string concatenation

#### Scenario: Code review catches SQL interpolation
- **WHEN** a PR contains SQL built with f-strings or `.format()`
- **THEN** the review MUST reject the change

### Requirement: Input validation through Pydantic schemas
All user input MUST be validated through Pydantic schemas. Raw dicts or `**kwargs` from request data are forbidden.

#### Scenario: Endpoint accepts Pydantic model
- **WHEN** an endpoint accepts a request body
- **THEN** the parameter type MUST be a Pydantic model, not `dict` or raw JSON

### Requirement: Password hashing with bcrypt
Passwords MUST be hashed with bcrypt via `passlib`. Plain-text password storage is forbidden.

#### Scenario: Password stored as hash
- **WHEN** a user password is stored
- **THEN** it MUST be hashed with bcrypt — never stored in plaintext

### Requirement: Secrets from environment configuration
JWT secrets and API keys MUST come from `settings` (pydantic-settings loaded from `.env`). Hardcoded secrets are forbidden.

#### Scenario: Secret not hardcoded
- **WHEN** a secret (JWT key, API key) is used in code
- **THEN** it MUST be loaded from `settings` via environment variables

### Requirement: No dynamic code execution
`eval()`, `exec()`, and dynamic code execution are forbidden in all application code.

#### Scenario: Bandit catches eval/exec
- **WHEN** code contains `eval()` or `exec()`
- **THEN** bandit MUST flag it and CI MUST fail

### Requirement: No sensitive data in error responses
Error responses MUST NOT expose internal details (stack traces, database errors, file paths) in production.

#### Scenario: Production error hides internals
- **WHEN** an unhandled exception occurs in production
- **THEN** the error response MUST return `{"detail": "Internal server error"}` without stack traces or system paths

### Requirement: No sensitive data in logs
Logs MUST NOT contain passwords, tokens, secrets, API keys, or PII.

#### Scenario: Log sanitization
- **WHEN** an error is logged
- **THEN** the log entry MUST NOT include passwords, tokens, API keys, or user PII
