---
label: "II"
subtitle: "Project setup & structure"
group: "Angular"
order: 2
---
Angular — project setup & structure
Modern Angular apps are **standalone** (no root `NgModule`), bootstrapped with **`bootstrapApplication`**, and organized with the **CLI**. Examples assume **Angular 17+** and **TypeScript**.

Previous: [Overview](i-overview.md).

## 1. Create the project

**Requirements:** Node.js 20+ LTS, npm.

```text
npm install -g @angular/cli
ng new my-app --standalone --routing --style=css
cd my-app
ng serve
```

Open `http://localhost:4200`.

| CLI flag | Meaning |
|----------|---------|
| **`--standalone`** | Standalone components (default in recent CLI) |
| **`--routing`** | Creates `app.routes.ts` |
| **`--style=css`** | Component styles format (scss, sass also available) |

| Script | Command | Purpose |
|--------|---------|---------|
| **serve** | `ng serve` | Dev server + live reload |
| **build** | `ng build` | Production output → `dist/` |
| **test** | `ng test` | Unit tests (Karma/Jest per config) |

## 2. Top-level layout

```text
my-app/
  angular.json           # workspace config — build, serve, assets
  package.json
  tsconfig.json          # TypeScript compiler options
  src/
    index.html           # <app-root> shell
    main.ts              # bootstrapApplication(...)
    styles.css           # global styles
    app/
      app.component.ts   # root component
      app.config.ts      # providers (router, http, etc.)
      app.routes.ts      # route table
    assets/              # static files (copied to dist)
    environments/        # optional env-specific constants
      environment.ts
      environment.development.ts
```

**`angular.json`** defines how **`ng build`** bundles — browser target, assets, file replacements for prod.

## 3. Recommended `src/app/` layout

```text
src/app/
  app.component.ts       # shell: nav + <router-outlet>
  app.config.ts
  app.routes.ts
  core/                  # singleton services, guards, interceptors (import once)
    auth/
      auth.service.ts
      auth.interceptor.ts
      auth.guard.ts
    api/
      api-base.ts
  shared/                # dumb UI reused everywhere
    components/
      button/
      modal/
    pipes/
    directives/
  features/              # domain slices — lazy-loaded when app grows
    items/
      items.routes.ts
      items-list.component.ts
      item-form.component.ts
      items.service.ts
    auth/
      login.component.ts
  pages/                 # optional alias for route-level components
    dashboard/
      dashboard.component.ts
```

## 4. What goes where

| Folder | Put here | Do not put here |
|--------|----------|-----------------|
| **`core/`** | Auth, HTTP interceptors, app-wide singletons | Feature-specific templates |
| **`shared/`** | Presentational components, pipes, directives | HTTP calls to business APIs |
| **`features/`** | One domain: components + service + routes for that area | Cross-feature utilities |
| **`*.service.ts`** | Data access, stateless API wrappers | DOM manipulation |
| **`*.component.ts`** | Template + user interaction for one UI unit | Raw HTTP in every component (use services) |
| **`assets/`** | Images/fonts at fixed paths | Files you import in TypeScript |
| **`environments/`** | `apiUrl`, feature flags | Secrets (never commit prod keys) |

**Rule of thumb:** **components** display and emit events; **services** fetch and hold business logic; **core** wires auth and HTTP once for the whole app.

## 5. Bootstrap and providers (`main.ts` + `app.config.ts`)

```typescript
// src/main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

```typescript
// src/app/app.config.ts
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { authInterceptor } from './core/auth/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
  ],
};
```

## 6. Root component and routes

```typescript
// src/app/app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <nav>
      <a routerLink="/items">Items</a>
      <a routerLink="/login">Login</a>
    </nav>
    <router-outlet />
  `,
})
export class AppComponent {}
```

```typescript
// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent) },
  {
    path: 'items',
    canActivate: [authGuard],
    loadComponent: () => import('./features/items/items-list.component').then(m => m.ItemsListComponent),
  },
  { path: '', redirectTo: 'items', pathMatch: 'full' },
];
```

**Lazy `loadComponent`** keeps initial bundle smaller — one file per route.

## 7. CLI generators

```text
ng generate component features/items/item-row --standalone
ng generate service features/items/items
ng generate guard core/auth/auth --functional
ng generate interceptor core/auth/auth
```

Naming convention: **`feature-name.type.ts`** — e.g. `items.service.ts`, `login.component.ts`.

## 8. Environment API URL

```typescript
// src/environments/environment.development.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080',
};
```

```typescript
// inject in service
import { environment } from '../../../environments/environment';
private base = environment.apiUrl;
```

Use **`fileReplacements`** in `angular.json` for prod builds.

## Next

Continue with [Rendering & server requests](iii-rendering-and-server-requests.md).
