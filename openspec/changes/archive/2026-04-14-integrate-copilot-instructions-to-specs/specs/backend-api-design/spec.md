## ADDED Requirements

### Requirement: API version prefix
All endpoints SHALL be under `/api/v1/` with explicit version prefix.

#### Scenario: Endpoint path includes version
- **WHEN** a new endpoint is added
- **THEN** its path MUST start with `/api/v1/`

### Requirement: Consistent error format
All error responses SHALL use the format `{"detail": "message"}`.

#### Scenario: Error response structure
- **WHEN** an endpoint returns an error (4xx or 5xx)
- **THEN** the response body MUST be `{"detail": "<descriptive message>"}`

### Requirement: Correct HTTP status codes
Endpoints SHALL return correct status codes: 200 OK, 201 Created (POST creation), 204 No Content (DELETE), 400 Bad Request, 404 Not Found, 422 Validation Error, 500 Internal Server Error.

#### Scenario: POST creation returns 201
- **WHEN** a resource is successfully created via POST
- **THEN** the response status code MUST be 201

#### Scenario: DELETE returns 204
- **WHEN** a resource is successfully deleted
- **THEN** the response status code MUST be 204 with no body

### Requirement: Response model on all endpoints
Every endpoint MUST set `response_model` to control serialization.

#### Scenario: Endpoint declares response model
- **WHEN** a new route is defined
- **THEN** it MUST include a `response_model` parameter

### Requirement: Pagination on list endpoints
All list endpoints SHALL support pagination with `limit`/`offset` or cursor parameters.

#### Scenario: List endpoint without pagination rejected
- **WHEN** a list endpoint is added without pagination parameters
- **THEN** the code review MUST flag it as a violation

### Requirement: Idempotent POST endpoints
POST endpoints SHALL handle duplicate submissions gracefully.

#### Scenario: Duplicate POST does not create duplicate resources
- **WHEN** the same POST request is submitted twice
- **THEN** the system MUST NOT create duplicate resources

### Requirement: OpenAPI auto-generated at /docs
The API SHALL auto-generate OpenAPI/Swagger documentation at `/docs`.

#### Scenario: Swagger UI accessible
- **WHEN** a user navigates to `/docs`
- **THEN** the OpenAPI Swagger UI MUST be rendered with all endpoints documented

### Requirement: Routes delegate to services
Route handlers SHALL be thin HTTP handlers that delegate business logic to service functions. Routes MUST NOT contain business logic.

#### Scenario: Route handler delegation
- **WHEN** a route handler processes a request
- **THEN** it MUST call a service function for business logic and only handle HTTP concerns (status codes, response models)
