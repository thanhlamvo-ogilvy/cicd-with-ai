## MODIFIED Requirements

### Requirement: Response model on all endpoints
Every endpoint MUST set `response_model` to control serialization. Route handlers that return ORM model instances MUST explicitly validate them to the declared schema type using `SchemaClass.model_validate(orm_obj)` before returning. Implicit Pydantic coercion via `response_model` alone is insufficient for type-checker correctness.

#### Scenario: Endpoint declares response model
- **WHEN** a new route is defined
- **THEN** it MUST include a `response_model` parameter

#### Scenario: ORM model explicitly validated to schema
- **WHEN** a route handler returns an ORM model instance
- **THEN** it MUST call `ResponseSchema.model_validate(orm_instance)` and the declared return type MUST match the schema class — not the ORM model class

#### Scenario: Mypy passes on route return types
- **WHEN** mypy runs in strict mode against the routes
- **THEN** there MUST be zero `[return-value]` or `[arg-type]` errors related to ORM-to-schema coercion
