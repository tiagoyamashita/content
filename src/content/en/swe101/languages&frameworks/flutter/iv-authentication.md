---
label: "IV"
subtitle: "Authentication"
group: "Flutter"
order: 4
---
Flutter — authentication
Mobile and desktop Flutter apps use **Bearer tokens** (or refresh-token flows) stored in **secure storage**. Attach tokens on HTTP calls and **guard routes** so logged-out users cannot reach protected screens.

Previous: [Rendering & server requests](iii-rendering-and-server-requests.md). Parallel: [React Native auth](../javascript/react-native/iv-authentication.md), [React auth](../javascript/react/iv-authentication.md).

## 1. Storage on device

| Storage | Package | Use |
|---------|---------|-----|
| **Secure storage** | `flutter_secure_storage` | Access / refresh tokens |
| **Shared preferences** | `shared_preferences` | Theme, flags — not secrets |
| **Memory** | Your `AuthService` | Short-lived token for session |

```text
flutter pub add flutter_secure_storage
```

**Rule:** Client auth state is **UX** only — [Spring Boot](../java/springboot/security-basics-and-filter-chain.md) (or any API) must validate every request.

## 2. Login flow

```text
LoginScreen submit
  → POST /api/auth/login { email, password }
  → 200 { accessToken, user }
  → secure storage write
  → auth state updates
  → go_router → /home
Later GET /api/items
  → Authorization: Bearer …
  → 401 → clear storage → /login
```

## 3. Token storage service

```dart
// lib/services/token_storage.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenStorage {
  static const _key = 'access_token';
  final _storage = const FlutterSecureStorage();

  Future<String?> read() => _storage.read(key: _key);

  Future<void> write(String token) => _storage.write(key: _key, value: token);

  Future<void> clear() => _storage.delete(key: _key);
}
```

## 4. Auth service + state

```dart
// lib/services/auth_service.dart
import '../models/user.dart';
import 'api_client.dart';
import 'token_storage.dart';

class AuthService {
  AuthService(this._api, this._tokens);

  final ApiClient _api;
  final TokenStorage _tokens;
  User? user;

  Future<void> restoreSession() async {
    final token = await _tokens.read();
    if (token == null) return;
    _api.getToken = () async => token;
    final data = await _api.get('/api/auth/me') as Map<String, dynamic>;
    user = User.fromJson(data);
  }

  Future<void> login(String email, String password) async {
    final data = await _api.post('/api/auth/login', {
      'email': email,
      'password': password,
    }) as Map<String, dynamic>;
    final token = data['accessToken'] as String;
    await _tokens.write(token);
    _api.getToken = () async => token;
    user = User.fromJson(data['user'] as Map<String, dynamic>);
  }

  Future<void> logout() async {
    await _tokens.clear();
    _api.getToken = () async => null;
    user = null;
  }

  bool get isAuthenticated => user != null;
}
```

Wire **`restoreSession`** in `main()` before `runApp` if you need splash-until-ready:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final auth = AuthService(api, tokens);
  await auth.restoreSession();
  runApp(MyApp(auth: auth));
}
```

## 5. Expose auth to the widget tree

**Provider** example:

```dart
// lib/providers/auth_provider.dart
import 'package:flutter/foundation.dart';
import '../services/auth_service.dart';

class AuthNotifier extends ChangeNotifier {
  AuthNotifier(this._auth);
  final AuthService _auth;

  bool get isAuthenticated => _auth.isAuthenticated;
  User? get user => _auth.user;

  Future<void> login(String email, String password) async {
    await _auth.login(email, password);
    notifyListeners();
  }

  Future<void> logout() async {
    await _auth.logout();
    notifyListeners();
  }
}
```

Wrap app:

```dart
ChangeNotifierProvider(
  create: (_) => AuthNotifier(authService),
  child: const MyApp(),
);
```

## 6. Protected routes with `go_router`

```dart
// lib/router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

GoRouter createRouter(AuthNotifier auth) {
  return GoRouter(
    initialLocation: '/',
    refreshListenable: auth,
    redirect: (context, state) {
      final loggingIn = state.matchedLocation == '/login';
      if (!auth.isAuthenticated && !loggingIn) return '/login';
      if (auth.isAuthenticated && loggingIn) return '/';
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
      GoRoute(path: '/items', builder: (_, __) => const ItemsScreen()),
    ],
  );
}
```

| Piece | Role |
|-------|------|
| **`refreshListenable`** | Re-run `redirect` when auth changes |
| **`redirect`** | Send unauthenticated users to `/login` |

After login: **`context.go('/')`**. After logout: **`context.go('/login')`**.

## 7. Handle 401 in API client

```dart
dynamic _handle(http.Response res) {
  if (res.statusCode == 401) throw AuthException();
  // ...
}
```

In UI or a global listener:

```dart
try {
  await itemsService.fetchItems();
} on AuthException {
  await auth.logout();
  if (context.mounted) context.go('/login');
}
```

With **Dio**, use an **interceptor** to call logout on 401 once for all requests.

## 8. Biometrics (preview)

**`local_auth`** — Face ID / fingerprint to unlock an existing session (after token is in secure storage), not a replacement for server login.

## 9. OAuth (preview)

Use **`url_launcher`** or **`flutter_appauth`** to open the system browser, receive redirect, exchange code on your backend — same pattern as [React Native §9](../javascript/react-native/iv-authentication.md).

## Next

Continue with [Forms & validation](v-forms-and-validation.md).
