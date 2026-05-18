## MODIFIED Requirements

### Requirement: Domain exception naming convention
All domain-specific exception classes MUST follow PEP 8 naming: class names SHALL end with the `Error` suffix (e.g., `AppError`, `ConversationNotFoundError`). The `Exception` suffix is forbidden for custom domain exceptions.

#### Scenario: Exception class name ends with Error
- **WHEN** a new domain exception is defined
- **THEN** its class name MUST end with `Error` (e.g., `class ItemNotFoundError(AppError)`)

#### Scenario: Ruff N818 catches wrong naming
- **WHEN** an exception class is named with a suffix other than `Error` (e.g., `AppException`, `ItemNotFoundExc`)
- **THEN** Ruff rule N818 MUST flag it and CI MUST fail

#### Scenario: Existing usages updated on rename
- **WHEN** an exception class is renamed to comply with the `Error` suffix convention
- **THEN** all `except`, `raise`, and `import` usages across the codebase MUST be updated to the new name
