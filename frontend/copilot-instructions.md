<!--
Frontend-specific coding standards for React 19 + TypeScript + Vite 6.
Use alongside shared standards: SOLID, Clean Code, Git, Security in `.github/copilot-instructions.md`.
Key: Strict TypeScript. All code enforced via ESLint + Prettier in CI; blocks merge on violations.
-->

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

- Use React built-in state (`useState`, `useReducer`)
- Lift state to nearest common ancestor; limit prop drilling to 2 levels
- Prefer `useReducer` for complex state transitions
- Never mutate state directly; return new objects/arrays

### API & Data Fetching

- All API calls in `src/services/api.ts`; components never call `fetch` directly
- Explicit return types on all API functions
- Handle errors gracefully with user-friendly messages
- Streaming (SSE): use async generators (`async function*`)
- Always check `response.ok` before parsing; throw descriptive errors on failure

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

- Check existing components before creating new ones
- Extract repeated patterns into custom hooks or utilities
- Shared types go in `src/types/`
- API functions go in `src/services/`

### Internationalization (i18n)

- Externalize all user-facing strings (e.g., `react-i18next`)
- Use locale-aware APIs: `Intl.DateTimeFormat`, `Intl.NumberFormat`
- RTL support: use logical CSS (`margin-inline-start` not `margin-left`)
- UTF-8 encoding everywhere
- Allow 30-50% text expansion for translations
- Store/transmit times in UTC; display in local timezone
- Handle pluralization correctly

### Data Privacy

- Never store sensitive data unencrypted in storage
- Clear sensitive data on logout
- No PII in browser console (production)
- Implement data collection consent UI
- Ensure forms with PII have appropriate `autocomplete` attrs, served over HTTPS
- Exclude PII from analytics/error tracking

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

### SOLID in Practice

- **SRP**: Components render UI; hooks manage state; services handle API; types define contracts
- **OCP**: Use composition over modification; extend with wrappers or hooks
- **LSP**: Components with same props interface behave consistently
- **ISP**: Keep props interfaces focused; split if >5-6 props
- **DIP**: Depend on interfaces; inject services via props/Context; never import directly

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

- Retry failed API calls with exponential backoff; use `AbortController` to cancel on unmount
- Show loading states during async operations
- User-friendly error states with retry actions
- React Error Boundaries for render errors
- Detect offline with `navigator.onLine`
- Use `AbortController` cleanup to prevent state updates on unmounted components
- Optimistic UI updates with server error rollback

### Dependency Management

- `package-lock.json` committed; ensures reproducible builds
- Run `npm audit` regularly and in CI
- Prefer established libraries with active maintenance
- Tree-shakable imports: `import { debounce } from "lodash-es`
- Review bundle impact before adding (check bundlephobia)
- Separate `devDependencies` from `dependencies`
- All deps in `package.json`; no global installs
- Regular updates: patch/minor automated, major manual reviews

### Deployment

- Build outputs to `dist/`; this is the only artifact deployed
- Env vars prefixed `VITE_` available in client code (PUBLIC; embedded in bundle)
- Use `import.meta.env.VITE_*` for env-specific config
- nginx: SPA routing (serve `index.html` for all routes)
- gzip/brotli compression in nginx
- Long cache headers for hashed assets (`assets/index-[hash].js`)
- `.dockerignore`: exclude `node_modules/`, `.git/`, source; copy only `dist/` + nginx config
- Source maps: enable staging, disable production

### Documentation

- JSDoc for complex utilities, custom hooks, non-obvious logic
- Document props in interface definition
- File-level comments only for non-obvious modules
- Keep README + `copilot-instructions.md` in sync
- Inline comments explain *why*, not *what*; workarounds and browser quirks

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
