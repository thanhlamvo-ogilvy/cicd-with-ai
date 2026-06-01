# Enforced Quality Gates — Developer Setup Guide

This guide gets a new developer from zero to a fully compliant local environment in under 5 minutes.

---

## What Is Enforced

This project uses a two-layer enforcement model:

| Layer | Tools | When |
|-------|-------|------|
| **Local (pre-commit)** | Husky + Ruff format | On every `git commit` |
| **Local (commit-msg)** | commitlint | On every `git commit` |
| **CI (blocking)** | Ruff lint, Mypy, Bandit, Pytest, pip-audit | On every PR to `main` |
| **CI (informational)** | PR Agent AI review | On every PR to `main` |

A PR **cannot merge** until all CI checks pass. The AI review is advisory — it does not block merge, but findings are expected to be addressed or explicitly dismissed.

---

## Step 1: Install Node Dependencies

Husky hooks are activated by `npm install`. Run this once after cloning:

```bash
npm install
```

This installs Husky, commitlint, and wires the `.husky/` hooks into your local Git configuration.

**Verify** hooks are active:

```bash
ls .husky/
# Expected: commit-msg  pre-commit
```

---

## Step 2: Install Python Dev Dependencies

```bash
cd backend
pip install -e ".[dev]"
```

This installs all tools used in CI: `ruff`, `mypy`, `bandit`, `pytest`, `pytest-cov`, `pip-audit`.

---

## Step 3: Verify Your Setup

Run all CI checks locally to confirm everything is working:

```bash
cd backend

# Lint (should print "All checks passed!")
ruff check app/

# Format check (should print nothing)
ruff format --check app/

# Type check (should print "Success: no issues found")
mypy app/ --strict

# Security scan (should print no HIGH/CRITICAL findings)
bandit -r app/ -c pyproject.toml -ll

# Tests with coverage (should reach ≥80%)
pytest

# Dependency CVE scan
pip-audit --skip-editable --desc
```

If all pass, you're ready to contribute.

---

## Step 4: Understand the Commit Format

Every commit message must follow this format — commitlint will reject non-compliant messages:

```
[Primary Change]; [Secondary] & more…

{PackageName}
- Add description of change (≤120 chars)
- Fix another change

(No dependency updates.)
```

**Example:**

```
Add pagination to items endpoint

{Backend}
- Add limit/offset pagination to GET /api/v1/items
- Return 200 with items array and total count

(No dependency updates.)
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full format specification.

---

## Step 5: Use the Correct Branch Prefix

Your branch name must start with `feat/`, `fix/`, `hotfix/`, or `release/`:

```bash
git checkout -b feat/add-user-profile
```

---

## What Happens When You Commit

1. **pre-commit hook** runs `ruff format app/` — auto-fixes formatting in `backend/`. If it fails, the commit is aborted.
2. **commit-msg hook** runs commitlint — validates your commit message. If the format is invalid, the commit is aborted with an error showing what's wrong.

---

## What Happens When You Open a PR

1. All five CI jobs run in parallel on GitHub Actions:
   - `ruff` — lint + format check
   - `mypy` — strict type checking
   - `bandit` — security scan (HIGH+ issues block merge)
   - `pytest` — tests must pass; coverage must be ≥80%
   - `pip-audit` — no high-severity CVEs
2. A `CI Status Check` aggregator reports overall pass/fail.
3. The PR Agent AI reviewer posts inline comments on architecture, security patterns, and error handling violations.

**You cannot merge until the `CI Status Check` is green.**

---

## Troubleshooting

### Commit rejected — "header-max-length"

The title line exceeds 120 characters. Shorten it.

### Commit rejected — "Co-authored-by"

Remove any `Co-authored-by:` trailer from your commit message. These are prohibited.

### Ruff format fails in pre-commit

Run `ruff format app/` manually in `backend/`, then `git add` the auto-fixed files and retry the commit.

### Mypy strict errors

Run `mypy app/ --strict` locally to see all errors. Common fixes:
- Add explicit return type annotations to functions
- Use `Optional[X]` or `X | None` for nullable values
- Avoid `Any` — use proper types or `cast()` with comment

### Coverage below 80%

Run `pytest --cov=app --cov-report=term-missing` to see which lines are uncovered. Add targeted tests for uncovered paths.

### Husky not running on commit

Run `npm install` again from the repo root. If hooks are still missing, run `npx husky install`.

---

## Quick Reference

```bash
# Activate hooks (once after clone)
npm install

# Install Python tools
cd backend && pip install -e ".[dev]"

# Run all CI checks locally
cd backend
ruff check app/ && ruff format --check app/
mypy app/ --strict
bandit -r app/ -c pyproject.toml -ll
pytest
pip-audit --skip-editable --desc

# Create a compliant branch
git checkout -b feat/my-feature

# Commit with valid message
git commit -m "Add my feature

{Backend}
- Add description of what changed

(No dependency updates.)"
```
