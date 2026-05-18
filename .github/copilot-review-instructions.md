<!--
AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
Source: openspec/specs/guidelines/
Regenerate with: bash scripts/sync-guidelines.sh
-->

# Copilot Code Review Instructions

> These instructions define what GitHub Copilot reviews in pull requests.
> **Scope:** Only semantic, contextual, and cross-cutting concerns that automated tools cannot catch.
> CI tools (ruff, mypy, bandit, pip-audit) handle all mechanical/syntactic checks — do not duplicate their work.

## What Automated Tools Already Handle (Do Not Review)

| Concern | Tool |
|---|---|
| Code formatting, import order, line length | ruff (format + I + E/W) |
| Type errors, missing type annotations | mypy |
| Unused imports, dead code | ruff (F401, F841) |
| `eval()` / `exec()` usage | bandit (B307) |
| Hardcoded password string literals | bandit (B105, B106) |
| SQL injection via string literal patterns | bandit (B608) |
| Known CVE vulnerabilities in dependencies | pip-audit, Dependabot |
| Test coverage percentage | pytest --cov |
| React hooks violations | ESLint |

---

## Block (Request Changes) Rules

### Architecture & API Design


- Route handlers MUST be thin HTTP handlers — business logic belongs in service functions
- Routes handle only: HTTP concerns (status codes, response models) and calling the relevant service


- `POST` (resource creation) → `201 Created`
- `DELETE` (successful) → `204 No Content` with no body
- `GET` (success) → `200 OK`
- Errors → appropriate `4xx`/`5xx`



- Every endpoint MUST declare a `response_model` parameter to control serialization
- All error responses MUST use `{"detail": "<descriptive message>"}` format



- ALL list endpoints MUST support pagination — `limit`/`offset` or cursor parameters; missing pagination MUST be flagged in code review



- `POST` endpoints MUST handle duplicate submissions gracefully — never create duplicate resources
- `PATCH` endpoints MUST use `payload.model_dump(exclude_unset=True)` to distinguish "not provided" from "set to None"


### Schema Design


Every resource MUST follow the four-variant schema pattern:

```python
class XxxBase(BaseModel):       # shared fields (no id/timestamps)
class XxxCreate(XxxBase):       # input for creation (no id/timestamps)
class XxxUpdate(BaseModel):     # all fields optional (for PATCH)
class XxxResponse(XxxBase):     # output (id + timestamps + from_attributes)
    model_config = ConfigDict(from_attributes=True)
```

Rules:
- `XxxResponse` MUST include `model_config = ConfigDict(from_attributes=True)` for ORM compatibility
- `XxxUpdate` fields MUST all be `Optional` — never required on a PATCH schema
- Schema fields with domain constraints MUST use `Field()` (e.g., `Field(min_length=1, max_length=255)`)



- PATCH operations MUST use `payload.model_dump(exclude_unset=True)` to distinguish "not provided" from "set to None" — omitted fields MUST remain unchanged



- All SQLAlchemy model attributes MUST use `Mapped` type annotations (e.g., `name: Mapped[str]`)

### Error Handling

> Note: bare `except:` patterns are a hint, but focus on semantic violations — swallowed errors,
> missing timeouts on external calls, and missing graceful degradation that no tool can detect.


- MUST handle specific exception types — bare `except:` (Python) and untyped `catch` (TypeScript) are forbidden
- NEVER swallow errors silently — every caught error MUST be logged, re-raised, or explicitly recovered from; empty catch blocks are forbidden



- Retry logic MUST use exponential backoff with jitter — tight fixed-interval loops are forbidden
- ALL network, database, and external service calls MUST have explicit timeouts — unbounded waits are forbidden



- Services MUST degrade gracefully when dependencies are unavailable — return cached data or a meaningful fallback response; never hang or crash



- Services MUST raise domain-specific exceptions (e.g., `ItemNotFoundError`)
- Route handlers MUST catch domain exceptions and map them to the appropriate `HTTPException` (e.g., 404)

### Security

> Note: `eval()`/`exec()` exact patterns and hardcoded password string literals are caught by bandit.
> Focus on contextual violations: ORM usage in DB queries, secrets loaded from config, safe error responses.


- ALL database queries MUST use SQLAlchemy ORM/Core with bound parameters
- String interpolation in SQL (f-strings, `.format()`, concatenation) is forbidden — code review MUST reject it



- Passwords MUST be hashed with bcrypt via `passlib` — plain-text password storage is forbidden
- JWT secrets and API keys MUST be loaded from `settings` (pydantic-settings via `.env`) — hardcoded secrets are forbidden



- Production error responses MUST NOT expose stack traces, database errors, or internal file paths
- Unhandled exceptions in production MUST return `{"detail": "Internal server error"}`



- Logs MUST NOT contain passwords, tokens, API keys, or PII — see also [Backend Observability](../backend-observability/spec.md)

### Observability & Logging


- ALL logging MUST use `structlog.get_logger(__name__)` — `print()` and stdlib `logging` are forbidden
- Log entries MUST use structured context binding, not string formatting:
  - ✅ `log.info("item_created", item_id=item.id)`
  - ❌ `log.info(f"item created: {item.id}")`
- Log levels:
  - `info` — normal business events (item created, request processed)
  - `warning` — recoverable issues
  - `error` — failures, with structured context



- Logs MUST NEVER contain passwords, tokens, API keys, or PII
- AI provider API calls MUST log only: `provider`, `model`, `token_count`, `latency` — NEVER request/response bodies


### PII & Data Privacy


**Backend:** Chat-related log entries MUST include `conversation_id` and `message_id` — NEVER log `message.content` or any substring of user input.

**Frontend:** Error logs, error tracking payloads, and analytics events MUST NOT include message content.



- `allow_methods` in CORS middleware MUST list specific methods for production: `["GET", "POST", "DELETE", "OPTIONS"]` — NEVER use `["*"]`
- Authentication plan MUST be documented in the instruction file: JWT middleware activation via `Depends()`, list of protected routes, and toggle mechanism (environment variable or feature flag)

### Commit Message Format


All commit messages MUST follow this structured release notes format:

```
[Primary Change Description]; [Secondary Changes] & more…

{PackageName}
- [Action verb] [concise description ≤ 120 chars]
- [Action verb] [another change description]

(No dependency updates.)
```

Rules:
- **Title line** — lead with the most newsworthy change; end with `& more…` if multi-topic; no trailing period
- **Group changes** under `{PkgName}` headers (e.g., `{Backend}`, `{Frontend}`, `{CI}`, `{Docs}`, `{Dependencies}`)
- **Bullets** — present-tense action verb (`Add`, `Fix`, `Refactor`, `Improve`, `Remove`); ≤ 120 chars; no trailing period
- **No dependency updates** — include the literal line `(No dependency updates.)` when no deps changed
- **Body line limit** — body (all lines after title) MUST NOT exceed 10 lines; reference an issue or PR link (`See #123`) for additional context
- **No attribution tags** — NEVER include `Co-authored-by:` trailers or AI generator attribution


---

## Comment (Non-Blocking) Rules

- Flag endpoints that lack both a positive (happy path) **and** a negative (error case) test
- Flag test function names that do not follow `test_<action>_<expected_outcome>` pattern
- Flag PRs that contain more than one logical change and should be split
- Suggest graceful degradation where a dependency failure would crash the service rather than degrade

---

## Ignore (Handled by Automated Tools)

Do not comment on anything listed in the **What Automated Tools Already Handle** table above.
Do not comment on code style, formatting, naming conventions, or type annotations.
These are enforced by ruff, mypy, bandit, and other CI tools — duplicate comments add noise without value.
