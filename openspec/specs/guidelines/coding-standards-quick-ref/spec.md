# Coding Standards Quick Reference

> Developer-facing quick-reference guide for coding standards — scannable Do/Don't examples for active development.

## Document Requirements

- The project MUST have a `CODING_STANDARDS.md` at the repository root — under 300 lines, organized by topic with code snippets showing correct and incorrect patterns

## Sections Required

### Backend
Covers: naming conventions, function size limits, type annotations, async patterns, error handling, FastAPI endpoint patterns, testing patterns — each with a Do/Don't code example.

Cross-references: `backend-ci-pipeline`, `backend-testing-standards`, `backend-api-design`, `backend-security-owasp`, `backend-observability`, `backend-schema-design`

### Frontend
Covers: component patterns, hook patterns, TypeScript conventions, event handler naming, API call patterns, accessibility basics, testing patterns — each with a Do/Don't code example.

Cross-references: `frontend-security`, `frontend-accessibility`, `frontend-resilience`

### Git & PR Standards
Covers: commit message format with a concrete example, branch naming, PR checklist expectations.

Cross-reference: `shared-git-workflow`

### CI Checks & Fix Commands
Lists all CI checks with local fix commands so developers can resolve failures before pushing:
- `cd backend && ruff check . --fix && ruff format .`
- `cd backend && mypy app/`
- `cd backend && bandit -r app/ -c pyproject.toml`
- `cd backend && pytest`

## Language Policy

All code, comments, docstrings, variable names, function names, class names, commit messages, and documentation MUST be written in English.
