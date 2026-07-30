---
label: "I"
subtitle: "Overview"
group: "Flutter"
order: 1
---
Flutter — overview
**Flutter** is Google’s **cross-platform UI toolkit** — one **Dart** codebase for **iOS, Android, web, and desktop**. Widgets compose the whole UI; Flutter draws pixels with its own engine (Skia/Impeller), so look-and-feel is consistent across platforms.

Parent track: [SWE101 overview](../i-overview.md). Compare with [React Native](../javascript/react-native/i-overview.md) (JavaScript) and [React](../javascript/react/i-overview.md) (web).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Flutter vs RN, Dart, when to use Flutter |
| **II — Project setup & structure** | `flutter create`, `pubspec.yaml`, `lib/`, `go_router` |
| **III — Rendering & server requests** | Widget tree, layout, lists, `FutureBuilder`, HTTP |
| **IV — Authentication** | Secure storage, auth state, protected routes |
| **V — Forms & validation** | `TextFormField`, `Form`, validators, server errors |

## What it is

```text
Flutter app  →  Dart widgets  →  Flutter engine  →  iOS / Android / web / desktop
```

| | **Flutter** | **React Native** |
|---|-------------|------------------|
| **Language** | Dart | JavaScript / TypeScript |
| **UI model** | Widget tree (everything is a widget) | React components → native views |
| **Rendering** | Own engine (consistent pixels) | Platform native widgets |
| **Web** | `flutter build web` | React web is separate |
| **Hot reload** | Yes | Yes (Fast Refresh) |

Unlike [Expo-managed React Native](../javascript/react-native/ii-project-setup-and-structure.md), a standard Flutter project **always includes** `android/` and `ios/` folders — but most UI work stays in **`lib/`** (Dart only).

## Quick start

```text
flutter create my_app
cd my_app
flutter run
```

Install the [Flutter SDK](https://docs.flutter.dev/get-started/install) first; run **`flutter doctor`** to check Xcode/Android tooling. Details: [Project setup & structure](ii-project-setup-and-structure.md).

## Smallest example

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: CounterScreen(),
    );
  }
}

class CounterScreen extends StatefulWidget {
  @override
  State<CounterScreen> createState() => _CounterScreenState();
}

class _CounterScreenState extends State<CounterScreen> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
          onPressed: () => setState(() => count++),
          child: Text('Count: $count'),
        ),
      ),
    );
  }
}
```

## When Flutter fits

| Good fit | Consider alternatives |
|----------|------------------------|
| One team, iOS + Android (+ web) from one codebase | Team only knows React → [React Native](../javascript/react-native/i-overview.md) |
| Pixel-perfect, branded UI across platforms | Maximum platform-native feel day one → Swift/Kotlin |
| Greenfield mobile MVP | Tiny web-only app → React SPA or [HTMX](../htmx/i-overview.md) |
| Animations and custom UI | Reuse existing React web + JS hiring pool → React Native |

## Flutter vs React Native (short)

| | **Flutter** | **React Native** |
|---|-------------|------------------|
| **Ecosystem** | pub.dev, Google-backed | npm, Meta-backed |
| **Native folders** | Generated; edit for signing/plugins | Bare CLI: you own; Expo can hide at first |
| **Look** | Same widgets everywhere | Closer to platform controls |
| **Web** | Supported, not always primary | React web is the main web story |

## Next

Continue with [Project setup & structure](ii-project-setup-and-structure.md).
