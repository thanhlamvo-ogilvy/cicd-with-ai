## 1. Frontend Test Infrastructure

- [x] 1.1 Install Vitest, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, and jsdom as frontend dev dependencies
- [x] 1.2 Add Vitest configuration to `vite.config.ts` (jsdom environment, setup file, test file patterns)
- [x] 1.3 Create test setup file `frontend/src/test-setup.ts` that imports `@testing-library/jest-dom/vitest`
- [x] 1.4 Add `test`, `test:run`, and `test:coverage` scripts to `frontend/package.json`
- [x] 1.5 Create example component test `frontend/src/components/__tests__/MessageBubble.test.tsx`
- [x] 1.6 Create example hook test `frontend/src/hooks/__tests__/useConversations.test.ts`
- [x] 1.7 Create example API service test `frontend/src/services/__tests__/api.test.ts`
- [x] 1.8 Verify all example tests pass locally with `npm run test:run`

## 2. Frontend ESLint Setup

- [x] 2.1 Install ESLint 9, @eslint/js, typescript-eslint, eslint-plugin-react-hooks, eslint-plugin-react-refresh, and eslint-plugin-jsx-a11y as frontend dev dependencies
- [x] 2.2 Create `frontend/eslint.config.js` with flat config: TypeScript recommended, React hooks, React refresh, jsx-a11y, and import ordering rules
- [x] 2.3 Add `lint` and `lint:fix` scripts to `frontend/package.json`
- [x] 2.4 Run ESLint on existing frontend code, fix any violations or add targeted rule overrides for existing patterns
- [x] 2.5 Verify `npm run lint` passes locally with zero violations

## 3. Frontend CI Jobs

- [x] 3.1 Add frontend ESLint lint job to `.github/workflows/ai-review.yml` — install Node 20, run `npm ci`, run `npm run lint`, post violations as PR comment
- [x] 3.2 Add frontend TypeScript type-check job — run `npx tsc --noEmit`, post type errors as PR comment
- [x] 3.3 Add frontend Vitest test job — run `npm run test:run`, post failures as PR comment using JUnit XML output
- [x] 3.4 Add frontend bundle size check job — run `npm run build`, check gzipped JS size against budget, post result as PR comment
- [x] 3.5 Update the summary comment job to include frontend check results (ESLint, TypeCheck, Tests, Bundle Size) alongside backend checks in a single table
- [x] 3.6 Ensure frontend jobs have no dependencies on backend jobs (parallel execution)

## 4. Coding Standards Quick-Reference

- [x] 4.1 Create `CODING_STANDARDS.md` at repo root with document structure: Overview, Backend Standards, Frontend Standards, Git & PR Standards, CI Checks Reference
- [x] 4.2 Write backend standards section with Do/Don't code examples for: naming, function size, type annotations, async patterns, error handling, FastAPI endpoints, testing
- [x] 4.3 Write frontend standards section with Do/Don't code examples for: component patterns, hook patterns, TypeScript conventions, event handlers, API calls, accessibility, testing
- [x] 4.4 Write Git & PR standards section with commit message format example and branch naming conventions
- [x] 4.5 Write CI checks reference section listing each check with its fix command for local resolution

## 5. Verification

- [x] 5.1 Run full backend CI checks locally (`ruff check .`, `mypy app/`, `bandit -r app/`, `pytest`)
- [x] 5.2 Run full frontend CI checks locally (`npm run lint`, `npx tsc --noEmit`, `npm run test:run`, `npm run build`)
- [ ] 5.3 Open a test PR to verify the updated workflow runs all jobs and posts correct summary comment
