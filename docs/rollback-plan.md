# Rollback Plan — Quality Gates

This document describes how to disable or roll back each quality gate component in case of emergency (e.g., a gate is blocking a critical hotfix, or a tool produces mass false positives after an update).

---

## Guiding Principle

Roll back the *smallest possible scope*. Disabling an entire CI pipeline is a last resort — prefer disabling a single job or temporarily lowering a threshold.

**Always re-enable gates within 24 hours.** Document every rollback in the PR or incident ticket.

---

## Component Rollback Procedures

### 1. Disable a Single CI Job

**When**: One tool (e.g., `bandit`) produces mass false positives after a dependency update.

**How**: Add `if: false` to the specific job in `.github/workflows/backend-ci.yml`:

```yaml
bandit:
  name: Bandit Security Scan
  if: false          # ← temporarily disabled
  runs-on: ubuntu-latest
  ...
```

Open a PR with this change. The job will be skipped. The `status-check` aggregator checks `result != "success"` — a skipped job returns `"skipped"`, not `"success"`, so you must also update the status check condition to allow `"skipped"` for that job:

```yaml
status-check:
  steps:
    - name: Check job statuses
      run: |
        if [ "${{ needs.ruff.result }}" != "success" ] || \
           [ "${{ needs.mypy.result }}" != "success" ] || \
           # bandit skipped — temporarily excluded
           [ "${{ needs.pytest.result }}" != "success" ] || \
           [ "${{ needs.pip-audit.result }}" != "success" ]; then
```

**Re-enable**: Revert both changes in a follow-up PR once the root cause is resolved.

---

### 2. Lower the Coverage Threshold

**When**: A large refactor or new code path temporarily drops coverage below 80%.

**How**: Edit `pyproject.toml` in `backend/`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=70"
#                                                                               ^^^
#                                                          Temporarily lowered from 80
```

**Re-enable**: Restore to 80 once coverage is recovered. Never leave below 80% for more than one sprint.

---

### 3. Disable the Entire Backend CI Workflow

**When**: The workflow file itself has a critical syntax error blocking all PRs, or a GitHub Actions outage.

**How**: Rename the workflow file to remove it from GitHub's detection:

```bash
git mv .github/workflows/backend-ci.yml .github/workflows/backend-ci.yml.disabled
git commit -m "Disable backend CI temporarily

{CI}
- Disable backend-ci.yml to unblock critical hotfix
- Track re-enable in <ticket/issue link>

(No dependency updates.)"
```

**Re-enable**:

```bash
git mv .github/workflows/backend-ci.yml.disabled .github/workflows/backend-ci.yml
```

---

### 4. Disable the AI PR Review Agent

**When**: The PR Agent is posting noise, incorrect comments, or the API key has expired.

**How**: In `.github/workflows/pr-agent.yml`, comment out the review step or disable the entire workflow:

```yaml
# Temporarily disabled — see <ticket>
# on:
#   pull_request:
#     types: [opened, synchronize]
on:
  workflow_dispatch:    # ← only runs manually
```

Since the AI review is advisory (non-blocking), disabling it does not affect merge ability.

**Re-enable**: Revert the trigger change once the issue is resolved.

---

### 5. Disable Husky Pre-commit Hooks Locally

**When**: A developer needs to make an emergency commit that bypasses hooks (e.g., reverting a broken config file).

**How**: Use the `--no-verify` flag (one-time bypass — never use habitually):

```bash
git commit --no-verify -m "Revert broken config

{CI}
- Revert .commitlintrc.json change that broke hooks

(No dependency updates.)"
```

This bypasses both `pre-commit` and `commit-msg` hooks for that single commit.

To disable hooks entirely for a session:

```bash
HUSKY=0 git commit -m "..."
```

**Re-enable**: No action needed — hooks are re-enabled on the next normal commit.

---

### 6. Remove a CVE Exception from pip-audit

If a CVE is added to `.pip-audit-ignore` and later the dependency is patched, remove the exception:

```bash
# Edit .pip-audit-ignore and remove the relevant GHSA/CVE line
# Then verify pip-audit is clean
pip-audit --skip-editable --desc
```

---

## GitHub Branch Protection

If branch protection rules themselves need to be temporarily relaxed (e.g., to force-merge a hotfix during an incident):

1. Go to **GitHub → Settings → Branches → main → Edit**
2. Temporarily uncheck the required status check(s)
3. Merge the hotfix
4. **Immediately re-enable** the status check and document the exception in the incident ticket

This should only happen for P0 production incidents. Notify the team before doing this.

---

## Rollback Communication Checklist

Before rolling back any gate:

- [ ] Document the reason in the PR description or incident ticket
- [ ] Notify the team in the engineering channel
- [ ] Set a re-enable deadline (max 24h for CI gates, max 1 sprint for coverage threshold)
- [ ] Create a follow-up ticket to re-enable and fix root cause
