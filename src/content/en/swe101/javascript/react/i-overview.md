---
label: "I"
subtitle: "Overview"
group: "React"
order: 1
---
React — overview
**React** is a **component-based UI library** from Meta. You describe UI as **functions of state** (JSX), React updates the DOM efficiently, and the ecosystem (Vite, Next.js, React Router) covers routing, SSR, and data fetching.

Parent track: [JavaScript overview](../i-overview.md). Contrast with [HTMX](../htmx/i-overview.md) when most UI can stay server-rendered.

## Core ideas

| Concept | Meaning |
|---------|---------|
| **Component** | Reusable UI unit — `function Button({ label }) { … }` |
| **JSX** | HTML-like syntax in JavaScript — compiles to `React.createElement` |
| **Props** | Inputs passed parent → child (read-only) |
| **State** | Data that changes over time — `useState`, `useReducer` |
| **Hooks** | `useEffect`, `useContext`, etc. — logic in function components |
| **Virtual DOM** | Diff tree → minimal real DOM updates |

## Smallest example

```jsx
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Typical project shape

```text
src/
  main.jsx          # mount <App /> to #root
  App.jsx           # layout, routes
  components/       # presentational pieces
  pages/            # route-level screens
  hooks/            # shared use* logic
  api/              # fetch wrappers
package.json
vite.config.js      # or Next.js / CRA
```

## Tooling you will meet

| Tool | Role |
|------|------|
| **Vite** | Fast dev server + production build |
| **Next.js** | React + routing + SSR/SSG |
| **React Router** | Client-side routes in SPAs |
| **TanStack Query** | Server state, cache, refetch |
| **TypeScript** | Optional but common for large apps |

## When React fits

| Good fit | Consider alternatives |
|----------|------------------------|
| Rich client UX (editors, wizards, dashboards) | Mostly CRUD + forms → HTMX or server templates |
| Mobile/web shared component thinking (React Native) | Content site → static/SSR without heavy client state |
| Large frontend team, component library | Small internal tool → simpler stack |

## Data flow (preview)

```text
User action  →  setState / dispatch  →  re-render component  →  React commits DOM changes
Async fetch  →  useEffect or Query  →  set state with response  →  UI updates
```

## Next steps (future notes)

Create app with Vite, props vs state, lists and keys, forms, routing, and testing with React Testing Library.
