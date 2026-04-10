# AI Chat PII

## Purpose

Define PII classification, retention, log sanitization, and security hardening rules for AI chat messages across backend and frontend.

## Requirements

### Requirement: AI chat message classification as PII

Both backend and frontend instruction files SHALL classify AI chat messages (user prompts and AI responses) as PII requiring specific handling.

#### Scenario: PII fields identified

- **WHEN** a developer reviews the PII section of the instruction files
- **THEN** they SHALL find an explicit list: `Message.content`, `Conversation.title`, and any user-identifiable metadata are classified as PII

### Requirement: Chat message retention policy

The backend instruction file SHALL define a data retention policy for AI chat messages.

#### Scenario: Retention rules documented

- **WHEN** a developer implements message storage
- **THEN** the instruction file SHALL specify: messages MUST have `created_at` timestamps, retention period MUST be configurable via environment variable, and a purge mechanism MUST exist for expired messages

#### Scenario: Right to deletion

- **WHEN** a user requests data deletion
- **THEN** the system MUST support cascading deletion of all conversations and messages for that user without breaking referential integrity

### Requirement: Chat message log sanitization

Both instruction files SHALL define rules preventing chat message content from appearing in logs.

#### Scenario: Backend log sanitization

- **WHEN** the backend logs a chat-related event
- **THEN** it MUST log `conversation_id` and `message_id` but NEVER log `message.content` or any substring of user input

#### Scenario: Frontend log sanitization

- **WHEN** the frontend logs an error related to chat
- **THEN** it MUST NOT include message content in console logs, error tracking payloads, or analytics events

### Requirement: CORS and auth hardening for chat endpoints

The backend instruction file SHALL strengthen CORS and authentication guidance for chat-related endpoints.

#### Scenario: CORS methods restricted

- **WHEN** configuring CORS middleware for production
- **THEN** `allow_methods` MUST list specific methods (`["GET", "POST", "DELETE", "OPTIONS"]`) — never use `["*"]`

#### Scenario: Auth activation plan documented

- **WHEN** a developer reads the authentication section
- **THEN** they SHALL find a concrete plan: JWT middleware activation via `Depends()`, protected routes list, and the toggle mechanism (environment variable or feature flag)
