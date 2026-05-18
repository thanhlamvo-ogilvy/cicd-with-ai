# Backend API Design

> API design conventions ensuring consistent endpoint patterns, status codes, error formats, and architectural layering.

## URL & Versioning

- All endpoints MUST be under `/api/v1/` — explicit version prefix required
- API documentation MUST be auto-generated at `/docs` (OpenAPI/Swagger)

## HTTP Status Codes

- `POST` (resource creation) → `201 Created`
- `DELETE` (successful) → `204 No Content` with no body
- `GET` (success) → `200 OK`
- Errors → appropriate `4xx`/`5xx`

## Response & Error Format

- Every endpoint MUST declare a `response_model` parameter to control serialization
- All error responses MUST use `{"detail": "<descriptive message>"}` format

## List Endpoints

- ALL list endpoints MUST support pagination — `limit`/`offset` or cursor parameters; missing pagination MUST be flagged in code review

## Mutations

- `POST` endpoints MUST handle duplicate submissions gracefully — never create duplicate resources
- `PATCH` endpoints MUST use `payload.model_dump(exclude_unset=True)` to distinguish "not provided" from "set to None"

## Architecture

- Route handlers MUST be thin HTTP handlers — business logic belongs in service functions
- Routes handle only: HTTP concerns (status codes, response models) and calling the relevant service
