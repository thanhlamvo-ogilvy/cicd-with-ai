## Why

The project has strong coding standards documented across multiple files (`.github/copilot-instructions.md`, `backend/copilot-instructions.md`, `frontend/copilot-instructions.md`, `.github/copilot-review-instructions.md`), but several gaps exist that reduce their effectiveness: no frontend CI quality gates (linting, type-checking, testing), no automated code review enforcement beyond Copilot review requests, and missing best-practice guidance in areas like frontend testing, E2E testing, performance budgets, and structured logging patterns. Additionally, the current CI workflow only covers backend checks — the frontend has zero automated validation in the pipeline.

## What Changes

- Add **frontend CI quality gates** to the GitHub Actions workflow: ESLint linting, TypeScript type-checking (`tsc --noEmit`), and Vitest unit test execution with coverage thresholds
- Add **ESLint configuration** for the frontend with React, TypeScript, accessibility (jsx-a11y), and import ordering rules
- Add **Vitest testing setup** with React Testing Library for frontend component and hook testing
- Add **frontend test examples** demonstrating patterns for components, hooks, and API service mocking
- Enhance **copilot-review-instructions.md** with concrete code examples for common violation patterns, making reviews more actionable
- Add **per-PR automated review comment** that summarizes both backend and frontend check results in a single table
- Add **bundle size budget check** to frontend CI to catch dependency bloat early
- Add **coding standards quick-reference** that developers can consult during development (not just during review)

## Capabilities

### New Capabilities
- `frontend-ci-pipeline`: ESLint, TypeScript, Vitest, and bundle size checks added to the GitHub Actions workflow for frontend code
- `frontend-test-infrastructure`: Vitest + React Testing Library setup with example tests for components, hooks, and API services
- `coding-standards-quick-ref`: Developer-facing quick-reference guide for coding standards, separate from the review-focused checklist

### Modified Capabilities
<!-- No existing specs to modify -->

## Impact

- **CI workflow** (`.github/workflows/ai-review.yml`): Extended with 3-4 new frontend jobs (lint, typecheck, test, bundle size)
- **Frontend config**: New `eslint.config.js`, updated `package.json` with dev dependencies (eslint, vitest, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event)
- **Frontend tests**: New `frontend/src/__tests__/` directory with example test files
- **Documentation**: New `CODING_STANDARDS.md` quick-reference at repo root; enhanced `.github/copilot-review-instructions.md` with violation examples
- **PR review flow**: Summary comment updated to include frontend check results alongside backend results
- **Dependencies**: Frontend dev dependencies added (ESLint plugins, Vitest, Testing Library)
