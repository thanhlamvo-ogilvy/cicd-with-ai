# Copilot Instructions

## Build & Run

```bash
pip install -e ".[dev]"          # install with dev extras (pytest, ruff, bandit, etc.)
uvicorn app.main:app --reload    # dev server at http://localhost:8000
```

Docker alternative:

```bash
docker compose up --build
docker compose exec app alembic upgrade head
```

## Test

```bash
pytest                                        # all tests
pytest tests/test_items.py                    # one file
pytest tests/test_items.py::test_create_item  # one test
pytest --cov=app --cov-report=term-missing    # with coverage
```

Tests use in-memory SQLite (`aiosqlite`) — no external services needed. The `conftest.py` auto-creates/drops tables per test and provides a `client` fixture (httpx `AsyncClient` via `ASGITransport`).

## Lint & Format

```bash
ruff check . --fix && ruff format .   # fix lint + format
ruff check .                          # lint only
mypy app/                             # static type check
bandit -r app/ -c pyproject.toml      # security scan
pre-commit run --all-files            # all pre-commit hooks (ruff + mypy)
```

Ruff config: line-length 100, target Python 3.12, double quotes. Security rules (`S`) and annotation rules (`ANN`) are ignored in tests.

## Coding Standard

The project enforces these standards automatically via ruff, mypy, and CI. All code generated or modified must comply — CI will block merge on any violation.

### Type Safety

- All functions must have parameter and return type annotations (ruff `ANN`, mypy `--strict`). Tests are exempt.
- Use `Mapped` type annotations for SQLAlchemy models, `Field()` constraints for Pydantic schemas.

### Naming & Formatting

- PEP 8 naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants (ruff `N`).
- Double quotes, 100-char line length, auto-sorted imports (ruff format + `I`).
- Simplify code: no unnecessary `else` after `return`, no unnecessary variable assignments before `return` (ruff `RET`, `SIM`).

### Security

- Never hardcode secrets, API keys, passwords, or tokens. Load from environment variables via `settings`.
- All user input must be validated through Pydantic schemas — never accept raw dicts.
- SQL queries must use SQLAlchemy ORM/Core with parameterised statements — never use f-strings or string interpolation in SQL.
- Passwords must be hashed with bcrypt via `passlib`. JWT secrets must come from `settings.secret_key`.
- CORS origins must be explicitly listed — never use `*` in production.
- Never use `eval()`, `exec()`, or similar dynamic execution.
- No path traversal, SSRF, or injection vulnerabilities.

### Async Rules

- Use `async`/`await` consistently — never use sync blocking calls (`time.sleep`, `requests.get`, sync file I/O) inside async functions.
- All database access must be async (`asyncpg` for Postgres, `aiosqlite` for tests).

### FastAPI Patterns

- Set `response_model` on every endpoint to control serialization.
- Return `status_code=201` for `POST` creation endpoints, `status_code=204` for `DELETE` (no body).
- Use `Annotated` type aliases for dependency injection (e.g., `DbSession = Annotated[AsyncSession, Depends(get_db)]`).
- Group related routes into `APIRouter` instances — never add routes directly to the `app` object.
- Raise `HTTPException` in the API layer. Services/business logic should raise plain Python exceptions.
- Database sessions must be obtained via the `get_db` dependency — never instantiate sessions manually in routes.
- Validate path/query parameters with `Field` constraints in Pydantic models or `Query`/`Path` helpers.
- Use lifespan context managers for startup/shutdown — not the deprecated `on_event`.

### Testing

- Every new endpoint must have at least one positive and one negative test case.
- Tests use the async `httpx.AsyncClient` with `ASGITransport` — no real network calls.
- Use the `client` and `db_session` fixtures from `conftest.py`. Fixtures auto-clean DB state per test.
- Use `@pytest.mark.asyncio` for async tests. Prefer fixtures over setup/teardown (ruff `PT`).
- Do not skip tests with `pytest.mark.skip` without a comment explaining why.
- Tests must assert actual behavior — no empty or trivially-passing assertions.

### Code Reuse

- Before writing new code, check if existing services/utilities already provide the functionality.
- Do not duplicate logic that exists in `app/services/`.
- Verify library APIs actually exist — do not use non-existent function signatures.

### Error Handling

- Define domain-specific exceptions in the service layer (e.g., `ItemNotFoundError`). Routes catch them and map to `HTTPException`.
- Never let raw Python exceptions (e.g., `ValueError`, `KeyError`) leak to the client — always return structured JSON error responses.
- Use a consistent error response shape: `{"detail": "message"}` for single errors, `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}` for validation errors (FastAPI default).
- Log errors with structured context (`structlog`) before returning error responses.
- Never expose internal details (stack traces, DB errors, file paths) in production error responses.

### Logging

- Use `structlog.get_logger(__name__)` — never `print()` or stdlib `logging` directly.
- Log at appropriate levels: `info` for business events (created, updated, deleted), `warning` for recoverable issues, `error` for failures.
- Bind structured context to log entries: `log.info("item_created", item_id=item.id)` — not string formatting.
- Never log sensitive data: passwords, tokens, secrets, full request bodies containing PII.
- Log on entry/exit of significant operations (API requests, external calls) to aid debugging.

### Schema Design

- Follow the Base/Create/Update/Response pattern for every resource:
  - `XxxBase` — shared fields (used as parent for Create and Response)
  - `XxxCreate(XxxBase)` — fields needed to create (no `id`, no timestamps)
  - `XxxUpdate(BaseModel)` — all fields optional for partial updates
  - `XxxResponse(XxxBase)` — includes `id`, timestamps, `model_config = ConfigDict(from_attributes=True)`
  - `XxxListResponse` — wraps a list with pagination metadata (`items`, `total`, `skip`, `limit`)
- Use `payload.model_dump(exclude_unset=True)` for partial updates so unset fields are not overwritten with `None`.

### Git Workflow

- Never commit directly to `main` — always create a feature branch and open a PR.
- Keep PRs focused — one logical change per PR.
- All CI checks (ruff, mypy, bandit, pytest) must pass before merge. At least one human approval is required.

### Git Commit Message Format

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
2. **Group changes** under curly-brace headers (`{PkgName}`) — common buckets: `{Dependencies}`, `{Makefile}`, `{Requests}`, `{Docs}`, `{ServiceName}`
3. **Bullet points** — Start with present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); keep ≤ 120 characters; no periods
4. **Dependencies** — If no dependency updates, include literal line `(No dependency updates.)` after last section
5. **No attribution tags** — Never add co-authored-by trailers or generator attribution

**Example:**
```
Add mypy strict type checking; Expand ruff lint rules & more…

{CI}
- Add Mypy Type Check job to CI workflow
- Update branch protection to require mypy as a required status check

{Config}
- Expand ruff rules with ANN, N, RET, SIM, PT rule sets
- Add mypy strict mode with pydantic plugin to pyproject.toml

{Dependencies}
- Add mypy>=1.10.0 to dev dependencies
```

### Dependency Injection

- Define reusable `Annotated` type aliases for common dependencies at the top of route files:
  ```python
  DbSession = Annotated[AsyncSession, Depends(get_db)]
  ```
- Compose dependencies — build complex ones from simple ones rather than creating monolithic dependency functions.
- Never store mutable state in module-level variables that dependencies read — use `settings` or the DI system.

All rules are defined in `pyproject.toml` under `[tool.ruff]` and `[tool.mypy]`. The full review checklist is in `.github/copilot-review-instructions.md`.

## Database Migrations

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
```

New ORM models must be imported in `app/models/__init__.py` so Alembic's autogenerate detects them. The alembic `env.py` reads `DATABASE_URL` from `app.core.config.settings`, overriding `alembic.ini`.

## Architecture

This is an async FastAPI app with a layered structure:

- **Routes** (`app/api/routes/`) — Thin HTTP handlers. Use `Annotated` type aliases for dependency injection (e.g., `DbSession`). Must set `response_model`, correct `status_code`, and delegate to services.
- **Services** (`app/services/`) — Business logic. Receive an `AsyncSession`, perform queries, raise `HTTPException` for not-found. Use `flush()` + `refresh()` instead of `commit()` — the `get_db` dependency handles commit/rollback.
- **Models** (`app/models/`) — SQLAlchemy 2.0 `DeclarativeBase` with `Mapped` type annotations. All models re-exported from `app/models/__init__.py`.
- **Schemas** (`app/schemas/`) — Pydantic v2 models with `ConfigDict(from_attributes=True)` for ORM serialization. Use `Field()` constraints for validation.
- **Config** (`app/core/config.py`) — `pydantic-settings` `BaseSettings` loading from `.env`. Access via the singleton `settings` instance.

The app is created via `create_app()` factory in `app/main.py`. Swagger UI is disabled in production.

## Key Conventions

- Services call `db.flush()` / `db.refresh()`, not `db.commit()`. The `get_db` dependency auto-commits on success and rolls back on exception.
- Structured logging via `structlog` — console format in dev, JSON in production.
- API routes are versioned under `/api/v1/`. Health check is at `/health` (no version prefix).
- JWT auth utilities exist in `app/core/security.py` (HS256 + bcrypt) but are not yet wired into routes.
- `test_demo.py` contains intentional failures for CI demo purposes — do not fix or merge to main.

## CI/CD

The `ai-review.yml` workflow runs on PRs to `main`:

1. Ruff lint + format check
2. Mypy type check
3. Bandit security scan
4. Pytest
5. Requests code review automatically
6. Posts a summary comment

All checks (1–4) are required to pass before merge. Review guidelines for Copilot PR reviews are in `.github/copilot-review-instructions.md`.
