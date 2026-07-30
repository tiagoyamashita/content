---
label: "VI"
subtitle: "APIs & dynamic content"
group: "CDN"
order: 6
---
CDN — APIs & dynamic content
Not every response belongs on a CDN — but **read-heavy public GETs** (config, product catalog snippets, OG images) can shave latency and origin load when cache rules are strict.

## 1. Cacheable GET criteria

All must be true (or consciously accepted):

- [ ] **No user-specific secrets** in body
- [ ] **Same URL → same bytes** for all users (or `Vary` is correct)
- [ ] **Stale window acceptable** for business
- [ ] **Origin sets explicit** `Cache-Control` (not accidental default)

```http
GET /v1/public/features HTTP/1.1

HTTP/1.1 200 OK
Cache-Control: public, max-age=120
Content-Type: application/json

{"darkMode":true,"minVersion":"2.1.0"}
```

## 2. Never cache (defaults)

| Route | Header |
|-------|--------|
| `/api/me`, `/cart`, `/orders` | `Cache-Control: private, no-store` |
| Anything with **`Set-Cookie`** | `no-store` |
| POST/PUT/PATCH/DELETE | Not cacheable by HTTP spec |

Authenticate at origin; CDN passes **`Authorization`** through unless you design shared cache keys (usually **don’t** for private data).

## 3. `Vary` header

When response differs by request header:

```http
Vary: Accept-Language
```

CDN stores **separate cache entries** per language — hit rate drops; use only when needed.

| Header | Common use |
|--------|------------|
| **`Accept-Encoding`** | gzip vs br (often automatic) |
| **`Accept-Language`** | Localized JSON |
| **`Origin`** | CORS — usually not for CDN cache |

Avoid **`Vary: Cookie`** unless you fully understand cache fragmentation.

## 4. GraphQL and POST

Default: **do not CDN-cache GraphQL POST** — same path, different body.

Options:

- Public queries via **GET** with persisted query hash (niche)
- **Separate REST** read endpoints for cacheable public data
- Cache at **[Redis](../redis/iv-patterns-and-use-cases.md)** in app layer instead

## 5. Purge and invalidation

When you must remove cached content immediately:

| Method | Use |
|--------|-----|
| **Path purge** | `/products/8812.json` — security fix, bad deploy |
| **Wildcard purge** | `/assets/*` — expensive; avoid habit |
| **Surrogate keys** (Fastly etc.) | Tag related URLs; purge by tag |
| **Version bump** | Prefer URL/version over purge for static |

```bash
# CloudFront example
aws cloudfront create-invalidation --distribution-id E123 --paths "/v1/public/config"
```

Propagation is **not instant globally** — plan seconds to minutes.

## 6. Edge workers / compute at edge

Run lightweight logic at PoP:

| Provider | Product |
|----------|---------|
| Cloudflare | Workers |
| Fastly | Compute@Edge |
| CloudFront | Lambda@Edge, CloudFront Functions |

Use cases: A/B headers, geo redirects, token validation at edge, HTML rewriting — **not** full database access.

Keep edge functions **stateless** and fast (&lt; few ms CPU limits).

## 7. Dynamic site acceleration

Some CDNs **route dynamic HTML/API** through optimized paths to origin (TCP tuning, keep-alive) without caching body — latency help without cache risk.

Distinct from **caching** — read provider docs (CloudFront “dynamic content”, Cloudflare “Argo”).

## 8. OG / social preview images

Generated image URLs are good CDN candidates:

```text
GET /og/product/8812.png   →  max-age=3600, purge on product update
```

Generate on miss at origin or pre-render in batch.

## Next

Continue with [Operations & troubleshooting](vii-operations-and-troubleshooting.md) for monitoring and debug checklist.
