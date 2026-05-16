## Context

Currently, the project relies on manual code review for all quality checks. Without systematic enforcement, coding standards are inconsistently applied, security vulnerabilities (SQL injection, PII leaks, hardcoded secrets) can slip through, and architectural patterns diverge. There is no local feedback mechanism—developers only discover issues when CI runs or during review. Additionally, PR turnaround times are slow due to manual feedback on formatting, type safety, and basic security smells that could be automated.

We operate in a hybrid monorepo (backend/Python + frontend/React) with shared CI/CD and deployment pipelines. All changes flow through GitHub, so GitHub Actions is our natural platform for CI enforcement. The team values fast iteration and wants to avoid "CI red herring" (false positives from overzealous linters).

## Goals / Non-Goals

**Goals:**

- Enforce deterministic, non-negotiable rules (formatting, type safety, security basics) via CI/CD before human review, ensuring zero-tolerance for mechanical errors.
- Use AI to catch architectural and design-level issues (thin routes, correct schemas, error handling, security patterns) without burdening manual reviewers or generating noise.
- Enable developers to receive feedback locally (pre-commit via Husky) before pushing, reducing surprise CI failures.
- Prevent vulnerable dependencies from entering the codebase via automated CVE scanning.
- Maintain high code coverage (≥80%) as a merge blocker to ensure testability.
- Reduce PR review turnaround by 30%+ by eliminating formatting/type arguments and automating architecture checks.

**Non-Goals:**

- Replace human code review; AI review is supplementary.
- Enforce frontend linting (ESLint/Prettier integration) in this phase; focus backend first, then extend to frontend.
- Implement custom static analysis tools or SAST platforms; use industry-standard tools (ruff, mypy, bandit).
- Support backends other than GitHub; other platforms can be added later.
- Enforce runtime security (WAF, RASP); scope is pre-merge.

## Decisions

### 1. **Two-Layer Enforcement: Deterministic vs. Heuristic**

**Decision**: Split enforcement into CI/CD (deterministic: ruff, mypy, bandit, pytest) and AI PR review (heuristic: architecture, security patterns, error handling).

**Rationale**: Not all code quality issues are automatable. Type errors and formatting have one correct answer; architectural patterns and error handling require context and judgment. Separate layers allow each tool to excel at its purpose without false positives.

**Alternatives Considered**:
- Single AI reviewer for everything: Risk of noise (formatting corrections from LLM are unreliable) and cost (slower than local linters).
- Single linter-based approach: Misses architectural and business logic issues; rules become increasingly complex and fragile.

### 2. **Tooling: Ruff for Python Linting & Formatting**

**Decision**: Use Ruff (written in Rust, bundled with Python ecosystem) for linting and formatting instead of Flake8 + Black.

**Rationale**: Ruff is 10-100x faster than traditional tools, has a single binary, and is increasingly adopted by the Python community. Single source of truth for lint + format reduces tool friction.

**Alternatives Considered**:
- Flake8 + Black: Slower, two separate tools, two configuration files.
- pylint: Slower than Ruff, more false positives on docstrings.

### 3. **Type Checking: Mypy in Strict Mode**

**Decision**: Enforce Mypy with `--strict` flag on the `app/` directory to catch type errors at CI time.

**Rationale**: Strict type checking prevents entire categories of runtime errors (None dereferences, type confusion). Strict mode is non-negotiable for data pipelines and security-critical code. Must pass before merge.

**Alternatives Considered**:
- Pyright: Also valid; Mypy is entrenched in project conventions.
- No type checking: Too risky; SQL queries, authentication, and data transformations benefit from type safety.

### 4. **Security Scanning: Bandit + Pip-audit**

**Decision**: Use Bandit for code-level security patterns (SQL injection, eval/exec, hardcoded secrets) and pip-audit for dependency vulnerabilities.

**Rationale**: Bandit catches common mistakes (e.g., `f"SELECT * FROM users WHERE id={id}"`). Pip-audit prevents CVEs in transitive dependencies. Both are lightweight and fail-fast.

**Alternatives Considered**:
- Commercial SAST (Snyk, Veracode): Cost and complexity not justified at current scale.
- Hadolint (Docker only): Covers container security but not Python code.

### 5. **Testing & Coverage: Pytest with ≥80% Threshold**

**Decision**: Pytest is the test runner; coverage threshold of ≥80% is a merge blocker. Tests must use `httpx.AsyncClient + ASGITransport` and aiosqlite (no external services).

**Rationale**: 80% is a practical threshold—high enough to catch untested logic, low enough to avoid diminishing returns. Isolated tests (no external calls) run fast (<5s) and are deterministic.

**Alternatives Considered**:
- 100% coverage: Leads to brittle, pointless tests (mocking everything).
- Mock external services: Tests become fragile and slow to debug; in-memory aiosqlite is clearer.

### 6. **AI PR Review: Codium PR Agent with Claude 3.5 Sonnet**

**Decision**: Use Codium's PR Agent (open-source GitHub Action) configured with project-specific guidelines via `.pr_agent.toml` and Claude 3.5 Sonnet as the model backend.

**Rationale**: PR Agent is lightweight, runs in GitHub Actions (no new infrastructure), and is customizable via TOML. Claude 3.5 Sonnet has strong code comprehension and follows instructions well. `.pr_agent.toml` allows us to inject project guidelines into the system prompt.

**Alternatives Considered**:
- GitHub Copilot for Pull Requests: Proprietary, limited customization.
- Self-hosted LLM (Llama, Mistral): Infrastructure burden; Claude is cheaper per request.
- GPT-4o: Equivalent to Claude; we standardize on Claude for consistency.

### 7. **Local Feedback: Husky Pre-commit Hooks**

**Decision**: Use Husky to run Ruff lint + format checks locally before commits are pushed.

**Rationale**: Developers see formatting issues immediately without waiting for CI. Pre-commit hooks are non-blocking by default (can override with `--no-verify`), so they don't frustrate developers during rapid iteration.

**Alternatives Considered**:
- No pre-commit: CI feedback only; slower iteration loop.
- Pre-commit framework (Python): Overlaps with Husky; stick with one tool.

### 8. **Commit Message Enforcement: Commitlint**

**Decision**: Enforce commit message format via commitlint: branch prefixes (feat/, fix/, hotfix/, release/), {PackageName} in commit body, ≤10 lines, no Co-authored-by trailers.

**Rationale**: Structured commit messages enable automating release notes and bisecting bugs. Commitlint is lightweight and integrates with Husky.

**Alternatives Considered**:
- GitHub Actions on push: Catches failures after push; pre-commit is faster feedback.
- No enforcement: Messages become inconsistent; release automation breaks.

### 9. **Repository Structure & Configuration Files**

**Decision**: Place all configuration files at the repo root: `.pr_agent.toml`, `.pre-commit-config.yaml`, `pyproject.toml` (for tool.ruff, tool.mypy, tool.bandit).

**Rationale**: Single source of truth; developers know where to look for rules. CI/CD workflows in `.github/workflows/` also root-level for discoverability.

**Alternatives Considered**:
- Separate configs per workspace (backend/.ruff.toml, frontend/.eslint.json): Fragmented; harder to maintain consistency.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **CI Failures Block Fast Iteration** → Developers get frustrated if CI is slow. | Keep Ruff + Mypy + Bandit runs to <1 min. Cache dependencies. Run linters in parallel in GitHub Actions. |
| **AI Review Generates False Positives** → Developers ignore useful feedback if noise is high. | Week-long tuning period post-launch. Monitor AI comments for patterns. Refine `.pr_agent.toml` based on feedback. Flag noisy rules and disable them. |
| **Coverage Threshold Too High** → Teams spend time on low-value tests to hit 80%. | 80% is pragmatic; accept that not all code needs tests (e.g., trivial getters). Encourage testing high-risk code (auth, data validation). |
| **Tool Version Pinning** → Ruff 0.2.0 may behave differently than 0.3.0. | Pin versions in `pyproject.toml` and lock files. Test in staging before upgrading. |
| **Dependency Conflicts** → Bandit or pip-audit may pull in incompatible versions. | Use separate dependency group for dev tools (e.g., `pip install -e ".[dev]"`). |
| **AI Model API Costs** → Claude API calls per PR may accumulate. | Monitor usage. Start with 3 code suggestions per PR; scale down if cost becomes prohibitive. |

## Migration Plan

**Phase 1: CI/CD Lockdown (Day 1-2)**
1. Add Ruff, Mypy, Bandit, Pytest config to `pyproject.toml`.
2. Create `.github/workflows/backend-ci.yml` that runs lint, type check, security scan, and tests.
3. Verify all workflows pass locally: `ruff check app/`, `mypy app/`, `bandit -r app/`, `pytest`.
4. Commit and push to a new branch (e.g., `feat/ci-lockdown`).
5. Enable GitHub Branch Protection on `main`: Require status checks from all CI jobs.
6. Merge PR (first CI run will be clean).

**Phase 2: Commit Standards (Day 2)**
1. Install Husky and commitlint: `npm install husky @commitlint/cli --save-dev`.
2. Create `.husky/pre-commit` to run Ruff.
3. Create `.husky/commit-msg` to run commitlint.
4. Create `.commitlintrc.json` with {PackageName} rules and rejection of Co-authored-by.
5. Test locally: Make a malformed commit and verify Husky blocks it.
6. Commit and push.

**Phase 3: AI PR Review (Day 3-4)**
1. Create `.pr_agent.toml` with security/architecture guidelines.
2. Create `.github/workflows/pr-agent.yml` that triggers on PR open/synchronize.
3. Set GitHub environment variable `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (for Claude).
4. Create a test PR to verify AI comments appear.
5. Monitor AI feedback for 1 week. Refine prompt if needed (disable noisy rules, add missing patterns).
6. Lock PR Agent configuration after tuning.

**Rollback Strategy**:
- Remove workflow files from `.github/workflows/` to disable CI checks.
- Delete `.husky/` to disable pre-commit hooks.
- Delete `.pr_agent.toml` and PR Agent workflow to disable AI review.
- Disable GitHub Branch Protection on `main` if necessary.
- Each step can be rolled back independently; no data loss.

## Open Questions

1. **Claude vs. GPT-4o**: Which model endpoint should we use? Cost difference? (Decision: Start with Claude 3.5 Sonnet; switch to GPT-4o if cost becomes prohibitive.)
2. **Coverage Exclusions**: Should we exclude `__pycache__`, migrations (alembic/), or test files from coverage? (Decision: Exclude test files and migrations; measure coverage on app/ only.)
3. **Staged Rollout**: Should we enforce AI review as "Request Changes" or "Comment Only" initially? (Decision: Comment-only for 1 week; switch to "Request Changes" after tuning.)
4. **Frontend Scope**: Does Phase 1-3 apply only to backend, or should ESLint + Prettier be added to frontend in parallel? (Decision: Backend first; frontend in Phase 4 if successful.)

