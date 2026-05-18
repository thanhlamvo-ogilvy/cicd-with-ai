## Context

Persona assignment rules currently exist but are optimized for simple single-workspace edits. Recent workflows include mixed backend/frontend changes, review-only requests, and cross-cutting root updates in the same session. Without explicit precedence rules, guidance may become inconsistent across files and review outputs.

Constraints:
- Must align with current monorepo structure (`backend/`, `frontend/`, root/.github/shared).
- Must preserve existing persona behavior for single-scope tasks.
- Must avoid introducing process overhead in common workflows.

## Goals / Non-Goals

**Goals:**
- Define deterministic persona activation and conflict resolution across mixed scopes.
- Ensure review-only tasks select persona based on reviewed file paths.
- Keep instruction and review docs synchronized with clear precedence rules.
- Make behavior testable through explicit scenarios in spec files.

**Non-Goals:**
- Introducing new AI personas beyond existing backend/frontend/devops roles.
- Implementing runtime persona detection in external tooling.
- Changing code generation style guides outside persona-activation scope.

## Decisions

### Decision 1: File-path-first activation model
Use file path as primary selector for persona activation. For mixed-scope tasks, apply scoped guidance per touched file group rather than selecting one global persona.

Alternatives considered:
- Single global persona per task: rejected because mixed changes cause rule conflicts.
- User-selected manual persona every task: rejected for extra friction and inconsistency.

### Decision 2: Workspace rule precedence over root standards for workspace files
When root/shared guidance conflicts with workspace guidance, workspace-specific rules win for files inside that workspace; root guidance remains authoritative for shared files.

Alternatives considered:
- Root-first precedence: rejected because it weakens specialized backend/frontend constraints.
- Merge-all precedence: rejected because ambiguous outcomes are hard to verify.

### Decision 3: Review workflow uses reviewed-path persona
For review-only operations, derive persona from paths under review to maintain consistent quality and defect detection in domain-specific files.

Alternatives considered:
- Always use cross-cutting reviewer persona: rejected because domain-specific issues are missed.

## Risks / Trade-offs

- [Risk] Mixed-scope responses may be longer due to scoped guidance per workspace.
  -> Mitigation: Keep output segmented and concise by file group.

- [Risk] Existing docs may drift if precedence rules are duplicated.
  -> Mitigation: Keep canonical rules in root instructions and reference them from review guidance.

- [Risk] Ambiguous tasks without file paths may still produce inconsistent behavior.
  -> Mitigation: Require clarification or default to cross-cutting analysis with explicit limitation.

## Migration Plan

1. Update persona-role specs with new multi-scope and review-only requirements.
2. Update instruction docs (`.github/copilot-instructions.md`, workspace files if needed) to encode precedence rules.
3. Update review instructions to validate persona activation based on reviewed paths.
4. Verify no contradictory statements remain across instruction files.

Rollback strategy:
- Revert doc/spec updates to previous commit if downstream workflow quality regresses.

## Open Questions

- Should we require explicit output section labels for mixed-scope responses, or leave format flexible?
- Do we need a lightweight checklist item in PR templates to confirm persona-path mapping was followed?

## Change Summary

### Behavior Changes

1. **Mixed-scope tasks now use scoped guidance per file group** — previously, a single global persona could be applied to a mixed backend/frontend task. Now, backend persona rules apply to backend files and frontend persona rules apply to frontend files within the same task.

2. **Review-only tasks derive persona from reviewed file paths** — previously, reviews could default to a generic reviewer role. Now, the persona is selected based on the paths under review, matching the same file-path-first activation used for code generation.

3. **Workspace standards override root for workspace files** — explicitly codified that when root-level and workspace-specific standards conflict, the workspace standard takes precedence for files inside that workspace. Root standards remain authoritative for shared files.

4. **No file-path context requires clarification** — when a task lacks concrete file paths, the system must request clarification or default to cross-cutting analysis rather than fabricating workspace scope.

### Rationale

These changes make persona activation deterministic and predictable across all task types. The file-path-first model eliminates ambiguity in mixed-scope scenarios and ensures domain-specific quality standards are applied consistently during both code generation and review.

### Files Modified

- `.github/copilot-instructions.md` — Added "Persona Activation & Precedence" subsection with 7 numbered rules
- `.github/copilot-review-instructions.md` — Added "Persona-Path Selection for Reviews" section referencing root precedence rules
