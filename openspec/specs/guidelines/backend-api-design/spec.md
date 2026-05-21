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

### Requirement: Response model on all endpoints

Every endpoint MUST declare a `response_model` parameter to control serialization. Route handlers that return ORM model instances MUST explicitly validate them to the declared schema type using `SchemaClass.model_validate(orm_obj)` before returning. Implicit Pydantic coercion via `response_model` alone is insufficient for type-checker correctness.

#### Scenario: Endpoint declares response model
- **WHEN** a new route is defined
- **THEN** it MUST include a `response_model` parameter

#### Scenario: ORM model explicitly validated to schema
- **WHEN** a route handler returns an ORM model instance
- **THEN** it MUST call `ResponseSchema.model_validate(orm_instance)` and the declared return type MUST match the schema class — not the ORM model class

#### Scenario: Mypy passes on route return types
- **WHEN** mypy runs in strict mode against the routes
- **THEN** there MUST be zero `[return-value]` or `[arg-type]` errors related to ORM-to-schema coercion

- All error responses MUST use `{"detail": "<descriptive message>"}` format

## List Endpoints

- ALL list endpoints MUST support pagination — `limit`/`offset` or cursor parameters; missing pagination MUST be flagged in code review

## Mutations

- `POST` endpoints MUST handle duplicate submissions gracefully — never create duplicate resources
- `PATCH` endpoints MUST use `payload.model_dump(exclude_unset=True)` to distinguish "not provided" from "set to None"

## Architecture

- Route handlers MUST be thin HTTP handlers — business logic belongs in service functions
- Routes handle only: HTTP concerns (status codes, response models) and calling the relevant service
