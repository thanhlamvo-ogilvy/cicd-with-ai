## MODIFIED Requirements

### Requirement: Backend standards section
The quick-reference SHALL include a backend section covering: naming conventions, function size limits, type annotation requirements, async patterns, error handling patterns, FastAPI endpoint patterns, and testing patterns — each with a brief "Do / Don't" code example. The section SHALL cross-reference the following detailed specs: `backend-ci-pipeline`, `backend-testing-standards`, `backend-api-design`, `backend-security-owasp`, `backend-observability`, `backend-schema-design`.

#### Scenario: Developer checks backend naming convention
- **WHEN** a developer looks up the naming section
- **THEN** they find examples of correct variable/function/class names and common mistakes to avoid

#### Scenario: Developer checks error handling pattern
- **WHEN** a developer looks up error handling
- **THEN** they find the service-exception-to-HTTPException pattern with a code snippet

#### Scenario: Developer navigates to detailed backend spec
- **WHEN** a developer needs deeper detail on a backend standard
- **THEN** the section provides references to the corresponding detailed spec (e.g., `backend-api-design`)

### Requirement: Frontend standards section
The quick-reference SHALL include a frontend section covering: component patterns, hook patterns, TypeScript conventions, event handler naming, API call patterns, accessibility basics, and testing patterns — each with a brief "Do / Don't" code example. The section SHALL cross-reference the following detailed specs: `frontend-security`, `frontend-accessibility`, `frontend-resilience`.

#### Scenario: Developer checks component pattern
- **WHEN** a developer looks up the component section
- **THEN** they find the named-export, typed-props, destructured-params pattern with example code

#### Scenario: Developer checks hook pattern
- **WHEN** a developer looks up the hook section
- **THEN** they find the return-object, explicit-return-type, dependency-array pattern with example code

#### Scenario: Developer navigates to detailed frontend spec
- **WHEN** a developer needs deeper detail on a frontend standard
- **THEN** the section provides references to the corresponding detailed spec (e.g., `frontend-security`)

### Requirement: Git and PR standards section
The quick-reference SHALL include a section on commit message format, branch naming, and PR checklist expectations with examples of correct commit messages. The section SHALL cross-reference the `shared-git-workflow` spec for full rules.

#### Scenario: Developer checks commit message format
- **WHEN** a developer looks up the commit section
- **THEN** they find the structured release notes format with a concrete example

#### Scenario: Developer navigates to detailed git workflow spec
- **WHEN** a developer needs full git workflow rules
- **THEN** the section provides a reference to `shared-git-workflow`
