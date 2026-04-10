## ADDED Requirements

### Requirement: Vitest unit and component testing

The frontend workspace SHALL use Vitest with React Testing Library for unit and component tests as the base of the test pyramid.

#### Scenario: Component render test

- **WHEN** a new React component is created
- **THEN** it MUST have at least one render test and one interaction test using React Testing Library

#### Scenario: Test runs in CI

- **WHEN** a PR is opened against `main`
- **THEN** CI SHALL run `npx vitest run` and block merge on test failures

#### Scenario: Hook testing

- **WHEN** a custom hook contains business logic
- **THEN** it MUST be tested using `renderHook` from React Testing Library

### Requirement: Playwright E2E testing

The frontend workspace SHALL use Playwright for end-to-end tests covering critical user journeys.

#### Scenario: Chat flow E2E test

- **WHEN** Playwright E2E suite runs
- **THEN** it SHALL verify the complete chat flow: create conversation, send message, receive streamed response

#### Scenario: E2E tests are minimal

- **WHEN** deciding between unit test and E2E test for new functionality
- **THEN** the developer SHALL prefer unit/component tests and only add E2E for critical user journeys (following Test Pyramid)

### Requirement: Testing instruction section

The `frontend/copilot-instructions.md` SHALL replace the placeholder "Testing (When Added)" section with concrete testing standards.

#### Scenario: Testing commands documented

- **WHEN** a developer reads the frontend instruction file
- **THEN** they SHALL find commands for `npx vitest run`, `npx playwright test`, and coverage reporting

#### Scenario: Test file conventions documented

- **WHEN** a developer creates a new test file
- **THEN** the instruction file SHALL specify: unit tests in `src/**/*.test.ts(x)`, E2E tests in `e2e/**/*.spec.ts`, test naming pattern `describe > it("should ...")`
