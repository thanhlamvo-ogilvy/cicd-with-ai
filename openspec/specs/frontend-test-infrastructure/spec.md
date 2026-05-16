# Frontend Test Infrastructure

## Purpose

Vitest + React Testing Library test infrastructure for the frontend workspace, with example tests demonstrating patterns for components, hooks, and API services.

## Requirements

### Requirement: Vitest configuration
The frontend project SHALL have a Vitest configuration that uses jsdom as the test environment, supports TypeScript/TSX transforms via Vite, and integrates with React Testing Library. The configuration SHALL live in `vite.config.ts` or a separate `vitest.config.ts`.

#### Scenario: Vitest runs with correct environment
- **WHEN** a developer runs `npm test` in the frontend directory
- **THEN** Vitest starts with jsdom environment, resolves TypeScript/TSX imports, and executes test files matching `**/*.test.{ts,tsx}`

### Requirement: React Testing Library setup
The frontend project SHALL include `@testing-library/react`, `@testing-library/jest-dom`, and `@testing-library/user-event` as dev dependencies. A setup file SHALL configure jest-dom matchers globally.

#### Scenario: Custom matchers available in tests
- **WHEN** a test file uses matchers like `toBeInTheDocument()`, `toHaveTextContent()`, or `toBeVisible()`
- **THEN** the matchers resolve correctly without per-file imports

### Requirement: Example component test
The frontend project SHALL include at least one example component test demonstrating the pattern for testing React components with user interactions, rendering assertions, and prop-driven behavior.

#### Scenario: Component renders with props
- **WHEN** a component test renders `MessageBubble` with a message prop
- **THEN** the test verifies the message content appears in the document using `getByText` or `getByRole`

#### Scenario: Component handles user interactions
- **WHEN** a component test simulates a button click or form submission
- **THEN** the test verifies the expected callback was called or DOM state changed

### Requirement: Example hook test
The frontend project SHALL include at least one example custom hook test demonstrating the pattern for testing hooks in isolation using `renderHook` with mocked dependencies.

#### Scenario: Hook returns expected state
- **WHEN** a hook test renders `useConversations` with mocked API responses
- **THEN** the test verifies the hook returns the expected conversations list and loading state

### Requirement: Example API service test
The frontend project SHALL include at least one example API service test demonstrating the pattern for testing API functions with mocked `fetch` responses.

#### Scenario: API function handles success response
- **WHEN** an API test calls `createConversation()` with a mocked successful fetch response
- **THEN** the test verifies the function returns the parsed conversation object

#### Scenario: API function handles error response
- **WHEN** an API test calls an API function with a mocked error response (non-200 status)
- **THEN** the test verifies the function throws an error with a descriptive message

### Requirement: Test npm scripts
The frontend `package.json` SHALL include scripts for running tests: `test` (watch mode), `test:run` (single run for CI), and `test:coverage` (with coverage report).

#### Scenario: CI runs tests in single-run mode
- **WHEN** the CI pipeline executes `npm run test:run`
- **THEN** Vitest runs all tests once without watch mode and exits with code 0 on success or non-zero on failure
