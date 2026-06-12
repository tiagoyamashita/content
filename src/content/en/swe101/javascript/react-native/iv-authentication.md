---
label: "IV"
subtitle: "Authentication"
group: "React Native"
order: 4
---
React Native — authentication
Mobile apps authenticate with **Bearer tokens** or **refresh-token flows** — there is no HttpOnly cookie model like a same-site browser tab (unless you use WebView login). Store tokens in **secure storage**, attach them on API calls, and **guard navigation** so logged-out users never reach protected screens.

Previous: [Rendering & server requests](iii-rendering-and-server-requests.md). Web parallel: [React authentication](../react/iv-authentication.md). Backend: [Spring Security](../../java/springboot/security-basics-and-filter-chain.md).

## 1. Storage options on mobile

| Storage | Security | Use |
|---------|----------|-----|
| **`expo-secure-store`** | Encrypted keychain/Keystore | Access + refresh tokens |
| **Memory only** | Lost on app kill | Short-lived access token + refresh on launch |
| **`AsyncStorage`** | Not encrypted | User preferences — **not** for secrets |
| **`localStorage`** | N/A on native | Web-only |

**Rule:** Never trust the client — auth state is **UX**; the API must **verify** JWT or session on every request.

## 2. Login flow (token-based)

```text
LoginScreen submit
  → POST /api/auth/login { email, password }
  → 200 { accessToken, refreshToken?, user }
  → SecureStore.setItemAsync('accessToken', …)
  → AuthContext updates user
  → navigate to Home (tabs)
Subsequent fetch
  → api client reads token, Authorization header
  → 401 → clear storage, navigate to Login
```

## 3. Secure storage helper

```text
npx expo install expo-secure-store
```

```typescript
// src/lib/tokenStorage.ts
import * as SecureStore from 'expo-secure-store';

const ACCESS_KEY = 'accessToken';

export async function getAccessToken(): Promise<string | null> {
  return SecureStore.getItemAsync(ACCESS_KEY);
}

export async function setAccessToken(token: string): Promise<void> {
  await SecureStore.setItemAsync(ACCESS_KEY, token);
}

export async function clearTokens(): Promise<void> {
  await SecureStore.deleteItemAsync(ACCESS_KEY);
}
```

## 4. Auth context

Same pattern as web — load token on startup, expose `login` / `logout`:

```tsx
// src/context/AuthContext.tsx
import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { login as apiLogin, getCurrentUser } from '../api/auth';
import { getAccessToken, setAccessToken, clearTokens } from '../lib/tokenStorage';
import { setTokenGetter } from '../api/client';

type User = { id: string; email: string };

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const token = await getAccessToken();
      if (token) {
        setTokenGetter(() => token);
        try {
          const profile = await getCurrentUser(); // GET /api/auth/me
          setUser(profile);
        } catch {
          await clearTokens();
        }
      }
      setLoading(false);
    })();
  }, []);

  const login = async (email: string, password: string) => {
    const { accessToken, user: profile } = await apiLogin(email, password);
    await setAccessToken(accessToken);
    setTokenGetter(() => accessToken);
    setUser(profile);
  };

  const logout = async () => {
    await clearTokens();
    setTokenGetter(() => null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      logout,
      isAuthenticated: !!user,
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth outside AuthProvider');
  return ctx;
}
```

## 5. Attach token in API client

```typescript
// src/api/client.ts
let getToken: () => string | null | Promise<string | null> = () => null;

export function setTokenGetter(fn: typeof getToken) {
  getToken = fn;
}

export async function api(path: string, options: RequestInit = {}) {
  const token = await getToken();
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (res.status === 401) throw new AuthError();
  // ... parse JSON, throw on !ok
}

export class AuthError extends Error {
  constructor() {
    super('Unauthorized');
    this.name = 'AuthError';
  }
}
```

Wire **`setTokenGetter`** after login and on cold start when a stored token exists.

## 6. Protected navigation

### Expo Router

Split **auth** vs **app** groups:

```text
app/
  _layout.tsx           # AuthProvider, QueryClient
  (auth)/
    _layout.tsx
    login.tsx
  (app)/
    _layout.tsx         # redirect if !user
    (tabs)/
      index.tsx
      profile.tsx
```

```tsx
// app/(app)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '../../src/context/AuthContext';
import { ActivityIndicator, View } from 'react-native';

export default function AppLayout() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center' }}>
        <ActivityIndicator />
      </View>
    );
  }
  if (!isAuthenticated) return <Redirect href="/login" />;

  return <Stack screenOptions={{ headerShown: false }} />;
}
```

```tsx
// app/(auth)/login.tsx — after successful login
import { router } from 'expo-router';
// await login(email, password);
router.replace('/(app)/(tabs)');
```

### React Navigation

```tsx
// src/navigation/RootNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuth } from '../context/AuthContext';
import { LoginScreen } from '../screens/LoginScreen';
import { AppTabs } from './AppTabs';

const Stack = createNativeStackNavigator();

export function RootNavigator() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return null; // or splash screen

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <Stack.Screen name="App" component={AppTabs} />
        ) : (
          <Stack.Screen name="Login" component={LoginScreen} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## 7. Handle 401 globally

```tsx
// In AuthProvider or a dedicated hook
import { useEffect } from 'react';
import { AuthError } from '../api/client';

export function useAuthInterceptor(logout: () => Promise<void>) {
  useEffect(() => {
    // Option: wrap api() to call logout on AuthError
    // Or listen to query cache onError for 401
  }, [logout]);
}
```

On any **`AuthError`**: `await logout()` and navigation returns to Login (protected layout handles redirect).

## 8. Biometrics (preview)

**`expo-local-authentication`** — Face ID / fingerprint to **unlock** an already-logged-in session (not a substitute for server login).

```text
npx expo install expo-local-authentication
```

Flow: user logs in once → token in SecureStore → next app open prompts biometrics before reading token.

## 9. OAuth / social login (preview)

Common pattern: **open system browser** or in-app browser (`expo-auth-session`) → redirect URI → exchange code for tokens on your backend. Avoid embedding login WebViews for Google/Apple when their policies require system browser.

## Next

Continue with [Forms & validation](v-forms-and-validation.md) — `TextInput`, keyboard avoidance, and server field errors.
