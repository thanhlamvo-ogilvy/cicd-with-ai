## Context

Running `ruff check app/ --select=E,F,W,I,UP,S,B,A,C4,T20,ANN,N,RET,SIM,PT` and `mypy app/` against the backend codebase surfaces **6 Ruff violations** and **30 Mypy errors** across 11 files. The `quality-gates-ai-review` CI pipeline introduced in the previous change requires all of these to pass on every PR to `main`. The current `feat/coding-standards-and-ci` branch is blocked from merging until they are resolved.

No external APIs or response contracts change. The fixes are purely internal type-correctness, naming convention, and security hygiene improvements.

## Goals / Non-Goals

**Goals:**
- Zero Ruff violations (E, F, W, I, UP, S, B, A, C4, T20, ANN, N, RET, SIM, PT rule sets)
- Zero Mypy strict-mode errors across all 11 affected files
- No hardcoded insecure defaults for `secret_key`
- Exception hierarchy follows PEP 8 naming (`Error` suffix)
- Forward-reference model imports use `TYPE_CHECKING` guard

**Non-Goals:**
- No API endpoint changes (paths, request/response shapes unchanged)
- No new test coverage (existing tests still pass; coverage improvements are out of scope)
- No dependency upgrades
- No refactoring beyond minimum necessary to satisfy type-checker

## Decisions

### 1. Fix model forward references with `TYPE_CHECKING`

**Problem**: `app/models/conversation.py` references `"Message"` and `app/models/message.py` references `"Conversation"` — both as string forward references in `relationship()`. Mypy cannot resolve these because neither model imports the other at module level (circular import risk).

**Decision**: Add `from __future__ import annotations` at top of each model file, and wrap cross-model imports in `if TYPE_CHECKING:` blocks. This satisfies Mypy without introducing circular imports at runtime.

**Alternative considered**: Use a shared `models/__init__.py` to import all models and rely on SQLAlchemy's string-based lazy resolution — rejected because it complicates the import graph further.

### 2. Fix OpenAI provider types with explicit casts

**Problem**: `AsyncOpenAI(**kwargs)` where `kwargs: dict[str, str | int]` is too wide — Mypy can't match against individual keyword argument types. The chat message list uses `dict[str, str]` but OpenAI SDK expects `ChatCompletionUserMessageParam` etc.

**Decision**: Replace the `**kwargs` pattern with explicit named arguments. Cast the message list to `list[ChatCompletionMessageParam]` using `cast()`. Annotate `stream=True` explicitly so Mypy narrows the return to `AsyncStream[ChatCompletionChunk]`.

**Alternative considered**: Use `# type: ignore` — rejected; it hides real type errors and contradicts the strict-mode policy.

### 3. Fix Anthropic provider with `cast()` to `MessageParam`

**Problem**: `list[dict[str, str]]` is not assignable to `Iterable[MessageParam]` expected by the Anthropic SDK.

**Decision**: Import `MessageParam` from `anthropic.types` and cast the messages list. This is safe because the runtime dict shape matches `MessageParam`'s expected structure.

### 4. Fix Google provider with `Content` type

**Problem**: `generate_content_stream` expects `Content` objects, not raw dicts.

**Decision**: Import `Content` from `google.genai.types` and construct proper `Content` objects, or cast the list to the expected type. Use `cast()` since the runtime shape is correct but the type annotation is stricter than needed.

### 5. Fix `security.py` return types

**Problem**: `pwd_context.verify()` and `jwt.encode()`/`jwt.decode()` return `Any` from their library stubs. Mypy flags all callers with `no-any-return`.

**Decision**: Add explicit `cast()` calls at each return site to narrow the return type to the declared signature. This keeps the declared types accurate without suppressing the error globally.

### 6. Fix `health.py` and `security.py` missing type args

**Problem**: `dict` used without type parameters (`dict` vs `dict[str, Any]`).

**Decision**: Add explicit type arguments — `dict[str, Any]` where the value is mixed, `dict[str, str]` where values are strings only.

### 7. Fix route return type mismatches (items, conversations)

**Problem**: Services return ORM model objects (`Item`, `Conversation`), but routes are annotated as returning Pydantic schema types (`ItemResponse`, `ConversationResponse`). Mypy can't verify the implicit coercion.

**Decision**: Cast the return explicitly using `schema.model_validate(orm_obj)` in the route handlers that do point-return. For list returns (`ItemListResponse`), pass ORM objects and rely on Pydantic's `from_attributes=True` — but update the schema field type to `list[Item] | list[ItemResponse]` or use `model_validate` at the response construction site.

### 8. Rename `AppException` → `AppError`

**Problem**: N818 rule requires exception class names to end with `Error`.

**Decision**: Rename `AppException` → `AppError` and cascade to all subclasses and `except` usages. This is a pure rename with no behavioral change.

### 9. Remove insecure `secret_key` default

**Problem**: `secret_key: str = "change-me"` will be flagged by S105 and is a security risk if deployed to production without an explicit override.

**Decision**: Remove the default value and require `secret_key` to be set via environment variable. For development convenience, raise a clear `ValueError` on startup if it is missing in non-test environments.

### 10. Fix `chat.py` event_stream return type

**Problem**: `async def event_stream() -> ...:` uses `...` (Ellipsis) as a return type, which is invalid. The `# type: ignore[override]` comment is unused.

**Decision**: Annotate `event_stream` as `AsyncGenerator[str, None]` with proper import.

## Risks / Trade-offs

- **`AppError` rename cascade** → Any external code catching `AppException` by name will break. Since this is an internal-only exception used within the same service, the risk is contained. Mitigation: grep for all usages before renaming; the CI test suite will catch missing updates.

- **`secret_key` without default** → Existing `.env` files that don't set `SECRET_KEY` will cause a startup crash. Mitigation: document the required variable in `README.md` and `.env.example`; this is the correct behavior (fail fast, don't silently use an insecure default).

- **`cast()` usage** → Casts suppress type errors without changing runtime behavior. If the underlying library changes its type signatures, the casts may silently allow type mismatches. Mitigation: keep casts as narrow as possible and use them only where the shape is verified correct at runtime.

## Open Questions

_(none — all decisions above are made; implementation may proceed)_
