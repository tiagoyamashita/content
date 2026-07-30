---
label: "II"
subtitle: "Project setup & structure"
group: "Flutter"
order: 2
---
Flutter — project setup & structure
Flutter apps are **Dart projects** managed by the **Flutter SDK** — not npm. You write UI in **`lib/`**; **`pubspec.yaml`** declares dependencies (like `package.json`). Platform folders **`android/`** and **`ios/`** exist from day one but are **thin shells** compared to bare React Native — most teams rarely edit them until release signing or native plugins.

Previous: [Overview](i-overview.md). Mobile parallel: [React Native setup](../javascript/react-native/ii-project-setup-and-structure.md).

## 1. Install and create

**Requirements:** [Flutter SDK](https://docs.flutter.dev/get-started/install), Git. For device builds: Xcode (macOS, for iOS) and/or Android Studio (Android SDK).

```text
flutter doctor          # fix anything marked ✗
flutter create my_app
cd my_app
flutter run
```

| Command | Purpose |
|---------|---------|
| **`flutter run`** | Dev build + hot reload on connected device/emulator |
| **`flutter run -d chrome`** | Run web target |
| **`flutter devices`** | List emulators and plugged-in phones |
| **`dart pub get`** | Install packages from `pubspec.yaml` |
| **`flutter analyze`** | Static analysis / lint |
| **`flutter test`** | Run unit/widget tests |

**IDE:** VS Code with Flutter extension, or Android Studio / IntelliJ with Flutter plugin.

## 2. What `flutter create` gives you

```text
my_app/
  lib/
    main.dart               # entry — runApp()
  pubspec.yaml              # name, version, dependencies
  analysis_options.yaml     # linter rules
  android/                  # Gradle shell — launcher, manifest
  ios/                      # Xcode shell — Info.plist, icons
  web/                      # web entry (if enabled)
  test/
  README.md
```

```text
lib/main.dart  →  runApp(MyApp())  →  widget tree fills the screen
```

Unlike Expo’s managed workflow, **`android/` and `ios/` are always present** — but Flutter tooling generates and updates them. You spend most time in **`lib/`**, not in Swift/Kotlin.

| Folder | You edit when… |
|--------|----------------|
| **`lib/`** | Always — screens, widgets, API, state |
| **`pubspec.yaml`** | Adding packages, assets, app version |
| **`android/` / `ios/`** | App ID, signing, permissions, native plugins |
| **`test/`** | Unit and widget tests |

## 3. `pubspec.yaml` — dependencies and assets

```yaml
name: my_app
description: Demo app
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0
  go_router: ^14.0.0
  flutter_secure_storage: ^9.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
```

| Section | Role |
|---------|------|
| **`dependencies`** | Runtime packages from [pub.dev](https://pub.dev) |
| **`dev_dependencies`** | Tests, linters — not shipped |
| **`flutter.assets`** | Bundled images, fonts |
| **`version`** | `1.0.0+1` — semantic version + build number |

After editing: **`flutter pub get`**.

## 4. Recommended `lib/` layout

Grow into this as the app gets real:

```text
lib/
  main.dart                 # runApp, top-level providers
  app.dart                  # MaterialApp.router or theme
  router.dart               # go_router routes (optional split)
  screens/
    home_screen.dart
    login_screen.dart
    items_screen.dart
  widgets/
    item_row.dart
    loading_indicator.dart
  models/
    item.dart
    user.dart
  services/                 # or api/ — HTTP, no widgets
    api_client.dart
    items_service.dart
    auth_service.dart
  providers/                # if using Riverpod / Provider
    auth_provider.dart
  utils/
    validators.dart
  theme/
    app_theme.dart
```

## 5. What goes where

| Folder | Put here | Do not put here |
|--------|----------|-----------------|
| **`screens/`** | One screen widget per major route | Generic buttons |
| **`widgets/`** | Reusable UI used on multiple screens | Direct HTTP (use `services/`) |
| **`services/`** or **`api/`** | `http` / Dio calls, JSON parsing | `BuildContext` or widgets |
| **`models/`** | Data classes (`fromJson` / `toJson`) | UI layout |
| **`providers/`** | App state (auth user, theme) | One-off screen logic |

**Rule of thumb:** **`screens`** compose UI; **`services`** talk to the server; **`widgets`** draw data passed in.

**Naming:** Flutter convention is **`snake_case.dart`** files and **`PascalCase`** classes (`items_screen.dart` → `ItemsScreen`).

## 6. Entry point and app shell

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'app.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}
```

```dart
// lib/app.dart
import 'package:flutter/material.dart';
import 'router.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'My App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      routerConfig: appRouter,
    );
  }
}
```

## 7. Navigation with `go_router`

Declarative routes — similar mental model to Expo Router or React Router:

```text
flutter pub add go_router
```

```dart
// lib/router.dart
import 'package:go_router/go_router.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/items_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
    GoRoute(path: '/items', builder: (_, __) => const ItemsScreen()),
    GoRoute(
      path: '/items/:id',
      builder: (_, state) => ItemDetailScreen(id: state.pathParameters['id']!),
    ),
  ],
);
```

Navigate: **`context.go('/items')`**, **`context.push('/items/42')`**. Protected routes: [Authentication](iv-authentication.md) §6.

## 8. API client (shared pattern with React)

```dart
// lib/services/api_client.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({this.baseUrl = 'https://api.example.com', this.getToken});

  final String baseUrl;
  final Future<String?> Function()? getToken;

  Future<dynamic> get(String path) async {
    final token = await getToken?.call();
    final res = await http.get(
      Uri.parse('$baseUrl$path'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
    );
    return _handle(res);
  }

  Future<dynamic> post(String path, Map<String, dynamic> body) async {
    final token = await getToken?.call();
    final res = await http.post(
      Uri.parse('$baseUrl$path'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode(body),
    );
    return _handle(res);
  }

  dynamic _handle(http.Response res) {
    if (res.statusCode == 401) throw AuthException();
    if (res.statusCode >= 400) {
      final body = jsonDecode(res.body) as Map<String, dynamic>? ?? {};
      throw ApiException(res.statusCode, body['message'] as String?, body['fields']);
    }
    if (res.body.isEmpty) return null;
    return jsonDecode(res.body);
  }
}

class AuthException implements Exception {}
class ApiException implements Exception {
  ApiException(this.status, this.message, this.fields);
  final int status;
  final String? message;
  final dynamic fields;
}
```

**Dio** is a popular alternative with interceptors — common in production apps.

## 9. Flutter vs React Native: native folders

| | **Flutter** | **RN bare CLI** | **Expo managed** |
|---|-------------|-----------------|------------------|
| **`ios/` / `android/`** | Always created; minimal edits early | Full ownership day one | Often absent until prebuild |
| **UI code location** | 100% `lib/` (Dart) | `src/` (JS/TS) | Same JS/TS |
| **Who draws pixels** | Flutter engine | Native widgets | Native widgets |
| **Custom native code** | Platform channels / plugins | Edit Xcode/Gradle | Prebuild + plugins |

Flutter’s native folders are mainly **embedders** — they host the Flutter engine and load your Dart bundle. You still need them for **signing** and **store submission**, but not for every feature.

## 10. Build targets (preview)

| Target | Command | Output |
|--------|---------|--------|
| **Android APK** (testing) | `flutter build apk` | `build/app/outputs/` |
| **Android App Bundle** (Play Store) | `flutter build appbundle` | `.aab` |
| **iOS** (App Store) | `flutter build ipa` | Requires macOS + Xcode |
| **Web** | `flutter build web` | `build/web/` |

## Next

Continue with [Rendering & server requests](iii-rendering-and-server-requests.md) — widgets, lists, and loading API data.
