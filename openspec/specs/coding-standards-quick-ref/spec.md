# Coding Standards Quick Reference

## Purpose

Developer-facing quick-reference guide for coding standards, separate from the review-focused checklist, providing scannable Do/Don't examples for active development.

## Requirements

### Requirement: Quick-reference document exists
The project SHALL have a `CODING_STANDARDS.md` file at the repository root that provides a scannable, concise reference for coding standards applicable during active development.

#### Scenario: Developer consults standards during coding
- **WHEN** a developer opens `CODING_STANDARDS.md`
- **THEN** they find a concise document (under 300 lines) organized by topic with code snippets showing correct and incorrect patterns

### Requirement: Backend standards section
The quick-reference SHALL include a backend section covering: naming conventions, function size limits, type annotation requirements, async patterns, error handling patterns, FastAPI endpoint patterns, and testing patterns — each with a brief "Do / Don't" code example.

#### Scenario: Developer checks backend naming convention
- **WHEN** a developer looks up the naming section
- **THEN** they find examples of correct variable/function/class names and common mistakes to avoid

#### Scenario: Developer checks error handling pattern
- **WHEN** a developer looks up error handling
- **THEN** they find the service-exception-to-HTTPException pattern with a code snippet

### Requirement: Frontend standards section
The quick-reference SHALL include a frontend section covering: component patterns, hook patterns, TypeScript conventions, event handler naming, API call patterns, accessibility basics, and testing patterns — each with a brief "Do / Don't" code example.

#### Scenario: Developer checks component pattern
- **WHEN** a developer looks up the component section
- **THEN** they find the named-export, typed-props, destructured-params pattern with example code

#### Scenario: Developer checks hook pattern
- **WHEN** a developer looks up the hook section
- **THEN** they find the return-object, explicit-return-type, dependency-array pattern with example code

### Requirement: Git and PR standards section
The quick-reference SHALL include a section on commit message format, branch naming, and PR checklist expectations with examples of correct commit messages.

#### Scenario: Developer checks commit message format
- **WHEN** a developer looks up the commit section
- **THEN** they find the structured release notes format with a concrete example

### Requirement: CI checks reference section
The quick-reference SHALL include a section listing all CI checks with their fix commands, so developers can resolve failures locally before pushing.

#### Scenario: Developer fixes a failing CI check
- **WHEN** a developer's PR fails a CI check
- **THEN** they find the fix command for that check in the quick-reference (e.g., `cd backend && ruff check . --fix && ruff format .`)
