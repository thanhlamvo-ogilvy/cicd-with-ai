## MODIFIED Requirements

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
