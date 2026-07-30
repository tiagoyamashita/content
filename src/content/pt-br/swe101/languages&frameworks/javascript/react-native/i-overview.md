---
label: "I"
subtitle: "Overview"
group: "React Native"
order: 1
---
React Native — overview
**React Native** builds **iOS and Android apps** with **React** components — not HTML/CSS in a browser, but native widgets (`View`, `Text`, `Image`) rendered by the platform. One JavaScript/TypeScript codebase; optional shared logic with a [React](../react/i-overview.md) web app.

Parent track: [JavaScript overview](../i-overview.md). Learn [React](../react/i-overview.md) fundamentals first (components, hooks, state).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | RN vs web React, Expo, when to use RN |
| **II — Project setup & structure** | Expo vs bare CLI, scaffold, `screens/`, `api/`, Expo Router |
| **III — Rendering & server requests** | Native UI, Flexbox, `FlatList`, `useEffect` fetch, TanStack Query |
| **IV — Authentication** | Secure token storage, protected routes, 401 handling |
| **V — Forms & validation** | `TextInput`, keyboard UX, client + server validation |

## What it is

```text
React (web)     →  JSX  →  DOM in browser
React Native    →  JSX  →  native iOS/Android UI (UIKit / Android views)
```

| | **React (web)** | **React Native** |
|---|-----------------|------------------|
| **UI primitives** | `div`, `span`, `button` | `View`, `Text`, `Pressable` |
| **Styling** | CSS files, Tailwind | `StyleSheet` objects (flexbox-centric) |
| **Runs in** | Browser | Mobile app shell + JS engine (Hermes) |
| **Distribution** | URL / hosting | App Store, Google Play |

You still use **components**, **props**, **useState**, **useEffect**, and often the same **API layer** (`fetch`, TanStack Query) as web React.

## Quick start (Expo)

```text
npx create-expo-app@latest my-app
cd my-app
npx expo start
```

Scan the QR code with **Expo Go**, or press **`i`** / **`a`** for simulator/emulator.

### Expo vs React Native CLI (short)

| | **Expo** | **React Native CLI (“bare”)** |
|---|----------|-------------------------------|
| **What it is** | Toolkit + SDK + build services **on top of** React Native | Official scaffold that creates full **`ios/`** and **`android/`** projects |
| **You write** | JS/TSX (same React Native components) | Same JS/TSX |
| **Native projects** | Hidden at first; optional via `expo prebuild` | In your repo from day one — edit in Xcode / Android Studio |
| **Best for** | Most new apps, fast dev with **Expo Go** | Heavy custom native SDKs, full control of native code |

**Expo** is not a different UI library — it is how many teams **bootstrap, develop, and ship** React Native without becoming iOS/Android build experts on day one. Full comparison: [Project setup §8](ii-project-setup-and-structure.md#8-expo-vs-bare-react-native-cli).

## Smallest example

```tsx
import { useState } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

export function Counter() {
  const [count, setCount] = useState(0);
  return (
    <View style={styles.box}>
      <Pressable onPress={() => setCount(c => c + 1)}>
        <Text>Count: {count}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { flex: 1, justifyContent: 'center', alignItems: 'center' },
});
```

## When React Native fits

| Good fit | Consider alternatives |
|----------|------------------------|
| iOS + Android from one team | Web-only product → React SPA |
| Already invested in React | Maximum native performance/feel → Swift/Kotlin |
| MVP mobile with Expo | Heavy 3D/games → native or game engines |
| Shared JS skills with web app | Dart + one engine → [Flutter track](../../flutter/i-overview.md) (5 parts) |

## React Native vs native (Swift/Kotlin)

| | **React Native** | **Swift / Kotlin** |
|---|------------------|---------------------|
| **Language** | JavaScript/TypeScript | Platform languages |
| **UI** | React components → native bridge | Platform UI frameworks |
| **Reuse** | Share logic with React web | Best platform integration |
| **OTA updates** | Possible (Expo) with limits | Store releases |

## Next

Continue with [Project setup & structure](ii-project-setup-and-structure.md).
