## ADDED Requirements

### Requirement: Deterministic persona activation governance

The system SHALL define deterministic persona activation governance so persona selection is predictable across single-workspace, cross-workspace, and review-only tasks.

#### Scenario: Single-workspace priority
- **WHEN** all touched files are within a single workspace context
- **THEN** the persona mapped to that workspace MUST be activated for the task

#### Scenario: Shared-file with workspace file
- **WHEN** a task includes root/shared files and one workspace-specific path
- **THEN** the workspace-specific persona MUST govern workspace file changes and shared-file guidance MUST follow cross-cutting constraints

#### Scenario: No file-path context available
- **WHEN** the task lacks concrete file paths
- **THEN** the system MUST require explicit user clarification or default to cross-cutting analysis without fabricating workspace scope

### Requirement: Persona conflict resolution for mixed scopes

The system SHALL define conflict resolution rules for mixed scopes to avoid contradictory guidance.

#### Scenario: Backend and frontend rules conflict
- **WHEN** a recommendation is valid for one workspace but invalid for the other
- **THEN** the system MUST emit scoped guidance per workspace file path and MUST NOT apply one workspace rule globally

#### Scenario: Root standard conflicts with workspace standard
- **WHEN** a root-level standard and workspace standard conflict for a workspace file
- **THEN** the workspace standard MUST take precedence for that file while the root standard remains authoritative for shared files
