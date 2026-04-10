## ADDED Requirements

### Requirement: ESLint configuration

The frontend workspace SHALL have an ESLint configuration that enforces TypeScript-aware linting rules aligned with the existing coding standards in `frontend/copilot-instructions.md`.

#### Scenario: ESLint catches type-unsafe code

- **WHEN** a developer or AI agent writes TypeScript code using `any` type without justification
- **THEN** ESLint SHALL report an error for `@typescript-eslint/no-explicit-any`

#### Scenario: ESLint catches React anti-patterns

- **WHEN** code uses `dangerouslySetInnerHTML` or missing hook dependencies
- **THEN** ESLint SHALL report errors via `react-hooks/exhaustive-deps` and custom rules

#### Scenario: ESLint enforces import order

- **WHEN** imports are not sorted (React first, external libs, internal modules, types)
- **THEN** ESLint SHALL report and auto-fix import ordering

### Requirement: Prettier configuration

The frontend workspace SHALL have a Prettier configuration that enforces consistent formatting.

#### Scenario: Prettier formats on save

- **WHEN** a file is saved in the frontend workspace
- **THEN** Prettier SHALL format it with double quotes, 100-char line length, and trailing commas (matching backend ruff config)

### Requirement: Lint CI integration

The frontend linting SHALL be enforced in CI alongside the backend checks.

#### Scenario: CI blocks merge on lint violations

- **WHEN** a PR contains frontend code with ESLint errors
- **THEN** the CI pipeline SHALL fail and block the merge

### Requirement: Instruction file documents lint setup

The `frontend/copilot-instructions.md` SHALL contain a Lint & Format section with commands and configuration details.

#### Scenario: Lint commands documented

- **WHEN** a developer reads the frontend instruction file
- **THEN** they SHALL find `npx eslint .` and `npx prettier --check .` commands with explanations
