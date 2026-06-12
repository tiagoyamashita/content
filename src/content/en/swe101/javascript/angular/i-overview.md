---
label: "I"
subtitle: "Overview"
group: "Angular"
order: 1
---
Angular — overview
**Angular** is a **full framework** (Google) for building SPAs — **TypeScript by default**, **opinionated structure**, **dependency injection**, and **RxJS** for async streams. Compare with [React](react/i-overview.md) (library + ecosystem) and [jQuery](jquery/i-overview.md) (DOM helper).

Parent track: [JavaScript overview](../i-overview.md).

## Core ideas

| Concept | Meaning |
|---------|---------|
| **Component** | `@Component` — template + class + styles |
| **Module / standalone** | `NgModule` (legacy) or **standalone components** (modern) |
| **Template syntax** | `*ngIf`, `*ngFor`, `(click)`, `[(ngModel)]` |
| **Service + DI** | `@Injectable()` — shared logic injected into components |
| **RxJS** | `Observable` streams for HTTP, websockets, user input |
| **Angular CLI** | `ng new`, `ng generate`, `ng serve`, `ng build` |

## Smallest component (standalone)

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-hello',
  standalone: true,
  template: `<h1>Hello, {{ name }}</h1>`,
})
export class HelloComponent {
  name = 'Angular';
}
```

## Typical project shape

```text
src/
  app/
    app.config.ts      # providers, routes
    app.routes.ts
    components/
    services/
    pages/
  main.ts              # bootstrapApplication(AppComponent)
angular.json
package.json
```

## CLI quick start

```text
npm install -g @angular/cli
ng new my-app
cd my-app && ng serve
```

Open `http://localhost:4200`.

## When Angular fits

| Good fit | Consider alternatives |
|----------|------------------------|
| Enterprise SPA with strict structure | Small marketing site |
| Team wants batteries-included (router, forms, HTTP) | Prefer minimal React + Vite |
| Heavy forms and validation (`ReactiveFormsModule`) | Server-rendered CRUD → [HTMX](../htmx/i-overview.md) |
| Long-lived apps with many developers | Prototype → simpler stack first |

## Angular vs React (brief)

| | **Angular** | **React** |
|---|-------------|-----------|
| **Scope** | Full framework | UI library |
| **Language** | TypeScript expected | JS or TS |
| **Async** | RxJS observables | Promises, hooks, optional Rx |
| **Learning curve** | Steeper upfront | Smaller core, many choices |

## Next steps (future notes)

Routing, `HttpClient`, reactive forms, change detection, and testing with Jasmine/Karma or Jest.
