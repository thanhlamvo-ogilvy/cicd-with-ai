## Why

The backend codebase contains violations across Ruff lint rules, Mypy strict type-checking, and security guidelines (S105, N818, F821). These violations break the CI quality gates introduced in `quality-gates-ai-review` and represent real security and type-safety risks that must be resolved before the feature branch can merge to `main`.

## What Changes

- **Fix S105 security violation** in `app/core/config.py`: remove the hardcoded `"change-me"` default for `secret_key` — require it to be provided via environment variable in production
- **Fix N818 naming violation** in `app/core/exceptions.py`: rename `AppException` → `AppError` to comply with PEP 8 Exception naming convention
- **Fix F821 undefined name** in `app/models/conversation.py` and `app/models/message.py`: resolve the forward reference issue by adding `TYPE_CHECKING` guard imports
- **Fix Mypy `dict` missing type args** in `app/core/security.py` and `app/api/routes/health.py`: add explicit generic types (`dict[str, Any]`)
- **Fix Mypy `no-any-return`** in `app/core/security.py`: annotate return types correctly using proper typed return values
- **Fix Mypy type mismatch** in `app/api/routes/items.py` and `app/api/routes/conversations.py`: services return ORM models, routes expect schema types — use `model_validate()` or fix return type annotations
- **Fix Mypy type errors** in `app/services/providers/openai.py`: resolve `AsyncOpenAI` kwargs typing and chat message TypedDict ambiguity
- **Fix Mypy type error** in `app/services/providers/anthropic.py`: cast message list to `Iterable[MessageParam]`
- **Fix Mypy type error** in `app/services/providers/google.py`: fix `generate_content_stream` content argument type
- **Fix Mypy `call-arg` error** in `app/services/chat_service.py`: `OpenAIProvider` constructor called with too many args
- **Fix Mypy `misc` error** in `app/api/routes/chat.py`: replace `...` return type annotation on `event_stream` with proper `AsyncGenerator`

## Capabilities

### New Capabilities

_(none — this is a compliance fix, not a new feature)_

### Modified Capabilities

- `backend-security-owasp`: `secret_key` must not have a hardcoded insecure default; production safety guard required
- `backend-api-design`: route return types must match declared response schemas; ORM models must be explicitly validated to schema types
- `shared-error-handling`: exception base class naming must follow PEP 8 (`Error` suffix); all exception hierarchy names updated

## Impact

- **Files changed**: `app/core/config.py`, `app/core/exceptions.py`, `app/models/conversation.py`, `app/models/message.py`, `app/core/security.py`, `app/api/routes/health.py`, `app/api/routes/items.py`, `app/api/routes/conversations.py`, `app/services/providers/openai.py`, `app/services/providers/anthropic.py`, `app/services/providers/google.py`, `app/services/chat_service.py`, `app/api/routes/chat.py`
- **Exception rename cascade**: `AppException` → `AppError` requires updating all `except AppException` usages and imports across the codebase
- **No API contract changes**: response shapes and endpoint paths are unchanged
- **No new dependencies**: all fixes use stdlib typing improvements or existing library types
