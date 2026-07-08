---
label: "V"
subtitle: "Static assets & SPAs"
group: "CDN"
order: 5
---
CDN — static assets & SPAs
Single-page apps (React, Vue, Svelte) ship **hashed static files** plus a small **HTML shell**. CDNs excel at serving the static layer globally.

## 1. Build output layout

```text
dist/
  index.html              ← entry, short cache TTL
  assets/
    main-Dk3f9a2b.js      ← hashed, long TTL
    main-Cx8e1f0c.css
    logo-3f2a1b.png
```

Vite/Webpack/Next static export emit **content hashes** in filenames — safe **`immutable`** caching.

## 2. Deploy pipeline

```text
git push tag v1.2.0
  → CI: npm run build
  → sync dist/assets/* to S3 with long Cache-Control
  → sync index.html with short Cache-Control
  → optional: invalidate /index.html only
  → users get new shell → load new hashed JS
```

```bash
# Long cache for hashed assets
aws s3 sync dist/assets/ s3://bucket/assets/ \
  --cache-control "public,max-age=31536000,immutable"

# Short cache for shell
aws s3 cp dist/index.html s3://bucket/index.html \
  --cache-control "public,max-age=60,must-revalidate" \
  --content-type "text/html"
```

## 3. Why not purge everything on deploy

| Approach | Downside |
|----------|----------|
| Purge `/*` | Origin spike; slower global rollout |
| Versioned filenames | Old JS stays cached but unused — **preferred** |
| Same `/app.js` forever | Users on stale code until purge |

Only **`index.html`** (and service worker, if any) needs frequent invalidation.

## 4. Service workers (PWA)

Service workers cache aggressively — can **override CDN** in the browser.

| Practice | Why |
|----------|-----|
| Version SW file name or hash | Force update on deploy |
| `skipWaiting` + `clients.claim` | Careful — understand UX |
| Cache bust on activate | Delete old caches |

Misconfigured SW causes “deployed but users see old app” despite CDN purge.

## 5. Images and media

| Type | CDN pattern |
|------|-------------|
| **Responsive images** | `srcset` same CDN; multiple widths in `/assets/` |
| **Video** | HLS/DASH segments — each `.ts` chunk long TTL |
| **User uploads** | Separate origin/path; shorter TTL; auth via signed URLs |

Use modern formats (**WebP**, **AVIF**) at build or via CDN **image optimization** (Cloudflare Polish, CloudFront image handler).

## 6. Compression

Enable **Brotli/gzip** at CDN or origin:

```http
Content-Encoding: br
Vary: Accept-Encoding
```

Cache key must include **encoding** — otherwise gzip client gets br bytes.

## 7. Subresource integrity (optional)

For third-party scripts from CDN:

```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-…"
        crossorigin="anonymous"></script>
```

SRI verifies file content — good for supply chain; your own hashed assets already pin by URL.

## 8. Platform-managed CDN

| Platform | You manage |
|----------|------------|
| **Vercel / Netlify / CF Pages** | Git push; platform sets headers |
| **S3 + CloudFront** | Full control — headers, invalidation, OAC |

Managed platforms encode best practices; custom S3+CDN teaches the underlying knobs.

## Next

Continue with [APIs & dynamic content](vi-apis-and-dynamic-content.md) for cacheable GET endpoints and edge logic.
