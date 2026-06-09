## Why

Developers currently only see PR Agent feedback after pushing a branch and opening a PR. This creates a slow feedback loop — violations that PR Agent catches (semantic issues like missing pagination, PII in logs, logic in route handlers) don't surface until CI runs remotely. A local PR Agent check would let developers preview the AI code review before push, catching issues earlier and reducing PR iteration cycles.

## What Changes

- Add a `scripts/local-pr-review.sh` script that runs PR Agent locally against the current diff (staged or branch diff vs main)
- Reuse the existing `build-pr-agent-config.sh` output (`.pr_agent.toml`) as the review ruleset
- Support reviewing either staged changes or the full branch diff against `main`
- Output review findings to terminal (and optionally to a file for IDE integration)

## Capabilities

### New Capabilities
- `local-pr-agent-check`: Script and configuration for running PR Agent review locally against uncommitted or branch changes before pushing

### Modified Capabilities
_(none — no existing spec requirements change)_

## Impact

- **New files**: `scripts/local-pr-review.sh`
- **Dependencies**: Requires PR Agent CLI (`pip install pr-agent`) or Docker image available locally
- **Existing code**: No modifications — builds on existing `build-pr-agent-config.sh` output
- **Developer workflow**: Adds optional local pre-push review step; no breaking changes to existing CI

## Guideline Alignment

- `guidelines/shared-git-workflow` — supports the PR review workflow by shifting feedback left
- `local-verify-scripts` — follows the same pattern (local mirror of CI checks)

## Non-Goals

- Replacing the CI-based PR Agent review (GitHub Actions workflow stays unchanged)
- Implementing auto-fix or code modification based on review findings
- Supporting non-Python files (frontend review) in this iteration
