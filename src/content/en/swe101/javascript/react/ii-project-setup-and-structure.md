---
label: "II"
subtitle: "Project setup & structure"
group: "React"
order: 2
---
React — project setup & structure
This track uses **Vite + React** for a standard SPA. **Next.js** uses a similar mental model but adds file-based routing and server components — folder names shift slightly (see §6).

Previous: [Overview](i-overview.md).

## 1. Create the project

**Requirements:** Node.js 20+ LTS, npm (or pnpm/yarn).

```text
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

| Script | Command | Purpose |
|--------|---------|---------|
| **dev** | `npm run dev` | Hot reload dev server |
| **build** | `npm run build` | Production bundle → `dist/` |
| **preview** | `npm run preview` | Serve production build locally |

**TypeScript variant:** use `--template react-ts` — recommended for teams; examples below use `.jsx` for brevity.

## 2. What Vite gives you

```text
my-app/
  index.html              # single HTML shell — <div id="root">
  vite.config.js          # dev server, plugins, build options
  package.json            # dependencies and scripts
  public/                 # static files copied as-is (favicon, robots.txt)
  src/
    main.jsx              # entry — mounts React to #root
    App.jsx               # root component
    index.css             # global styles
    assets/               # images imported from components
```

**`index.html`** loads **`/src/main.jsx`** as a module. Vite bundles on the fly in dev; Rollup bundles for production.

## 3. Recommended `src/` layout (SPA)

Grow into this shape as the app gets real — not every folder on day one.

```text
src/
  main.jsx                 # ReactDOM.createRoot, providers, router
  App.jsx                  # layout shell (nav, outlet)
  routes.jsx               # route definitions (optional split)
  pages/                   # or views/ — one file per screen / URL
    HomePage.jsx
    ItemsPage.jsx
    LoginPage.jsx
  components/              # reusable UI — no route-specific data fetching
    Button.jsx
    Modal.jsx
    ItemRow.jsx
  features/                # optional — domain slices (items, auth, billing)
    items/
      ItemsList.jsx
      useItems.js          # feature-specific hook
  hooks/                   # shared hooks (useDebounce, useLocalStorage)
  api/                     # fetch wrappers — no JSX
    client.js              # or lib/client.js — base URL, headers, auth
    items.js               # getItems(), createItem()
  lib/                     # optional — shared non-UI (or use utils/)
  context/                 # React context providers (AuthContext)
  utils/                   # pure helpers (formatDate, validators)
  styles/                  # global CSS modules or theme tokens
  assets/                  # logos, icons imported in components
```

## 4. What goes where

| Folder / file | Put here | Do not put here |
|---------------|----------|-----------------|
| **`pages/`** or **`views/`** | Route-level screens, compose components, wire data | Generic buttons, low-level UI |
| **`components/`** | Presentational pieces used on multiple pages | Direct `fetch` (prefer hooks/api) |
| **`features/`** | Domain bundle: list + form + hook for one area | Cross-domain utilities |
| **`api/`** | HTTP functions, JSON parsing, error mapping | React hooks or JSX |
| **`hooks/`** | Reusable state/effect logic | Page-specific one-offs (keep in `pages/` or `features/`) |
| **`context/`** | App-wide providers (auth user, theme) | Business logic that belongs in hooks |
| **`public/`** | Files referenced by fixed URL (`/logo.png`) | Files you `import` in JS (use `assets/`) |

**Rule of thumb:** **`pages`** know *which* data to load; **`api`** knows *how* to talk to the server; **`components`** know *how* to draw props.

## 5. Naming variants — same role, different labels

React does **not** define folder names. Teams pick conventions; **consistency** matters more than the label.

### Route-level screens: `pages/` vs `views/` vs `screens/`

All three usually mean: **one component (or folder) per major route / URL**.

| Folder | Common in | Meaning |
|--------|-----------|---------|
| **`pages/`** | Vite SPAs, Next.js docs | “One URL = one page” |
| **`views/`** | React + Vue teams, MVVM heritage | “What the user sees” — same as pages |
| **`screens/`** | React Native, mobile-first | Full-screen route target |

```text
pages/ItemsPage.jsx   ≡   views/ItemsView.jsx   ≡   screens/ItemsScreen.jsx
```

**When to use which:** pick **one** name for the whole repo. Use **`pages`** if you follow most web tutorials; use **`views`** if your team already uses that word or splits “thin route” vs “heavy view” (optional pattern below).

**Optional split (large apps only):**

| Folder | Some teams use it for |
|--------|------------------------|
| **`pages/`** | Router entry — thin file that imports a view |
| **`views/`** | Presentation-heavy screen logic |

Many apps **do not** split — one folder is enough.

### Shared code: `lib/` vs `utils/` vs `services/`

| Folder | Typical contents | Avoid |
|--------|------------------|-------|
| **`lib/`** | Project “library” code: HTTP client, formatters, constants, third-party wrappers | JSX, route components |
| **`utils/`** | Same as `lib` in many repos — **pick one**, not both | Duplicating `lib/` |
| **`services/`** | Sometimes business logic + API calls (blurs with `api/`) | Random one-off helpers |

```text
lib/formatDate.js     ← pure helper
lib/http.js           ← fetch wrapper (some teams put this in api/ instead)
utils/validators.js   ← if you use utils/ instead of lib/
```

**Why `lib` exists:** signals **reusable infrastructure** — not UI, not a single feature. Popular in Next.js examples (`lib/db.ts`, `lib/auth.ts`).

**When to use `lib/`:** app grows past a few files and you need a clear home for shared non-UI code. **Skip it** on day one — a single `utils/` or inline helpers in `api/client.js` is fine.

### `api/` layout: flat vs `api/lib/`

**Flat (this track’s default):**

```text
api/
  client.js    ← base URL, headers, errors
  items.js     ← getItems(), createItem()
  auth.js
```

**Nested `api/lib/` (HTTP internals only):**

```text
api/
  lib/
    client.ts    ← fetch/axios instance, interceptors
    errors.ts    ← ApiError, map 422 field errors
    types.ts     ← shared response types
  items.ts       ← imports from ./lib/client
  auth.ts
```

| Style | Why | When |
|-------|-----|------|
| **Flat `api/client.js`** | Simple, obvious entry point | Small/medium SPAs, learning projects |
| **`api/lib/`** | Endpoint files stay thin; HTTP plumbing isolated | Many endpoints, shared error/auth logic |
| **`src/lib/http` + `api/`** | HTTP client is app-wide, `api/` is domain-only | Same as above; client imported by `api/*` |

```text
View/Page  →  hook  →  api/items.js  →  api/lib/client  →  backend
```

**Rule:** exactly **one** HTTP client location — not `lib/http`, `api/client`, and `api/lib/client` all at once.

## 6. Structure patterns — how, why, when

Choose structure by **team size**, **app size**, and **how long the codebase will live** — not because a tutorial used one folder name.

### Pattern A — Flat / starter (1–10 screens)

```text
src/
  App.jsx
  pages/          # or views/
  components/
  api/client.js
  api/items.js
```

| | |
|--|--|
| **How** | Everything visible in a few folders; minimal indirection |
| **Why** | Fast to navigate; no ceremony |
| **When** | Prototypes, learning, internal tools, solo dev |

### Pattern B — Feature slices (medium apps)

```text
src/
  features/
    items/
      ItemsPage.jsx
      ItemForm.jsx
      useItems.js
      items.api.js
    auth/
      LoginPage.jsx
      auth.api.js
  components/       # truly shared UI
  lib/ or api/      # shared client only
```

| | |
|--|--|
| **How** | Colocate everything for one domain under **`features/<name>/`** |
| **Why** | Change “items” without hunting across `pages/`, `api/`, `hooks/` |
| **When** | 5+ domains (auth, billing, admin, …), multiple devs |

### Pattern C — Layered (enterprise / large SPA)

```text
src/
  pages/            # thin route targets
  views/            # optional — heavy presentation
  components/
  hooks/
  api/
    lib/
  lib/
  context/
```

| | |
|--|--|
| **How** | Strict layers: UI → hooks → api → lib |
| **Why** | Clear boundaries, easier code review rules (“no fetch in components”) |
| **When** | Long-lived product, many contributors, lint rules enforce layers |

### Pattern D — Next.js App Router

```text
app/
  items/
    page.tsx        # route — replaces pages/ItemsPage
    loading.tsx
  layout.tsx
lib/                # db, auth, server helpers
components/
```

| | |
|--|--|
| **How** | Folders under **`app/`** = URLs; **`lib/`** often holds server-only helpers |
| **Why** | Framework owns routing and SSR |
| **When** | SEO, server components, API routes in same repo |

## 7. Decision guide

| Question | Lean toward |
|----------|-------------|
| Solo dev, first React app? | **Pattern A** — `pages/` or `views/`, flat `api/` |
| Same repo naming as Vue/backend “views”? | **`views/`** — fine, document it in README |
| 10+ API modules? | **`api/lib/client`** + thin `api/*.ts` files |
| “Where does shared code go?” fights? | Pick **`lib/` OR `utils/`**, write one sentence in README |
| Features copy-pasted across folders? | **Pattern B** — `features/<domain>/` |
| Need SSR / file routing? | **Next.js Pattern D** |

**Onboarding rule:** new files go where **similar files already live**. If the repo uses **`views/`** and **`api/lib/`**, match that — renaming mid-project helps only when the whole team agrees.

## 8. Entry wiring (`main.jsx`)

```jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import App from './App.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
```

Providers stack outside **`App`** so routes and deep components share auth, query client, theme, etc.

## 9. Next.js differences (brief)

| Vite SPA | Next.js App Router |
|----------|-------------------|
| **`src/pages/`** or **`routes.jsx`** | **`app/`** directory — folders = URLs |
| Client-only by default | **`page.tsx`**, **`layout.tsx`**, **`loading.tsx`** |
| **`public/`** same | **`public/`** same |
| API calls from browser | **`app/api/`** route handlers (server) optional |

Same React components; routing and data-fetch location change.

## 10. Dependencies to add (typical SPA)

```text
npm install react-router-dom
npm install @tanstack/react-query    # server state (optional but common)
```

Dev-only: ESLint, Prettier, Testing Library — add when the team cares about CI.

## Next

Continue with [Rendering & server requests](iii-rendering-and-server-requests.md) for the render cycle and `fetch` patterns.
