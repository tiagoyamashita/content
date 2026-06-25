---
label: "III"
subtitle: "Rendering & server requests"
group: "Angular"
order: 3
---
Angular — rendering & server requests
Angular **renders templates** bound to **component class** properties. When data changes, **change detection** updates the DOM. Server data flows through **`HttpClient`**, which returns **RxJS Observables** — consumed in templates with **`async` pipe** or in the class with **`subscribe`**.

Previous: [Project setup & structure](ii-project-setup-and-structure.md).

## 1. Boot to first paint

```text
index.html <app-root>
  → main.ts bootstrapApplication(AppComponent)
  → AppComponent template renders
  → router-outlet loads routed component
  → child template + bindings applied to DOM
```

```typescript
@Component({
  selector: 'app-root',
  standalone: true,
  template: `<h1>{{ title }}</h1><router-outlet />`,
})
export class AppComponent {
  title = 'My App';
}
```

**Interpolation** `{{ title }}` displays the property value. Updates when change detection runs.

## 2. Template bindings

| Syntax | Direction | Example |
|--------|-----------|---------|
| **`{{ expr }}`** | class → DOM | `{{ item.name }}` |
| **`[property]="expr"`** | class → DOM | `[disabled]="loading"` |
| **`(event)="handler()"`** | DOM → class | `(click)="save()"` |
| **`[(ngModel)]="field"`** | two-way | needs `FormsModule` import |
| **`*ngIf` / `@if`** | conditional | `@if (loading) { … }` |
| **`*ngFor` / `@for`** | lists | `@for (item of items; track item.id) { … }` |

Modern **control flow** (`@if`, `@for`) is preferred over structural directives in new code.

## 3. Change detection (mental model)

```text
Event (click, HTTP response, timer)
  → zone or signal notifies Angular
  → change detection walks component tree
  → bindings re-evaluated → DOM patched
```

| Approach | Notes |
|----------|-------|
| **Default (Zone.js)** | Most apps — any async callback triggers check |
| **Signals** (`signal()`, `computed()`) | Fine-grained updates — Angular 16+ |
| **OnPush** | Component checks only when inputs change or events fire — performance |

Keep components **thin**: template + delegation to services.

## 4. List page example

```typescript
// features/items/items-list.component.ts
import { Component, inject, OnInit } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { ItemsService } from './items.service';

@Component({
  selector: 'app-items-list',
  standalone: true,
  imports: [AsyncPipe],
  template: `
    @if (items$ | async; as items) {
      <ul>
        @for (item of items; track item.id) {
          <li>{{ item.name }}</li>
        }
      </ul>
    } @else {
      <p>Loading…</p>
    }
  `,
})
export class ItemsListComponent implements OnInit {
  private itemsService = inject(ItemsService);
  items$ = this.itemsService.getItems();

  ngOnInit() {
    // optional: trigger refresh, combine streams, etc.
  }
}
```

**`async` pipe** subscribes and unsubscribes automatically — avoids memory leaks in templates.

## 5. HTTP service layer

```typescript
// features/items/items.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Item {
  id: number;
  name: string;
}

@Injectable({ providedIn: 'root' })
export class ItemsService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/api/items`;

  getItems(): Observable<Item[]> {
    return this.http.get<Item[]>(this.base);
  }

  createItem(payload: { name: string }): Observable<Item> {
    return this.http.post<Item>(this.base, payload);
  }
}
```

**`providedIn: 'root'`** — one app-wide singleton, no module registration.

## 6. Loading, error, and empty states

```typescript
import { Component, inject } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { ItemsService } from './items.service';
import { catchError, of, startWith } from 'rxjs';

@Component({
  standalone: true,
  imports: [AsyncPipe],
  template: `
    @if (state$ | async; as state) {
      @if (state.error) {
        <p role="alert">Error: {{ state.error }}</p>
      } @else if (state.loading) {
        <p>Loading…</p>
      } @else {
        <ul>
          @for (item of state.items; track item.id) {
            <li>{{ item.name }}</li>
          }
        </ul>
      }
    }
  `,
})
export class ItemsListComponent {
  private items = inject(ItemsService);

  state$ = this.items.getItems().pipe(
    startWith(null),
    // map to { loading, items, error } — or use separate observables
    catchError(err => of({ loading: false, items: [], error: err.message })),
  );
}
```

At scale, use **`switchMap`**, **`BehaviorSubject`**, or libraries like **NgRx** / **TanStack Query (experimental)** — start with service + `async` pipe.

## 7. Request flow (end to end)

```text
Route activates ItemsListComponent
  → template evaluates items$ | async
  → ItemsService.getItems() called once (shareReplay optional)
  → HttpClient GET /api/items
  → JSON → Observable emits
  → async pipe updates view
User clicks Add
  → component calls createItem().subscribe()
  → POST /api/items
  → refresh list (re-fetch or push to local Subject)
```

Backend is often [Spring Boot REST](../../java/springboot/iv-rest-controllers.md) — Angular only sees HTTP + JSON.

## 8. HttpClient setup reminder

In **`app.config.ts`:**

```typescript
import { provideHttpClient, withInterceptors } from '@angular/common/http';

provideHttpClient(withInterceptors([authInterceptor])),
```

Interceptors attach headers (auth), log, or map errors globally — see [Authentication](iv-authentication.md).

## 9. RxJS essentials

| Operator | Use |
|----------|-----|
| **`map`** | Transform response body |
| **`catchError`** | Map HTTP failure to fallback or rethrow |
| **`tap`** | Side effect (logging) without changing stream |
| **`switchMap`** | Cancel prior request when new search term arrives |
| **`shareReplay(1)`** | Cache last HTTP result for multiple subscribers |

Prefer **`async` pipe** over manual **`subscribe`** in components when possible.

## Next

Continue with [Authentication](iv-authentication.md).
