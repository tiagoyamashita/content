---
label: "IV"
subtitle: "Authentication"
group: "Angular"
order: 4
---
Angular — authentication
Angular apps authenticate with **`HttpClient`** + **`AuthService`**, attach credentials via an **HTTP interceptor**, and block routes with **functional guards**. The server still validates every API call — client auth is for **UX and routing** only.

Previous: [Rendering & server requests](iii-rendering-and-server-requests.md). Backend: [Spring Security filter chain](../../java/springboot/security-basics-and-filter-chain.md).

## 1. Token vs cookie (same as React)

| Model | Browser | HttpClient config |
|-------|---------|-------------------|
| **Bearer JWT** | `sessionStorage` / memory | Interceptor adds `Authorization` header |
| **Cookie session** | HttpOnly cookie from server | `{ withCredentials: true }` on requests |

Never trust the client — guards hide pages; **API must return 401** for invalid tokens.

## 2. Auth service

```typescript
// core/auth/auth.service.ts
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface User {
  id: number;
  email: string;
  name: string;
}

interface LoginResponse {
  accessToken: string;
  user: User;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private tokenKey = 'access_token';

  user = signal<User | null>(null);

  get token(): string | null {
    return sessionStorage.getItem(this.tokenKey);
  }

  get isAuthenticated(): boolean {
    return !!this.token;
  }

  login(email: string, password: string) {
    return this.http
      .post<LoginResponse>(`${environment.apiUrl}/api/auth/login`, { email, password })
      .pipe(
        tap(res => {
          sessionStorage.setItem(this.tokenKey, res.accessToken);
          this.user.set(res.user);
        }),
      );
  }

  logout() {
    sessionStorage.removeItem(this.tokenKey);
    this.user.set(null);
  }

  bootstrap() {
    if (!this.token) return;
    return this.http.get<User>(`${environment.apiUrl}/api/auth/me`).pipe(
      tap(u => this.user.set(u)),
    );
  }
}
```

Call **`bootstrap()`** once at app start (see §6).

## 3. HTTP interceptor (attach token)

```typescript
// core/auth/auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const token = auth.token;

  const cloned = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(cloned).pipe(
    catchError(err => {
      if (err.status === 401) {
        auth.logout();
        router.navigateByUrl('/login');
      }
      return throwError(() => err);
    }),
  );
};
```

Register in **`app.config.ts`** with **`withInterceptors([authInterceptor])`**.

## 4. Route guard

```typescript
// core/auth/auth.guard.ts
import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isAuthenticated) return true;
  return router.createUrlTree(['/login']);
};
```

```typescript
// app.routes.ts
{
  path: 'dashboard',
  canActivate: [authGuard],
  loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent),
},
```

**`createUrlTree`** redirects without losing router state.

## 5. Login component

```typescript
// features/auth/login.component.ts
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input type="email" formControlName="email" />
      <input type="password" formControlName="password" />
      @if (error) { <p role="alert">{{ error }}</p> }
      <button type="submit" [disabled]="form.invalid || loading">Sign in</button>
    </form>
  `,
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);

  loading = false;
  error: string | null = null;

  form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
  });

  submit() {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = null;
    const { email, password } = this.form.getRawValue();

    this.auth.login(email, password).subscribe({
      next: () => this.router.navigateByUrl('/dashboard'),
      error: err => {
        this.error = err.error?.message ?? 'Login failed';
        this.loading = false;
      },
      complete: () => (this.loading = false),
    });
  }
}
```

## 6. Bootstrap on app load

Avoid flash of login on protected routes:

```typescript
// app.config.ts — APP_INITIALIZER pattern (functional)
import { APP_INITIALIZER, ApplicationConfig } from '@angular/core';
import { AuthService } from './core/auth/auth.service';
import { firstValueFrom } from 'rxjs';

function initAuth(auth: AuthService) {
  return () => (auth.token ? firstValueFrom(auth.bootstrap()!) : Promise.resolve());
}

export const appConfig: ApplicationConfig = {
  providers: [
    { provide: APP_INITIALIZER, useFactory: initAuth, deps: [AuthService], multi: true },
    // ... router, http
  ],
};
```

Show a shell spinner until initializer completes if bootstrap is slow.

## 7. Cookie sessions

```typescript
this.http.post(`${environment.apiUrl}/api/auth/login`, body, { withCredentials: true });
this.http.get(`${environment.apiUrl}/api/items`, { withCredentials: true });
```

Server sets **`HttpOnly`** cookie — interceptor may only need **`withCredentials`**, not `Authorization`. Configure API **CORS** with credentials.

## 8. Security checklist

- [ ] **`authGuard`** on all protected routes
- [ ] Interceptor handles **401** globally
- [ ] No secrets in `environment.ts` committed to git
- [ ] Short-lived access token or HttpOnly refresh cookie for production
- [ ] HTTPS only in prod

## Next

Continue with [Forms & validation](v-forms-and-validation.md).
