## ADDED Requirements

### Requirement: ESLint linting job in CI
The CI workflow SHALL run ESLint on all frontend TypeScript/TSX files when a PR targets `main`. The job SHALL post lint violations as a PR comment in a table format (file, line, rule, message) consistent with the backend Ruff comment format.

#### Scenario: Clean frontend code passes lint
- **WHEN** a PR contains frontend code with no ESLint violations
- **THEN** the lint job passes and the summary table shows "✅ Passed" for Frontend Lint

#### Scenario: Frontend code with lint violations
- **WHEN** a PR contains frontend code with ESLint violations
- **THEN** the lint job fails, a PR comment lists each violation (file, line, rule, message), and the summary table shows "❌ Failed" for Frontend Lint

### Requirement: TypeScript type-check job in CI
The CI workflow SHALL run `tsc --noEmit` on frontend code to verify type correctness. Type errors SHALL be posted as a PR comment with file, line, and error message.

#### Scenario: Frontend code passes type checking
- **WHEN** a PR contains frontend code with no TypeScript errors
- **THEN** the type-check job passes and the summary table shows "✅ Passed" for Frontend TypeCheck

#### Scenario: Frontend code with type errors
- **WHEN** a PR contains frontend TypeScript code with type errors
- **THEN** the type-check job fails and a PR comment lists each error with file path, line number, and error description

### Requirement: Vitest test execution job in CI
The CI workflow SHALL run `npx vitest run` on frontend tests. Test failures SHALL be reported as a PR comment. The job SHALL use JUnit XML output for structured reporting.

#### Scenario: All frontend tests pass
- **WHEN** a PR is opened and all frontend Vitest tests pass
- **THEN** the test job passes and the summary table shows "✅ Passed" for Frontend Tests

#### Scenario: Frontend test failures
- **WHEN** a PR contains code that causes frontend test failures
- **THEN** the test job fails and a PR comment lists up to 20 failed test names with error messages

### Requirement: Bundle size budget check in CI
The CI workflow SHALL build the frontend with `npm run build` and check that the total gzipped JS bundle size does not exceed a configured budget. The budget SHALL be defined in a CI variable or config file.

#### Scenario: Bundle size within budget
- **WHEN** the frontend build produces JS bundles within the size budget
- **THEN** the bundle size check passes and the summary reports current size vs. budget

#### Scenario: Bundle size exceeds budget
- **WHEN** the frontend build produces JS bundles exceeding the size budget
- **THEN** the check fails and the PR comment shows current size, budget, and overage amount

### Requirement: Frontend checks run in parallel with backend
The frontend CI jobs SHALL run independently of backend CI jobs with no job dependencies between the two groups. Both groups SHALL feed into a single summary comment.

#### Scenario: Backend and frontend checks run concurrently
- **WHEN** a PR modifies both backend and frontend files
- **THEN** backend jobs (ruff, mypy, bandit, pytest) and frontend jobs (eslint, tsc, vitest, bundle size) execute in parallel

### Requirement: Unified PR summary comment
The existing summary comment SHALL be extended to include frontend check results. The summary table SHALL show all backend and frontend checks in a single table.

#### Scenario: Full summary with all checks
- **WHEN** all CI jobs complete
- **THEN** a single PR comment displays a summary table with rows for each check (backend and frontend), each showing ✅ Passed or ❌ Failed
