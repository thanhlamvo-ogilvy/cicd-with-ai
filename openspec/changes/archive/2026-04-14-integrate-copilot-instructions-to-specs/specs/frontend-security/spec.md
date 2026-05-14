## ADDED Requirements

### Requirement: No dangerouslySetInnerHTML without sanitization
`dangerouslySetInnerHTML` MUST NOT be used unless content is sanitized with a library like `DOMPurify`.

#### Scenario: XSS prevention
- **WHEN** raw HTML needs to be rendered
- **THEN** it MUST be sanitized with DOMPurify before using `dangerouslySetInnerHTML`

### Requirement: No tokens in localStorage
JWTs and sensitive tokens MUST NOT be stored in `localStorage`. Use `httpOnly` cookies or in-memory state that clears on tab close.

#### Scenario: Token storage
- **WHEN** an authentication token is received
- **THEN** it MUST be stored in `httpOnly` cookies or in-memory state — never `localStorage`

### Requirement: No secrets in frontend code
API keys, secrets, and credentials MUST NOT appear in frontend code. `VITE_`-prefixed env vars are visible in the bundle.

#### Scenario: Secret in frontend rejected
- **WHEN** a PR adds a secret or API key to frontend code
- **THEN** the review MUST reject it — even `VITE_` env vars are public

### Requirement: CSP headers configured
Content-Security-Policy headers MUST be configured in nginx/server. `unsafe-inline` and `unsafe-eval` MUST be avoided.

#### Scenario: CSP enforcement
- **WHEN** the frontend is served in production
- **THEN** CSP headers MUST be set without `unsafe-inline` or `unsafe-eval`

### Requirement: Client and server-side validation
All form inputs MUST be validated client-side (for UX) AND server-side (for security).

#### Scenario: Form submission validation
- **WHEN** a form is submitted
- **THEN** inputs MUST be validated on both client and server — client validation alone is insufficient

### Requirement: CSRF protection
State-changing operations MUST implement CSRF protection via tokens or `SameSite` cookie attributes.

#### Scenario: State-changing request has CSRF protection
- **WHEN** a POST/PUT/DELETE request is made
- **THEN** it MUST include CSRF protection (token or `SameSite` cookies)

### Requirement: External links use noopener noreferrer
All external links with `target="_blank"` MUST include `rel="noopener noreferrer"`.

#### Scenario: External link safety
- **WHEN** a link opens in a new tab (`target="_blank"`)
- **THEN** it MUST include `rel="noopener noreferrer"`

### Requirement: User content sanitization
All user-generated content MUST be sanitized before rendering — including in attributes like `href` to prevent `javascript:` URLs.

#### Scenario: Href sanitization
- **WHEN** a user-provided URL is rendered in an `href` attribute
- **THEN** it MUST be validated to prevent `javascript:` protocol injection
