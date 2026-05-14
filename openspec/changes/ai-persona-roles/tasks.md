## 1. Spec and Rule Alignment

- [x] 1.1 Finalize delta spec updates for `ai-persona-roles` with multi-workspace and review-only scenarios
- [x] 1.2 Add and validate new capability spec `persona-activation-governance`
- [x] 1.3 Cross-check normative language (SHALL/MUST) and scenario formatting consistency

## 2. Instruction Updates

- [x] 2.1 Update `.github/copilot-instructions.md` with deterministic persona precedence rules
- [x] 2.2 Ensure workspace instruction files reference root precedence without duplicating conflicting guidance
- [x] 2.3 Add review-workflow persona-path selection rule in `.github/copilot-review-instructions.md`

## 3. Verification and Quality Gates

- [x] 3.1 Verify mixed-scope examples produce scoped backend/frontend guidance
- [x] 3.2 Verify review-only requests map persona by reviewed file path
- [x] 3.3 Run consistency audit across instruction and review files to remove contradictory statements

## 4. Documentation and Handoff

- [x] 4.1 Document behavior changes and rationale in the change summary
- [x] 4.2 Confirm `openspec status --change ai-persona-roles` reports apply-ready state
