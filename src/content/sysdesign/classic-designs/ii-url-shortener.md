---
label: "II"
subtitle: "URL shortener"
group: "System design"
order: 2
---
URL shortener
**Bitly-style** service: create a short link, **redirect** to the long URL, optional **analytics**.

## 1. Requirements

| Functional | Non-functional |
|------------|----------------|
| Create short URL from long URL | Low redirect latency (p99 < 50 ms) |
| Redirect short → long | Highly **read-heavy** |
| Optional expiry, custom alias | 99.9%+ availability |
| Click analytics (async OK) | Scale: see below |

**Scale (example):** 100 M URLs created/day; 10 B redirects/day → ~**115 K reads/s** average (peaks higher).

## 2. API sketch

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/v1/urls` | Create `{ long_url, custom_alias?, ttl? }` → `{ short_url }` |
| GET | `/{short_code}` | **302/301** redirect to long URL |
| GET | `/v1/urls/{code}/stats` | Analytics (authenticated) |

## 3. Short key generation

| Approach | How | Pros | Cons |
|----------|-----|------|------|
| **Hash + truncate** | MD5/SHA of URL → base62 first 7 chars | Stateless | Collisions — must check DB |
| **Counter + base62** | Global counter → encode | No collision | Single counter hotspot |
| **KGS pool** | Key Generation Service pre-allocates batches | Fast insert, no collision at write | Extra service |

Base62 charset: `[a-zA-Z0-9]` → 7 chars ≈ 62^7 ≈ 3.5 trillion keys.

## 4. Data model

| Column | Type | Notes |
|--------|------|-------|
| `short_code` | VARCHAR PK | 7–8 chars |
| `long_url` | TEXT | Target |
| `user_id` | BIGINT | Optional owner |
| `created_at` | TIMESTAMP | |
| `expires_at` | TIMESTAMP | Nullable |

**Shard key:** hash(`short_code`) → N DB shards.

## 5. Redirect: 301 vs 302

| Code | Browser behavior | Analytics |
|------|------------------|-----------|
| **301** Permanent | May cache redirect — fewer origin hits | Under-counts clicks |
| **302** Temporary | Hits server every click | Accurate counts |

Product choice: **302** for analytics; **301** + async click log if load dominates.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="URL shortener read path with cache">
  <rect x="12" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Client</text>
  <path d="M68 60 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="44" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="64" fill="#e4e4e7" font-size="9">Redis</text>
  <text x="108" y="88" fill="#86efac" font-size="8">cache-aside hit</text>
  <path d="M172 60 H212" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="212" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="220" y="64" fill="#e4e4e7" font-size="9">DB shard</text>
  <path d="M268 60 H308" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="308" y="44" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="316" y="64" fill="#e4e4e7" font-size="9">302 redirect</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Redirect hot path</text>
</svg></figure>

## 6. Scaling reads

1. **Redis** cache-aside: `GET short:{code}` → long URL; TTL + LRU eviction.
2. **CDN** at edge for popular links (short TTL if analytics matter).
3. **DB sharding** by `short_code` hash.
4. **Analytics:** async — click event → Kafka → Flink → ClickHouse (don’t block redirect).

## 7. Bottlenecks

| Risk | Mitigation |
|------|------------|
| Hot short link | CDN + local cache |
| KGS single point | Multiple KGS instances with partitioned ranges |
| Shard imbalance | Consistent hashing; re-shard plan |

**Related:** Scalable patterns `vi-cdn-and-edge-caching.md`, Part I caching/sharding.
