## Why

The three `copilot-instructions.md` files (root, backend, frontend) already cover ~80% of the project's coding standards, but several critical gaps exist: frontend has zero linting/formatting tooling configured, frontend testing says "When Added" with no actual setup, PII guidelines are generic despite the app handling AI chat messages (user PII), CORS config contradicts its own rules (`allow_methods=["*"]`), and there is no AI persona instruction to ensure the agent adopts the correct role per context. These gaps mean generated code is not fully governed by the instruction files.

## What Changes

- Add AI Persona Roles section to root `.github/copilot-instructions.md` — defines which expert role the AI adopts per workspace context
- Add frontend linting & formatting standards to `frontend/copilot-instructions.md` — ESLint + Prettier configuration and CI enforcement
- Replace the placeholder "Testing (When Added)" section in `frontend/copilot-instructions.md` with concrete Vitest + React Testing Library (unit/component) and Playwright (E2E) setup
- Strengthen PII/data privacy sections in both backend and frontend instructions with AI-chat-specific rules (message retention, log sanitization, encryption of chat content)
- Add authentication activation plan to `backend/copilot-instructions.md` — when and how to wire JWT into routes
- Harden CORS guidance in `backend/copilot-instructions.md` — explicitly disallow `["*"]` for methods in production, align code with rules
- Add frontend error handling patterns to `frontend/copilot-instructions.md` — replace silent catch blocks with structured error handling

## Capabilities

### New Capabilities
- `ai-persona-roles`: AI agent persona definitions per workspace context (backend, frontend, shared)
- `frontend-linting`: ESLint + Prettier configuration, rules, and CI integration for frontend
- `frontend-testing-setup`: Vitest + React Testing Library + Playwright testing infrastructure for frontend
- `ai-chat-pii`: AI-chat-specific PII handling rules for both backend and frontend (message lifecycle, retention, purging, log sanitization)

### Modified Capabilities

## Impact

- `.github/copilot-instructions.md`: New AI Persona Roles section (~20 lines)
- `backend/copilot-instructions.md`: Updated PII, auth activation, CORS hardening, error handling sections (~40 lines)
- `frontend/copilot-instructions.md`: New linting section, replaced testing section, updated PII and error handling sections (~80 lines)
- No code changes — instruction files only
- No dependency changes
