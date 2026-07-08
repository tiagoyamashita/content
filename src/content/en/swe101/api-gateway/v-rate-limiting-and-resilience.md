---
label: "V"
subtitle: "Rate limiting & resilience"
group: "API Gateway"
order: 5
---
API gateway — rate limiting & resilience
**Rate limiting** at the gateway protects upstream from abuse and unfair usage. Pair with **timeouts**, **retries** (careful), and **circuit breakers** for resilience.

Deep dive on algorithms: [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md). App-layer limiter: [Redis patterns](../redis/iv-patterns-and-use-cases.md).

## 1. Why limit at the gateway

| Goal | Example |
|------|---------|
| **Abuse** | Block scraping, credential stuffing |
| **Fairness** | Free tier 100 req/min; paid 10 K |
| **Cost** | LLM/GPU endpoints |
| **Stability** | One tenant cannot exhaust connection pool |

Reject with **429 Too Many Requests** + **`Retry-After`** header when possible.

## 2. Limit dimensions

| Key | Use |
|-----|-----|
| **API key / client id** | Partner quotas |
| **User id** (from JWT) | Per-account fairness |
| **IP address** | Anonymous endpoints — noisy neighbor |
| **Route** | Stricter on `/search` vs `/health` |

```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 500
      policy: local   # or redis for cluster-wide
      limit_by: consumer
```

Use **Redis-backed** limiter when multiple gateway instances must share counters.

## 3. Token bucket (typical)

- Bucket size **B** allows burst
- Refill rate **R** caps sustained QPS

Gateway plugins often expose “requests per minute” — maps to bucket/window internally.

## 4. Timeouts and payload limits

| Setting | Purpose |
|---------|---------|
| **Connect timeout** | Fail fast if upstream dead |
| **Read timeout** | Max wait for response body |
| **Max body size** | Reject huge uploads at edge |

Gateway timeout should be **≤ CDN timeout** and **≥ upstream p99** — align all three layers ([CDN & gateway together](../cdn/viii-cdn-and-api-gateway-together.md)).

## 5. Circuit breaker

When upstream error rate spikes, **fail fast** instead of queueing threads:

| State | Behavior |
|-------|----------|
| **Closed** | Normal proxy |
| **Open** | Immediate 503/504 to client |
| **Half-open** | Probe requests — recover or stay open |

**Resilience4j** (Java), **Envoy outlier detection**, **Istio destination rules** — gateway or mesh.

Without breaker: retry storms amplify outages.

## 6. Retries at gateway

| Safe to retry | Not safe |
|---------------|----------|
| **GET** idempotent | **POST** payment |
| **503** with idempotent id | Any non-idempotent write |

If gateway retries, use **bounded retries + jitter**; prefer idempotency keys in app for writes.

## 7. WAF and bot protection

Many stacks combine:

```text
CDN/WAF (SQLi, XSS patterns) → Gateway (auth, rate limit) → service
```

Cloudflare, AWS WAF on ALB/API Gateway — block obvious attacks before app code.

## Next

Continue with [Setup & providers](vi-setup-and-providers.md) for AWS API Gateway, Kong, and NGINX patterns.
