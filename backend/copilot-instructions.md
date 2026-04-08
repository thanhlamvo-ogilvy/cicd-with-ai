# Backend Copilot Instructions

> Python 3.12 · FastAPI · SQLAlchemy 2.0 · Pydantic v2
>
> See also: shared standards in [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) (SOLID, Clean Code, Git, Security)

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

### Design for Testability (Michael Feathers)

- Dependencies must be **injected**, not hardcoded — use FastAPI `Depends`, never instantiate services/sessions inline.
- Side effects (DB, API calls, file I/O) must be isolated behind **seams** — abstractions/interfaces that can be swapped in tests (e.g., `AIProvider` base class, `get_db` dependency override).
- No hidden state or global mutable state — use `settings` singleton for config, DI for everything else.
- Functions must be **pure** where possible — same input produces same output, no side effects.
- Complex logic must be extracted into small, independently testable units — not buried inside route handlers.
- New code must not be "legacy on arrival" — every new code path must have a test.

### TDD Compliance (Kent Beck)

- Tests should be written before or alongside production code: **Red → Green → Refactor**.
- Every new or changed function must have a corresponding unit test.
- Tests must follow the **AAA pattern**: Arrange → Act → Assert.
- Test names must describe *what* is tested and the *expected outcome*: `test_create_item_returns_201_with_valid_payload`.
- Code coverage must meet the team threshold (target: 80%+).

### Test Pyramid (Martin Fowler)

- **Unit tests (base)** — fast, isolated, cover all logic branches. Mock DB sessions and external services.
- **Integration tests (middle)** — verify modules work together. Use the in-memory SQLite test DB with `conftest.py` fixtures.
- **E2E tests (top)** — minimal, cover critical user journeys only. Do not over-invest here.
- No inverted pyramid — if you have more slow integration tests than fast unit tests, refactor.
- Mocks/stubs at the unit level, real dependencies (test DB) at the integration level.

### The Beyoncé Rule (Google)

- *If you liked it, you should have put a test on it.* Any behavior you rely on must be covered by a test.
- Tests must be **deterministic** — no flaky dependencies on time, network, order, or external services.

### Testing Standards

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

### Performance

- No N+1 queries — use `selectinload` / `joinedload` for relationships.
- Use pagination for all list endpoints — never return unbounded result sets.
- Avoid unnecessary loops over large collections — use SQL aggregations where possible.
- No resource leaks — ensure async sessions, connections, and file handles are properly closed.
- Consider caching for expensive or frequently-repeated queries.

### Code Reuse

- Before writing new code, check if existing services/utilities already provide the functionality.
- Do not duplicate logic that exists in `app/services/`.
- Verify library APIs actually exist — do not use non-existent function signatures.

### Error Handling & Resilience

- Use `tenacity` for retry logic with exponential backoff on external API calls (e.g., AI providers).
- Set timeouts on all external HTTP calls (`httpx` timeout parameter) — never allow unbounded waits.
- Implement circuit breaker pattern for AI provider calls — fail fast when a provider is down.
- Use dead letter patterns for failed async jobs or messages that cannot be processed.
- Log all caught exceptions with full context (`structlog` bindings) before re-raising or returning error responses.
- Never use bare `except:` — always catch specific exception types.
- Graceful degradation: if an AI provider fails, return an appropriate error response — don't crash the app.

### API Design

- All endpoints under `/api/v1/` — version prefix required. See also: shared standards in `.github/copilot-instructions.md`.
- Use OpenAPI/Swagger auto-generated docs (FastAPI provides this by default at `/docs`).
- Implement pagination for all list endpoints using `limit`/`offset` or cursor-based patterns.
- Return consistent error format: `{"detail": "message"}` for all error responses.
- Use appropriate HTTP status codes: `200` OK, `201` Created, `204` No Content, `400` Bad Request, `404` Not Found, `422` Validation Error, `500` Internal Server Error.
- Idempotency: `POST` endpoints that create resources should handle duplicate submissions gracefully.
- Rate limiting should be considered for public-facing endpoints.

### Database & Data Integrity

- All migrations must have both `upgrade()` and `downgrade()` functions — no irreversible migrations.
- Test migrations against a staging/test database before applying to production.
- Add database indexes for columns used in `WHERE` clauses and `JOIN` conditions.
- Use `selectinload`/`joinedload` to avoid N+1 queries on relationships.
- Wrap multi-step operations in transactions (`get_db` dependency handles commit/rollback).
- Schema changes must be backward-compatible: use the expand-then-contract pattern.
- Never delete columns/tables immediately — deprecate first, remove in the next release.
- Sensitive data (passwords, tokens) must be hashed/encrypted before storage.

### Data Privacy & Compliance

- Identify PII fields in models and document them. See also: shared standards in `.github/copilot-instructions.md`.
- Never log PII (user emails, names, IP addresses) — use structured logging with PII filtering.
- Implement data retention: add `created_at` timestamps to all models for lifecycle management.
- Support user data deletion: design models so user data can be purged without breaking referential integrity.
- Encrypt sensitive data at rest (database-level encryption or application-level for specific fields).
- API responses must not leak internal IDs or system details unnecessarily.

### Observability

- Use `structlog` for structured JSON logging in production — console output in development.
- Include correlation/request IDs in all log entries (middleware should inject these).
- Log at appropriate levels: `info` for business events, `warning` for recoverable issues, `error` for failures.
- Add metrics for: request rate, error rate, response duration (RED method).
- Create health check endpoint at `/health` with dependency checks (DB connectivity).
- Never log sensitive data: passwords, tokens, API keys, PII.

### Dependency Management

- All dependencies declared in `pyproject.toml` with version constraints.
- Dev dependencies in `[project.optional-dependencies.dev]`.
- Run `pip audit` or use Dependabot for vulnerability scanning.
- Prefer well-maintained libraries with active communities.
- Pin major versions, allow minor/patch updates: `fastapi>=0.100,<1.0`.

### SOLID in Practice (Python/FastAPI)

- **SRP**: Routes handle HTTP only (parse request, call service, return response). Services handle business logic. Models define data structure. Never mix concerns — a route should not contain SQL queries or business rules.
- **OCP**: Use the `AIProvider` abstract base class pattern — add new providers by creating new classes, not modifying existing ones. Use strategy pattern via dependency injection for swappable behaviors.
- **LSP**: All `AIProvider` subclasses must implement the full `stream_chat` contract. If a subclass can't support an operation, raise `NotImplementedError` with a clear message — never silently return wrong data.
- **ISP**: Keep Pydantic schemas focused — split `XxxCreate`, `XxxUpdate`, `XxxResponse` instead of one monolithic model. Route dependencies should only require what they use.
- **DIP**: Depend on `AIProvider` ABC, not `OpenAIProvider` directly. Use FastAPI `Depends()` to inject `AsyncSession`, services, and config — never import and instantiate directly.

### Security (OWASP for Python)

- SQL injection: always use SQLAlchemy ORM/Core with bound parameters — never interpolate user input into queries with f-strings or `.format()`.
- Input validation: all request bodies MUST pass through Pydantic schemas — never use `dict` or `**kwargs` from raw request data.
- Authentication: use `Depends()` for auth middleware — protect routes at the decorator level, not inside handler bodies.
- CORS: configure `CORSMiddleware` with explicit `allow_origins` list from `settings` — never use `["*"]` in production.
- Rate limiting: use `slowapi` or middleware-based rate limiting for public endpoints.
- Secrets: all secrets via `pydantic-settings` from environment variables — never in source code, comments, or default values.
- File uploads: validate file type, size, and content — never trust `Content-Type` header alone.
- Dependency scanning: run `bandit -r app/` in CI and `pip-audit` for known CVEs.

### Internationalization (i18n)

- API error messages should use error codes (not localized strings) — let the client handle translation.
- Accept `Accept-Language` header for content negotiation where applicable.
- Store all timestamps as UTC in the database — use `datetime.datetime.now(datetime.UTC)`, never `datetime.now()`.
- Use `babel` or `gettext` for server-side string localization if needed (e.g., email templates).
- Number and currency formatting should respect locale when generating reports or exports.

### Deployment

- Use multi-stage Docker builds: separate build stage (install deps) from runtime stage (copy app only).
- Run `uvicorn` with `--workers` in production (not `--reload`) — worker count = `2 * CPU cores + 1`.
- Configure health check at `/health` that verifies DB connectivity and returns `200` or `503`.
- Use `lifespan` context manager for startup (DB pool, connections) and shutdown (cleanup, drain) — not deprecated `@app.on_event`.
- Environment variables for all config: `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS`, `LOG_LEVEL` — never hardcode.
- Pin Python version in `Dockerfile` and `pyproject.toml` (`requires-python = ">=3.12"`).
- Use `.dockerignore` to exclude tests, docs, `.git`, `__pycache__`, `.env` from image.
- Graceful shutdown: handle `SIGTERM` — finish in-flight requests before exiting.

### Documentation

- Use Google-style docstrings for all public functions, classes, and modules.
- Example:
  ```python
  async def create_item(db: AsyncSession, payload: ItemCreate) -> Item:
      """Create a new item in the database.

      Args:
          db: Async database session.
          payload: Validated item creation data.

      Returns:
          The newly created Item with generated ID.

      Raises:
          HTTPException: If item with same name already exists.
      """
  ```
- Enrich FastAPI endpoints with `summary`, `description`, and `response_description` parameters for better OpenAPI docs.
- Add `example` values in Pydantic `Field()` definitions — these appear in Swagger UI.
- Module-level docstrings for non-obvious modules — explain purpose and key abstractions.
- Keep README and `copilot-instructions.md` in sync with actual architecture and commands.

### Developer Experience (DX)

- `pip install -e ".[dev]"` installs all dev dependencies (ruff, mypy, pytest, bandit) in one command.
- Use `--reload` flag during development — uvicorn watches for file changes.
- Debug with `import pdb; pdb.set_trace()` or use VS Code's Python debugger with launch.json targeting uvicorn.
- Use `ruff check . --fix && ruff format .` as a pre-commit step — automate with git hooks or `pre-commit`.
- Profile slow endpoints with `cProfile` or `py-spy` — don't guess at performance issues.
- Use `httpie` or `curl` for quick API testing — Swagger UI at `/docs` for interactive exploration.
- Keep `conftest.py` fixtures simple and composable — new tests should work with minimal setup.

## Database Migrations

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
```

New ORM models must be imported in `app/models/__init__.py` so Alembic's autogenerate detects them. Migrations must be safe and reversible.

## Key Conventions

- Services call `db.flush()` / `db.refresh()`, not `db.commit()`. The `get_db` dependency auto-commits on success, rolls back on exception.
- Structured logging via `structlog` — console in dev, JSON in production.
- API routes versioned under `/api/v1/`. Health check at `/health` (no version prefix).
- JWT auth utilities in `app/core/security.py` (HS256 + bcrypt) — not yet wired into routes.
- `test_demo.py` contains intentional failures for CI demo — do not fix.
- All tool config is in `pyproject.toml` under `[tool.ruff]`, `[tool.mypy]`, `[tool.bandit]`.
