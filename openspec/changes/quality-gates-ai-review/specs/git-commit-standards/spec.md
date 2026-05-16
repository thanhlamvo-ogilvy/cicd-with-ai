# Git Commit Standards

## Purpose

Define commit message format, branch naming, and pre-commit validation to ensure consistency, enable automatable release notes, and maintain a clean, bisectable git history.

## ADDED Requirements

### Requirement: Branch naming conventions
Branch names MUST start with one of the following prefixes followed by a slash and kebab-case name:
- `feat/` for new features
- `fix/` for bug fixes
- `hotfix/` for urgent production fixes
- `release/` for release branches

#### Scenario: Feature branch naming
- **WHEN** a developer creates a new feature branch
- **THEN** it MUST follow the pattern `feat/<kebab-case-name>` (e.g., `feat/add-user-auth`)

#### Scenario: Fix branch naming
- **WHEN** a developer creates a bug fix branch
- **THEN** it MUST follow the pattern `fix/<kebab-case-name>` (e.g., `fix/null-pointer-exception`)

#### Scenario: Invalid branch name rejected
- **WHEN** a branch is created with a name not matching the allowed prefixes
- **THEN** pre-commit or GitHub validation MUST reject commits to main from this branch

### Requirement: Commit message format with package grouping
Commit messages MUST follow the structure: `[Primary Change]; [Secondary Changes] & more…` followed by package-grouped bullet points.

Format:
- **Line 1** (title): Lead with the most newsworthy change; end with `& more…` if multi-topic; no trailing period
- **Blank line**
- **Package groups** (curly-brace headers): Group changes under `{PackageName}` headers
- **Bullet points** under each group: Start with present-tense action verb (Add, Fix, Refactor); ≤120 characters; no periods
- **Final line**: `(No dependency updates.)` if no dependencies changed

#### Scenario: Single-package commit message
- **WHEN** a commit touches only one package (e.g., backend)
- **THEN** the message MUST follow: `Add feature X; no more changes` followed by `{Backend}` section and `(No dependency updates.)`

#### Scenario: Multi-package commit message
- **WHEN** a commit touches multiple packages (backend, frontend, CI)
- **THEN** the message MUST list the primary change; end line 1 with `& more…`; group changes under `{Backend}`, `{Frontend}`, `{CI}` headers

#### Scenario: Commitlint validates format
- **WHEN** a commit is created
- **THEN** commitlint MUST verify the format and reject commits that don't match

### Requirement: Commit message body constraints
Commit message bodies MUST NOT exceed 10 lines total.

#### Scenario: Body line limit
- **WHEN** a commit message body is written
- **THEN** the total number of lines (excluding title) MUST be ≤10

### Requirement: No Co-authored-by trailers
Commit messages MUST NOT contain `Co-authored-by:` trailers.

#### Scenario: Commitlint rejects Co-authored-by
- **WHEN** a commit message includes a `Co-authored-by:` trailer
- **THEN** commitlint MUST reject the commit with a clear error message

### Requirement: Branch protection on main
Direct commits to `main` MUST be blocked via GitHub Branch Protection rules.

#### Scenario: Direct push to main rejected
- **WHEN** a developer attempts to push directly to `main`
- **THEN** GitHub MUST reject the push and require a pull request

### Requirement: Pre-commit validation with Husky
Commit messages MUST be validated locally before push via Husky pre-commit hooks.

#### Scenario: Husky runs pre-commit check
- **WHEN** a developer runs `git commit`
- **THEN** Husky MUST run commitlint validation before allowing the commit

