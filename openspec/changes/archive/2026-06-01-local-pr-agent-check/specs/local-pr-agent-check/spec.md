## ADDED Requirements

### Requirement: Local review script runs PR Agent against branch diff
The system SHALL provide `scripts/local-pr-review.sh` that runs PR Agent review against the current branch's diff compared to `main`.

#### Scenario: Default review of branch diff
- **WHEN** developer runs `scripts/local-pr-review.sh` from any working directory
- **THEN** the script computes `git diff main...HEAD`, passes it to PR Agent with `.pr_agent.toml` config, and prints review findings to stdout

#### Scenario: Review of staged changes only
- **WHEN** developer runs `scripts/local-pr-review.sh --staged`
- **THEN** the script computes `git diff --staged`, passes it to PR Agent, and prints review findings to stdout

#### Scenario: Review scoped to specific files
- **WHEN** developer runs `scripts/local-pr-review.sh --files backend/app/api/items.py`
- **THEN** the script reviews only the specified file's diff against `main`

### Requirement: Script reuses CI review configuration
The system SHALL generate and use the same `.pr_agent.toml` configuration that CI uses.

#### Scenario: Config generated before review
- **WHEN** the script starts
- **THEN** it runs `scripts/build-pr-agent-config.sh` to produce `.pr_agent.toml` and passes it to PR Agent

#### Scenario: Config content matches CI
- **WHEN** comparing the local `.pr_agent.toml` with the config generated in CI
- **THEN** the review rules, suggestion rules, and model settings are identical

### Requirement: Script runs PR Agent via Docker
The system SHALL use the official `codiumai/pr-agent` Docker image to run the review, avoiding dependency conflicts.

#### Scenario: Docker available
- **WHEN** developer has Docker installed and running
- **THEN** the script pulls/uses `codiumai/pr-agent:<pinned-version>` to execute the review

#### Scenario: Docker not available
- **WHEN** developer does not have Docker installed or Docker daemon is not running
- **THEN** the script prints a clear error message with installation instructions and exits with code 1

### Requirement: Script requires API key via environment variable
The system SHALL read the LLM API key from environment variables and MUST NOT hardcode or log any secrets.

#### Scenario: API key present
- **WHEN** `OPENAI_API_KEY` or `GITHUB_TOKEN` environment variable is set
- **THEN** the script passes it to the PR Agent container and proceeds with review

#### Scenario: API key missing
- **WHEN** neither `OPENAI_API_KEY` nor `GITHUB_TOKEN` is set
- **THEN** the script prints an error explaining which env var to set and exits with code 1

#### Scenario: API key never logged
- **WHEN** the script runs with verbose output or encounters an error
- **THEN** the API key value MUST NOT appear in any stdout, stderr, or generated file output

### Requirement: Script follows existing script conventions
The system SHALL follow the same conventions as `backend/scripts/verify-*.sh`.

#### Scenario: Script is executable from any directory
- **WHEN** developer runs `./scripts/local-pr-review.sh` from the repo root or any subdirectory
- **THEN** the script resolves paths relative to its own location using `SCRIPT_DIR` pattern

#### Scenario: Script has proper header
- **WHEN** developer opens `scripts/local-pr-review.sh`
- **THEN** it contains `#!/usr/bin/env bash`, `set -euo pipefail`, and a comment identifying its purpose

### Requirement: Script reports findings with appropriate exit codes
The system SHALL exit with code 0 when no blocking issues are found and code 1 when blocking issues are detected.

#### Scenario: No blocking findings
- **WHEN** PR Agent review finds no issues that warrant "Request Changes"
- **THEN** the script prints a success summary and exits with code 0

#### Scenario: Blocking findings detected
- **WHEN** PR Agent review finds issues that would trigger "Request Changes"
- **THEN** the script prints the findings and exits with code 1

#### Scenario: Large diff warning
- **WHEN** the computed diff exceeds 500 lines
- **THEN** the script prints a warning about potential cost/latency but proceeds with the review
