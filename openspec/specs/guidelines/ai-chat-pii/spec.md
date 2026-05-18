# AI Chat PII

> PII classification, retention, log sanitization, and security hardening rules for AI chat messages.

## PII Classification

The following fields are classified as PII and MUST be handled accordingly:
- `Message.content` (user prompts and AI responses)
- `Conversation.title`
- Any user-identifiable metadata

## Data Retention

- Messages MUST have `created_at` timestamps
- Retention period MUST be configurable via environment variable
- A purge mechanism MUST exist to delete expired messages
- Users MUST be able to request deletion of all their conversations and messages — cascading deletion MUST NOT break referential integrity

## Log Sanitization

**Backend:** Chat-related log entries MUST include `conversation_id` and `message_id` — NEVER log `message.content` or any substring of user input.

**Frontend:** Error logs, error tracking payloads, and analytics events MUST NOT include message content.

## CORS & Auth Hardening

- `allow_methods` in CORS middleware MUST list specific methods for production: `["GET", "POST", "DELETE", "OPTIONS"]` — NEVER use `["*"]`
- Authentication plan MUST be documented in the instruction file: JWT middleware activation via `Depends()`, list of protected routes, and toggle mechanism (environment variable or feature flag)
