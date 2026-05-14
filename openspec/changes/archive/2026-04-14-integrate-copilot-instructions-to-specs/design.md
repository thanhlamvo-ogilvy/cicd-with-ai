## Context

The project maintains coding standards in three `copilot-instructions.md` files: root (shared), backend (Python/FastAPI), and frontend (React/TypeScript). These files are comprehensive but exist outside the OpenSpec system. Currently only 7 specs exist, mostly covering frontend tooling and a few cross-cutting concerns. The majority of documented standards — backend CI, security, testing, API design, observability, error handling, git workflow — have no formal spec representation.

## Goals / Non-Goals

**Goals:**
- Formalize all major coding standard domains from copilot-instructions into OpenSpec specs
- Each spec captures verifiable, testable requirements (SHALL/MUST language)
- Specs organized by scope: `backend-*`, `frontend-*`, `shared-*`
- Coverage of backend-specific, frontend-specific, and cross-cutting standards

**Non-Goals:**
- Replacing or modifying the copilot-instructions.md files (they remain the authoring source)
- Creating specs for aspirational guidelines that cannot be verified (e.g., "code should be elegant")
- Duplicating content already covered by existing specs (ai-chat-pii, ai-persona-roles, frontend-ci-pipeline, frontend-linting, frontend-test-infrastructure, frontend-testing-setup)
- Adding specs for deployment, i18n, cost efficiency, or other domains not yet implemented in the codebase

## Decisions

### 1. One spec per domain, scoped by workspace prefix
Each spec covers a single domain (e.g., `backend-api-design`, `frontend-security`). The prefix (`backend-`, `frontend-`, `shared-`) mirrors how copilot-instructions are layered.

**Rationale**: Matches the existing spec naming convention (e.g., `frontend-ci-pipeline`). Makes it clear which workspace a spec applies to. Keeps specs focused and independently maintainable.

**Alternative considered**: Grouping all backend standards into one large spec. Rejected — too broad, harder to track and verify.

### 2. Extract only verifiable requirements
Only standards that can be checked (by CI, code review, or automated tools) become spec requirements. Aspirational guidance (e.g., "leave code cleaner than found") is omitted.

**Rationale**: Specs should drive testable tasks. Non-verifiable guidelines are useful in instructions but don't belong in specs.

### 3. Modified capability for coding-standards-quick-ref only
The only existing spec being modified is `coding-standards-quick-ref`, to add cross-references to the new specs. All other existing specs remain untouched.

**Rationale**: The quick-ref spec serves as an index; it should point to detailed specs. Other existing specs (ai-chat-pii, frontend-ci-pipeline, etc.) already cover their domains adequately.

### 4. Derive spec content from copilot-instructions, not invent new rules
Every requirement in a spec MUST trace back to a specific rule in one of the three copilot-instructions files. No new rules are introduced.

**Rationale**: This is a formalization effort, not a standards-creation effort. Keeps specs aligned with the existing documented consensus.

## Risks / Trade-offs

- **Spec drift** — Specs may fall out of sync with copilot-instructions if either is updated independently → Mitigation: Document that copilot-instructions are the source of truth; specs are derived views
- **Volume** — 12 new specs is a significant batch → Mitigation: Each spec is focused and concise; they can be reviewed incrementally
- **Over-specification** — Too-detailed specs become maintenance burden → Mitigation: Keep requirements at the "what" level, not "how"; focus on CI-enforceable or review-checkable rules
