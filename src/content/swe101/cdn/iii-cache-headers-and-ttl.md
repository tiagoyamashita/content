---
label: "III"
subtitle: "Cache headers & TTL"
group: "CDN"
order: 3
---
CDN — cache headers & TTL
Browsers and CDNs cache based on **HTTP cache headers**. You control behavior from the **origin response** (or CDN override rules).

## 1. Core headers

| Header | Meaning |
|--------|---------|
| **`Cache-Control: max-age=3600`** | Fresh for 3600 seconds at CDN/browser |
| **`Cache-Control: public`** | Shared caches (CDN) may store |
| **`Cache-Control: private`** | Only end-user browser — not CDN |
| **`Cache-Control: no-store`** | Do not cache at all |
| **`Cache-Control: no-cache`** | Cache but must revalidate before use |
| **`Cache-Control: immutable`** | Content never changes (with hashed URL) |
| **`ETag: "abc123"`** | Validator for conditional GET |
| **`Last-Modified`** | Time-based validator |

Example — long-lived asset:

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

Example — API config:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=300
ETag: "config-v7"
```

## 2. Revalidation

When TTL expires, edge may **revalidate** without full download:

```http
GET /v1/public/config HTTP/1.1
If-None-Match: "config-v7"

HTTP/1.1 304 Not Modified
```

**304** saves bandwidth; origin still gets a request — tune TTL to balance freshness vs origin load.

## 3. Versioned URLs (best for static assets)

Instead of purging, ship new filename:

```text
/app.v2.js   →  max-age=1 year, immutable
/app.v3.js   →  new deploy; old cache harmless
```

Build tools emit hashes:

```text
/assets/main-Dk3f9a2b.js
/assets/main-Cx8e1f0c.css
```

HTML references new hashes — no CDN purge needed for JS/CSS on deploy.

## 4. HTML and SPA shell

`index.html` often **should not** cache forever — it points at hashed assets:

```http
Cache-Control: public, max-age=60, must-revalidate
```

Or:

```http
Cache-Control: no-cache
```

**`stale-while-revalidate`** — serve stale HTML while fetching fresh (smooth spikes):

```http
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

## 5. CDN behavior vs origin headers

Providers let you **override** at the edge:

| Rule | Example |
|------|---------|
| Path pattern | `/assets/*` → 1 year TTL |
| File type | `*.jpg` → 7 days |
| Query string | Ignore `utm_*` in cache key |
| Origin missing headers | Default TTL 86400 |

Prefer setting headers **at origin** (S3 metadata, app middleware) so behavior is consistent if you change CDN.

## 6. Dangerous mistakes

| Mistake | Consequence |
|---------|-------------|
| `public, max-age=3600` on `/api/me` | User A’s data served to User B |
| Caching `Set-Cookie` responses | Broken sessions |
| Ignoring `Authorization` in cache key | Leaked private JSON |
| Long TTL on unversioned `/app.js` | Users stuck on old bundle after deploy |

Default sensitive routes to **`Cache-Control: private, no-store`**.

## 7. Quick reference table

| Asset | Typical policy |
|-------|----------------|
| Hashed JS/CSS | `public, max-age=31536000, immutable` |
| Images (versioned path) | `public, max-age=604800` |
| `index.html` | `max-age=0, must-revalidate` or short TTL |
| Public GET API | `public, max-age=60–300` + ETag |
| Authenticated API | `private, no-store` |

## Next

Continue with [Setup & origin](iv-setup-and-origin.md) for CloudFront, Cloudflare, and origin patterns.
