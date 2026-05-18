## Why

Persona guidance exists, but role activation and behavior boundaries are underspecified for mixed-file tasks and review-only workflows. This causes inconsistent code generation and review output quality across backend, frontend, and shared platform changes.

## What Changes

- Clarify persona activation rules when a task spans multiple workspace contexts.
- Define precedence rules for nested scopes (root/shared vs workspace-specific files).
- Add requirements for review-only tasks to ensure persona selection aligns with the file(s) under review.
- Standardize expected persona coverage in instruction files and verification criteria in review guidance.

## Capabilities

### New Capabilities
- `persona-activation-governance`: Rules for persona precedence, mixed-context tasks, and review-only workflows.

### Modified Capabilities
- `ai-persona-roles`: Expand requirements for persona activation order, conflict resolution, and non-announcement behavior in complex multi-file tasks.

## Impact

- Affected specs: `openspec/specs/ai-persona-roles/spec.md` and new capability spec for governance.
- Affected docs: root and workspace instruction documents, review instruction checklist.
- Process impact: more deterministic AI behavior and clearer review validation criteria.
