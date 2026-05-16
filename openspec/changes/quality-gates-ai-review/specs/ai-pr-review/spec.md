# AI-Powered Pull Request Review

## Purpose

Define requirements for automated AI-driven code review focusing on architecture, business logic, error handling, security patterns, and design consistency. The AI reviewer operates as a supplementary layer after deterministic CI checks, catching issues that linters cannot.

## ADDED Requirements

### Requirement: AI review agent configuration
The AI PR review agent MUST be configured via `.pr_agent.toml` with project-specific guidelines injected into the system prompt.

#### Scenario: Configuration file exists
- **WHEN** the repository is initialized
- **THEN** `.pr_agent.toml` MUST exist at the repository root with `[pr_reviewer]` and `[pr_code_suggestions]` sections

#### Scenario: Extra instructions customized per project
- **WHEN** the AI agent reviews a PR
- **THEN** the `extra_instructions` field in `.pr_agent.toml` MUST define project-specific rules (security patterns, schema design, error handling)

### Requirement: AI agent focuses on high-level logic
The AI agent MUST ignore formatting, syntax, and type hints (handled by CI) and focus exclusively on business logic, architecture, security patterns, and design consistency.

#### Scenario: AI ignores formatting issues
- **WHEN** a PR has code style violations
- **THEN** the AI review MUST NOT comment on formatting (ruff/mypy already caught these in CI)

#### Scenario: AI reviews architectural patterns
- **WHEN** a PR modifies route handlers or service layer
- **THEN** the AI review MUST check for thin routes, proper layering, and correct schema usage

#### Scenario: AI reviews error handling
- **WHEN** a PR contains exception handling or external API calls
- **THEN** the AI review MUST check for specific exception types, logging, and retries

### Requirement: AI blocks PRs on security violations
The AI MUST request changes (block) on high-confidence security issues and only comment (non-blocking) on lower-severity patterns.

#### Scenario: SQL injection vulnerability detected
- **WHEN** the AI detects SQL built with f-strings or `.format()` (not SQLAlchemy ORM)
- **THEN** the AI MUST request changes with a comment: "SQL queries MUST use SQLAlchemy ORM/Core with bound parameters."

#### Scenario: PII logging detected
- **WHEN** the AI detects logging of passwords, tokens, or user content (e.g., `log.info(f"message: {message.content}")`)
- **THEN** the AI MUST request changes with guidance on sanitization

#### Scenario: Bare exception handlers detected
- **WHEN** the AI detects `except:` or `except Exception:` without re-raising or logging
- **THEN** the AI MUST comment (non-blocking) suggesting specific exception types or logging

### Requirement: AI reviews Pydantic schema compliance
The AI MUST verify that all request/response schemas follow project conventions (Pydantic Base/Create/Update/Response pattern, `model_config = ConfigDict(from_attributes=True)`).

#### Scenario: Response schema missing ORM config
- **WHEN** a PR adds a response schema without `model_config = ConfigDict(from_attributes=True)`
- **THEN** the AI MUST comment suggesting the config to enable direct ORM model conversion

#### Scenario: Partial update endpoint reviewed
- **WHEN** a PR adds a PATCH endpoint
- **THEN** the AI MUST verify it uses `exclude_unset=True` for partial updates

### Requirement: AI reviews API design standards
The AI MUST verify HTTP status codes are correct (201 for POST, 204 for DELETE), response_model is set, and error format is consistent (`{"detail": "message"}`).

#### Scenario: POST returns correct status
- **WHEN** a new POST endpoint is added
- **THEN** the AI MUST verify it returns 201 Created (not 200) and includes the created resource

#### Scenario: Delete returns 204 No Content
- **WHEN** a DELETE endpoint is implemented
- **THEN** the AI MUST verify it returns 204 No Content (not 200)

#### Scenario: Error response format checked
- **WHEN** an error is returned
- **THEN** the AI MUST verify the format is `{"detail": "message"}` (not custom formats)

### Requirement: AI reviews pagination requirements
List endpoints MUST include pagination (limit/offset or cursor-based). The AI MUST flag endpoints lacking pagination.

#### Scenario: List endpoint has pagination
- **WHEN** a new list endpoint is added
- **THEN** the AI MUST verify it accepts `limit` and `offset` query parameters (or cursor)

#### Scenario: Missing pagination flagged
- **WHEN** a list endpoint lacks pagination
- **THEN** the AI MUST comment: "List endpoints MUST support pagination."

### Requirement: AI reviews observability requirements
Logging MUST use structlog, with structured context binding (not string formatting). AI provider calls MUST NOT log request/response bodies.

#### Scenario: Structlog usage verified
- **WHEN** a PR adds logging code
- **THEN** the AI MUST verify it uses `structlog.get_logger()`, not `print()` or stdlib `logging`

#### Scenario: AI provider logging sanitized
- **WHEN** a PR calls an AI provider API
- **THEN** the AI MUST verify logs include only provider/model/tokens/latency — never request/response content

### Requirement: AI generates code suggestions
The AI MUST generate up to 3 code suggestions per PR, focusing on security, error handling, and schema design improvements.

#### Scenario: Code suggestions provided
- **WHEN** a PR is reviewed
- **THEN** the AI MUST provide up to 3 actionable code suggestions with rationale

#### Scenario: Suggestions enforce project standards
- **WHEN** suggestions are generated
- **THEN** they MUST adhere to the security, error handling, and schema design rules in `.pr_agent.toml`

### Requirement: AI review runs on pull request events
The AI agent MUST trigger on every PR open and push event (on updates).

#### Scenario: AI review triggers on PR open
- **WHEN** a new PR is opened
- **THEN** the Codium AI Agent workflow MUST trigger automatically

#### Scenario: AI review updates on push
- **WHEN** new commits are pushed to a PR
- **THEN** the AI review MUST re-run and update comments

### Requirement: AI review is human-readable and actionable
AI comments MUST be clear, provide specific guidance, and include examples where helpful.

#### Scenario: AI comment is understandable
- **WHEN** the AI leaves a comment
- **THEN** the comment MUST explain what the issue is, why it matters, and how to fix it

#### Scenario: AI suggestion includes example
- **WHEN** suggesting a schema change
- **THEN** the comment MUST include before/after code examples

### Requirement: Tuning period for AI review
After initial deployment, the AI review rules MUST be monitored and refined for 1 week to eliminate false positives.

#### Scenario: Tuning monitoring
- **WHEN** the AI review is first enabled
- **THEN** the team MUST monitor AI comments for patterns (noise, wrong flagging, missed issues)

#### Scenario: Noisy rules disabled
- **WHEN** a rule generates more false positives than actionable feedback
- **THEN** it MUST be disabled or refined in `.pr_agent.toml`

