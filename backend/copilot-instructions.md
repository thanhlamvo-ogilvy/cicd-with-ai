<!--
Backend-specific coding standards for Python 3.12 + FastAPI + SQLAlchemy 2.0 + Pydantic v2.
Use alongside shared standards: SOLID, Clean Code, Git, Security in `.github/copilot-instructions.md`.
Key: Type safety enforced (ANN, mypy strict). All code in CI blocks merge on violations (ruff, mypy, bandit, pytest).
-->

# Backend Copilot Instructions

> Python 3.12 · FastAPI · SQLAlchemy 2.0 · Pydantic v2
> See: shared standards in [`.github/copilot-instructions.md`](../.github/copilot-instructions.md)

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

### Design for Testability

- Inject dependencies; never hardcode (use FastAPI `Depends`)
- Isolate side effects behind seams (DB, API calls, file I/O) with abstractions
- No hidden state; use `settings` singleton for config
- Pure functions where possible; extract complex logic into small, independently testable units
- Every new code path must have a test

### TDD Compliance

- Red → Green → Refactor: write tests before/alongside code
- AAA pattern: Arrange → Act → Assert
- Test names describe what and expected outcome: `test_create_item_returns_201_with_valid_payload`
- Target coverage: 80%+

### Test Pyramid

- **Unit tests**: fast, isolated, mock DB/services
- **Integration tests**: test together with test DB + fixtures
- **E2E tests**: minimal, critical paths only
- No inverted pyramid; many fast unit tests at base

### The Beyoncé Rule

- If you relied on it, test it. Tests must be deterministic (no flaky time/network/order dependencies).

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

- Use `Annotated` type aliases at top of route files (`DbSession = Annotated[AsyncSession, Depends(get_db)]`)
- Compose dependencies from simple ones; never hardcode instantiation
- Never store mutable state in module-level variables

### Performance

- No N+1 queries; use `selectinload` / `joinedload` on relationships
- Paginate all list endpoints
- Use SQL aggregations instead of loops
- Close all resources (sessions, connections, files)
- Cache expensive/repeated queries

### Code Reuse

- Check existing services/utilities before writing new code
- Never duplicate logic in `app/services/`
- Verify library APIs exist; don't use non-existent signatures

### Error Handling & Resilience

- Use `tenacity` for retry logic with exponential backoff on external calls
- Set timeouts on all external HTTP calls; never allow unbounded waits
- Circuit breaker pattern for AI provider calls (fail fast)
- Dead letter patterns for failed async jobs
- Log all exceptions with context before re-raising
- Never bare `except:`; catch specific types only
- Graceful degradation: fail cleanly, return proper error responses

### API Design

- All endpoints under `/api/v1/` (version prefix required)
- OpenAPI/Swagger auto-generated at `/docs`
- Paginate all list endpoints with `limit`/`offset` or cursor
- Consistent error format: `{"detail": "message"}` for all errors
- HTTP status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found, 422 Validation Error, 500 Internal Server Error
- Idempotency: `POST` endpoints handle duplicate submissions gracefully
- Rate limiting for public endpoints

### Database & Data Integrity

- Migrations: both `upgrade()` and `downgrade()` functions; test before production
- Index columns used in WHERE/JOIN
- Use `selectinload`/`joinedload` to avoid N+1 queries
- Wrap multi-step ops in transactions; `get_db` handles commit/rollback
- Schema changes: backward-compatible (expand-then-contract)
- Never delete columns/tables immediately; deprecate first
- Hash/encrypt sensitive data (passwords, tokens) before storage

### Data Privacy & Compliance

- Identify PII fields in models and document them. See also: shared standards in `.github/copilot-instructions.md`.
- Never log PII (user emails, names, IP addresses) — use structured logging with PII filtering.
- Implement data retention: add `created_at` timestamps to all models for lifecycle management.
- Support user data deletion: design models so user data can be purged without breaking referential integrity.
- Encrypt sensitive data at rest (database-level encryption or application-level for specific fields).
- API responses must not leak internal IDs or system details unnecessarily.

#### AI Chat PII Rules

The following fields are classified as PII and require special handling:
- `Message.content` — user prompts and AI responses
- `Conversation.title` — may contain user-identifiable information
- Any user-identifiable metadata (IP addresses, user agent strings)

Rules:
- Log `conversation_id` and `message_id` for tracing — NEVER log `message.content` or any substring of user input.
- Message retention period MUST be configurable via `MESSAGE_RETENTION_DAYS` environment variable.
- Implement a purge mechanism for expired messages (cron job or management command).
- Support cascading user deletion: deleting a user MUST delete all their conversations and messages without breaking referential integrity (use `CASCADE` on foreign keys).
- AI provider API calls MUST NOT log request/response bodies — log only provider name, model, token count, and latency.

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

### SOLID in Practice

- **SRP**: Routes handle HTTP; services handle logic; models define data. Never mix.
- **OCP**: `AIProvider` ABC; add providers via new classes, not modifying existing
- **LSP**: All ABC subclasses implement full contract; raise `NotImplementedError` if unsupported
- **ISP**: Split schemas (`Create`, `Update`, `Response`); route deps require only what they use
- **DIP**: Depend on abstractions (ABC), not concrete classes; inject via `Depends()`

### Security (OWASP for Python)

- SQL injection: always use SQLAlchemy ORM/Core with bound parameters — never interpolate user input into queries with f-strings or `.format()`.
- Input validation: all request bodies MUST pass through Pydantic schemas — never use `dict` or `**kwargs` from raw request data.
- Authentication: use `Depends()` for auth middleware — protect routes at the decorator level, not inside handler bodies.
- CORS: configure `CORSMiddleware` with explicit `allow_origins` list from `settings` — never use `["*"]` in production. `allow_methods` MUST list specific HTTP methods (`["GET", "POST", "DELETE", "OPTIONS"]`) — never use `["*"]` in production.
- Rate limiting: use `slowapi` or middleware-based rate limiting for public endpoints.
- Secrets: all secrets via `pydantic-settings` from environment variables — never in source code, comments, or default values.
- File uploads: validate file type, size, and content — never trust `Content-Type` header alone.
- Dependency scanning: run `bandit -r app/` in CI and `pip-audit` for known CVEs.

### Internationalization (i18n)

- Use error codes (not localized strings); let client translate
- Accept `Accept-Language` header for content negotiation
- All timestamps UTC: `datetime.now(datetime.UTC)`, never `datetime.now()`
- Use `babel`/`gettext` for server-side strings if needed
- Respect locale for numbers/currency in exports

### Deployment

- Multi-stage Docker: build stage (install deps) → runtime stage (copy app)
- Production: `uvicorn --workers N` (where N = 2 * CPU cores + 1), no `--reload`
- Health check at `/health`: verify DB connectivity, return 200/503
- Use `lifespan` context manager for startup/shutdown
- All config via env vars: `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS`, `LOG_LEVEL`
- Pin Python version in Dockerfile + `pyproject.toml`
- Use `.dockerignore` to exclude tests, docs, `.git`, `__pycache__`, `.env`
- Graceful shutdown: finish in-flight requests before exit

### Documentation

- Google-style docstrings for public functions, classes, modules
- Enrich endpoints with `summary`, `description`, `response_description` for OpenAPI
- Add `example` values in Pydantic `Field()` definitions
- Module-level docstrings explaining purpose for non-obvious modules
- Keep README + `copilot-instructions.md` in sync with architecture

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

### Authentication Activation Plan

JWT auth code exists in `app/core/security.py` but is not yet wired into routes. When authentication is needed:

1. Create `app/api/dependencies/auth.py` with a `get_current_user` dependency using `Depends()` and `decode_access_token`.
2. Routes to protect: all `/api/v1/chat` and `/api/v1/conversations` endpoints. Health check (`/health`) and docs remain public.
3. Toggle mechanism: use `AUTH_ENABLED` environment variable (default: `false`). When disabled, routes skip auth checks. When enabled, all protected routes require a valid JWT Bearer token.
4. Auth middleware must be at the route decorator level (`Depends(get_current_user)`) — never inside handler bodies.
