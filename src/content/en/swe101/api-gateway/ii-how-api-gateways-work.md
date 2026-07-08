---
label: "II"
subtitle: "How gateways work"
group: "API Gateway"
order: 2
---
API gateway — how gateways work
**North-south** traffic flows from **clients** (internet, mobile, partners) **into** your system through the gateway. The gateway terminates the client connection, applies policy, and opens a **new** connection to upstream services.

## 1. Request flow

```text
1. Client TLS handshake with gateway (api.example.com)
2. Gateway matches route (path, method, host)
3. Plugins/policies run (auth, rate limit, WAF)
4. Gateway forwards to upstream (HTTP/gRPC/Lambda)
5. Upstream responds
6. Gateway may transform response → client
```

| Step | Failure mode |
|------|--------------|
| **Route miss** | 404 from gateway — no upstream hit |
| **Auth fail** | 401/403 — upstream not called |
| **Rate limit** | 429 — protect upstream |
| **Upstream timeout** | 504 — tune gateway vs service timeouts |

## 2. North-south vs east-west

| Direction | Path | Tooling |
|-----------|------|---------|
| **North-south** | Client → gateway → service | **API gateway**, CDN |
| **East-west** | Service ↔ service | K8s DNS, **service mesh** (Istio, Linkerd) |

Gateway handles **external** trust boundary. Internal service calls often skip the public gateway — use mesh or direct cluster DNS with mTLS.

See [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## 3. Gateway vs load balancer

| | **Load balancer (ALB/NLB)** | **API gateway** |
|---|----------------------------|-----------------|
| **Layer** | L4/L7 distribution | L7 API semantics |
| **Routing** | Host/path → target group | Versioned routes, plugins |
| **Auth** | Minimal | JWT, API keys, OAuth |
| **Rate limit** | Optional slow | First-class |
| **Typical stack** | Gateway **→** ALB **→** pods | Both layers common |

ALB spreads load; gateway adds **API product** features.

## 4. With CDN in front

```text
GET /assets/app.js     → CDN → S3 (gateway not involved)
POST /api/v1/orders    → CDN bypass → Gateway → orders-service
```

CDN may share hostname — **path-based behaviors** send API traffic to gateway origin. Details: [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

## 5. Synchronous vs async integration

| Upstream type | Pattern |
|---------------|---------|
| **HTTP service** | Proxy pass-through |
| **AWS Lambda** | API Gateway event invoke |
| **Queue** | Gateway HTTP → service enqueues (gateway stays sync to client) |
| **WebSocket** | Gateway upgrade + route (provider-specific) |

Client usually waits for **one** synchronous response unless you expose async pattern (202 + poll/webhook).

## 6. Headers and context

Gateway injects context for upstream:

```http
X-Request-Id: 7f3a9c2e-...
X-Forwarded-For: 203.0.113.10
X-Authenticated-User: user_42
Authorization: (stripped or forwarded per policy)
```

Services trust **gateway-validated** identity headers only if internal network prevents client spoofing (mTLS or private subnet).

## 7. Cold path vs hot path

| | Gateway | Upstream service |
|---|---------|------------------|
| **Keep stateless** | Yes — horizontal scale | Business state in DB |
| **Config changes** | Routes, plugins — deploy carefully | App releases |
| **Latency budget** | Single-digit ms overhead target | Most work here |

## Next

Continue with [Routing & versions](iii-routing-and-versions.md) for paths, staging, and canaries.
