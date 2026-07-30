---
label: "VI"
subtitle: "CDN & edge caching"
group: "System design"
order: 6
---
CDN and edge caching
A **CDN (Content Delivery Network)** caches content at **edge PoPs** near users — lower latency and less load on origin.

## 1. Request flow

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="CDN cache hit vs miss to origin">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">CDN pull model</text>
  <rect x="12" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="60" fill="#e4e4e7" font-size="9">User EU</text>
  <path d="M68 56 H108" stroke="#86efac" stroke-width="1.5"/>
  <rect x="108" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.15)" stroke="#fbbf24"/>
  <text x="118" y="56" fill="#fbbf24" font-size="8" font-weight="600">Edge PoP</text>
  <text x="118" y="68" fill="#86efac" font-size="7">HIT → fast</text>
  <path d="M172 56 H212" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="212" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="220" y="60" fill="#e4e4e7" font-size="9">Origin</text>
  <text x="108" y="92" fill="#a1a1aa" font-size="9">MISS: PoP fetches once, caches with TTL, serves next user from edge</text>
</svg></figure>

| Step | Event |
|------|--------|
| 1 | Client requests `cdn.example.com/app.v3.js` |
| 2 | DNS resolves to **nearest PoP** (Anycast or geo DNS) |
| 3 | **Cache hit** → return from edge |
| 4 | **Cache miss** → PoP GET from **origin** → store → respond |

## 2. What belongs on a CDN

| Asset type | Cacheability | Notes |
|------------|--------------|-------|
| Static JS/CSS/images | High | Long TTL + versioned URLs |
| Video segments | High | HLS/DASH chunks |
| Public API GET | Medium | Short TTL; watch auth headers |
| Personalised HTML | Low | `Vary: Cookie` or bypass CDN |
| POST/PUT/DELETE | No | Pass through to origin |

## 3. Cache control

| Mechanism | How | When |
|-----------|-----|------|
| **TTL** | `Cache-Control: max-age=3600` | Default; accept staleness window |
| **Versioned URL** | `/app.v3.js` vs `/app.v2.js` | Immutable assets forever |
| **Purge API** | Invalidate URL on all PoPs | Urgent security fix |
| **Stale-while-revalidate** | Serve stale while fetching fresh | Smooth traffic spikes |

## 4. Pull vs push CDN

| | Pull | Push |
|---|------|------|
| Setup | Origin URL; CDN fetches on miss | You upload to CDN storage |
| Cold start | First user in region slower | Pre-warmed before launch |
| Use | Web apps, APIs with cache headers | Large file distribution, live events |

## 5. Invalidation strategies

```text
Immutable:  /assets/logo.a1b2c3.png     max-age=31536000, immutable
HTML shell: /index.html                 max-age=60, must-revalidate
API:        /v1/public/config         max-age=300 + ETag
```

**Cache key** includes URL + relevant headers (`Accept-Language`, `Authorization` usually **excluded** from public cache).

## 6. Pitfalls

| Pitfall | Fix |
|---------|-----|
| Caching private data | `Cache-Control: private` or no-store |
| Query string ignored | Configure cache key to include `?v=` |
| HTTPS cert at edge | CDN terminates TLS; origin cert can be private |
| Dynamic geo content | Edge workers / short TTL |

**Related:** Part I (caching layers), networking DNS/geo (Part IV–V).
