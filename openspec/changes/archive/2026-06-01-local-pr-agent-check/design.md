## Context

The project already has:
- `scripts/build-pr-agent-config.sh` — generates `.pr_agent.toml` with review rules sourced from guideline specs
- `.github/workflows/pr-agent.yml` — runs PR Agent in CI via `Codium-ai/pr-agent` GitHub Action
- `backend/scripts/verify-*.sh` — local mirrors of CI lint/type/security/test checks

The missing piece is a local script that runs the same AI-powered review locally before push, completing the "shift-left" pattern established by `verify-*.sh`.

## Goals / Non-Goals

**Goals:**
- Run PR Agent review locally against the current branch diff vs `main`
- Reuse the same `.pr_agent.toml` configuration used in CI
- Provide fast terminal feedback on semantic violations
- Follow the same script conventions as `backend/scripts/verify-*.sh` (shebang, `set -euo pipefail`, SCRIPT_DIR pattern)

**Non-Goals:**
- Auto-fixing code based on review output
- Supporting frontend/non-Python review
- Replacing the CI-based review (both coexist)
- Building a custom review engine — we use PR Agent as-is

## Decisions

### 1. Use PR Agent CLI via Docker (not pip install)

**Choice:** Run PR Agent via its official Docker image (`codiumai/pr-agent`)

**Rationale:**
- No Python dependency conflicts with the backend venv
- Same image used in CI — identical behavior guaranteed
- Developer doesn't need to manage PR Agent version in their environment
- Fallback: support direct `python -m pr_agent` if Docker is unavailable

**Alternatives considered:**
- `pip install pr-agent` into backend venv → pollutes dev dependencies, version conflicts
- Standalone binary → not officially distributed

### 2. Diff source: branch diff against `main` (default) or staged changes

**Choice:** Default to `git diff main...HEAD` (branch diff); support `--staged` flag for reviewing only staged changes.

**Rationale:**
- Branch diff matches what PR Agent sees in CI (the full PR diff)
- Staged mode is useful for pre-commit spot-checks on partial work
- Both are local-only — no GitHub API calls needed

### 3. Config reuse: generate `.pr_agent.toml` then pass to CLI

**Choice:** Run `build-pr-agent-config.sh` (without `--env`) to produce `.pr_agent.toml`, then pass it to PR Agent via `--config` flag.

**Rationale:**
- Single source of truth for review rules
- Already tested in CI — no duplication
- `.pr_agent.toml` is gitignored (generated artifact)

### 4. Output format: terminal text (default) with optional JSON file

**Choice:** Print findings to stdout in human-readable format; support `--output <file>` flag for JSON output (IDE integration).

**Rationale:**
- Terminal output for quick review during development
- JSON for future IDE integration (VS Code problems panel, etc.)

## Risks / Trade-offs

- **[Docker dependency]** → Mitigation: Check for Docker availability at script start; print clear install instructions if missing. Support fallback to pip-installed pr-agent.
- **[API key requirement]** → Mitigation: PR Agent needs an LLM API key. Script checks for `OPENAI_API_KEY` or `GITHUB_TOKEN` env var; fails fast with guidance if missing. Never hardcode keys.
- **[Large diffs may be slow/expensive]** → Mitigation: Warn if diff exceeds 500 lines; support `--files <path>` to scope review to specific files.
- **[PR Agent version drift]** → Mitigation: Pin Docker image tag in script (same version as CI workflow). Document update procedure.

## Standards Mapping

| Decision | Guideline spec |
|----------|----------------|
| No hardcoded secrets; env var for API key | `guidelines/backend-security-owasp` |
| Script conventions (shebang, pipefail, SCRIPT_DIR) | `local-verify-scripts` |
| Fail-fast with clear error messages | `guidelines/shared-error-handling` |
| No new pip dependency in backend | `guidelines/shared-dependency-management` |

## Security Implications

- API key (`OPENAI_API_KEY` / `GITHUB_TOKEN`) loaded from environment only — never logged, never stored in script
- Diff content sent to LLM provider — same trust boundary as CI workflow (developer accepts this when using PR Agent)
- Script does not modify any files — read-only operation

## Testing Implications

- Script is a standalone shell script — tested by running against a known-bad diff (e.g., `demo_pr_agent_review.py`)
- No unit test needed (shell script, not library code)
- Verification: run script, confirm it produces findings matching CI PR Agent output

## Observability Implications

- Script prints execution status (config generated, diff computed, review running, findings count)
- Exit code 0 = no blocking findings, exit code 1 = blocking findings detected
- No structured logging (shell script, not a service)
