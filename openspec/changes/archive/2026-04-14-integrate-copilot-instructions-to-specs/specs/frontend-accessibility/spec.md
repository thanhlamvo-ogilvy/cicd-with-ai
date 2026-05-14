## ADDED Requirements

### Requirement: Semantic HTML elements
Interactive and structural elements MUST use semantic HTML (`<nav>`, `<main>`, `<button>`, `<form>`) — not `<div onClick>` or `<span>` soup.

#### Scenario: Button uses button element
- **WHEN** a clickable interactive element is created
- **THEN** it MUST use `<button>` — not `<div>` or `<span>` with an `onClick` handler

### Requirement: Keyboard accessibility
All interactive elements MUST be keyboard-accessible. No mouse-only interactions are allowed.

#### Scenario: Keyboard navigation
- **WHEN** a user navigates with keyboard only
- **THEN** all interactive elements MUST be reachable and operable via Tab, Enter, and Space keys

### Requirement: Form labels
All form inputs MUST have associated `<label>` elements or `aria-label`. Placeholder-only labels are forbidden.

#### Scenario: Input with label
- **WHEN** a form input is rendered
- **THEN** it MUST have an associated `<label>` or `aria-label` — never rely on `placeholder` alone

### Requirement: WCAG AA color contrast
Color contrast MUST meet WCAG 2.1 AA standards: 4.5:1 for normal text, 3:1 for large text.

#### Scenario: Text contrast check
- **WHEN** text is displayed
- **THEN** the contrast ratio between text and background MUST meet 4.5:1 (normal) or 3:1 (large text)

### Requirement: No color-only information
Information MUST NOT be conveyed by color alone. Icons, text, or patterns MUST supplement color.

#### Scenario: Error state indication
- **WHEN** an error state is displayed
- **THEN** it MUST use icons or text in addition to color to convey the state

### Requirement: ARIA used only when semantic HTML insufficient
ARIA attributes MUST only be used when semantic HTML elements cannot convey the meaning. Native elements are always preferred.

#### Scenario: ARIA usage check
- **WHEN** an ARIA role or attribute is added
- **THEN** there MUST be a reason why a native semantic element cannot be used instead

### Requirement: Focus management
Focus MUST be managed correctly after route changes, modal open/close, and dynamic content updates.

#### Scenario: Modal focus trap
- **WHEN** a modal opens
- **THEN** focus MUST move to the modal and be trapped within it until closed

#### Scenario: Route change focus
- **WHEN** a route change occurs
- **THEN** focus MUST be set to the main content area or page heading

### Requirement: Error messages associated with form fields
Error messages MUST be programmatically associated with their form fields using `aria-describedby`.

#### Scenario: Form validation error
- **WHEN** a form field has a validation error
- **THEN** the error message MUST be linked via `aria-describedby` on the input
