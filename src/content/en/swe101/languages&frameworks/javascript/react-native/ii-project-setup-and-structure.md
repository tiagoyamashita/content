---
label: "II"
subtitle: "Project setup & structure"
group: "React Native"
order: 2
---
React Native — project setup & structure
This track uses **Expo** (managed workflow) as the default — fast dev, sensible defaults, and a path to store builds via **EAS**. **React Native CLI** (“bare”) is the escape hatch when you need custom native modules Expo does not ship.

Previous: [Overview](i-overview.md). Web parallel: [React project setup](../react/ii-project-setup-and-structure.md).

## 1. Create the project

**Requirements:** Node.js 20+ LTS, npm (or pnpm/yarn). For simulators: Xcode (macOS) and/or Android Studio.

```text
npx create-expo-app@latest my-app --template blank-typescript
cd my-app
npx expo start
```

| Command | Purpose |
|---------|---------|
| **`npx expo start`** | Dev server, QR code, hot reload |
| **`npx expo start --ios`** | Open iOS Simulator |
| **`npx expo start --android`** | Open Android emulator |
| **`npx expo install <pkg>`** | Install a version compatible with your Expo SDK |

**TypeScript** (`blank-typescript`) is recommended for teams; examples below use `.tsx`.

## 2. What Expo gives you

```text
my-app/
  App.tsx                 # root component (default entry)
  app.json                # Expo config — name, slug, icons, permissions
  package.json
  tsconfig.json
  assets/                 # icons, splash images
  node_modules/
```

**`app.json`** (or `app.config.js`) is where you set display name, bundle identifier, and plugins (camera, notifications, etc.).

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": { "image": "./assets/splash-icon.png" },
    "ios": { "bundleIdentifier": "com.example.myapp" },
    "android": { "package": "com.example.myapp" }
  }
}
```

## 3. Recommended layout (grow into this)

```text
my-app/
  App.tsx                 # providers + root navigator (or delete if using Expo Router)
  app/                    # Expo Router — file-based routes (optional)
    _layout.tsx
    index.tsx
    (tabs)/
      _layout.tsx
      home.tsx
      profile.tsx
    login.tsx
  src/
    screens/              # full-screen targets (if not using app/ for every screen)
      ItemsScreen.tsx
    components/           # reusable UI — no route-level fetching
      ItemRow.tsx
      Button.tsx
    features/             # optional domain slices
      items/
        useItems.ts
    hooks/                  # shared hooks
    api/                    # fetch wrappers — no JSX
      client.ts
      items.ts
      auth.ts
    context/                # AuthContext, ThemeContext
    utils/
    constants/              # colors, spacing tokens
  assets/
```

## 4. What goes where

| Folder / file | Put here | Do not put here |
|---------------|----------|-----------------|
| **`screens/`** or **`app/` routes** | One screen per major flow / route | Generic buttons |
| **`components/`** | Presentational pieces used on multiple screens | Direct `fetch` (use `api/` + hooks) |
| **`api/`** | HTTP functions, JSON parsing, error mapping | React hooks or JSX |
| **`hooks/`** | Reusable state/effect logic | Screen-specific one-offs |
| **`context/`** | App-wide providers (auth, theme) | Business logic that belongs in hooks |
| **`assets/`** | Images bundled with the app | Large remote-only media (use CDN URLs) |

**Rule of thumb:** **`screens`** compose UI and wire data; **`api`** talks to the server; **`components`** draw props.

## 5. `screens/` vs `app/` (Expo Router)

Both mean “one place per major screen.” Pick **one** primary pattern.

| Approach | Folder | Mental model |
|----------|--------|--------------|
| **Expo Router** | `app/` | File = route (like Next.js) — `app/items/[id].tsx` |
| **Classic** | `src/screens/` + React Navigation | Screens registered in a navigator config |

```text
screens/ItemsScreen.tsx   ≡   app/items/index.tsx   (same role)
```

**Expo Router** (recommended for new Expo apps):

```text
npx expo install expo-router react-native-safe-area-context react-native-screens
```

Set `"main": "expo-router/entry"` in `package.json`, then add files under `app/`.

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="login" options={{ title: 'Sign in' }} />
    </Stack>
  );
}
```

**React Navigation** (manual stack) — see [Rendering & server requests](iii-rendering-and-server-requests.md) §6 for navigation after data loads.

## 6. Shared `api/` with web React

If you also ship a [React](../react/i-overview.md) web app, extract HTTP into a package or copy the same shape:

```text
api/
  client.ts     # BASE_URL, auth header, error handling
  items.ts      # getItems(), createItem()
  auth.ts       # login(), logout()
```

| Concern | Web React | React Native |
|---------|-----------|--------------|
| **Base URL** | `import.meta.env.VITE_API_URL` | `process.env.EXPO_PUBLIC_API_URL` |
| **Auth header** | Same `Authorization: Bearer` | Same |
| **CORS** | Browser enforces | Not applicable (native HTTP) |

Set env in `.env`:

```text
EXPO_PUBLIC_API_URL=https://api.example.com
```

```typescript
// src/api/client.ts
const BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8080';

export async function api(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw Object.assign(new Error(body.message ?? res.statusText), {
      status: res.status,
      fields: body.fields,
    });
  }
  return res.status === 204 ? null : res.json();
}
```

## 7. Providers at the root

Wrap the app once — same idea as web `main.jsx`:

```tsx
// App.tsx (or app/_layout.tsx with Expo Router)
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './src/context/AuthContext';
import { RootNavigator } from './src/navigation/RootNavigator';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RootNavigator />
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

## 8. Expo vs bare React Native CLI

React Native is the **UI framework** (JSX → native widgets). To ship an app you also need **native projects** — the iOS and Android shells that Apple and Google require. **Expo** and the **React Native CLI** are two different ways to get those pieces wired up.

### 8.1 What “native” means here

A store-ready app is not just JavaScript. Each platform has a **native project**:

| Platform | Native project | Built with | Output |
|----------|----------------|------------|--------|
| **iOS** | `ios/` folder (Xcode) | Swift / Objective-C + CocoaPods | `.ipa` → App Store |
| **Android** | `android/` folder (Gradle) | Kotlin / Java | `.aab` / `.apk` → Play Store |

Those projects contain:

- **App entry** — launches the JS runtime (Hermes) and loads your bundle  
- **Permissions** — camera, location, notifications in `Info.plist` / `AndroidManifest.xml`  
- **Native modules** — bridge code so JS can call platform APIs  
- **Icons, splash, signing** — certificates and store metadata  

**“Native CLI”** (informal name) means you own these folders from the start and edit them in **Xcode** and **Android Studio** when you need platform behavior Expo has not packaged for you.

### 8.2 What React Native CLI is

The **React Native Community CLI** is the **default scaffolding tool** for a “vanilla” React Native app — not a separate framework, but the command that creates a project with full `ios/` and `android/` trees:

```text
npx @react-native-community/cli init MyApp
```

```text
MyApp/
  App.tsx
  package.json
  ios/                    # Xcode project — always in repo
    MyApp.xcodeproj
    Podfile
  android/                # Gradle project — always in repo
    app/build.gradle
  metro.config.js         # JS bundler (Metro)
```

| You do yourself | Typical tasks |
|-----------------|---------------|
| **Install Xcode / Android Studio** | Required for simulators and local release builds |
| **CocoaPods / Gradle** | `pod install`, SDK versions, build errors |
| **Link native libraries** | Add SDKs (maps, payments, analytics) by editing native projects |
| **CI / store builds** | Configure Fastlane, Xcode archive, Gradle signing |

**When teams say “bare React Native”** they mean: **React Native without Expo’s managed layer** — you maintain `ios/` and `android/` directly. Maximum control; more mobile-platform work.

### 8.3 What Expo is

**[Expo](https://expo.dev)** is a **platform and toolkit on top of React Native** (by Expo Inc.). It does not replace React Native — your app still uses `View`, `Text`, hooks, and Metro. Expo adds:

| Layer | What it provides |
|-------|------------------|
| **Expo SDK** | Pre-built native modules (`expo-camera`, `expo-location`, `expo-secure-store`, …) with JS APIs that work across iOS and Android |
| **Expo CLI** | `npx expo start` — dev server, hot reload, device/simulator launch |
| **Expo Go** | Dev-only phone app — scan QR, load your JS bundle without installing a custom build (limited to SDK modules Expo Go ships) |
| **Config** | `app.json` / `app.config.js` instead of hand-editing Xcode/Gradle for many settings |
| **EAS** | **E**xpo **A**pplication **S**ervices — cloud **Build**, **Submit**, **Update** (OTA JS updates) |

```text
Your App.tsx + src/
        ↓
React Native (components, bridge)
        ↓
Expo SDK modules (optional) + native shell
        ↓
iOS / Android binary
```

**Managed workflow (classic Expo):** you start with **no** `ios/` or `android/` in git. Expo (or EAS) generates native projects at build time from your config. You write JS/TS and use Expo SDK packages; you do not open Xcode for day-to-day work.

```text
npx create-expo-app@latest my-app    # no ios/ android/ initially
```

**Development builds:** when you outgrow Expo Go (custom native code or modules not in Expo Go), you create a **custom dev client** — your own installable app with your native dependencies, still using Expo tooling:

```text
eas build --profile development
```

### 8.4 How the two paths compare

```text
                    ┌─────────────────────────────────────┐
                    │     Your JS/TSX (React Native)      │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              │                                               │
     ┌────────▼────────┐                           ┌─────────▼─────────┐
     │  Expo toolchain │                           │  RN CLI (bare)    │
     │  app.json, EAS  │                           │  ios/ android/    │
     │  Expo SDK       │                           │  you maintain     │
     └────────┬────────┘                           └─────────┬─────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      ▼
                         Native iOS + Android apps
```

| | **Expo (recommended start)** | **Bare React Native CLI** |
|---|-------------------------------|---------------------------|
| **Who maintains `ios/` / `android/`** | Often Expo / EAS (or generated on demand) | Your team, in-repo |
| **Day-one setup** | Node only; phone + Expo Go | Node + Xcode and/or Android Studio |
| **Native features** | Expo SDK + [config plugins](https://docs.expo.dev/config-plugins/introduction/); custom code via prebuild | Any npm native module; edit Xcode/Gradle directly |
| **Third-party native SDK** | Possible via prebuild + plugins; sometimes harder | Straightforward if library documents RN install |
| **Store builds** | `eas build` (cloud) or local after `prebuild` | Local Xcode archive / Gradle, or your CI |
| **OTA JS updates** | `eas update` (policy limits — no native changes) | Roll your own (CodePush, etc.) or store-only |
| **Best for** | Most new apps, JS-heavy teams, MVPs | Unusual native integrations, forked RN, legacy bare repos |

### 8.5 `expo prebuild` — the middle ground

Modern Expo is not only “managed.” **`npx expo prebuild`** generates `ios/` and `android/` from `app.json` and installed Expo modules — you can then open Xcode or add native code, while keeping Expo SDK and EAS:

```text
npx expo prebuild        # creates ios/ android/
npx expo run:ios         # build and run locally
```

| Workflow | `ios/` / `android/` in repo? | Typical team |
|----------|------------------------------|--------------|
| **Expo managed** | No (or gitignored; CI runs prebuild) | Startups, web devs new to mobile |
| **Expo + prebuild** | Yes, committed or CI-generated | Apps needing one custom native module |
| **Bare RN CLI** | Yes, from day one | Strong mobile team, heavy native customization |

You can **eject** mentally from pure managed → prebuild → bare maintenance without rewriting your React components.

### 8.6 Choosing a path

| Situation | Reasonable choice |
|-----------|-------------------|
| New app, team knows React not Swift/Kotlin | **Expo** (`create-expo-app`) |
| Need camera, push, secure storage, maps | **Expo SDK** modules first |
| Vendor ships RN SDK with “edit `Podfile`” docs | **Bare CLI** or **Expo prebuild** + manual native edits |
| Existing bare RN app from 2019 | Stay **bare** or migrate gradually to Expo modules |
| Prototype on a physical phone in 10 minutes | **Expo Go** + `expo start` |

**Practical default for SWE101:** start with **Expo**. Move toward prebuild or bare only when a concrete native requirement (unsupported SDK, forked React Native, special build pipeline) forces it.

### 8.7 Glossary

| Term | Meaning |
|------|---------|
| **React Native** | Meta’s framework — React components rendered to native UI |
| **Metro** | JS bundler for RN (like Vite/webpack for the app bundle) |
| **Hermes** | JS engine tuned for React Native on mobile |
| **Expo** | Tooling + SDK + services layered on React Native |
| **Expo Go** | Generic dev app; only for prototyping with supported modules |
| **Development build** | Your app’s own debug binary with your native deps |
| **EAS Build** | Expo cloud service that compiles store binaries |
| **Bare / RN CLI** | Project with full native folders you maintain directly |
| **Native module** | Bridge code exposing iOS/Android APIs to JavaScript |
| **Config plugin** | Expo hook that modifies native projects during prebuild |

## 9. Scripts and release (preview)

| Task | Command |
|------|---------|
| **Dev** | `npx expo start` |
| **Typecheck** | `npx tsc --noEmit` |
| **Production build** | `eas build` (requires [EAS](https://docs.expo.dev/build/introduction/)) |
| **OTA update** | `eas update` (JS bundle only — store rules apply) |

## Next

Continue with [Rendering & server requests](iii-rendering-and-server-requests.md) — Flexbox, lists, and loading data from your API.
