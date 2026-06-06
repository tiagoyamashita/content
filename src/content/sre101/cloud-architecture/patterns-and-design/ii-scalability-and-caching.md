---
label: "II"
subtitle: "Scalability & caching"
group: "Cloud architecture"
order: 2
---
Scalability & caching
Handle growth by **scaling** compute and **offloading** repeated reads. Cloud auto scaling assumes **stateless** application tiers.

## 1. Vertical vs horizontal scaling

| | Vertical (scale up) | Horizontal (scale out) |
|---|---------------------|------------------------|
| Action | Bigger VM (more CPU/RAM) | More instances behind LB |
| Pros | Simple, no code change | High ceiling, fault tolerant |
| Cons | Hard ceiling, SPOF | App must be stateless or shared state |
| Cloud example | `t3.micro` → `t3.xlarge` | ASG 2 → 20 EC2 instances |

```text
Vertical:  [====      ]  →  [============]
Horizontal: [==] [==]     →  [==] [==] [==] [==] [==]
            load balancer distributes requests
```

## 2. Stateless services

Each request must carry enough context for **any** instance to handle it:

| Stateful (bad for scale-out) | Stateless (good) |
|------------------------------|------------------|
| Session in JVM memory | JWT or session in Redis |
| Local file upload cache | S3 pre-signed upload |
| In-memory shopping cart | Cart in DB/Redis |

```http
GET /api/orders HTTP/1.1
Authorization: Bearer eyJhbG...
X-Request-Id: 7f3a9c2e-...
```

Any pod behind the load balancer can serve the request.

## 3. Auto Scaling

**AWS Auto Scaling Group** (similar: Azure VMSS, GKE HPA):

| Policy type | Behavior |
|-------------|----------|
| **Target tracking** | Keep metric at target (e.g. CPU 60%) — simplest |
| **Step scaling** | Add N instances when CPU > 80% |
| **Scheduled** | Scale up before known peak (Black Friday) |

```yaml
# Conceptual ASG target tracking
TargetValue: 60.0
PredefinedMetricType: ASGAverageCPUUtilization
ScaleOutCooldown: 300   # seconds — prevent thrashing
ScaleInCooldown: 300
```

| Setting | Why |
|---------|-----|
| **Cooldown** | Avoid add/remove loop on noisy metrics |
| **Min / max / desired** | Floor for HA, ceiling for cost |
| **Health checks** | LB deregisters unhealthy instances before scale-in |

## 4. Caching layers

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" role="img" aria-label="Cache tiers CDN Redis read replica">
  <rect x="12" y="36" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="9">CDN edge</text>
  <path d="M84 52 H104" stroke="#a1a1aa"/>
  <rect x="104" y="36" width="72" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="116" y="56" fill="#e4e4e7" font-size="9">Redis</text>
  <path d="M176 52 H196" stroke="#a1a1aa"/>
  <rect x="196" y="36" width="88" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="56" fill="#e4e4e7" font-size="9">Read replica</text>
  <path d="M284 52 H304" stroke="#a1a1aa"/>
  <rect x="304" y="36" width="72" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="56" fill="#e4e4e7" font-size="9">Primary DB</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Closer to user = lower latency</text>
</svg></figure>

| Layer | Stores | TTL / invalidation |
|-------|--------|-------------------|
| **CDN** (CloudFront, Cloudflare) | Static assets, cacheable GET APIs | Cache-Control headers |
| **In-memory** (Redis, Memcached) | Hot rows, sessions, rate limits | Key TTL, pub/sub invalidation |
| **Read replica** | Full DB copy | Async replication lag |
| **Application** | Computed aggregates | Local Caffeine — watch staleness |

## 5. Cache-aside pattern

```text
1. GET key from Redis
2. Miss → read DB → SET Redis → return
3. Write → update DB → DELETE Redis key (or update)
```

| Pitfall | Mitigation |
|---------|------------|
| **Cache stampede** | Single-flight lock, request coalescing |
| **Stale reads** | Short TTL + invalidation on write |
| **Hot key** | Shard key, local L1 cache |

## 6. Read vs write scaling

| Bottleneck | Pattern |
|------------|---------|
| Read-heavy | Replicas + Redis + CDN |
| Write-heavy | Sharding, queue-backed writes, partition keys |
| Mixed | CQRS — separate read and write models |

## 7. Example: e-commerce product page

```text
User → CloudFront (product image, static JS)
     → ALB → API pods (stateless, HPA on CPU)
     → Redis (product catalog cache, 5 min TTL)
     → RDS primary (orders) + read replica (browse catalog)
```

Scale API pods on request rate; warm Redis on deploy; CDN for 90% of bytes transferred.

## 8. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Sticky sessions on LB | Externalize session |
| Scale DB vertically forever | Read replicas, cache, shard |
| Cache everything with no TTL | Define freshness requirements |
| Scale out during incident without root cause | Fix leak/OOM first |

**Related:** [Microservices vs monolith](iii-microservices-vs-monolith.md), system design scalable-patterns CDN note.
