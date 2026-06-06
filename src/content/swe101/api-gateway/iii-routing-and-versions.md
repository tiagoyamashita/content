---
label: "III"
subtitle: "Routing & versions"
group: "API Gateway"
order: 3
---
API gateway — routing & versions
Route by **path**, **method**, **host**, and **headers** — map public URLs to internal services and API **versions** without exposing every microservice hostname.

## 1. Path-based routing

```text
GET  /api/v1/orders/*     → orders-service:8080
GET  /api/v1/users/*      → users-service:8080
POST /api/v1/webhooks/*   → webhook-handler
```

Kong-style conceptual config:

```yaml
routes:
  - name: orders-v1
    paths: ["/api/v1/orders"]
    strip_path: false
    service: orders-upstream
  - name: users-v1
    paths: ["/api/v1/users"]
    service: users-upstream
```

| Option | Effect |
|--------|--------|
| **`strip_path: true`** | `/api/v1/orders/123` → upstream `/123` |
| **`strip_path: false`** | Upstream sees full path — service mounts `/api/v1/orders` |
| **Method match** | `GET` vs `POST` on same path → different routes |

## 2. API versioning strategies

| Strategy | Example | Pros / cons |
|----------|---------|-------------|
| **URL path** | `/api/v1/`, `/api/v2/` | Obvious; easy at gateway |
| **Header** | `Accept: application/vnd.app.v2+json` | Clean URLs; harder to test in browser |
| **Query** | `/api/orders?version=2` | Rare for public APIs |

Gateway often routes **`/api/v1/*`** and **`/api/v2/*`** to different upstreams during migration.

## 3. Host-based routing

```text
api.example.com      → public REST gateway
partner.example.com  → partner routes + stricter limits
internal.example.com → VPN-only (network policy + gateway)
```

Same gateway cluster, different **route tables** per hostname.

## 4. Canary and traffic split

Send small % of traffic to new version:

```text
95% /api/v1/orders → orders-v1
 5% /api/v1/orders → orders-v2-canary
```

Implemented via:

- Gateway **weighted upstream** (Kong, Envoy, AWS weighted targets)
- **Service mesh** traffic split (internal)
- **Feature flag** in app (not gateway — different concern)

Watch error rate on canary — automated rollback via CI.

## 5. Rewrites and redirects

| Action | Use |
|--------|-----|
| **Path rewrite** | Public `/v1/orders` → internal `/orders` |
| **301/302 redirect** | Deprecate old hostname |
| **Header injection** | `X-Api-Version: 1` for upstream logging |

Avoid complex rewrite chains — hard to debug.

## 6. OpenAPI / schema (optional)

Some gateways import **OpenAPI** spec to define routes and validate requests (**Cloudflare API Shield**, **Azure APIM**, **Kong request validator**).

Benefits: reject malformed requests at edge; document contract.

## 7. gRPC and WebSocket

| Protocol | Gateway support |
|----------|-----------------|
| **HTTP/JSON** | Universal |
| **gRPC** | Envoy, Kong gRPC, AWS HTTP API (limited) — often gRPC-gateway translate |
| **WebSocket** | Provider-specific routes; sticky sessions may matter |

Pick gateway product matching your protocol — not all support gRPC natively.

## Next

Continue with [Authentication](iv-authentication.md) for JWT, API keys, and OAuth at the gateway.
