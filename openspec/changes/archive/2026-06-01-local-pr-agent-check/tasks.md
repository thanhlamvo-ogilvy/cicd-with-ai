## 1. Script Setup

- [x] 1.1 Create `scripts/local-pr-review.sh` with shebang (`#!/usr/bin/env bash`), `set -euo pipefail`, and `SCRIPT_DIR`/`REPO_ROOT` resolution pattern
- [x] 1.2 Add header comment identifying purpose: "Run PR Agent review locally against branch diff"
- [x] 1.3 Mark script executable with `chmod +x scripts/local-pr-review.sh`

## 2. Prerequisite Checks

- [x] 2.1 Add Docker availability check — fail with clear install instructions if `docker` command not found or daemon not running
- [x] 2.2 Add API key check — verify `OPENAI_API_KEY` or `GITHUB_TOKEN` env var is set; fail with guidance if missing
- [x] 2.3 Add git repo check — verify script is running inside a git repository with a `main` branch

## 3. Config Generation

- [x] 3.1 Call `$REPO_ROOT/scripts/build-pr-agent-config.sh` (without `--env`) to generate `.pr_agent.toml`
- [x] 3.2 Verify `.pr_agent.toml` was created successfully; fail if generation failed

## 4. Diff Computation

- [x] 4.1 Implement default mode: compute diff via `git diff main...HEAD`
- [x] 4.2 Implement `--staged` flag: compute diff via `git diff --staged`
- [x] 4.3 Implement `--files <path>` flag: scope diff to specific file(s) via `git diff main...HEAD -- <path>`
- [x] 4.4 Add large diff warning: print advisory if diff exceeds 500 lines

## 5. PR Agent Execution

- [x] 5.1 Pin Docker image version to match CI workflow (`codiumai/pr-agent:0.35.0` or latest stable)
- [x] 5.2 Run PR Agent container with: mounted repo, `.pr_agent.toml` config, API key passed as env var (not logged)
- [x] 5.3 Capture PR Agent output and print to stdout
- [x] 5.4 Parse exit behavior: exit 0 if no blocking findings, exit 1 if "Request Changes" severity detected

## 6. Argument Parsing

- [x] 6.1 Support `--staged` flag for staged-only review
- [x] 6.2 Support `--files <path>` flag for file-scoped review
- [x] 6.3 Support `--output <file>` flag for JSON output to file
- [x] 6.4 Support `--help` flag with usage documentation
- [x] 6.5 Print error for unknown flags

## 7. Security Compliance

- [x] 7.1 Verify API key is never echoed, logged, or written to any file in any code path
- [x] 7.2 Ensure Docker mounts are read-only where possible (mount repo as `:ro` except for output)

## 8. Verification

- [x] 8.1 Run `scripts/local-pr-review.sh --help` — confirm usage output
- [x] 8.2 Run without Docker — confirm clear error message about missing Docker
- [x] 8.3 Run without API key — confirm clear error about missing env var
- [x] 8.4 Run against `demo_pr_agent_review.py` branch diff — confirm findings are reported and script exits 1
- [x] 8.5 Run against a clean branch with no violations — confirm exit 0
