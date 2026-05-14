## ADDED Requirements

### Requirement: Base/Create/Update/Response pattern
Every resource MUST follow the schema pattern: `XxxBase` (shared fields), `XxxCreate(XxxBase)` (no id/timestamps), `XxxUpdate(BaseModel)` (all optional), `XxxResponse(XxxBase)` (id + timestamps + `from_attributes`).

#### Scenario: New resource schema structure
- **WHEN** a new resource schema is created
- **THEN** it MUST define `Base`, `Create`, `Update`, and `Response` variants following the documented pattern

### Requirement: ConfigDict from_attributes on Response schemas
All Response schemas MUST include `model_config = ConfigDict(from_attributes=True)` for ORM compatibility.

#### Scenario: Response schema has from_attributes
- **WHEN** a `XxxResponse` schema is defined
- **THEN** it MUST include `model_config = ConfigDict(from_attributes=True)`

### Requirement: Field constraints for validation
Pydantic schemas MUST use `Field()` for validation constraints (min_length, max_length, ge, le, etc.).

#### Scenario: Schema field validation
- **WHEN** a schema field has domain constraints (e.g., name length)
- **THEN** it MUST use `Field()` with appropriate validators

### Requirement: Partial updates with exclude_unset
Partial update operations MUST use `payload.model_dump(exclude_unset=True)` to distinguish between "not provided" and "set to None".

#### Scenario: PATCH with partial data
- **WHEN** a PATCH request provides only some fields
- **THEN** only the provided fields MUST be updated; omitted fields MUST remain unchanged

### Requirement: Mapped type annotations for SQLAlchemy models
All SQLAlchemy model attributes MUST use `Mapped` type annotations.

#### Scenario: Model field typing
- **WHEN** a SQLAlchemy model field is defined
- **THEN** it MUST use `Mapped[type]` annotation (e.g., `name: Mapped[str]`)
