---
label: "I"
subtitle: "Overview"
group: "React"
order: 1
---
React — overview
**React** is a **component-based UI library** from Meta. You describe UI as **functions of state** (JSX), React updates the DOM efficiently, and the ecosystem (Vite, Next.js, React Router) covers routing, SSR, and data fetching.

Parent track: [JavaScript overview](../i-overview.md). Contrast with [HTMX](../../htmx/i-overview.md) when most UI can stay server-rendered.

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Components, JSX, hooks, when to use React |
| **II — Project setup & structure** | Vite, folders, `pages` vs `views`, `lib`, `api/lib`, when to use each pattern |
| **III — Rendering & server requests** | Mount/render cycle, `useEffect` fetch timeline, stale-data guards, TanStack Query |
| **IV — Authentication** | Tokens, cookies, protected routes, auth context |
| **V — Forms & validation** | Controlled inputs, client validation, server errors |

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

## When React fits

| Good fit | Consider alternatives |
|----------|------------------------|
| Rich client UX (editors, wizards, dashboards) | Mostly CRUD + forms → [HTMX](../../htmx/i-overview.md) |
| Mobile/web shared component thinking (React Native) | Content site → static/SSR without heavy client state |
| Large frontend team, component library | Small internal tool → simpler stack |

## Next

Continue with [Project setup & structure](ii-project-setup-and-structure.md).
