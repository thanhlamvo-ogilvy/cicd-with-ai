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

### Observability

- Use structured error logging — capture error message, stack trace, component name, and user action context.
- Integrate with error tracking service (e.g., Sentry) for production error monitoring.
- Add performance monitoring for critical user flows (page load, time to interactive).
- Log API call failures with request context (endpoint, status code, duration).
- Never log sensitive data (tokens, passwords, PII) in client-side logs.

### Testing (When Added)

- Use React Testing Library + Vitest for component tests.
- Test user interactions, not implementation details — query by role, label, or text.
- Mock API calls at the service layer — never mock `fetch` directly.
- Every new component should have at least one render test and one interaction test.

## Key Conventions

- Vite dev server proxies `/api/*` and `/health` to `http://localhost:8000` — see `vite.config.ts`.
- Production uses nginx to proxy API requests to the `backend` Docker service — see `nginx.conf`.
- The app defaults to `provider: "openai"` and `model: "google/gemma-3-4b"` (LMStudio local).
- SSE streaming: the first event from `/api/v1/chat` contains `conversation_id`, subsequent events contain `token`, and the final event is `[DONE]`.
