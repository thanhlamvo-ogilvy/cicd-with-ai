# Contributing

## Prerequisites

- Python 3.12+
- Node.js 20+ (for Husky pre-commit hooks)
- Docker & Docker Compose (for local full-stack dev)

## Local Setup

```bash
# Clone and install Node deps to activate Husky hooks
git clone <repo>
cd cicd-with-ai
npm install

# Install Python dev dependencies
cd backend
pip install -e ".[dev]"
```

## Branch Naming

All branches must use one of these prefixes:

| Prefix | Use for |
|--------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `hotfix/` | Critical production fixes |
| `release/` | Release preparation |

```bash
git checkout -b feat/add-user-auth
git checkout -b fix/pagination-off-by-one
```

Branches that don't match these prefixes will be rejected by branch protection rules.

## Commit Message Format

All commit messages must follow this structured format:

```
[Primary Change Description]; [Secondary Changes] & more…

{PackageName}
- Add concise description of change (≤120 chars)
- Fix another change description

(No dependency updates.)
```

### Rules

1. **Title line**: Lead with the most newsworthy change. Append `& more…` if multiple topics. No trailing period.
2. **Group bullets** under `{PackageName}` headers (e.g. `{Backend}`, `{Frontend}`, `{CI}`, `{Docs}`).
3. **Bullets**: Start with a present-tense action verb (`Add`, `Fix`, `Refactor`, `Remove`, `Improve`). Max 120 characters each.
4. **Dependencies**: If no dependency changes, include the literal line `(No dependency updates.)`.
5. **No attribution**: Never add `Co-authored-by` trailers or AI generator attribution.

### Valid example

```
Add pagination to items endpoint; fix conversation schema

{Backend}
- Add limit/offset pagination to GET /api/v1/items
- Fix ConversationResponse missing from_attributes config

{CI}
- Add pip-audit step to backend-ci.yml

(No dependency updates.)
```

### Invalid examples

```
# ❌ Missing {PackageName} header
- fixed the bug

# ❌ Co-authored-by trailer
Fix auth bug

Co-authored-by: github-copilot[bot] <...>

# ❌ Trailing period in title
Add pagination.
```

The `commit-msg` Husky hook runs commitlint on every commit and will block invalid messages.

## Pre-commit Hooks

Husky runs two hooks automatically after `npm install`:

- **pre-commit**: Runs `ruff format app/` in `backend/` to auto-fix formatting before the commit is recorded.
- **commit-msg**: Runs `commitlint` to validate the commit message format.

If a hook fails, the commit is aborted. Fix the issue and retry.

## CI Requirements

All pull requests to `main` must pass these checks before merge:

| Check | Tool | Failure means |
|-------|------|---------------|
| Lint & format | Ruff | Fix lint errors or run `ruff format app/` |
| Type safety | Mypy (strict) | Fix type errors in `backend/app/` |
| Security scan | Bandit | Fix HIGH/CRITICAL security findings |
| Tests & coverage | Pytest | Fix failing tests or add coverage (target ≥80%) |
| Dependency CVEs | pip-audit | Upgrade or document CVE exception |

Run all checks locally before pushing:

```bash
cd backend

# Lint
ruff check app/

# Format check
ruff format --check app/

# Type check
mypy app/ --strict

# Security scan (HIGH+ issues)
bandit -r app/ -c pyproject.toml -ll

# Tests with coverage
pytest

# Dependency scan
pip-audit --skip-editable --desc
```

## AI PR Review

Every PR receives an automated AI review comment from PR Agent. The agent:

- Flags architectural violations (logic in route handlers, missing pagination, wrong HTTP status codes)
- Flags security patterns (f-strings in SQL, hardcoded secrets, PII in logs)
- Flags error handling issues (bare `except:`, missing timeouts, swallowed errors)
- Does **not** duplicate what CI tools already enforce (formatting, type errors, lint)

See [docs/ai-review-rules.md](docs/ai-review-rules.md) for the full rule set and how to address common comments.

## Pull Request Checklist

Before opening a PR:

- [ ] Branch name follows `feat/`, `fix/`, `hotfix/`, or `release/` prefix
- [ ] All CI checks pass locally (`ruff`, `mypy`, `bandit`, `pytest`)
- [ ] Coverage remains ≥80%
- [ ] PR contains one logical change (split if multi-topic)
- [ ] PR description explains *what* changed and *why*
- [ ] No secrets, tokens, or PII in code or logs
