# Coding Standards Quick Reference

> A scannable guide for developers during active coding.
> For the full review checklist, see [`.github/copilot-review-instructions.md`](.github/copilot-review-instructions.md).

---

## Overview

This project is a monorepo with two workspaces:

| Workspace | Stack | CI Checks |
|-----------|-------|-----------|
| `backend/` | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 | Ruff, Mypy, Bandit, Pytest |
| `frontend/` | React 19, TypeScript, Vite 6 | ESLint, tsc, Vitest, Bundle Size |

---

## Backend Standards

### Naming

```python
# ✅ Do — intention-revealing, snake_case
async def fetch_conversation_by_id(conversation_id: str) -> Conversation:
    ...

# ❌ Don't — abbreviated, unclear purpose
async def get_conv(cid):
    ...
```

### Function Size

```python
# ✅ Do — small, single-responsibility
async def validate_message(content: str) -> str:
    content = content.strip()
    if not content:
        raise ValueError("Message cannot be empty")
    return content
# ❌ Don't — 50-line function doing validation, persistence, and notification
```

### Type Annotations

```python
# ✅ Do — all parameters and return types annotated
async def create_item(name: str, price: float) -> Item:
    ...

# ❌ Don't
async def create_item(name, price):  # missing annotations
    ...
```

### Async Patterns

```python
# ✅ Do — async all the way, no blocking calls
async def get_items(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return list(result.scalars().all())

# ❌ Don't — blocking call inside async
async def get_items(db):
    time.sleep(1)  # blocks the event loop
```

### Error Handling

```python
# ✅ Do — service raises domain exception, route converts to HTTP
class ItemNotFoundError(Exception):
    pass

# In service:
async def get_item(item_id: str) -> Item:
    item = await repo.find(item_id)
    if not item:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return item

# In route:
@router.get("/items/{item_id}")
async def get_item_route(item_id: str):
    try:
        return await item_service.get_item(item_id)
    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
# ❌ Don't — bare except, swallowed errors
try:
    result = await risky_call()
except:
    pass
```
### FastAPI Endpoints

```python
# ✅ Do — typed request/response, dependency injection, proper status codes
@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(
    request: CreateItemRequest,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    return await service.create(request)

# ❌ Don't — untyped, no DI, wrong status code
@router.post("/items")
async def create_item(data: dict):
    ...
```
### Testing

```python
# ✅ Do — arrange/act/assert, isolated, descriptive name
async def test_create_item_returns_201_with_valid_data(client: AsyncClient):
    response = await client.post("/api/v1/items", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"

# ❌ Don't — multiple assertions for different behaviors in one test
async def test_items(client):  # tests create, read, update, delete all in one
    ...
```

---

## Frontend Standards

### Component Patterns

```tsx
// ✅ Do — named export, typed props, destructured
interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  return <div>{message.content}</div>;
}

// ❌ Don't — default export, untyped, inline props
export default function (props) {
  return <div>{props.message.content}</div>;
}
```
### Hook Patterns

```tsx
// ✅ Do — explicit return type, cleanup
interface UseConversationsReturn {
  conversations: Conversation[];
  loading: boolean;
  refresh: () => Promise<void>;
}

export function useConversations(): UseConversationsReturn {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  // ...
  return { conversations, loading, refresh };
}

// ❌ Don't — no return type, implicit any
export function useConversations() {
  const [data, setData] = useState();
}
```
### TypeScript Conventions

```tsx
// ✅ Do — strict types, no any, interface for props
interface ChatInputProps {
  onSend: (content: string) => void;
  disabled: boolean;
}

// ❌ Don't — any, loose types
const ChatInput = (props: any) => { ... };
```
### Event Handlers

```tsx
// ✅ Do — named handler, prevents default where needed
function handleSubmit(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  onSend(input.trim());
}

// ❌ Don't — inline logic, no typing
<form onSubmit={(e) => { e.preventDefault(); /* 20 lines of logic */ }}>
```
### API Calls

```tsx
// ✅ Do — typed response, error handling
export async function fetchConversations(): Promise<ConversationListResponse> {
  const res = await fetch(`${API_BASE}/conversations`);
  if (!res.ok) throw new Error("Failed to fetch conversations");
  return res.json();
}

// ❌ Don't — untyped, no error handling
export async function fetchConversations() {
  return fetch("/api/conversations").then(r => r.json());
}
```
### Accessibility

```tsx
// ✅ Do — semantic HTML, keyboard accessible
<button onClick={handleDelete} aria-label="Delete conversation">
  🗑️
</button>

// ❌ Don't — div with click, no keyboard support
<div onClick={handleDelete}>🗑️</div>
```
### Testing

```tsx
// ✅ Do — render + assert + interaction
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

it("should render message content", () => {
  render(<MessageBubble message={mockMessage} />);
  expect(screen.getByText("Hello")).toBeInTheDocument();
});

it("should call onSend when form is submitted", async () => {
  const onSend = vi.fn();
  render(<ChatInput onSend={onSend} disabled={false} />);
  await userEvent.type(screen.getByRole("textbox"), "Hello");
  await userEvent.click(screen.getByRole("button"));
  expect(onSend).toHaveBeenCalledWith("Hello");
});

// ❌ Don't — snapshot-only tests, no interaction tests
it("should match snapshot", () => {
  const { container } = render(<MessageBubble message={msg} />);
  expect(container).toMatchSnapshot();
});
```

---

## Git & PR Standards

### Branch Naming

```
feat/add-conversation-search
fix/message-streaming-timeout
hotfix/cors-header-missing
release/v1.2.0
```

### Commit Message Format

```
Add frontend CI pipeline; ESLint, Vitest & bundle checks & more…

{CI}
- Add ESLint lint job for frontend TypeScript code
- Add TypeScript type-check job with tsc --noEmit
- Add Vitest test execution job with JUnit reporting
- Add bundle size budget check (200 KB gzipped)

{Frontend}
- Add ESLint flat config with React, a11y, and import rules
- Add Vitest setup with React Testing Library and jsdom
- Fix accessibility violation in Sidebar conversation list

(No dependency updates.)
```

### PR Checklist

- [ ] Branch is up to date with `main`
- [ ] All CI checks pass locally
- [ ] PR description explains *what* changed and *why*
- [ ] Breaking changes are called out
- [ ] Tests cover the new/changed behavior

---

## CI Checks Reference

| Check | Fix Command |
|-------|-------------|
| Backend Ruff Lint | `cd backend && ruff check . --fix` |
| Backend Ruff Format | `cd backend && ruff format .` |
| Backend Mypy | `cd backend && mypy app/` |
| Backend Bandit | `cd backend && bandit -r app/ -c pyproject.toml` |
| Backend Pytest | `cd backend && pytest --tb=short` |
| Frontend ESLint | `cd frontend && npm run lint:fix` |
| Frontend TypeCheck | `cd frontend && npx tsc --noEmit` |
| Frontend Tests | `cd frontend && npm run test:run` |
| Frontend Bundle Size | `cd frontend && npm run build` (check output) |
