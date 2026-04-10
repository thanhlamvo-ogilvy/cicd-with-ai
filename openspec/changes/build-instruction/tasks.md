## 1. Root Instruction — AI Persona Roles

- [x] 1.1 Add "AI Persona Roles" section to `.github/copilot-instructions.md` after the "AI Context & Token Efficiency" section, defining three personas: Senior Python/FastAPI Engineer (backend), Senior React/TypeScript Engineer (frontend), Senior DevOps/Platform Engineer (cross-cutting)
- [x] 1.2 Each persona definition must include: role name, expertise areas, and when it activates (based on file path context)

## 2. Backend Instruction — PII & Auth Hardening

- [x] 2.1 Update "Data Privacy & Compliance" section in `backend/copilot-instructions.md` to add AI-chat-specific PII rules: classify `Message.content` and `Conversation.title` as PII, require `conversation_id`/`message_id` in logs (never content), configurable retention period via env var, cascading user deletion support
- [x] 2.2 Add "Authentication Activation Plan" subsection under "Key Conventions" in `backend/copilot-instructions.md` documenting: JWT middleware via `Depends()`, list of routes to protect, toggle mechanism via environment variable or feature flag
- [x] 2.3 Update "Security (OWASP for Python)" section in `backend/copilot-instructions.md` to explicitly state `allow_methods` MUST list specific HTTP methods (`["GET", "POST", "DELETE", "OPTIONS"]`) — never `["*"]` in production

## 3. Frontend Instruction — Linting & Formatting

- [x] 3.1 Add "Lint & Format" section to `frontend/copilot-instructions.md` (after "Build & Run") documenting: ESLint with `@typescript-eslint`, `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`; Prettier with double quotes, 100-char line length, trailing commas
- [x] 3.2 Document lint commands: `npx eslint .`, `npx prettier --check .`, `npx prettier --write .`
- [x] 3.3 Document expected `devDependencies` for linting: `eslint`, `@typescript-eslint/eslint-plugin`, `@typescript-eslint/parser`, `prettier`, `eslint-config-prettier`

## 4. Frontend Instruction — Testing Setup

- [x] 4.1 Replace the placeholder "Testing (When Added)" section in `frontend/copilot-instructions.md` with a concrete "Testing" section covering: Vitest + React Testing Library for unit/component tests, Playwright for E2E tests
- [x] 4.2 Document test commands: `npx vitest run`, `npx vitest run --coverage`, `npx playwright test`
- [x] 4.3 Document test file conventions: unit tests in `src/**/*.test.ts(x)`, E2E tests in `e2e/**/*.spec.ts`, test naming pattern `describe("ComponentName") > it("should ...")`
- [x] 4.4 Document expected `devDependencies` for testing: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`, `@playwright/test`
- [x] 4.5 Document Test Pyramid rule: prefer unit/component tests (many, fast) over E2E tests (few, slow); every new component MUST have render + interaction test

## 5. Frontend Instruction — PII & Error Handling

- [x] 5.1 Update "Data Privacy" section in `frontend/copilot-instructions.md` to add AI-chat-specific rules: never include `message.content` in console logs, error tracking, or analytics; clear chat state on logout; no chat content in localStorage
- [x] 5.2 Update "Error Handling" section in `frontend/copilot-instructions.md` to add: all `catch` blocks MUST handle errors explicitly (no empty catch), API errors MUST show user-friendly messages with retry actions, malformed SSE data MUST be logged with event metadata (not content)

## 6. Verification

- [x] 6.1 Verify all three instruction files remain under 500 lines each
- [x] 6.2 Verify no duplication — new sections reference existing rules rather than restating them
