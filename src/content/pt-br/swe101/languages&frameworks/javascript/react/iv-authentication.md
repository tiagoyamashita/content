---
label: "IV"
subtitle: "Authentication"
group: "React"
order: 4
---
React — authentication
SPAs authenticate by sending **credentials or tokens** on API requests and by **guarding routes** so unauthenticated users never see protected screens. React holds **who is logged in** in context or global state; the **server** still validates every request.

Previous: [Rendering & server requests](iii-rendering-and-server-requests.md). Backend patterns: [Spring Security filter chain](../../java/springboot/security-basics-and-filter-chain.md).

## 1. Two common models

| Model | Browser stores | Sent to API | Notes |
|-------|----------------|-------------|-------|
| **Cookie session** | HttpOnly cookie (set by server on login) | Cookie auto-sent with `fetch(..., { credentials: 'include' })` | XSS cannot read HttpOnly cookie; needs CSRF care |
| **Bearer token (JWT)** | Memory, or `localStorage` / sessionStorage | `Authorization: Bearer <token>` header | Easy for mobile + SPA; protect against XSS stealing token |

**Rule:** Never trust the client — React auth state is **UX**; the API must **verify** session or JWT on every call.

## 2. Login flow (token-based)

```text
LoginPage submit
  → POST /api/auth/login { email, password }
  → 200 { accessToken, user }
  → save token + user in AuthContext
  → navigate to /dashboard
Subsequent fetch
  → api client attaches Authorization header
  → 401 → clear auth, redirect to /login
```

## 3. Auth context

```jsx
// src/context/AuthContext.jsx
import { createContext, useContext, useMemo, useState } from 'react';
import { login as apiLogin } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => sessionStorage.getItem('token'));

  const login = async (email, password) => {
    const { accessToken, user: profile } = await apiLogin(email, password);
    sessionStorage.setItem('token', accessToken);
    setToken(accessToken);
    setUser(profile);
  };

  const logout = () => {
    sessionStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, token, login, logout, isAuthenticated: !!token }),
    [user, token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth outside AuthProvider');
  return ctx;
}
```

**`sessionStorage`** clears when the tab closes — slightly safer than `localStorage` for tokens; best is **memory-only** + refresh cookie (more setup).

## 4. Attach token in API client

```javascript
// src/api/client.js — extend from rendering note
let getToken = () => null;
export function setTokenGetter(fn) { getToken = fn; }

export async function api(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (res.status === 401) throw new AuthError();
  // ... rest unchanged
}
```

Wire in **`App`** or **`AuthProvider`:**

```jsx
import { setTokenGetter } from './api/client';
import { useAuth } from './context/AuthContext';

// inside AuthProvider after token state exists:
setTokenGetter(() => token);
```

## 5. Protected routes (React Router)

```jsx
// src/components/ProtectedRoute.jsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}
```

```jsx
// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
      </Route>
    </Routes>
  );
}
```

**`<Outlet />`** renders nested child routes when auth passes.

## 6. Login page (minimal)

```jsx
// src/pages/LoginPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message ?? 'Login failed');
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
      {error && <p role="alert">{error}</p>}
      <button type="submit">Sign in</button>
    </form>
  );
}
```

## 7. Cookie sessions (sketch)

```javascript
await fetch('/api/auth/login', {
  method: 'POST',
  credentials: 'include',  // send/receive cookies
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
});

// later requests
await fetch('/api/items', { credentials: 'include' });
```

Server sets **`Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax`**. React does not read the cookie — browser attaches it. Configure **CORS** on API: `Access-Control-Allow-Credentials: true` and explicit origin (not `*`).

## 8. Refresh and bootstrap

On app load, call **`GET /api/auth/me`** with token or cookie to restore user after refresh:

```jsx
useEffect(() => {
  if (!token) return;
  getCurrentUser()
    .then(setUser)
    .catch(logout);
}, [token]);
```

Show a global loading shell until bootstrap finishes so protected routes do not flash.

## 9. Security checklist

- [ ] API validates auth on **every** protected endpoint
- [ ] Prefer **HttpOnly cookies** or **short-lived access token** + refresh
- [ ] Handle **401** globally (logout + redirect)
- [ ] Do not store tokens in URLs or logs
- [ ] CSP + sanitize HTML if rendering user content

## Next

Continue with [Forms & validation](v-forms-and-validation.md).
