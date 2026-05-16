# Backend Security (OWASP) - Delta

## MODIFIED Requirements

### Requirement: SQL injection prevention via ORM
All SQL queries MUST use SQLAlchemy ORM/Core with bound parameters. String interpolation (f-strings, `.format()`) in SQL is forbidden and MUST be caught by Bandit in CI/CD.

#### Scenario: SQL query uses parameterized statements
- **WHEN** a database query is constructed
- **THEN** it MUST use SQLAlchemy ORM/Core methods — never f-strings or string concatenation

#### Scenario: Bandit catches SQL interpolation
- **WHEN** code contains f-strings in SQL (e.g., `f"SELECT * FROM users WHERE id={id}"`)
- **THEN** bandit MUST flag it with HIGH severity in CI and the PR MUST not merge

#### Scenario: Code review catches SQL interpolation
- **WHEN** a PR contains SQL built with f-strings or `.format()`
- **THEN** the AI PR agent MUST request changes with guidance on using SQLAlchemy ORM/Core

### Requirement: No dynamic code execution (enforced by Bandit)
`eval()`, `exec()`, and dynamic code execution are forbidden in all application code. Bandit MUST flag any violations with CRITICAL severity.

#### Scenario: Bandit catches eval/exec
- **WHEN** code contains `eval()` or `exec()`
- **THEN** bandit MUST flag it with CRITICAL severity in CI and the PR MUST not merge

#### Scenario: AI review reinforces dynamic code prohibition
- **WHEN** a PR is reviewed
- **THEN** the AI MUST comment if any dynamic code execution patterns are detected

### Requirement: Secrets from environment configuration (enforced by Bandit)
JWT secrets and API keys MUST come from `settings` (pydantic-settings loaded from `.env`). Hardcoded secrets are forbidden and MUST be flagged by Bandit.

#### Scenario: Bandit detects hardcoded secrets
- **WHEN** code contains hardcoded API keys, passwords, or JWT secrets
- **THEN** bandit MUST flag it with HIGH severity in CI and the PR MUST not merge

#### Scenario: Secret correctly loaded from environment
- **WHEN** a secret is used in code
- **THEN** it MUST be loaded from `settings` via environment variables, not hardcoded

### Requirement: No sensitive data in error responses (enforced by AI review)
Error responses MUST NOT expose internal details (stack traces, database errors, file paths) in production. The AI PR agent MUST check for this pattern.

#### Scenario: Production error hides internals
- **WHEN** an unhandled exception occurs in production
- **THEN** the error response MUST return `{"detail": "Internal server error"}` without stack traces or system paths

#### Scenario: AI detects internal details in error response
- **WHEN** a PR returns detailed error information (DB errors, file paths)
- **THEN** the AI MUST comment suggesting sanitization

### Requirement: No sensitive data in logs (enforced by AI and code review)
Logs MUST NOT contain passwords, tokens, secrets, API keys, or PII. AI PR agent MUST flag logging of user message content or authentication credentials.

#### Scenario: Log sanitization
- **WHEN** an error is logged
- **THEN** the log entry MUST NOT include passwords, tokens, API keys, or user PII

#### Scenario: AI detects PII logging
- **WHEN** a PR logs user-controlled content or authentication details (e.g., `log.info(f"message: {message.content}")`)
- **THEN** the AI MUST request changes with sanitization guidance

