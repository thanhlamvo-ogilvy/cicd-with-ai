# AI Review Rules

The PR Agent AI reviewer runs on every pull request targeting `main`. It is configured via `.pr_agent.toml` and focuses exclusively on semantic, contextual, and cross-cutting concerns that automated tools cannot catch.

**Important**: The AI review is informational — it does not block merge. However, findings are expected to be addressed or explicitly dismissed with a reason in the PR thread.

---

## What the AI Reviewer Checks

### Architecture & API Design (blocking recommendation)

| Rule | Why | How to fix |
|------|-----|-----------|
| Route handlers must be thin — no business logic | Logic in routes can't be unit-tested without HTTP overhead | Move logic to a service function; route handler only calls service and returns response |
| All list endpoints must support pagination | Unbounded queries can OOM or time out in production | Add `limit: int = 10, offset: int = 0` query params; return `{"items": [...], "total": N}` |
| POST must return 201, DELETE must return 204 | HTTP status semantics — clients rely on these | Set `status_code=201` in `@router.post(...)`, return `Response(status_code=204)` for deletes |
| Every endpoint must declare `response_model` | Without it, FastAPI serializes raw ORM objects and may leak internal fields | Add `response_model=XxxResponse` to every route decorator |
| Errors must use `{"detail": "message"}` | Consistent error format for clients | Use `raise HTTPException(status_code=4xx, detail="message")` |
| PATCH must use `payload.model_dump(exclude_unset=True)` | Without `exclude_unset`, absent fields overwrite existing data with `None` | `update_data = payload.model_dump(exclude_unset=True)` before applying to ORM model |
| POST must handle duplicate submissions | Retrying a POST should not create duplicates | Catch unique constraint violations; return 409 Conflict |

### Schema Design (blocking recommendation)

| Rule | Why | How to fix |
|------|-----|-----------|
| Four-variant schema pattern required | Prevents field leakage and over-posting | Define `XxxBase`, `XxxCreate`, `XxxUpdate`, `XxxResponse` for every resource |
| `XxxResponse` needs `ConfigDict(from_attributes=True)` | Without it, Pydantic can't deserialize SQLAlchemy ORM objects | Add `model_config = ConfigDict(from_attributes=True)` to response schemas |
| `XxxUpdate` fields must all be `Optional` | PATCH should never require all fields | Annotate every field as `Optional[T] = None` |

### Error Handling (blocking recommendation)

| Rule | Why | How to fix |
|------|-----|-----------|
| No bare `except:` | Catches `SystemExit`, `KeyboardInterrupt`; hides bugs | Use `except SpecificError:` or `except Exception as exc:` and re-raise or log |
| No silent `except` blocks | Swallowed errors are invisible in production | At minimum, log the exception: `logger.error("event", exc_info=exc)` |
| All network/DB/external calls need explicit timeouts | Hanging calls block thread pools and degrade the whole service | Add `timeout=` param to httpx, SQLAlchemy, and external SDK calls |
| Services must raise domain exceptions; routes map them | Coupling HTTP semantics to service layer violates separation of concerns | Define domain exceptions (e.g., `ItemNotFoundError`); catch in route and raise `HTTPException` |
| Graceful degradation on dependency failure | Prevents cascade failures | Return cached data or a fallback response when external service is unavailable |

### Security (blocking recommendation)

| Rule | Why | How to fix |
|------|-----|-----------|
| SQL must use ORM/Core with bound parameters | f-strings in SQL = SQL injection | Use `session.execute(select(Model).where(Model.id == id))` — never `f"SELECT ... {id}"` |
| Secrets must come from `settings` (pydantic-settings) | Hardcoded secrets in code get committed to Git | Use `settings.secret_key`, `settings.api_key`; load from `.env` via pydantic-settings |
| Production errors must not expose internals | Stack traces reveal file paths, DB structure, and library versions | Catch and convert to generic `500` with `{"detail": "Internal server error"}` |
| Logs must not contain PII or secrets | Logged PII violates GDPR/CCPA; logged secrets are a breach waiting to happen | Log IDs, not values: `log.info("message", conversation_id=cid)` not `log.info(f"msg: {content}")` |
| CORS must list specific origins | Wildcard `*` allows any origin to call the API | Set `allow_origins=settings.cors_origins` (comma-separated env var) |

### Observability (blocking recommendation)

| Rule | Why | How to fix |
|------|-----|-----------|
| All logging must use `structlog.get_logger()` | Structured JSON logs are parseable; `print()` output is not | Replace `print(...)` and `import logging` with `import structlog; logger = structlog.get_logger()` |
| Use structured context binding | Free-form f-string messages are unsearchable | `logger.info("event_name", key=value)` not `logger.info(f"event {value}")` |
| AI provider calls: log only metadata | Request/response bodies from LLMs can contain user PII | Log only `provider`, `model`, `token_count`, `latency_ms` |

---

## What the AI Reviewer Does NOT Flag

The AI reviewer explicitly ignores issues handled by CI tools to avoid noise:

| Issue | Handled by |
|-------|-----------|
| Code formatting, line length, import order | Ruff (CI) |
| Type errors, missing annotations | Mypy (CI) |
| Unused imports, dead code | Ruff F401/F841 (CI) |
| `eval()`/`exec()` exact patterns | Bandit B307 (CI) |
| Hardcoded password string literals | Bandit B105/B106 (CI) |
| SQL injection via string literal patterns | Bandit B608 (CI) |
| CVE vulnerabilities in dependencies | pip-audit (CI) |
| Test coverage percentage | Pytest `--cov-fail-under` (CI) |

If the AI comments on any of the above, it is a misconfiguration — update `.pr_agent.toml` to add the pattern to the `IGNORE` section.

---

## Non-Blocking Comments

The AI reviewer posts advisory (non-blocking) comments for:

- Endpoints missing a negative test case (error path)
- Test names not following `test_<action>_<expected_outcome>` pattern
- PRs that contain more than one logical change and should be split

These are not required to be fixed before merge but represent good practice.

---

## Addressing AI Review Comments

1. **Read the comment** — it includes the specific rule violated and the file/line.
2. **Fix or dismiss** — either apply the fix or reply with a reason why it doesn't apply (e.g., "This endpoint is internal-only and pagination would add unnecessary complexity").
3. **Re-request review** — after fixing, re-request the PR Agent review to confirm the finding is resolved.

To refine the AI rules (reduce false positives or add missing patterns), edit `.pr_agent.toml` and open a PR. Changes to `.pr_agent.toml` take effect on the next PR review run.
