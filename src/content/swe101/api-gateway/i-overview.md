---
label: "I"
subtitle: "Overview"
group: "API Gateway"
order: 1
---
API gateway — overview
An **API gateway** is the **single public entry** for client traffic to your backend — it **routes** requests to services and applies **cross-cutting policies**: TLS, authentication, rate limits, request transforms, and observability hooks.

**CDN** caches static and some GET responses at the edge; **gateway** handles **dynamic API** traffic. Most SaaS stacks use both — see [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

For architecture patterns (north-south vs service mesh), see [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Role, vs load balancer, vs CDN |
| **II — How gateways work** | Request flow, north-south traffic |
| **III — Routing & versions** | Paths, host rules, canary, rewrites |
| **IV — Authentication** | JWT, API keys, OAuth at the edge |
| **V — Rate limiting & resilience** | Throttling, timeouts, circuit breakers |
| **VI — Setup & providers** | AWS, Kong, NGINX, cloud managed |
| **VII — Operations & troubleshooting** | Logs, debug, common failures |

## Gateway vs other edge pieces

| Component | Primary question |
|-----------|------------------|
| **CDN** | “Can I serve a cached copy?” ([CDN track](../cdn/i-overview.md)) |
| **API gateway** | “Who is allowed, and where does this request go?” |
| **Load balancer (ALB/NLB)** | “Which healthy instance gets this TCP/HTTP connection?” |
| **Reverse proxy (NGINX)** | Often **is** the gateway, or sits behind it |
| **WAF** | “Is this request malicious?” — often bundled with CDN/gateway |

```text
Client → CDN (optional) → API Gateway → Load balancer → Service pods
```

## What gateways typically do

| Capability | Example |
|------------|---------|
| **Routing** | `GET /api/v1/orders` → orders-service |
| **TLS termination** | HTTPS for `api.example.com` |
| **Authentication** | Validate JWT, API key, mTLS |
| **Rate limiting** | 1000 req/min per API key |
| **Request/response transform** | Strip path prefix, add headers |
| **Observability** | Access logs, metrics, trace ID injection |

Keep gateway **thin** — business rules stay in services.

## Common products

| Product | Notes |
|---------|-------|
| **AWS API Gateway** | REST API, HTTP API, Lambda/HTTP integrations |
| **Kong / Kong Gateway** | Open source, plugins, K8s-friendly |
| **NGINX / NGINX Plus** | Reverse proxy + gateway patterns |
| **Azure API Management** | Full API lifecycle |
| **Google API Gateway / Apigee** | GCP and enterprise API management |
| **Envoy + Gloo / Ambassador** | Kubernetes-native |
| **Cloudflare API Shield** | Edge + schema validation |

## When you need a gateway

| Need gateway | Skip for now |
|--------------|--------------|
| Multiple backend services behind one API host | Single monolith, one port |
| Partner/public API with keys and quotas | Internal-only VPC calls |
| Central auth and rate limits | Few clients, limits in app OK |
| API versioning at edge | Version only in app routes |

## Next

Continue with [How gateways work](ii-how-api-gateways-work.md) for request flow and north-south traffic.
