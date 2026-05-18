## 1. Security: Remove insecure secret_key default

- [x] 1.1 Remove the `"change-me"` default from `secret_key` in `app/core/config.py`
- [x] 1.2 Add a startup validator that raises `ValueError` if `secret_key` is empty in non-test environments
- [x] 1.3 Add `SECRET_KEY` to `.env.example` with a comment explaining it must be a strong random value
- [x] 1.4 Verify `ruff check app/core/config.py` passes with no S105 violation

## 2. Naming: Rename AppException → AppError

- [x] 2.1 Rename `AppException` to `AppError` in `app/core/exceptions.py`
- [x] 2.2 Update all `except AppException` usages across `app/` (grep for `AppException`)
- [x] 2.3 Update all `raise AppException` and `import AppException` references
- [x] 2.4 Verify `ruff check app/core/exceptions.py` passes with no N818 violation

## 3. Models: Fix forward reference circular imports

- [x] 3.1 Add `from __future__ import annotations` and `TYPE_CHECKING` guard import in `app/models/conversation.py`
- [x] 3.2 Add `from __future__ import annotations` and `TYPE_CHECKING` guard import in `app/models/message.py`
- [x] 3.3 Remove the `# noqa: F821` comment from `app/models/message.py` (no longer needed)
- [x] 3.4 Verify `mypy app/models/` reports zero errors

## 4. Security: Fix openai.py type errors

- [x] 4.1 Replace `AsyncOpenAI(**kwargs)` with explicit named arguments (`api_key=`, `base_url=`, `timeout=`) in `app/services/providers/openai.py`
- [x] 4.2 Import `ChatCompletionMessageParam` from `openai.types.chat` and cast the messages list
- [x] 4.3 Annotate `stream=True` call so Mypy narrows return to `AsyncStream[ChatCompletionChunk]`
- [x] 4.4 Verify `mypy app/services/providers/openai.py` reports zero errors

## 5. Type safety: Fix anthropic.py message type

- [x] 5.1 Import `MessageParam` from `anthropic.types` in `app/services/providers/anthropic.py`
- [x] 5.2 Cast the `chat_messages` list to `list[MessageParam]` before passing to `messages.stream()`
- [x] 5.3 Verify `mypy app/services/providers/anthropic.py` reports zero errors

## 6. Type safety: Fix google.py content type

- [x] 6.1 Import `Content` and `Part` from `google.genai.types` in `app/services/providers/google.py`
- [x] 6.2 Replace the raw dict list with proper `Content` objects, or cast to the expected type
- [x] 6.3 Verify `mypy app/services/providers/google.py` reports zero errors

## 7. Type safety: Fix security.py return types

- [x] 7.1 Add `cast(bool, ...)` around `pwd_context.verify()` return in `app/core/security.py`
- [x] 7.2 Add `cast(str, ...)` around `pwd_context.hash()` and `jwt.encode()` returns
- [x] 7.3 Change `decode_access_token` return type to `dict[str, Any]` and add `cast()`
- [x] 7.4 Add `from typing import Any, cast` imports
- [x] 7.5 Verify `mypy app/core/security.py` reports zero errors

## 8. Type safety: Fix health.py missing type args

- [x] 8.1 Change `-> dict:` to `-> dict[str, str]:` in `app/api/routes/health.py`
- [x] 8.2 Verify `mypy app/api/routes/health.py` reports zero errors

## 9. Routes: Fix items.py ORM-to-schema return types

- [x] 9.1 Wrap `item_service.get_items()` list result in `ItemListResponse` using `model_validate` or schema construction in `app/api/routes/items.py`
- [x] 9.2 Wrap the single-item returns (`get_item`, `create_item`, `update_item`) using `ItemResponse.model_validate(item)`
- [x] 9.3 Verify `mypy app/api/routes/items.py` reports zero errors

## 10. Routes: Fix conversations.py ORM-to-schema return type

- [x] 10.1 Wrap `chat_service.list_conversations()` result using `ConversationResponse.model_validate()` on each item in `app/api/routes/conversations.py`
- [x] 10.2 Verify `mypy app/api/routes/conversations.py` reports zero errors

## 11. Chat: Fix chat.py event_stream return annotation

- [x] 11.1 Import `AsyncGenerator` from `collections.abc` in `app/api/routes/chat.py`
- [x] 11.2 Change `async def event_stream() -> ...:` to `async def event_stream() -> AsyncGenerator[str, None]:`
- [x] 11.3 Remove the `# type: ignore[override]` comment (no longer needed)
- [x] 11.4 Verify `mypy app/api/routes/chat.py` reports zero errors

## 12. Validation: Full CI gate verification

- [x] 12.1 Run `ruff check app/` — confirm zero violations
- [x] 12.2 Run `ruff format app/ --check` — confirm zero formatting issues
- [x] 12.3 Run `mypy app/` — confirm zero errors across all 31 source files
- [x] 12.4 Run `pytest tests/ -v` — confirm all tests pass
- [x] 12.5 Commit all fixes with proper commit message format
