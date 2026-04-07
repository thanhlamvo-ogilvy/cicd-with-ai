# Copilot Instructions

## Project Structure

This is a monorepo with two workspaces. Each has its own coding standards:

- **`backend/`** — Python FastAPI API → see [`backend/copilot-instructions.md`](../backend/copilot-instructions.md)
- **`frontend/`** — React 19 + TypeScript + Vite UI → see [`frontend/copilot-instructions.md`](../frontend/copilot-instructions.md)

When working in a specific workspace, follow that workspace's instructions. This file covers shared, cross-workspace standards.

## Quick Start

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload        # http://localhost:8000

# Frontend
cd frontend
npm install
npm run dev                          # http://localhost:5173

# Docker (both)
docker compose up --build
```

## Git Workflow

- Never commit directly to `main` — always create a feature branch and open a PR.
- Keep PRs focused — one logical change per PR.
- All CI checks (ruff, mypy, bandit, pytest) must pass before merge. At least one human approval is required.

## Git Commit Message Format

All commit messages must follow this structured release notes format:

```
[Primary Change Description]; [Secondary Changes] & more…

{PackageName}
- [Action verb] [concise description of change ≤ 120 chars]
- [Action verb] [another change description]

{AnotherPackage}
- [Action verb] [change description]

(No dependency updates.)
```

**Rules:**
1. **Title line** — Lead with the most newsworthy change; end with `& more…` if multi-topic; no trailing period
2. **Group changes** under curly-brace headers (`{PkgName}`) — common buckets: `{Dependencies}`, `{Makefile}`, `{Requests}`, `{Docs}`, `{ServiceName}`, `{Backend}`, `{Frontend}`
3. **Bullet points** — Start with present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); keep ≤ 120 characters; no periods
4. **Dependencies** — If no dependency updates, include literal line `(No dependency updates.)` after last section
5. **No attribution tags** — Never add co-authored-by trailers or generator attribution

## Security (Cross-Cutting)

- Never hardcode secrets, API keys, passwords, or tokens — load from environment variables.
- Never use `eval()`, `exec()`, or similar dynamic execution in any language.
- CORS origins must be explicitly listed — never use `*` in production.
- No path traversal, SSRF, or injection vulnerabilities.
- Never expose internal details (stack traces, DB errors, file paths) in production error responses.
- Never log sensitive data: passwords, tokens, secrets, PII.

## CI/CD

The `ai-review.yml` workflow runs on PRs to `main` (backend CI jobs run from the `backend/` directory):

1. Ruff lint + format check
2. Mypy type check
3. Bandit security scan
4. Pytest
5. Requests code review automatically
6. Posts a summary comment

All checks (1–4) are required to pass before merge. Review guidelines are in `.github/copilot-review-instructions.md`.
