---
label: "III"
subtitle: "Rendering & server requests"
group: "React"
order: 3
---
React — rendering & server requests
React turns **component functions** into **DOM nodes**. When **state** or **props** change, affected components **re-render** — then React diffs the virtual tree and updates the browser. Server data enters through **fetch** (or a library), usually in **effects** or **query hooks**.

Previous: [Project setup & structure](ii-project-setup-and-structure.md).

## 1. First paint: mount to DOM

```text
index.html (#root)
  → main.jsx createRoot(...).render(<App />)
  → App returns JSX tree
  → React creates real DOM under #root
```

```jsx
// src/main.jsx
import { createRoot } from 'react-dom/client';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(<App />);
```

```jsx
// src/App.jsx
export default function App() {
  return <h1>Hello</h1>;  // becomes <h1> in the document
}
```

## 2. Re-render cycle

```text
Event (click, fetch done, timer)
  → setState / setQueryData
  → component function runs again
  → React diff vs last virtual tree
  → commit only changed DOM nodes
```

| Trigger | Example |
|---------|---------|
| **Local state** | `setCount(c => c + 1)` |
| **Parent props** | Parent re-render passes new `items` |
| **Context** | `AuthContext` user changes |
| **External store** | TanStack Query cache update |

**Important:** Re-running the component function is normal — keep it **pure** (same props/state → same JSX). Side effects belong in **`useEffect`** or event handlers, not arbitrary code during render.

## 3. Component tree example

```jsx
// pages/ItemsPage.jsx
import { useItems } from '../hooks/useItems';
import { ItemRow } from '../components/ItemRow';

export function ItemsPage() {
  const { items, loading, error } = useItems();

  if (loading) return <p>Loading…</p>;
  if (error) return <p role="alert">Error: {error.message}</p>;

  return (
    <ul>
      {items.map(item => (
        <ItemRow key={item.id} item={item} />
      ))}
    </ul>
  );
}
```

```text
ItemsPage
  ├── loading branch → <p>
  ├── error branch   → <p>
  └── list branch    → <ul>
        └── ItemRow × N
```

Each **`key`** on list items helps React match rows across updates.

## 4. Server requests — API layer

Keep HTTP in **`src/api/`** — components call functions, not raw URLs everywhere.

```javascript
// src/api/client.js
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8080';

export async function api(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.message ?? res.statusText);
  }
  return res.status === 204 ? null : res.json();
}

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}
```

```javascript
// src/api/items.js
import { api } from './client';

export function getItems() {
  return api('/api/items');
}

export function createItem(payload) {
  return api('/api/items', { method: 'POST', body: JSON.stringify(payload) });
}
```

**Vite env:** define **`VITE_API_URL`** in **`.env`** — only `VITE_*` vars are exposed to the client.

## 5. Loading data with a custom hook

```jsx
// src/hooks/useItems.js
import { useEffect, useState } from 'react';
import { getItems } from '../api/items';

export function useItems() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getItems()
      .then(data => { if (!cancelled) setItems(data); })
      .catch(err => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };  // ignore stale response on unmount
  }, []);

  return { items, loading, error };
}
```

## 6. TanStack Query (recommended at scale)

```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getItems, createItem } from '../api/items';

export function ItemsPage() {
  const qc = useQueryClient();
  const { data: items = [], isLoading, error } = useQuery({
    queryKey: ['items'],
    queryFn: getItems,
  });

  const create = useMutation({
    mutationFn: createItem,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['items'] }),
  });

  if (isLoading) return <p>Loading…</p>;
  if (error) return <p role="alert">{error.message}</p>;

  return (
    <>
      <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>
      <button onClick={() => create.mutate({ name: 'New' })}>Add</button>
    </>
  );
}
```

Query handles **cache**, **refetch**, **deduping** — less boilerplate than manual `useEffect`.

## 7. Request flow (end to end)

```text
User opens /items
  → ItemsPage mounts
  → useQuery calls getItems()
  → fetch GET /api/items (+ auth header if configured)
  → JSON → cache → re-render with data
User clicks Add
  → mutation POST /api/items
  → onSuccess → invalidate → refetch list → UI updates
```

Backend is often [Spring Boot REST](../../java/springboot/iv-rest-controllers.md), FastAPI, or Node — React only sees HTTP + JSON.

## 8. Mutations and optimistic UI (preview)

```jsx
create.mutate(
  { name: 'Draft' },
  {
    onMutate: async () => {
      await qc.cancelQueries({ queryKey: ['items'] });
      // optionally patch cache before server responds
    },
  }
);
```

Use when the UI should feel instant; roll back on error.

## Next

Continue with [Authentication](iv-authentication.md) for tokens, cookies, and protected routes.
