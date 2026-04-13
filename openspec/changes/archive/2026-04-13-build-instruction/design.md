## Context

The project has three `copilot-instructions.md` files that are auto-loaded by the AI agent:
- `.github/copilot-instructions.md` (~300 lines) — shared cross-workspace standards
- `backend/copilot-instructions.md` (~300 lines) — Python/FastAPI rules
- `frontend/copilot-instructions.md` (~250 lines) — React/TypeScript rules

These files are well-structured but have specific gaps identified through codebase review:
1. Frontend has zero linting/formatting tooling (no ESLint, no Prettier)
2. Frontend testing section is a placeholder ("When Added")
3. PII rules are generic — no AI-chat-specific data handling
4. Backend CORS config (`allow_methods=["*"]`) contradicts its own rules
5. JWT auth exists in code but no activation plan in instructions
6. No AI persona role definition for context-appropriate code generation

All changes are to instruction files only — no application code changes.

## Goals / Non-Goals

**Goals:**
- Fill all identified gaps in the three instruction files
- Ensure every rule needed for compliant code generation exists in auto-loaded files
- Keep each file under 500 lines (the efficient range for AI context loading)
- Make rules concrete and actionable (commands, file paths, exact config) not abstract

**Non-Goals:**
- Creating separate `guidelines/` directory (decided against — causes rule fragmentation)
- Actually installing ESLint/Prettier/Vitest/Playwright (that's implementation, not instructions)
- Changing application code (CORS config, auth wiring) — only documenting what the rules are
- Rewriting existing sections that are already adequate

## Decisions

### Decision 1: Edit existing files, don't create new guideline files

**Choice:** Add new sections to the three existing `copilot-instructions.md` files.

**Alternatives considered:**
- Separate `guidelines/` directory with topic-specific files → Rejected because separate files are not auto-loaded, causing rule fragmentation and lower AI compliance
- Single monolithic instruction file → Rejected because workspace-specific rules belong in workspace-specific files

**Rationale:** `copilot-instructions.md` files are auto-loaded on every AI prompt. Rules in these files are guaranteed to be in context. Rules in separate files require explicit discovery and may be skipped.

### Decision 2: AI Persona Roles in root instruction file

**Choice:** Add persona definitions to `.github/copilot-instructions.md` (the shared file).

**Rationale:** Persona selection is cross-cutting — it applies before any workspace-specific rules. The root file is always loaded regardless of which workspace the agent is working in.

### Decision 3: Frontend linting matches backend conventions

**Choice:** Configure ESLint + Prettier with double quotes, 100-char line length, trailing commas — matching the backend's ruff config.

**Rationale:** Consistent formatting across the monorepo reduces cognitive switching. The backend already enforces these via ruff in `pyproject.toml`.

### Decision 4: Test Pyramid structure for frontend testing section

**Choice:** Document Vitest + RTL as the base (unit/component), Playwright as the top (E2E).

**Rationale:** The existing instruction files already reference the Test Pyramid principle. Frontend testing section must align with this — not just Playwright alone (which would be an inverted pyramid).

### Decision 5: PII rules reference specific model fields

**Choice:** Name exact fields (`Message.content`, `Conversation.title`) rather than abstract "PII data."

**Rationale:** Abstract rules get ignored. Naming specific fields makes the rule enforceable — the AI agent can check its own output against the list.

## Risks / Trade-offs

- **Instruction file length growth** → Each file grows ~30-80 lines. All stay under 500 lines. Monitor and consolidate if they approach the threshold.
- **Rules without enforcement tooling** → Frontend linting rules are documented but ESLint/Prettier aren't installed yet. Risk: rules exist but aren't enforced in CI until tooling is set up. Mitigation: tasks should note this as a follow-up.
- **Persona definition too rigid** → Fixed personas may not fit edge cases (e.g., full-stack refactor). Mitigation: define a "cross-cutting" persona as fallback.
