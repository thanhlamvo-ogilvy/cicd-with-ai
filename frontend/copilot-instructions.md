# Frontend Copilot Instructions

> React 19 · TypeScript · Vite 6 · ES2020

## Build & Run

```bash
cd frontend
npm install
npm run dev              # dev server at http://localhost:5173 (proxies /api → backend:8000)
npm run build            # production build → dist/
npm run preview          # preview production build
```

## Lint & Format

```bash
npx eslint .                 # lint check
npx eslint . --fix           # lint + auto-fix
npx prettier --check .       # format check
npx prettier --write .       # format all files
```

ESLint config: `@typescript-eslint` for type-aware rules, `eslint-plugin-react-hooks` for hook dependency correctness, `eslint-plugin-react-refresh` for HMR compatibility. Prettier config: double quotes, 100-char line length, trailing commas — matching the backend's ruff config.

Expected `devDependencies`:
- `eslint`, `@typescript-eslint/eslint-plugin`, `@typescript-eslint/parser`
- `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`, `eslint-plugin-import`
- `prettier`, `eslint-config-prettier`

Import ordering is enforced via `eslint-plugin-import` — React imports first, external libs, internal modules, then types.

CI runs `npx eslint .` and `npx prettier --check .` — blocks merge on violations.

## Architecture

Single-page React application communicating with the FastAPI backend via REST + Server-Sent Events.

```
src/
├── components/          # UI components (one component per file)
│   ├── ChatBox.tsx      # Main container — orchestrates chat + sidebar
│   ├── ChatInput.tsx    # Message input form
│   ├── MessageBubble.tsx# Single message display
│   ├── MessageList.tsx  # Scrollable message list
│   └── Sidebar.tsx      # Conversation list with CRUD
├── hooks/               # Custom React hooks (business logic)
│   ├── useChat.ts       # Message streaming, send/receive
│   └── useConversations.ts  # Conversation list + CRUD
├── services/            # API client layer
│   └── api.ts           # REST + SSE streaming functions
├── types/               # Shared TypeScript interfaces
│   └── chat.ts          # Message, Conversation, ChatRequest types
├── App.tsx              # Root component
└── main.tsx             # Entry point
```

**Data flow:** Components → Hooks → Services → Backend API

## Coding Standard

### TypeScript

- **Strict mode enabled** — `strict: true` in `tsconfig.json`. Never use `@ts-ignore` or `any` unless absolutely necessary with a comment explaining why.
- All function parameters and return types must be explicitly typed or inferable.
- Use `interface` for object shapes, `type` for unions and intersections.
- Prefer `unknown` over `any` for values of uncertain type — then narrow with type guards.
- Use `readonly` for props and data that should not be mutated.
- Enable and respect `noUnusedLocals` and `noUnusedParameters` — remove dead code.

### React Patterns

- **Functional components only** — never use class components.
- **Named exports** for components: `export function ChatBox()` — not default exports (except `App.tsx`).
- **One component per file** — file name matches component name in PascalCase.
- Props must be defined as a TypeScript `interface` named `{ComponentName}Props`.
- Destructure props in the function signature: `function ChatBox({ messages, onSend }: ChatBoxProps)`.
- Keep components focused — if a component exceeds ~150 lines, extract sub-components.

### Hooks

- Custom hooks must start with `use` and live in `src/hooks/`.
- Return an object (not an array) for hooks with multiple return values — easier to destructure selectively.
- Define a return type interface: `interface UseChatReturn { ... }`.
- Keep side effects (`useEffect`) minimal — prefer event handlers for user-triggered actions.
- Always include proper dependency arrays in `useEffect`, `useCallback`, `useMemo`.
- Use `useCallback` for functions passed as props to prevent unnecessary re-renders.
- Use `useRef` for mutable values that should not trigger re-renders (e.g., abort flags).

### State Management

- Use React built-in state (`useState`, `useReducer`) — no external state libraries unless complexity demands it.
- Lift state to the nearest common ancestor — avoid prop drilling beyond 2 levels.
- For complex state transitions, prefer `useReducer` over multiple `useState` calls.
- Never mutate state directly — always return new objects/arrays.

### API & Data Fetching

- All API calls go through `src/services/api.ts` — components never call `fetch` directly.
- API functions must have explicit return types.
- Handle errors gracefully — show user-friendly messages, never raw error objects.
- For streaming (SSE), use async generators (`async function*`) to yield events.
- Always check `response.ok` before parsing — throw descriptive errors on failure.

### Error Handling

- Wrap async operations in try/catch — never let unhandled rejections propagate.
- Display user-friendly error messages in the UI — never raw stack traces or error objects.
- Use error boundaries for catching render errors in production (React `ErrorBoundary`).
- Log errors to console in development; suppress in production.
- All `catch` blocks MUST handle errors explicitly — no empty `catch {}` blocks. At minimum, log the error with context.
- API errors MUST show user-friendly messages with retry actions (e.g., "Something went wrong. Try again." with a retry button).
- Malformed SSE data MUST be logged with event metadata (event type, stream position) — never log the raw content (may contain PII).

### Naming Conventions

- **Files:** PascalCase for components (`ChatBox.tsx`), camelCase for everything else (`useChat.ts`, `api.ts`).
- **Components:** PascalCase (`function MessageBubble()`).
- **Hooks:** camelCase prefixed with `use` (`useChat`, `useConversations`).
- **Interfaces/Types:** PascalCase (`ChatRequest`, `Message`, `UseChatReturn`).
- **Constants:** UPPER_SNAKE_CASE for true constants (`const API_BASE = "/api/v1"`).
- **Event handlers:** prefix with `handle` in the component (`handleSend`, `handleDelete`), prefix with `on` in props (`onSend`, `onDelete`).

### Styling

- Use inline styles or CSS modules — no global CSS unless for resets.
- Prefer `style` objects for simple component styling.
- Use `system-ui, sans-serif` as the base font stack.
- Ensure interactive elements have visible focus states and proper cursor styles.
- All clickable elements must use `cursor: "pointer"`.

### Performance

- Memoize expensive computations with `useMemo`.
- Wrap callback props with `useCallback` to prevent child re-renders.
- Use `React.memo()` for pure components that receive stable props.
- Avoid creating objects/arrays inline in JSX — define outside the render or memoize.
- For lists, always provide a stable `key` prop — never use array index as key if items can reorder.
- Lazy load routes and heavy components with `React.lazy()` and `Suspense`.
- Measure and monitor Core Web Vitals (LCP, FID, CLS).
- Bundle size monitored — avoid importing entire libraries when only specific functions needed.
- Images optimized with appropriate formats (WebP) and lazy loading (`loading="lazy"`).

### Accessibility

- All interactive elements must be keyboard-accessible (use `<button>`, `<a>`, `<input>` — not `<div onClick>`).
- Form inputs must have associated labels or `aria-label`.
- Use semantic HTML elements (`<nav>`, `<main>`, `<form>`, `<header>`) where appropriate.
- Provide `placeholder` text for inputs.
- Disabled states must be visually distinct and prevent interaction.
- Color contrast must meet WCAG AA (4.5:1 for normal text, 3:1 for large text).
- No information conveyed by color alone — use icons, text, or patterns as well.
- ARIA attributes used only when semantic HTML isn't sufficient — prefer native elements.
- Screen reader testing performed (or automated a11y audit with axe-core).
- Error messages are descriptive and programmatically associated with their form fields (`aria-describedby`).
- Skip navigation link provided for keyboard users.
- Focus is managed correctly after route changes and modal open/close.

### Code Reuse

- Before writing a new component, check if existing components can be composed or extended.
- Extract repeated patterns into custom hooks or utility functions.
- Shared types go in `src/types/` — never duplicate type definitions across files.
- API functions go in `src/services/` — never inline fetch calls in components.

### Internationalization (i18n)

- No hardcoded user-facing strings — all text should be externalized to translation files (e.g., using `react-i18next` or similar).
- Use locale-aware APIs for date, time, number, and currency formatting (`Intl.DateTimeFormat`, `Intl.NumberFormat`).
- Consider RTL (right-to-left) layout support in CSS — use logical properties (`margin-inline-start` instead of `margin-left`).
- Ensure UTF-8 encoding throughout.
- UI layout must accommodate text expansion (translations can be 30–50% longer than English).
- Store and transmit times in UTC — display in user's local timezone.
- Handle pluralization properly — not just "item" vs "items".

### Data Privacy

- Never store sensitive data (tokens, passwords, PII) in `localStorage` or `sessionStorage` unencrypted.
- Clear sensitive data from state when user logs out.
- Do not log PII to the browser console in production.
- Implement consent UI for data collection where required (cookies, analytics).
- Ensure forms collecting PII have appropriate `autocomplete` attributes and are served over HTTPS.
- Do not include PII in analytics events or error tracking payloads.

#### AI Chat PII Rules

- `message.content` (user prompts and AI responses) is PII — never include it in console logs, error tracking payloads, or analytics events.
- Clear all chat messages and conversation state from memory when user logs out.
- Never store chat message content in `localStorage` or `sessionStorage` — keep it in React state only (cleared on tab close).
- When logging chat-related errors, log `conversationId` and event type only — never message content.

### Observability

- Use structured error logging — capture error message, stack trace, component name, and user action context.
- Integrate with error tracking service (e.g., Sentry) for production error monitoring.
- Add performance monitoring for critical user flows (page load, time to interactive).
- Log API call failures with request context (endpoint, status code, duration).
- Never log sensitive data (tokens, passwords, PII) in client-side logs.

### SOLID in Practice (React/TypeScript)

- **SRP**: Components render UI. Hooks manage state and side effects. Services handle API calls. Types define contracts. Never mix — a component should not contain `fetch` calls or complex business logic.
- **OCP**: Use React composition over modification — extend behavior with wrapper components, render props, or custom hooks instead of adding flags/props to existing components. Example: create `<ScrollableList>` wrapping `<MessageList>` instead of adding `scrollable` prop.
- **LSP**: Components accepting the same props interface must behave consistently. If `<PrimaryButton>` and `<DangerButton>` both accept `ButtonProps`, they must both handle `onClick`, `disabled`, and `children` identically.
- **ISP**: Keep prop interfaces focused. Split `ChatBoxProps` into smaller interfaces if it grows beyond 5-6 props. Prefer multiple specific props over a single `options` object. Never force a component to accept props it ignores.
- **DIP**: Components depend on prop interfaces, not concrete implementations. Services are injected via props or React Context — never import service instances directly in components. Use custom hooks as the abstraction layer between components and services.

### Security

- Never use `dangerouslySetInnerHTML` unless content is sanitized with a library like `DOMPurify` — this is the #1 XSS vector in React.
- Sanitize all user-generated content before rendering — even in attributes like `href` (prevent `javascript:` URLs).
- Never store JWTs or sensitive tokens in `localStorage` — prefer `httpOnly` cookies set by the backend or in-memory state that clears on tab close.
- Validate all form inputs client-side AND server-side — client validation is UX, server validation is security.
- Use `Content-Security-Policy` headers (configured in nginx/server) — avoid `unsafe-inline` and `unsafe-eval`.
- Never include API keys, secrets, or credentials in frontend code — Vite env vars prefixed with `VITE_` are embedded in the bundle and visible to users.
- Implement CSRF protection for state-changing operations — use tokens or `SameSite` cookie attributes.
- Use `rel="noopener noreferrer"` on all external links (`target="_blank"`).

### Resilience & Error Recovery

- Implement retry logic for failed API calls with exponential backoff — use `AbortController` to cancel in-flight requests on unmount.
- Show loading states during async operations — never leave the user staring at a blank screen.
- Display user-friendly error states with retry actions — `"Something went wrong. Try again."` with a button, not a raw error dump.
- Use React Error Boundaries to catch render errors — show a fallback UI instead of a white screen.
- Handle network offline gracefully — detect with `navigator.onLine` and show appropriate messaging.
- Use `AbortController` in `useEffect` cleanup to cancel pending requests when components unmount — prevent state updates on unmounted components.
- Implement optimistic UI updates for better perceived performance — rollback on server error.

### Dependency Management

- `package-lock.json` must be committed — ensures reproducible builds across environments.
- Run `npm audit` regularly and in CI — fix or document known vulnerabilities.
- Prefer established libraries with active maintenance — check npm download trends and GitHub activity before adding.
- Use tree-shakable imports: `import { debounce } from "lodash-es"` not `import _ from "lodash"`.
- Review bundle impact before adding a dependency — use `npx bundlephobia <package>` or build analysis.
- Keep `devDependencies` separate from `dependencies` — dev tools should not ship to production.
- Do not install packages globally for the project — all deps in `package.json`.
- Update dependencies regularly: patch/minor updates in automated PRs, major updates reviewed manually.

### Deployment

- Vite build outputs to `dist/` — this is the only artifact deployed to production.
- Environment variables must be prefixed with `VITE_` to be available in client code — and remember they are PUBLIC (embedded in bundle).
- Use `import.meta.env.VITE_*` for environment-specific config — never hardcode API URLs or feature flags.
- Configure nginx (or equivalent) for SPA routing: serve `index.html` for all routes, let React Router handle client-side routing.
- Enable gzip/brotli compression in nginx for static assets — significantly reduces bundle transfer size.
- Set long cache headers for hashed assets (`assets/index-[hash].js`) — Vite handles cache busting via content hashing.
- Use `.dockerignore` to exclude `node_modules/`, `.git/`, and source files from the Docker image — only copy `dist/` and nginx config.
- Source maps: generate for staging (debugging), disable for production (security).

### Documentation

- Use JSDoc comments for complex utility functions, custom hooks, and non-obvious logic.
- Example for hooks:
  ```typescript
  /**
   * Manages chat message state and streaming from the backend.
   *
   * @param conversationId - Active conversation ID, or null for new chat.
   * @returns Chat state and actions (messages, sendMessage, isStreaming).
   *
   * @example
   * const { messages, sendMessage, isStreaming } = useChat(conversationId);
   */
  ```
- Document component props in the interface definition — add JSDoc to complex or non-obvious props.
- Use descriptive file-level comments only for non-obvious modules — the file name and exports should be self-documenting.
- Keep `README.md` and `copilot-instructions.md` in sync with actual architecture and commands.
- Add inline comments for workarounds, browser quirks, or non-obvious behavior — explain *why*, not *what*.

### Developer Experience (DX)

- `npm install && npm run dev` — must be all that's needed to start developing.
- Vite provides HMR (Hot Module Replacement) — changes reflect instantly without full page reload.
- Use VS Code with ESLint and Prettier extensions for real-time feedback.
- Use React DevTools browser extension for inspecting component tree, state, and performance.
- Use the Network tab to debug API calls — check request/response payloads and timing.
- Add TypeScript path aliases in `tsconfig.json` for clean imports: `@/components/ChatBox` instead of `../../../components/ChatBox`.
- Use `console.table()` for debugging arrays/objects — more readable than `console.log()`.
- Storybook recommended for component development in isolation (when component library grows).

### Testing

#### Test Stack

- **Unit & Component tests**: Vitest + React Testing Library + `@testing-library/jest-dom` (with `jsdom` environment)
- **E2E tests**: Playwright

Expected `devDependencies`:
- `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`
- `@playwright/test`

#### Commands

```bash
npx vitest run                   # run all unit/component tests
npx vitest run --coverage        # run with coverage report
npx vitest --watch               # watch mode during development
npx playwright test              # run E2E tests
npx playwright test --ui         # run E2E tests with UI
```

#### File Conventions

- Unit/component tests: `src/**/*.test.ts(x)` — colocated with source files
- E2E tests: `e2e/**/*.spec.ts` — separate directory
- Test naming: `describe("ComponentName")` > `it("should ...")` pattern
- One test file per component/hook — file name matches source: `ChatBox.test.tsx` for `ChatBox.tsx`

#### Test Pyramid

- **Unit/component tests (base)** — many, fast. Every new component MUST have at least one render test and one interaction test.
- **Custom hooks** — MUST be tested using `renderHook` from `@testing-library/react`.
- **E2E tests (top)** — few, slow. Only for critical user journeys (chat flow, conversation CRUD). Do not add E2E tests for what unit tests can cover.
- Test user interactions, not implementation details — query by role, label, or text.
- Mock API calls at the service layer (`src/services/api.ts`) — never mock `fetch` directly.
- CI runs `npx vitest run` and `npx playwright test` — blocks merge on failures.

## Key Conventions

- Vite dev server proxies `/api/*` and `/health` to `http://localhost:8000` — see `vite.config.ts`.
- Production uses nginx to proxy API requests to the `backend` Docker service — see `nginx.conf`.
- The app defaults to `provider: "openai"` and `model: "google/gemma-3-4b"` (LMStudio local).
- SSE streaming: the first event from `/api/v1/chat` contains `conversation_id`, subsequent events contain `token`, and the final event is `[DONE]`.
