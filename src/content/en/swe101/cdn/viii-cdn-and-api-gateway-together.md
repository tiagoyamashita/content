---
label: "VIII"
subtitle: "CDN & API gateway together"
group: "CDN"
order: 8
---
CDN & API gateway — how they work together
**CDN** and **API gateway** sit at the **edge** of your system but solve different problems. Production stacks often use **both**: CDN for cacheable bytes, gateway for **dynamic API traffic**. Full gateway detail is in the [API gateway](../api-gateway/i-overview.md) track.

For cloud-architecture framing (north-south vs mesh), see [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## 1. Two layers, one client request

```text
Browser / mobile app
        │
        ▼
   ┌─────────┐
   │   CDN   │  Static: /assets/*, some GET /public/*
   └────┬────┘
        │ cache MISS or non-cacheable path
        ▼
   ┌─────────────┐
   │ API Gateway │  /api/* — auth, rate limit, route
   └──────┬──────┘
          ▼
   ALB / K8s Ingress / Lambda / microservices
```

| Component | Primary job | Typical paths |
|-----------|-------------|---------------|
| **CDN** | **Cache** responses close to user | `*.js`, `*.css`, images, cacheable GET |
| **API gateway** | **Route + policy** on dynamic requests | `/api/v1/*`, partner webhooks |
| **Origin / services** | Business logic, database | Behind gateway only |

CDN answers: “Can I serve a **stored copy**?”  
Gateway answers: “**Who** is this client, are they **allowed**, and **which service** handles it?”

## 2. Common combined topologies

### Web app + REST API (AWS-style)

```text
CloudFront (CDN)
  ├── /assets/*     → S3 origin (long TTL)
  ├── /index.html   → S3 (short TTL)
  └── /api/*        → API Gateway → Lambda or ALB → services
```

One hostname (`app.example.com`) or split (`cdn.` vs `api.`).

### SPA + separate API domain

```text
cdn.example.com   → CDN → S3 (static only)
api.example.com   → API Gateway → services (no CDN cache on authenticated routes)
```

Clear separation — fewer cache mistakes on private JSON.

### Cloudflare proxy everything

```text
Orange-cloud DNS → CDN/WAF edge
  ├── Cache static by path rule
  └── /api/* → bypass cache → origin or Workers → upstream
```

Gateway features may be **Cloudflare API shield**, **Workers**, or origin **Kong/NGINX**.

## 3. What each layer should do

| Concern | CDN | API gateway |
|---------|-----|-------------|
| **TLS** | Yes — public cert | Often yes (or CDN terminates first) |
| **Cache GET** | Yes — when headers allow | Rarely cache auth’d API |
| **JWT / API key validation** | Avoid — use gateway | Yes |
| **Rate limiting** | Basic (provider WAF) | Primary — per key/user ([Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md)) |
| **Path routing** | Origin selection by path | Service routing `/orders` → orders-svc |
| **WAF / DDoS** | CDN edge | Gateway + CDN together |
| **Request ID / tracing** | Optional at edge | Inject `X-Request-Id`, trace context |

**Thin gateway:** validate, route, limit — not business rules in gateway config.

## 4. Request walkthrough

**Static asset (cache hit):**

```text
GET /assets/main.a1b2.js
  → CDN edge HIT → 200 (origin never touched)
```

**Login API (no CDN cache):**

```text
POST /api/v1/auth/login
  → CDN BYPASS (POST never cached)
  → API Gateway: rate limit, optional WAF
  → auth-service → 200 + Set-Cookie
  → Cache-Control: no-store on response
```

**Public config GET (optional CDN cache):**

```text
GET /api/v1/public/config
  → CDN MISS → Gateway → config-service
  → Cache-Control: public, max-age=120
  → CDN stores; next user in region HIT
```

Configure CDN **behaviors** so `/api/me` never caches — see [APIs & dynamic content](vi-apis-and-dynamic-content.md).

## 5. TLS and hostname flow

```text
Client ──HTTPS──► CDN (cert: app.example.com)
                      ├── static → S3
                      └── /api → HTTPS → API Gateway (custom origin)
                                      └── HTTPS → internal ALB
```

Certificates at **CDN** and **gateway** must match hostnames clients use. Origin can use private CA inside VPC.

## 6. When you need only one

| Setup | Enough when |
|-------|-------------|
| **CDN only** | Static site, no public API |
| **Gateway only** | Internal API, no global static assets |
| **Both** | Typical SaaS — SPA + authenticated API + global users |

## 7. Pitfalls when combining

| Pitfall | Fix |
|---------|-----|
| CDN caches `/api/user` | Bypass or `no-store`; separate `api.` host |
| Gateway timeout &lt; CDN timeout | Align timeouts; CDN waits, client hangs |
| CORS only on gateway | CDN must forward `Origin`; both emit CORS headers consistently |
| Rate limit only in app | Enforce at gateway first — app is last line |
| Double gzip | Compress at one layer only |

## 8. Where to go next

| Topic | Note |
|-------|------|
| **API gateway track** | [Overview](../api-gateway/i-overview.md) — routing, auth, providers |
| **CDN operations** | [Operations & troubleshooting](vii-operations-and-troubleshooting.md) |
| **Rate limiting** | [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md) |
| **Redis limiter** | [Redis patterns](../redis/iv-patterns-and-use-cases.md) — app-layer complement |
