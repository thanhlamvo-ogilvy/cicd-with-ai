## ADDED Requirements

### Requirement: No direct commits to main
All changes MUST go through a feature branch and pull request. Direct commits to `main` are forbidden.

#### Scenario: PR required for main
- **WHEN** a developer wants to merge code to `main`
- **THEN** they MUST create a feature branch and open a PR

### Requirement: Branch naming convention
Branches MUST use descriptive prefixes: `feat/`, `fix/`, `hotfix/`, `release/`.

#### Scenario: Feature branch naming
- **WHEN** a new feature branch is created
- **THEN** its name MUST start with `feat/`, `fix/`, `hotfix/`, or `release/`

### Requirement: Short-lived branches
Branches MUST be merged or closed within days, not weeks.

#### Scenario: Stale branch detection
- **WHEN** a branch has been open for more than one week without activity
- **THEN** it SHOULD be flagged for review or closure

### Requirement: Focused PRs
Each PR MUST contain one logical change. Multi-topic PRs MUST be flagged.

#### Scenario: Single-concern PR
- **WHEN** a PR is opened
- **THEN** it MUST address a single logical change — not bundle unrelated modifications

### Requirement: Structured commit message format
All commit messages MUST follow the structured release notes format with a title line, change groups under `{PackageName}` headers, and present-tense action verb bullets.

#### Scenario: Commit message structure
- **WHEN** a commit is made
- **THEN** the message MUST include a title line, grouped changes under `{PkgName}` headers, and action verb bullets (≤120 chars)

#### Scenario: Dependency update notation
- **WHEN** a commit has no dependency updates
- **THEN** the message MUST include the literal line `(No dependency updates.)`

### Requirement: No attribution tags
Commit messages MUST NOT contain co-authored-by trailers or generator attribution tags.

#### Scenario: Attribution tag rejected
- **WHEN** a commit message contains a `Co-authored-by:` trailer
- **THEN** it MUST be removed before committing

### Requirement: Clean history via rebase or squash-merge
Merges to main MUST use rebase or squash-merge to keep history clean and bisectable.

#### Scenario: Merge strategy
- **WHEN** a PR is merged to main
- **THEN** it MUST use rebase or squash-merge — not a merge commit
