---
label: "III"
subtitle: "News feed & timeline"
group: "System design"
order: 3
---
News feed and timeline
**Twitter / Instagram-style** home timeline: show recent posts from people you **follow**, ranked by time or score.

## 1. Delivery models

| Model | On post | On read | Best for |
|-------|---------|---------|----------|
| **Fan-out on write (push)** | Write post id to every follower’s feed cache | Read pre-built list — O(1) | Normal users, moderate followers |
| **Fan-out on read (pull)** | Only write posts table | Merge N followees’ posts | Write-cheap; read expensive |
| **Hybrid** | Push for most; pull for celebrities | Merge push cache + celebrity pull | Production social graphs |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 130" role="img" aria-label="Fan-out on write vs hybrid with celebrity">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Fan-out on write (normal user)</text>
  <rect x="12" y="32" width="48" height="24" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="20" y="48" fill="#e4e4e7" font-size="8">Post</text>
  <path d="M60 44 H100" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="100" y="28" width="56" height="32" rx="2" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="108" y="48" fill="#e4e4e7" font-size="8">fan-out</text>
  <rect x="168" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="212" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="256" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="68" fill="#a1a1aa" font-size="8">follower feeds</text>
  <text x="12" y="92" fill="#fbbf24" font-size="9">Celebrity (10M followers): skip fan-out → fetch on read only</text>
</svg></figure>

## 2. Write amplification

| Followers | Fan-out writes per post |
|-----------|-------------------------|
| 500 | 500 Redis ZADD |
| 10 M | 10 M writes — unacceptable |

**Threshold rule:** if `followers > X` (e.g. 10 K), treat as **celebrity** — no push fan-out.

## 3. Data model

**Posts (source of truth)**

| Column | Type |
|--------|------|
| `post_id` | BIGINT (Snowflake) |
| `author_id` | BIGINT |
| `content` | TEXT |
| `media_ids` | JSON |
| `created_at` | TIMESTAMP |

**Feed cache (Redis)**

- Key: `feed:{user_id}`
- Type: **sorted set** — member = `post_id`, score = `created_at` epoch ms
- Trim to last K entries (e.g. 1000)

**Follow graph**

| `follower_id` | `followee_id` | `created_at` |

## 4. Read path (hybrid)

```text
1. ZREVRANGE feed:{user_id} 0 49          → pushed posts
2. For each celebrity followee: fetch recent posts (cached)
3. Merge + dedupe + rank → return page
```

Pagination: cursor = `(score, post_id)` tuple.

## 5. Scale tactics

| Component | Tactic |
|-----------|--------|
| Fan-out workers | Queue per post event; batch Redis pipeline |
| Hot users | Dedicated cache partition |
| Ranked feed | Precompute scores async; store in ZSET |

**Related:** Scalable patterns `iii-message-queues-and-async.md`, Part I Redis.
