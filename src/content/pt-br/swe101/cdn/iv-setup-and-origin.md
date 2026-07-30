---
label: "IV"
subtitle: "Setup & origin"
group: "CDN"
order: 4
---
CDN — setup & origin
Wire a CDN by choosing an **origin**, creating a **distribution**, pointing **DNS**, and locking origin access so only the CDN can fetch private buckets.

## 1. Typical architecture

```text
                    ┌─────────────┐
  cdn.example.com   │  CloudFront │─── OAI/OAC ───► S3 bucket (private)
  (or CF proxy)     │  / CF / etc │
                    └──────┬──────┘
                           │ cache miss
                    ┌──────▼──────┐
                    │ ALB / app   │  (optional second origin for API)
                    └─────────────┘
```

| Origin type | Use |
|-------------|-----|
| **S3 / GCS / R2** | Static site, built SPA, downloads |
| **Load balancer** | Dynamic app, mixed static + API |
| **Custom domain** | nginx, origin server |
| **Serverless URL** | API Gateway, Lambda function URL |

## 2. AWS CloudFront + S3 (pattern)

1. Create **private** S3 bucket with built assets.
2. Create **CloudFront distribution** — origin = bucket.
3. Enable **Origin Access Control (OAC)** — bucket policy allows only CloudFront.
4. Attach **ACM certificate** (us-east-1 for CloudFront) for `cdn.example.com`.
5. CNAME **`cdn.example.com`** → `dxxxxx.cloudfront.net`.

S3 object metadata:

```text
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

Upload via CI:

```bash
aws s3 sync dist/ s3://myapp-assets-prod/ --cache-control "public,max-age=31536000,immutable"
aws cloudfront create-invalidation --distribution-id E123456 --paths "/index.html"
```

## 3. Cloudflare (pattern)

1. Add site to Cloudflare — nameservers at registrar.
2. **Orange cloud (proxy)** on DNS record → traffic through CDN.
3. **SSL/TLS** → Full (strict) with origin cert.
4. **Cache Rules** — path TTL overrides.
5. **R2 + CDN** or origin = your server IP/hostname.

Free tier includes CDN + TLS — common for startups ([Hosting & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md)).

## 4. Origin security

| Mechanism | Purpose |
|-----------|---------|
| **OAC / OAI (AWS)** | S3 not public internet |
| **Signed URLs / cookies** | Time-limited access to private objects |
| **Origin secret header** | CDN adds header; origin rejects others |
| **IP allowlist** | Origin only accepts CDN egress IPs |

Never leave private assets in a **public** bucket without understanding the blast radius.

## 5. Multiple origins / behaviors

Split by path on one distribution:

| Path | Origin | Cache |
|------|--------|-------|
| `/assets/*` | S3 | Long TTL |
| `/api/*` | ALB | Short or no cache |
| `/` | S3 `index.html` | Short TTL |

CloudFront **behaviors**, Cloudflare **rules**, Fastly **conditions** — same idea.

## 6. HTTPS and HSTS

- User → CDN: **TLS 1.2+**, modern ciphers.
- Enable **HSTS** at CDN once HTTPS stable: `Strict-Transport-Security: max-age=31536000`.
- Redirect HTTP → HTTPS at edge.

## 7. Local dev vs production

| Environment | CDN |
|-------------|-----|
| **Localhost** | No CDN — Vite/webpack dev server |
| **Staging** | Separate distribution or prefix `staging-cdn.example.com` |
| **Production** | Full CDN; stricter cache on hashed assets only |

Test cache headers with curl:

```bash
curl -I https://cdn.example.com/assets/main.js
curl -I -H "Accept-Encoding: gzip" https://cdn.example.com/assets/main.js
```

Check **`Cache-Control`**, **`Age`** (time in CDN cache), **`X-Cache`** / **`CF-Cache-Status`** (provider-specific hit/miss).

## Next

Continue with [Static assets & SPAs](v-static-assets-and-spas.md) for build output and deploy pipelines.
