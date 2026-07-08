---
label: "VIII"
subtitle: "CDN と API ゲートウェイの統合"
group: "CDN"
order: 8
---
CDN および API ゲートウェイ — それらがどのように連携するか


**CDN** and **API gateway** sit at the **edge** of your system but solve different problems. Production stacks often use **both**: CDN for cacheable bytes, gateway for **dynamic API traffic**. Full gateway detail is in the [API gateway](../api-gateway/i-overview.md) track.

For cloud-architecture framing (north-south vs mesh), see [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## 1. 2 つのレイヤー、1 つのクライアント リクエスト

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

CDN は次のように答えます。「**保存されたコピー**を提供できますか?」  
ゲートウェイは、「**このクライアントは誰**ですか、**許可されています**、**どのサービス**がそれを処理しますか?」と答えます。

## 2. 一般的な組み合わせトポロジ

### Web アプリ + REST API (AWS-スタイル)

```text
CloudFront (CDN)
  ├── /assets/*     → S3 origin (long TTL)
  ├── /index.html   → S3 (short TTL)
  └── /api/*        → API Gateway → Lambda or ALB → services
```

One hostname (`app.example.com`) or split (`cdn.` vs `api.`).

### SPA + 別の API ドメイン

```text
cdn.example.com   → CDN → S3 (static only)
api.example.com   → API Gateway → services (no CDN cache on authenticated routes)
```

明確な分離 — プライベート JSON でのキャッシュミスが減少します。

### Cloudflare はすべてをプロキシします

```text
Orange-cloud DNS → CDN/WAF edge
  ├── Cache static by path rule
  └── /api/* → bypass cache → origin or Workers → upstream
```

ゲートウェイ機能は、**Cloudflare API シールド**、**Workers**、またはオリジン **Kong/NGINX** です。

## 3. 各層が行うべきこと

| Concern | CDN | API gateway |
|---------|-----|-------------|
| **TLS** | Yes — public cert | Often yes (or CDN terminates first) |
| **Cache GET** | Yes — when headers allow | Rarely cache auth’d API |
| **JWT / API key validation** | Avoid — use gateway | Yes |
| **Rate limiting** | Basic (provider WAF) | Primary — per key/user ([Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md)) |
| **Path routing** | Origin selection by path | Service routing `/orders` → orders-svc |
| **WAF / DDoS** | CDN edge | Gateway + CDN together |
| **Request ID / tracing** | Optional at edge | Inject `X-Request-Id`, trace context |

**シン ゲートウェイ:** 検証、ルーティング、制限 — ゲートウェイ構成のビジネス ルールではありません。

## 4. リクエストのウォークスルー

**静的アセット (キャッシュ ヒット):**

```text
GET /assets/main.a1b2.js
  → CDN edge HIT → 200 (origin never touched)
```

**ログイン API (CDN キャッシュなし):**

```text
POST /api/v1/auth/login
  → CDN BYPASS (POST never cached)
  → API Gateway: rate limit, optional WAF
  → auth-service → 200 + Set-Cookie
  → Cache-Control: no-store on response
```

**パブリック構成 GET (オプションの CDN キャッシュ):**

```text
GET /api/v1/public/config
  → CDN MISS → Gateway → config-service
  → Cache-Control: public, max-age=120
  → CDN stores; next user in region HIT
```

Configure CDN **behaviors** so `/api/me` never caches — see [APIs & dynamic content](vi-apis-and-dynamic-content.md).

## 5. TLS とホスト名のフロー

```text
Client ──HTTPS──► CDN (cert: app.example.com)
                      ├── static → S3
                      └── /api → HTTPS → API Gateway (custom origin)
                                      └── HTTPS → internal ALB
```

**CDN** および **ゲートウェイ** の証明書は、クライアントが使用するホスト名と一致する必要があります。 Origin は VPC 内でプライベート CA を使用できます。

## 6. 1 つだけ必要な場合

|セットアップ | | いつでも十分です。
|------|-----------|
| **CDN のみ** |静的サイト、パブリックなし API |
| **ゲートウェイのみ** |内部 API、グローバル静的資産なし |
| **両方** |典型的な SaaS — SPA + 認証済み API + グローバル ユーザー |

## 7. 組み合わせる際の落とし穴

| Pitfall | Fix |
|---------|-----|
| CDN caches `/api/user` | Bypass or `no-store`; separate `api.` host |
| Gateway timeout &lt; CDN timeout | Align timeouts; CDN waits, client hangs |
| CORS only on gateway | CDN must forward `Origin`; both emit CORS headers consistently |
| Rate limit only in app | Enforce at gateway first — app is last line |
| Double gzip | Compress at one layer only |

## 8. 次にどこへ行くか

| Topic | Note |
|-------|------|
| **API gateway track** | [Overview](../api-gateway/i-overview.md) — routing, auth, providers |
| **CDN operations** | [Operations & troubleshooting](vii-operations-and-troubleshooting.md) |
| **Rate limiting** | [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md) |
| **Redis limiter** | [Redis patterns](../redis/iv-patterns-and-use-cases.md) — app-layer complement |
