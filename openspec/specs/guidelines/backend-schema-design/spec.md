# Backend Schema Design

> Pydantic schema and SQLAlchemy model patterns ensuring consistent structure, validation, and ORM compatibility.

## Pydantic Schema Pattern

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

## Partial Updates

- PATCH operations MUST use `payload.model_dump(exclude_unset=True)` to distinguish "not provided" from "set to None" — omitted fields MUST remain unchanged

## SQLAlchemy Models

- All SQLAlchemy model attributes MUST use `Mapped` type annotations (e.g., `name: Mapped[str]`)
