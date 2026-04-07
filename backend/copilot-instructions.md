# Backend Copilot Instructions

> Python 3.12 · FastAPI · SQLAlchemy 2.0 · Pydantic v2

## Build & Run

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload        # http://localhost:8000
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
```

Ruff config: line-length 100, target Python 3.12, double quotes. Security rules (`S`) and annotation rules (`ANN`) are ignored in tests.

## Architecture

Layered async FastAPI application:

- **Routes** (`app/api/routes/`) — Thin HTTP handlers. Delegate to services. Must set `response_model` and correct `status_code`.
- **Services** (`app/services/`) — Business logic. Receive `AsyncSession`, raise `HTTPException` for not-found. Use `flush()` + `refresh()` — the `get_db` dependency handles commit/rollback.
- **AI Providers** (`app/services/providers/`) — Pluggable streaming AI implementations (OpenAI, Anthropic, Google) behind the `AIProvider` abstract base class.
- **Models** (`app/models/`) — SQLAlchemy 2.0 `DeclarativeBase` with `Mapped` annotations. All models re-exported from `app/models/__init__.py`.
- **Schemas** (`app/schemas/`) — Pydantic v2 with `ConfigDict(from_attributes=True)`. Use `Field()` for validation.
- **Config** (`app/core/config.py`) — `pydantic-settings` loading from `.env`. Access via singleton `settings`.

## Coding Standard

Enforced by ruff, mypy, bandit, and CI. All code must comply — CI blocks merge on violations.

### Type Safety

- All functions must have parameter and return type annotations (ruff `ANN`, mypy `--strict`). Tests are exempt.
- Use `Mapped` type annotations for SQLAlchemy models, `Field()` constraints for Pydantic schemas.

### Naming & Formatting

- PEP 8 naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants (ruff `N`).
- Double quotes, 100-char line length, auto-sorted imports (ruff format + `I`).
- Simplify code: no unnecessary `else` after `return`, no unnecessary variable assignments before `return` (ruff `RET`, `SIM`).

### Security

- All user input must be validated through Pydantic schemas — never accept raw dicts.
- SQL queries must use SQLAlchemy ORM/Core with parameterised statements — never f-strings or string interpolation in SQL.
- Passwords must be hashed with bcrypt via `passlib`. JWT secrets must come from `settings.secret_key`.

### Async Rules

- Use `async`/`await` consistently — never use sync blocking calls (`time.sleep`, `requests.get`, sync file I/O) inside async functions.
- All database access must be async (`asyncpg` for Postgres, `aiosqlite` for tests).

### FastAPI Patterns

- Set `response_model` on every endpoint to control serialization.
- Return `status_code=201` for `POST` creation, `status_code=204` for `DELETE` (no body).
- Use `Annotated` type aliases for dependency injection:
  ```python
  DbSession = Annotated[AsyncSession, Depends(get_db)]
  ```
- Group related routes into `APIRouter` instances — never add routes directly to the `app` object.
- Raise `HTTPException` in the API layer. Services should raise plain Python exceptions.
- Database sessions must be obtained via the `get_db` dependency — never instantiate sessions manually.
- Use lifespan context managers for startup/shutdown — not the deprecated `on_event`.

### Testing

- Every new endpoint must have at least one positive and one negative test case.
- Tests use async `httpx.AsyncClient` with `ASGITransport` — no real network calls.
- Use the `client` and `db_session` fixtures from `conftest.py`. Fixtures auto-clean DB state per test.
- Use `@pytest.mark.asyncio` for async tests. Prefer fixtures over setup/teardown (ruff `PT`).
- Do not skip tests with `pytest.mark.skip` without a comment explaining why.
- Tests must assert actual behavior — no empty or trivially-passing assertions.

### Error Handling

- Define domain-specific exceptions in the service layer. Routes catch them and map to `HTTPException`.
- Never let raw Python exceptions leak to the client — always return structured JSON: `{"detail": "message"}`.
- Log errors with structured context (`structlog`) before returning error responses.

### Logging

- Use `structlog.get_logger(__name__)` — never `print()` or stdlib `logging` directly.
- Log levels: `info` for business events, `warning` for recoverable issues, `error` for failures.
- Bind structured context: `log.info("item_created", item_id=item.id)` — not string formatting.

### Schema Design

- Follow the Base/Create/Update/Response pattern for every resource:
  - `XxxBase` — shared fields (parent for Create and Response)
  - `XxxCreate(XxxBase)` — no `id`, no timestamps
  - `XxxUpdate(BaseModel)` — all fields optional for partial updates
  - `XxxResponse(XxxBase)` — includes `id`, timestamps, `model_config = ConfigDict(from_attributes=True)`
  - `XxxListResponse` — wraps a list with pagination metadata
- Use `payload.model_dump(exclude_unset=True)` for partial updates.

### Dependency Injection

- Define reusable `Annotated` type aliases at the top of route files.
- Compose dependencies — build complex ones from simple ones.
- Never store mutable state in module-level variables — use `settings` or the DI system.

### Code Reuse

- Before writing new code, check if existing services/utilities already provide the functionality.
- Do not duplicate logic that exists in `app/services/`.
- Verify library APIs actually exist — do not use non-existent function signatures.

## Database Migrations

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
```

New ORM models must be imported in `app/models/__init__.py` so Alembic's autogenerate detects them.

## Key Conventions

- Services call `db.flush()` / `db.refresh()`, not `db.commit()`. The `get_db` dependency auto-commits on success, rolls back on exception.
- Structured logging via `structlog` — console in dev, JSON in production.
- API routes versioned under `/api/v1/`. Health check at `/health` (no version prefix).
- JWT auth utilities in `app/core/security.py` (HS256 + bcrypt) — not yet wired into routes.
- `test_demo.py` contains intentional failures for CI demo — do not fix.
- All tool config is in `pyproject.toml` under `[tool.ruff]`, `[tool.mypy]`, `[tool.bandit]`.
