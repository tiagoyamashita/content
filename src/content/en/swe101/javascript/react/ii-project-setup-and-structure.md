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
  pages/                   # one file per screen / URL
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
    client.js              # base URL, headers, auth attach
    items.js               # getItems(), createItem()
  context/                 # React context providers (AuthContext)
  utils/                   # pure helpers (formatDate, validators)
  styles/                  # global CSS modules or theme tokens
  assets/                  # logos, icons imported in components
```

## 4. What goes where

| Folder / file | Put here | Do not put here |
|---------------|----------|-----------------|
| **`pages/`** | Route-level screens, compose components, wire data | Generic buttons, low-level UI |
| **`components/`** | Presentational pieces used on multiple pages | Direct `fetch` (prefer hooks/api) |
| **`features/`** | Domain bundle: list + form + hook for one area | Cross-domain utilities |
| **`api/`** | HTTP functions, JSON parsing, error mapping | React hooks or JSX |
| **`hooks/`** | Reusable state/effect logic | Page-specific one-offs (keep in `pages/` or `features/`) |
| **`context/`** | App-wide providers (auth user, theme) | Business logic that belongs in hooks |
| **`public/`** | Files referenced by fixed URL (`/logo.png`) | Files you `import` in JS (use `assets/`) |

**Rule of thumb:** **`pages`** know *which* data to load; **`api`** knows *how* to talk to the server; **`components`** know *how* to draw props.

## 5. Entry wiring (`main.jsx`)

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

## 6. Next.js differences (brief)

| Vite SPA | Next.js App Router |
|----------|-------------------|
| **`src/pages/`** or **`routes.jsx`** | **`app/`** directory — folders = URLs |
| Client-only by default | **`page.tsx`**, **`layout.tsx`**, **`loading.tsx`** |
| **`public/`** same | **`public/`** same |
| API calls from browser | **`app/api/`** route handlers (server) optional |

Same React components; routing and data-fetch location change.

## 7. Dependencies to add (typical SPA)

```text
npm install react-router-dom
npm install @tanstack/react-query    # server state (optional but common)
```

Dev-only: ESLint, Prettier, Testing Library — add when the team cares about CI.

## Next

Continue with [Rendering & server requests](iii-rendering-and-server-requests.md) for the render cycle and `fetch` patterns.
