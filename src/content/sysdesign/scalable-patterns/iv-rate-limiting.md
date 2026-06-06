---
label: "IV"
subtitle: "Rate limiting"
group: "System design"
order: 4
---
Rate limiting
**Rate limiting** caps how many requests a client (user, IP, API key) can make in a window — protecting cost, fairness, and stability.

## 1. Why limit

| Goal | Example |
|------|---------|
| **Abuse prevention** | Scraping, credential stuffing |
| **Fairness** | Free tier 100 req/min vs paid 10 K |
| **Cost control** | Expensive LLM or GPU endpoints |
| **Stability** | Prevent one tenant saturating shared DB |

## 2. Algorithms

### Token bucket

- Bucket holds at most **B** tokens; refilled at **R** tokens/sec.
- Each request costs **1** token; empty bucket → reject.

| Param | Effect |
|-------|--------|
| Large **B** | Allows **bursts** up to B |
| High **R** | Sustained throughput ceiling |

### Leaky bucket

- Requests enter a **queue**; processed at **fixed rate**.
- Queue full → drop. **Smooths** bursts (no large spikes).

### Fixed window counter

- Count requests per calendar minute; reset at boundary.
- **Flaw:** 2× burst at window edges (599 + 599 in two adjacent minutes).

### Sliding window log

- Store timestamp per request; count in last **T** seconds.
- **Accurate**; memory heavy at high QPS.

### Sliding window counter

- Blend previous + current window counts — good balance of accuracy and memory (common in Redis implementations).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Token bucket allows burst then steady rate">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Token bucket (B=5, R=1/s)</text>
  <rect x="12" y="32" width="120" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="24" y="48" fill="#e4e4e7" font-size="9">●●●●● tokens</text>
  <text x="140" y="48" fill="#a1a1aa" font-size="9">5 rapid requests OK</text>
  <rect x="12" y="64" width="120" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="80" fill="#e4e4e7" font-size="9">○ empty</text>
  <text x="140" y="80" fill="#f87171" font-size="9">6th rejected until refill</text>
</svg></figure>

## 3. Comparison table

| Algorithm | Burst friendly | Memory | Edge-case |
|-----------|----------------|--------|-----------|
| Token bucket | Yes (bounded) | Low | Tune B vs R |
| Leaky bucket | No | Queue size | Steady output only |
| Fixed window | Yes at boundary | Low | Double burst at edge |
| Sliding window log | Controlled | High | Per-request timestamps |
| Sliding window counter | Controlled | Medium | Popular in production |

## 4. Where to enforce

| Layer | Pros | Cons |
|-------|------|------|
| **API Gateway** | Central policy, WAF integration | Single config blast radius |
| **Service mesh** | Per-route limits | Operational complexity |
| **App + Redis** | Fine-grained business rules | Every service must implement |
| **CDN / edge** | Blocks abuse before origin | Limited logic |

**Key dimensions:** `user_id`, `api_key`, `IP`, `tenant_id`, route (`POST /v1/generate`).

## 5. Client response

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716120060
```

Document limits in API docs; clients should **back off** exponentially with jitter.

## 6. Distributed rate limiting

Multiple API instances need a **shared counter** — typically **Redis** (`INCR` + `EXPIRE`, or sliding window Lua script). Clock skew matters for window boundaries; prefer monotonic TTL keys.

**Related:** `ii-api-design.md` (429 status), Part I caching (Redis).
