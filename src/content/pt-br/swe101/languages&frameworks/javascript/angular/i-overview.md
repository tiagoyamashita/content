---
label: "I"
subtitle: "Overview"
group: "Angular"
order: 1
---
Angular — overview
**Angular** is a **full framework** (Google) for building SPAs — **TypeScript by default**, **opinionated structure**, **dependency injection**, and **RxJS** for async streams. Compare with [React](../react/i-overview.md) (library + ecosystem) and [jQuery](../jquery/i-overview.md) (DOM helper).

Parent track: [JavaScript overview](../i-overview.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Components, DI, RxJS, when to use Angular |
| **II — Project setup & structure** | CLI, folders, standalone apps, what file goes where |
| **III — Rendering & server requests** | Templates, change detection, `HttpClient`, Observables |
| **IV — Authentication** | Interceptors, guards, login flow, session bootstrap |
| **V — Forms & validation** | Reactive forms, validators, server field errors |

## Core ideas

| Concept | Meaning |
|---------|---------|
| **Component** | `@Component` — template + class + styles |
| **Standalone** | Modern default — no `NgModule` required per feature |
| **Template syntax** | `*ngIf`, `@for`, `(click)`, signal/`async` bindings |
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

## When Angular fits

| Good fit | Consider alternatives |
|----------|------------------------|
| Enterprise SPA with strict structure | Small marketing site |
| Team wants batteries-included (router, forms, HTTP) | Prefer minimal React + Vite |
| Heavy forms and validation (`ReactiveFormsModule`) | Server-rendered CRUD → [HTMX](../../htmx/i-overview.md) |
| Long-lived apps with many developers | Prototype → simpler stack first |

## Angular vs React (brief)

| | **Angular** | **React** |
|---|-------------|-----------|
| **Scope** | Full framework | UI library |
| **Language** | TypeScript expected | JS or TS |
| **Async** | RxJS observables | Promises, hooks, optional Rx |
| **DI** | Built-in | Context / manual |

## Next

Continue with [Project setup & structure](ii-project-setup-and-structure.md).
