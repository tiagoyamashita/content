---
label: "III"
subtitle: "Rendering & server requests"
group: "React Native"
order: 3
---
React Native — rendering & server requests
React Native turns **component functions** into **native views** — not DOM nodes. When **state** or **props** change, components **re-render** and the native layer updates. Server data enters through **`fetch`** (or TanStack Query), same mental model as [web React](../react/iii-rendering-and-server-requests.md).

Previous: [Project setup & structure](ii-project-setup-and-structure.md).

## 1. First paint: mount to native root

```text
index (Expo entry)
  → registerRootComponent(App) or expo-router/entry
  → App returns JSX tree
  → React Native creates native View/Text under the root
```

There is **no** `document` or `#root` div — the app fills the device screen.

```tsx
// App.tsx (classic entry)
import { registerRootComponent } from 'expo';
import App from './App';

registerRootComponent(App);
```

With **Expo Router**, `app/_layout.tsx` is the root; navigation mounts child routes.

## 2. Re-render cycle

```text
Event (press, fetch done, timer)
  → setState / setQueryData
  → component function runs again
  → React Native reconciles native tree
  → changed native views update
```

| Trigger | Example |
|---------|---------|
| **Local state** | `setCount(c => c + 1)` |
| **Parent props** | Parent passes new `items` |
| **Context** | `AuthContext` user changes |
| **TanStack Query** | Cache update after refetch |

Keep render **pure** — side effects in **`useEffect`** or event handlers (`onPress`), not during render.

## 3. Layout: Flexbox by default

Every `View` defaults to **`flexDirection: 'column'`** (unlike CSS row default on web).

```tsx
<View style={styles.row}>
  <View style={styles.sidebar} />
  <View style={styles.main} />
</View>

const styles = StyleSheet.create({
  row: { flex: 1, flexDirection: 'row' },
  sidebar: { width: 80, backgroundColor: '#eee' },
  main: { flex: 1, padding: 16 },
});
```

| Style | Common use |
|-------|------------|
| **`flex: 1`** | Fill remaining space |
| **`justifyContent`** | Main-axis alignment (`center`, `space-between`) |
| **`alignItems`** | Cross-axis alignment |
| **`padding` / `margin`** | Spacing (numbers = density-independent pixels) |
| **`Platform.OS`** | `'ios'` vs `'android'` branches when needed |

No CSS files — use **`StyleSheet.create`** for performance (IDs passed to native) or inline for one-offs.

## 4. Lists: use `FlatList`, not `map` in `ScrollView`

Long lists inside `ScrollView` render every row — slow. **`FlatList`** virtualizes.

```tsx
import { FlatList, Text, View, ActivityIndicator } from 'react-native';
import { useItems } from '../hooks/useItems';
import { ItemRow } from '../components/ItemRow';

export function ItemsScreen() {
  const { items, loading, error } = useItems();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }
  if (error) {
    return <Text style={{ padding: 16 }}>Error: {error.message}</Text>;
  }

  return (
    <FlatList
      data={items}
      keyExtractor={item => String(item.id)}
      renderItem={({ item }) => <ItemRow item={item} />}
      ItemSeparatorComponent={() => <View style={{ height: 1, backgroundColor: '#ddd' }} />}
      contentContainerStyle={{ padding: 16 }}
    />
  );
}
```

| Component | When |
|-----------|------|
| **`FlatList`** | Long or unbounded lists |
| **`SectionList`** | Grouped sections (contacts A–Z) |
| **`ScrollView`** | Short static content, forms |

**Pull to refresh:** `refreshing` + `onRefresh` on `FlatList`.

## 5. Fetch in `useEffect` (manual pattern)

Same timeline as web React — see [web §6](../react/iii-rendering-and-server-requests.md).

```tsx
// src/hooks/useItems.ts
import { useEffect, useState } from 'react';
import { getItems } from '../api/items';

export function useItems() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const data = await getItems();
        if (!cancelled) setItems(data);
      } catch (e) {
        if (!cancelled) setError(e as Error);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, []);

  return { items, loading, error };
}
```

**Cancellation guard** — if the user navigates away before fetch completes, ignore the result.

## 6. Navigation + data loading

Load data **on the screen** that needs it (or in a parent layout), not in the tab bar.

```text
User taps Items tab
  → ItemsScreen mounts
  → useItems / useQuery runs
  → loading spinner → list
User taps row
  → navigate to ItemDetail with id param
  → ItemDetailScreen fetches GET /api/items/:id
```

**Expo Router** — read params:

```tsx
// app/items/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function ItemDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  // useQuery(['item', id], () => getItem(id))
}
```

**React Navigation:**

```tsx
navigation.navigate('ItemDetail', { id: item.id });
// ItemDetailScreen: const { id } = route.params;
```

## 7. TanStack Query on mobile

[`@tanstack/react-query`](https://tanstack.com/query) works the same in RN — cache, dedupe, refetch.

```text
npx expo install @tanstack/react-query
```

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getItems, createItem } from '../api/items';
import { FlatList, Text, Pressable, ActivityIndicator } from 'react-native';

export function ItemsScreen() {
  const qc = useQueryClient();
  const { data: items = [], isLoading, error, refetch, isRefetching } = useQuery({
    queryKey: ['items'],
    queryFn: getItems,
  });

  const create = useMutation({
    mutationFn: createItem,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['items'] }),
  });

  if (isLoading) return <ActivityIndicator style={{ marginTop: 40 }} />;
  if (error) return <Text>Error: {(error as Error).message}</Text>;

  return (
    <FlatList
      data={items}
      keyExtractor={i => String(i.id)}
      renderItem={({ item }) => <Text>{item.name}</Text>}
      refreshing={isRefetching}
      onRefresh={refetch}
      ListFooterComponent={
        <Pressable onPress={() => create.mutate({ name: 'New' })}>
          <Text>Add item</Text>
        </Pressable>
      }
    />
  );
}
```

**When to adopt:** multiple screens share API data, pull-to-refresh, or `useEffect` fetch logic spreads across the app. For one screen, `useEffect` is fine.

**App state:** React Query does not replace navigation or auth — pair with [AuthContext](iv-authentication.md).

## 8. Network and offline (basics)

| Topic | RN behavior |
|-------|-------------|
| **HTTPS** | Required in production (ATS on iOS, cleartext blocked on Android by default) |
| **Local dev API** | Use machine IP (`http://192.168.1.10:8080`) — `localhost` on device points to the phone |
| **Offline** | `fetch` fails — show message; optional `@react-native-community/netinfo` |
| **CORS** | Not a browser — no CORS preflight from “origin” |

Backend unchanged: [Spring Boot REST](../../java/springboot/iv-rest-controllers.md), etc.

## 9. Platform-specific UI (preview)

```tsx
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  header: {
    paddingTop: Platform.OS === 'ios' ? 48 : 24,
  },
});
```

For larger splits: `Button.ios.tsx` / `Button.android.tsx`, or `Platform.select({ ios: ..., android: ... })`.

**Safe areas:** wrap screens in `SafeAreaView` from `react-native-safe-area-context` (Expo Router layouts often do this automatically).

## Next

Continue with [Authentication](iv-authentication.md) — secure token storage and protected routes.
