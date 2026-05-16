## Context

This monorepo has a mature backend CI pipeline (Ruff, mypy, Bandit, pytest) and comprehensive review instructions (19-section checklist in `.github/copilot-review-instructions.md`). The frontend, however, has zero automated quality gates — no linting, no type-checking in CI, no test runner, and no bundle size monitoring. This creates an asymmetry where backend code is rigorously validated but frontend code reaches `main` with only manual review.

The project uses React 19 + TypeScript + Vite. Frontend coding standards are well-documented in `frontend/copilot-instructions.md` but not enforced by tooling. The existing CI workflow (`ai-review.yml`) posts check results as PR comments with a summary table — the frontend jobs need to integrate into this pattern.

## Goals / Non-Goals

**Goals:**
- Establish frontend CI parity with backend: automated linting, type-checking, testing, and bundle size checks
- Provide frontend test infrastructure (Vitest + React Testing Library) with example tests that demonstrate project patterns
- Create a developer-facing coding standards quick-reference that's concise and actionable (not the 19-section review checklist)
- Integrate frontend check results into the existing PR summary comment table

**Non-Goals:**
- E2E testing setup (Playwright/Cypress) — deferred to a future change
- i18n implementation — documented in standards but not scaffolded here
- Performance monitoring / APM setup — separate concern
- Changing existing backend CI jobs or review instructions
- Adding code coverage enforcement (start with tests running, add thresholds later)

## Decisions

### 1. ESLint 9 flat config over legacy `.eslintrc`

ESLint 9 uses the flat config format (`eslint.config.js`) which is the current standard. Legacy config is deprecated. The flat config is simpler, composable, and aligns with the project's preference for modern tooling.

**Alternatives considered:**
- Biome: Faster but less ecosystem support for React-specific rules (jsx-a11y, hooks). Risk of missing accessibility violations.
- Legacy ESLint config: Works but deprecated — would need migration later.

### 2. Vitest over Jest for frontend testing

Vitest is native to Vite, shares the same config and transform pipeline, and requires no additional Babel/SWC configuration. Jest would need separate transform config for TypeScript/JSX and has slower startup.

**Alternatives considered:**
- Jest: Industry standard but requires additional config for Vite projects. Slower test execution.
- Vitest covers the same API surface (`describe`, `it`, `expect`) so migration from Jest patterns is trivial if ever needed.

### 3. Bundle size check via `vite build` + file size assertion

Use `vite build` output and a simple script to check JS bundle size against a budget (e.g., 200KB gzipped). This avoids adding heavyweight tools like `bundlewatch` or `size-limit` as dependencies.

**Alternatives considered:**
- `size-limit`: Good tool but adds a dependency for what can be a 5-line shell script.
- `bundlewatch`: Requires GitHub token setup and external service. Over-engineered for current needs.

### 4. Quick-reference as `CODING_STANDARDS.md` at repo root

A separate markdown file at the repo root serves developers during active coding. The existing `copilot-review-instructions.md` is optimized for reviewers (checklist format) — developers need a scannable reference with code examples.

**Alternatives considered:**
- Merge into existing instructions: Would make the review doc too long and serve two audiences poorly.
- Wiki/Notion: Not version-controlled alongside code.

### 5. Frontend CI jobs follow existing backend pattern

Each frontend check runs as a separate job (like backend's `lint`, `typecheck`, `security`, `test` jobs), posts violations as PR comments, and feeds into the summary table. This maintains consistency and allows fine-grained failure visibility.

## Risks / Trade-offs

- **[Risk] ESLint rule set too strict initially** → Start with recommended presets only; add project-specific rules incrementally. Developers can propose rule changes via PR.
- **[Risk] Bundle size budget too tight/loose** → Set initial budget at 2x current build size as headroom; tighten after baseline is established.
- **[Risk] Vitest + jsdom may not catch all browser-specific issues** → Acceptable trade-off; browser-specific bugs are E2E testing territory (future scope).
- **[Risk] Adding multiple frontend CI jobs increases PR feedback time** → Frontend jobs run in parallel with backend jobs (no dependencies between them), so total CI time should not increase significantly.
- **[Trade-off] Quick-reference duplicates some content from review instructions** → Acceptable; the two docs serve different audiences (developer vs. reviewer) and the quick-ref is intentionally brief.
