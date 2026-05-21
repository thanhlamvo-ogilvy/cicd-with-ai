## Context

The `backend-ci.yml` workflow defines six independent jobs: `ruff-lint`, `ruff-format`, `mypy`, `bandit`, `pytest`, and `pip-audit`. Each job runs from the `backend/` directory after installing `pip install -e ".[dev]"`. There are no local equivalents — developers must push and wait for CI to surface failures.

## Goals / Non-Goals

**Goals:**
- Provide a script per CI job so each check can be run in isolation
- Provide a combined `verify-all.sh` that runs all checks and reports an aggregate pass/fail summary
- Mirror the exact commands used in CI (same flags, same working directory)
- Exit with non-zero status on any failure so the scripts are CI-composable themselves

**Non-Goals:**
- Installing Python dependencies (scripts assume `pip install -e ".[dev]"` has been run)
- Running frontend or Docker checks
- Replacing or modifying the GitHub Actions workflow
- Generating HTML coverage artifacts beyond what CI already does

## Decisions

**Decision: One script per CI job**
Each script maps 1:1 to a CI job rather than grouping related checks. This lets developers run only the check they care about (e.g., just lint after a formatting change) without wading through a monolithic script. Alternative (single parameterised script) was rejected for discoverability — named files are easier to find and invoke from editor run-configs.

**Decision: Scripts run from repo root, `cd backend/` inside**
Consistent with CI's working directory behaviour. Alternative (requiring `cd backend && ./scripts/verify-lint.sh`) was rejected — it breaks if called from any other directory and adds friction.

**Decision: `verify-all.sh` runs scripts sequentially, collects failures, prints summary**
Sequential execution (not parallel) keeps output readable and matches CI job ordering. Each sub-script's exit code is collected; the combined script exits 1 if any sub-script failed. Alternative (exit-on-first-failure) was rejected — developers benefit from seeing all failures at once, not just the first.

**Decision: Place scripts in `backend/scripts/`**
Co-located with the backend workspace. Alternative (`scripts/` at repo root) was considered but backend scripts should live with the backend; frontend would have its own `frontend/scripts/` in future.

## Risks / Trade-offs

- **Risk: Command drift** — if CI commands change, scripts must be updated manually → Mitigation: scripts are small and clearly labelled with the CI job they mirror; a comment block at the top of each script names the source job
- **Risk: Bandit report file left in `backend/`** — CI writes `bandit-report.json`; local script should skip the JSON output to avoid accidentally committing it → Mitigation: `verify-security.sh` uses only the `-ll` invocation (no `-o` flag), matching the "Check Bandit results" step in CI
- **Risk: `pip-audit` exits non-zero even on `|| true` step** — CI uses `|| true` on the first invocation to generate output, then a second call to actually fail → Mitigation: `verify-deps.sh` mirrors the same two-call pattern

## Migration Plan

No migration required — new files only. Scripts are added under `backend/scripts/` and committed. No existing files change.
