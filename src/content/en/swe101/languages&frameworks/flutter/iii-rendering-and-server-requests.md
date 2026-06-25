---
label: "III"
subtitle: "Rendering & server requests"
group: "Flutter"
order: 3
---
Flutter — rendering & server requests
Flutter UI is a **tree of widgets**. When **state** changes, Flutter calls **`build`** again and reconciles the tree — there is no DOM and no separate CSS file. Server data arrives via **`async`/`await`** with **`http`** or **Dio**, often wrapped in **`FutureBuilder`** or a state library.

Previous: [Project setup & structure](ii-project-setup-and-structure.md). Web parallel: [React rendering](../javascript/react/iii-rendering-and-server-requests.md).

## 1. Everything is a widget

```text
runApp(MyApp)
  → MaterialApp
    → Scaffold
      → AppBar, Body (Column, ListView, …)
```

Two widget kinds:

| Type | Role | Example |
|------|------|---------|
| **`StatelessWidget`** | UI from constructor args only | `ItemRow(item: item)` |
| **`StatefulWidget`** | UI that changes over time | Counter, form fields |

```dart
class HelloScreen extends StatelessWidget {
  const HelloScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Hello')),
    );
  }
}
```

**`build` must be pure** — no side effects. Fetch data in **`initState`**, callbacks, or a state-management layer; not directly inside `build`.

## 2. Re-render cycle (`setState`)

```text
User taps button
  → setState(() { count++ })
  → State object's build runs again
  → Flutter diffs widget tree
  → only changed render objects update
```

```dart
class _CounterState extends State<Counter> {
  int count = 0;

  void increment() {
    setState(() => count++);
  }

  @override
  Widget build(BuildContext context) {
    return Text('Count: $count');
  }
}
```

| Trigger | Example |
|---------|---------|
| **`setState`** | Local screen state |
| **`InheritedWidget` / Provider** | App-wide state |
| **`FutureBuilder` future completes** | API data arrived |
| **Stream / Riverpod** | Reactive updates |

## 3. Layout: `Column`, `Row`, `Expanded`

Flexbox-like layout — no CSS.

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [
    const Text('Title', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600)),
    const SizedBox(height: 8),
    Expanded(
      child: ListView.builder(
        itemCount: items.length,
        itemBuilder: (_, i) => ItemRow(item: items[i]),
      ),
    ),
  ],
)
```

| Widget | Role |
|--------|------|
| **`Column` / `Row`** | Vertical / horizontal flex |
| **`Expanded` / `Flexible`** | Share remaining space |
| **`Stack`** | Overlapping children |
| **`Padding` / `SizedBox`** | Spacing |
| **`Center` / `Align`** | Alignment |

**Themes:** `Theme.of(context).textTheme.bodyLarge` — centralize colors and typography in `ThemeData`.

## 4. Lists: `ListView.builder`

Never build huge lists with a naive `Column` of hundreds of children — use **`ListView.builder`** (virtualized).

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    final item = items[index];
    return ListTile(
      title: Text(item.name),
      onTap: () => context.push('/items/${item.id}'),
    );
  },
)
```

| Widget | When |
|--------|------|
| **`ListView.builder`** | Long or unbounded lists |
| **`GridView.builder`** | Grids |
| **`ListView`** (children: []) | Short static lists only |
| **`RefreshIndicator`** | Pull-to-refresh wrapper |

```dart
RefreshIndicator(
  onRefresh: _loadItems,
  child: ListView.builder(/* … */),
)
```

## 5. Manual fetch in `initState`

Same mental model as React **`useEffect`** fetch:

```dart
// lib/screens/items_screen.dart
class ItemsScreen extends StatefulWidget {
  const ItemsScreen({super.key});

  @override
  State<ItemsScreen> createState() => _ItemsScreenState();
}

class _ItemsScreenState extends State<ItemsScreen> {
  final _service = ItemsService();
  List<Item> items = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  Future<void> _loadItems() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final data = await _service.fetchItems();
      if (!mounted) return;
      setState(() {
        items = data;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        error = e.toString();
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (error != null) {
      return Scaffold(body: Center(child: Text('Error: $error')));
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Items')),
      body: RefreshIndicator(
        onRefresh: _loadItems,
        child: ListView.builder(
          itemCount: items.length,
          itemBuilder: (_, i) => ListTile(title: Text(items[i].name)),
        ),
      ),
    );
  }
}
```

**`if (!mounted) return`** — like React’s cancellation guard: widget may be disposed before `await` finishes (user navigated away).

## 6. `FutureBuilder` (declarative loading UI)

```dart
FutureBuilder<List<Item>>(
  future: _service.fetchItems(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Center(child: CircularProgressIndicator());
    }
    if (snapshot.hasError) {
      return Center(child: Text('Error: ${snapshot.error}'));
    }
    final items = snapshot.data ?? [];
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (_, i) => ListTile(title: Text(items[i].name)),
    );
  },
)
```

| `snapshot` | Meaning |
|------------|---------|
| **`connectionState.waiting`** | Future not complete |
| **`hasError`** | Threw exception |
| **`data`** | Success value |

**Caveat:** passing a **new** `future` on every `build` re-runs the request — create the future in `initState` or use a state library.

## 7. State libraries (production apps)

| Library | Style |
|---------|--------|
| **`setState`** | Single screen — fine for learning |
| **Provider** | `ChangeNotifier` + `context.watch` |
| **Riverpod** | Compile-safe providers, very common now |
| **Bloc** | Event → state streams, larger teams |

```dart
// Riverpod sketch — itemsProvider wraps async fetch
final itemsProvider = FutureProvider<List<Item>>((ref) async {
  return ref.read(itemsServiceProvider).fetchItems();
});

// In screen:
class ItemsScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final asyncItems = ref.watch(itemsProvider);
    return asyncItems.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, _) => Center(child: Text('$e')),
      data: (items) => ListView.builder(/* … */),
    );
  }
}
```

Adopt when fetch/cache logic spreads across screens — same reason teams pick [TanStack Query](../javascript/react/iii-rendering-and-server-requests.md) on web.

## 8. Request flow (end to end)

```text
User opens /items
  → ItemsScreen builds
  → fetchItems() → GET /api/items (+ auth header)
  → JSON → models → setState / provider update
  → ListView rebuilds with rows
User pulls to refresh
  → _loadItems() again
```

Backend unchanged: [Spring Boot REST](../java/springboot/iv-rest-controllers.md), FastAPI, etc.

## 9. Images and network

```dart
Image.network(
  'https://cdn.example.com/photo.jpg',
  loadingBuilder: (_, child, progress) {
    if (progress == null) return child;
    return const CircularProgressIndicator();
  },
  errorBuilder: (_, __, ___) => const Icon(Icons.broken_image),
)
```

**Local assets:** declare in `pubspec.yaml`, load with **`Image.asset('assets/images/logo.png')`**.

## 10. Platform differences (preview)

```dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

if (kIsWeb) { /* web */ }
else if (Platform.isIOS) { /* iOS */ }
else if (Platform.isAndroid) { /* Android */ }
```

**Safe areas:** `SafeArea` widget or `MediaQuery.of(context).padding` for notches. **Material vs Cupertino:** `MaterialApp` (Android-style) vs `CupertinoApp` (iOS-style) — or mix widgets per platform.

## Next

Continue with [Authentication](iv-authentication.md) — token storage and protected routes.
