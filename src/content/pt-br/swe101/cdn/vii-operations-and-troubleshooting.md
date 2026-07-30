---
label: "VII"
subtitle: "Operations & troubleshooting"
group: "CDN"
order: 7
---
CDN — operations & troubleshooting
Operate a CDN by watching **hit ratio**, **origin load**, **error rates**, and knowing how to **purge** and **debug headers** when something looks wrong in production.

## 1. Metrics to track

| Metric | Healthy signal |
|--------|----------------|
| **Cache hit ratio** | High for static paths (`/assets/*`) |
| **Origin requests** | Drop after CDN enabled |
| **4xx/5xx at edge** | Low; spike → config or origin |
| **Time to first byte (TTFB)** | Lower from edge than direct origin |
| **Bandwidth egress** | Origin egress down; CDN bill may rise |

Provider dashboards: CloudFront **Monitoring**, Cloudflare **Analytics**, Fastly **Real-Time Stats**.

## 2. Debug with curl

```bash
# Response headers
curl -sI https://cdn.example.com/assets/main.js

# Look for:
# Cache-Control, Age, ETag
# CloudFront: X-Cache: Hit from cloudfront
# Cloudflare: CF-Cache-Status: HIT | MISS | BYPASS
```

Compare **via CDN** vs **direct origin** (bypass DNS to origin IP in staging only):

```bash
curl -sI -H "Host: cdn.example.com" https://origin-internal/assets/main.js
```

## 3. Common failures

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Users see old JS after deploy | `index.html` or SW cached too long | Short TTL on shell; purge `index.html` |
| API returns wrong user’s data | Public cache on private route | `no-store`; disable CDN for path |
| 403 from S3 origin | OAC/OAI policy wrong | Fix bucket policy + distribution |
| SSL error | Cert not in right region / wrong SAN | ACM us-east-1 for CloudFront |
| Low hit rate | Query string busts cache | Cache key rules; strip tracking params |
| CORS failures | Headers only on origin | Add CORS headers at CDN or origin consistently |
| Infinite redirect loop | HTTP/HTTPS mismatch | SSL mode Full (strict); origin listens HTTPS |

## 4. Stale content playbook

```text
1. Confirm symptom (one region vs global)
2. curl -sI URL — Hit or Miss? Age?
3. Check recent deploy — index.html vs assets
4. Purge specific path(s) if needed
5. Verify Cache-Control at origin
6. Post-incident: version URLs or shorter TTL
```

Avoid habitual **purge all** — masks missing hash-based deploy discipline.

## 5. Security incidents

If malicious or leaked file was cached:

1. **Remove at origin** immediately.
2. **Purge CDN** for affected paths (and wildcards if needed).
3. Rotate secrets if response contained tokens.
4. Review **cache key** — ensure auth responses were not cacheable.

## 6. Cost awareness

| Cost driver | Note |
|-------------|------|
| **Egress** | CDN egress often cheaper than cloud origin egress |
| **Requests** | Per-request pricing on some tiers |
| **Invalidations** | CloudFront: free tier limited per month |
| **Edge compute** | Workers/Lambda@Edge per invocation |

Long TTL on immutable assets reduces origin **and** invalidation churn.

## 7. Checklist

- [ ] Hashed static assets — `max-age` ≥ 1 year, `immutable`
- [ ] `index.html` — short TTL or `must-revalidate`
- [ ] Private API — `no-store` or CDN bypass behavior
- [ ] Origin not publicly writable (OAC, signed uploads)
- [ ] TLS full chain valid; HSTS when ready
- [ ] Monitoring on hit ratio and 5xx
- [ ] Documented purge runbook for security deploys
- [ ] CI sets `Cache-Control` on upload — not manual clicks

## Next

Continue with [CDN & API gateway together](viii-cdn-and-api-gateway-together.md), then the [API gateway](../api-gateway/i-overview.md) track.

## Related notes

- [CDN & edge caching](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md) — design patterns
- [Network bottlenecks](../sysdesign/bottleneck-analysis/v-network.md) — CDN in latency story
- [Redis performance](../redis/vii-performance-and-optimizations.md) — app-layer cache complement
- [Regions, AZs & edge](../../sre101/cloud-architecture/foundations/iii-regions-azs-and-edge.md) — edge vs region
