---
label: "V"
subtitle: "API Gateway & service mesh"
group: "Cloud architecture"
order: 5
---
API Gateway & service mesh
**North-south** traffic (clients → cluster) and **east-west** traffic (service ↔ service) need different control planes. **Circuit breakers** stop failures from cascading.

## 1. Traffic directions

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 110" role="img" aria-label="North south API gateway east west service mesh">
  <text x="12" y="18" fill="#d4d4d8" font-size="11" font-weight="600">North-south vs east-west</text>
  <rect x="160" y="28" width="80" height="24" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="172" y="44" fill="#e4e4e7" font-size="9">API Gateway</text>
  <rect x="12" y="72" width="56" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="88" fill="#e4e4e7" font-size="8">Client</text>
  <path d="M68 84 H160 44" stroke="#60a5fa" stroke-width="1.5" fill="none"/>
  <rect x="100" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="108" y="88" fill="#e4e4e7" font-size="8">Svc A</text>
  <rect x="200" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="88" fill="#e4e4e7" font-size="8">Svc B</text>
  <rect x="300" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="308" y="88" fill="#e4e4e7" font-size="8">Svc C</text>
  <path d="M156 84 H200 84" stroke="#fbbf24" stroke-width="1.5"/>
  <path d="M256 84 H300 84" stroke="#fbbf24" stroke-width="1.5"/>
  <text x="220" y="68" fill="#71717a" font-size="8">east-west (mesh)</text>
</svg></figure>

## 2. API Gateway (north-south)

Single public entry point for clients.

| Capability | Example |
|------------|---------|
| **Routing** | `/api/orders` → orders service |
| **TLS termination** | HTTPS at edge |
| **Authentication** | JWT validation, API keys |
| **Rate limiting** | 1000 req/min per client |
| **Request transformation** | Header injection, path rewrite |
| **WAF integration** | Block SQLi patterns |

| Product | Cloud |
|---------|-------|
| **AWS API Gateway** | REST / HTTP API |
| **Azure API Management** | Azure |
| **Google Apigee / Gateway** | GCP |
| **Kong, NGINX** | Self-hosted / K8s Ingress |

```yaml
# Conceptual route (Kong-style)
routes:
  - name: orders
    paths: ["/api/v1/orders"]
    service: orders-upstream
    plugins:
      - name: rate-limiting
        config: { minute: 500 }
      - name: jwt
```

## 3. Service mesh (east-west)

**Sidecar proxy** (Envoy) next to each pod handles service-to-service traffic.

```text
Pod: [ app container ] [ Envoy sidecar ]
         │                    │
         └──── localhost ─────┘
                    │
              mTLS to peer Envoy
```

| Feature | Without mesh | With mesh (Istio, Linkerd) |
|---------|--------------|----------------------------|
| Retries / timeouts | Per-library | Policy in YAML |
| mTLS | App code or manual certs | Automatic |
| Traffic split | Custom LB rules | 90/10 canary in config |
| Metrics | Per-app instrumentation | Uniform sidecar metrics |

| Product | Notes |
|---------|-------|
| **Istio** | Feature-rich, complex |
| **Linkerd** | Lightweight |
| **AWS App Mesh** | AWS-native Envoy |

**When to adopt:** many microservices, need uniform mTLS and traffic policy — not for a 3-service system.

## 4. Circuit breaker

Track failures to a downstream dependency; **fail fast** when unhealthy.

| State | Behavior |
|-------|----------|
| **Closed** | Normal calls |
| **Open** | Fail immediately — don't wait for timeout |
| **Half-open** | Probe with limited calls — recover or re-open |

```text
Svc A ──▶ [ breaker CLOSED ] ──▶ Svc B (healthy)

Svc B down → failures exceed threshold
Svc A ──▶ [ breaker OPEN ] ──✕ fast fail (fallback or cached response)

After cooldown → HALF-OPEN → test call → CLOSED if OK
```

**Resilience4j** (Java), **Envoy outlier detection**, **Istio destination rules**.

| Without breaker | With breaker |
|-----------------|--------------|
| Threads blocked on timeouts | Fail in ms |
| Retry storm amplifies outage | Shed load |
| Cascade: A waits on B waits on C | A degrades gracefully |

## 5. Gateway + mesh together

| Layer | Handles |
|-------|---------|
| **Gateway** | External auth, public API versioning, WAF |
| **Mesh** | Internal mTLS, retries between services |
| **Both** | Correlation ID injection at gateway, propagated by mesh |

## 6. Ingress vs API Gateway (Kubernetes)

| | Ingress (NGINX, ALB) | API Gateway |
|---|----------------------|-------------|
| Scope | L7 routing into cluster | Full API management |
| Auth | Basic, OAuth via annotations | Built-in policies |
| Use | Internal + simple public | Public API product |

Often: **CloudFront → ALB Ingress → services** for web; **API Gateway** for partner APIs.

## 7. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Mesh on day one | Direct K8s DNS until pain appears |
| Gateway does business logic | Thin gateway — logic in services |
| No timeout on HTTP client | Set connect + read timeout + breaker |
| 20 retry with no jitter | Bounded retries + exponential backoff |

**Related:** networking ingress note, `vi-observability-slo-and-slis.md`, `iv-event-driven-architecture.md`.
