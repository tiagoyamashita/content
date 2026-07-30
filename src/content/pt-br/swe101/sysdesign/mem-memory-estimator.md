---
label: "Mem"
subtitle: "Memory Estimator"
group: "System design"
order: 5
---
System Design — Memory Estimation
Back-of-envelope **RAM** sizing for sessions, caches, and app heaps — essential for interviews and capacity planning before you buy instances or hit **OOM**.

## 1. Why estimate memory?

| Question | Memory estimate answers |
|----------|-------------------------|
| How many **Redis** nodes? | Hot data set + overhead |
| App **heap** size / pod limit? | Sessions + objects in flight |
| Will we **OOM** at peak? | Concurrent users × bytes per user |
| Scale **vertical** or **horizontal**? | Working set vs single-node RAM cap |

Memory is often the first hard limit after you fix obvious CPU bottlenecks — see **Bottleneck analysis → CPU & memory**.

## 2. Core formula

```text
RAM_working_set ≈ concurrent_users × bytes_per_active_user
```

**Not DAU** — only users **active at the same time** during peak.

```text
concurrent_users = DAU × concurrency_factor

Example:
  10_000_000 DAU × 0.08 × 50 KB ≈ 40 GB working set (sessions/cache only)
```

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="DAU to concurrent users to RAM">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Peak memory chain</text>
  <rect x="12" y="36" width="80" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="54" fill="#e4e4e7" font-size="9">DAU</text>
  <path d="M92 50 H112" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="96" y="44" fill="#71717a" font-size="7">× factor</text>
  <rect x="112" y="36" width="96" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="120" y="54" fill="#e4e4e7" font-size="9">concurrent</text>
  <path d="M208 50 H228" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="210" y="44" fill="#71717a" font-size="7">× bytes</text>
  <rect x="228" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="244" y="54" fill="#e4e4e7" font-size="9">RAM (GB)</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Add 2× headroom before dividing by node RAM (§6).</text>
</svg></figure>

## 3. Concurrency factor (peak)

| App type | Peak concurrent as % of DAU | Notes |
|----------|----------------------------|--------|
| General web / e-commerce | **5–10%** | Lunch + evening peaks |
| Social / feed (mobile) | **10–20%** | Long sessions |
| Real-time (chat, game, collab) | **20–40%** | WebSocket stays open |
| B2B SaaS (business hours) | **15–25%** of **WAU** | Use weekly active if DAU sparse |
| Batch / API-only | **negligible session RAM** | Size per request buffer instead |

**Interview tip:** state your assumption explicitly — “Assume 10 M DAU, 8% concurrent at peak → 800 K concurrent.”

## 4. Bytes per active user (what to count)

| In-memory item | Typical size | Count when |
|----------------|--------------|------------|
| HTTP session (server-side) | 1–20 KB | Sticky sessions, cart |
| JWT in memory (parsed claims) | < 1 KB | Usually stateless — **don’t** multiply by DAU |
| Cached user profile | 5–50 KB | Redis `user:{id}` |
| Home feed / timeline slice | 50–500 KB | Push model precomputed feed |
| Full page HTML fragment | 100 KB – 2 MB | Edge/page cache |
| WebSocket connection buffers | 4–16 KB+ | Chat, live updates |
| In-flight request context | 1–10 KB | Per concurrent request on app |

**Stack only what you store in RAM** — not everything in the database.

### Example session breakdown (50 KB total)

| Field | Size |
|-------|------|
| `user_id`, roles | 200 B |
| Cart (10 line items) | 8 KB |
| Recent views | 12 KB |
| CSRF + flash messages | 2 KB |
| Framework overhead | ~28 KB |
| **Total** | **~50 KB** |

## 5. Full-system RAM budget

One region at peak — allocate **per layer**:

| Component | What to size | Rule of thumb |
|-----------|--------------|---------------|
| **App servers** | Heap + native + threads | `working_set × 1.3` heap overhead (JVM/Go) |
| **Redis / Memcached** | Hot keys | Data + **~25%** fragmentation (`mem_fragmentation_ratio`) |
| **PostgreSQL** | Buffer cache | `shared_buffers` ≈ **25%** of DB instance RAM |
| **OS + kernel** | — | Reserve **512 MB – 2 GB** per node |
| **Sidecars / agents** | mesh, logs | 128–512 MB each |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 160" role="img" aria-label="Tiered memory from hot RAM to cold disk">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Tiered data temperature</text>
  <rect x="12" y="36" width="120" height="32" rx="3" fill="rgba(248,113,113,0.15)" stroke="#f87171"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="9">Hot — Redis RAM</text>
  <rect x="12" y="76" width="120" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="96" fill="#e4e4e7" font-size="9">Warm — SSD cache</text>
  <rect x="12" y="116" width="120" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="136" fill="#e4e4e7" font-size="9">Cold — DB disk</text>
  <text x="148" y="56" fill="#a1a1aa" font-size="9">Size with concurrent × bytes (§2)</text>
  <text x="148" y="96" fill="#a1a1aa" font-size="9">Less frequently accessed keys</text>
  <text x="148" y="136" fill="#a1a1aa" font-size="9">Source of truth — not in session RAM</text>
</svg></figure>

## 6. Headroom and node count

```text
total_RAM_required = working_set × 2        # GC, spikes, fragmentation
nodes              = ceil(total_RAM / RAM_per_node_usable)

usable_per_node    = node_RAM − OS_reserve − other_daemons
```

| Utilisation | Guidance |
|-------------|----------|
| **< 70%** steady | Healthy — room for spikes |
| **70–80%** | Plan scale event |
| **> 80%** | OOM risk — Linux killer is fast |

**Example — Redis cluster**

| Input | Value |
|-------|-------|
| Working set | 40 GB |
| With 2× headroom | 80 GB |
| Node size | 32 GB RAM, 2 GB OS → **30 GB usable** |
| Nodes | `ceil(80 / 30)` = **3** Redis shards/replicas |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 90" role="img" aria-label="Split working set across three nodes">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">80 GB target → 3 × ~27 GB shards</text>
  <rect x="12" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="36" y="58" fill="#e4e4e7" font-size="9">Node A</text>
  <rect x="120" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="144" y="58" fill="#e4e4e7" font-size="9">Node B</text>
  <rect x="228" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="252" y="58" fill="#e4e4e7" font-size="9">Node C</text>
</svg></figure>

## 7. Worked scenarios

### A — Session store (Redis)

| Assumption | Value |
|------------|-------|
| DAU | 5 M |
| Concurrency | 10% → **500 K** |
| Session size | 8 KB |
| Raw | 500 K × 8 KB = **4 GB** |
| +25% Redis overhead | **5 GB** |
| ×2 headroom | **10 GB** Redis fleet |

### B — Precomputed news feed (classic design)

| Assumption | Value |
|------------|-------|
| DAU | 20 M |
| Fan-out cache: 30% users get push feed | 6 M feeds stored (not full DAU) |
| 200 KB per feed slice in Redis | 6 M × 200 KB ≈ **1.2 TB** |
| Mitigation | Trim to top 500 posts; compress; tier celebrities to pull |

Shows **fan-out on write** is a **memory** problem, not just write amplification.

### C — JVM API pods

| Assumption | Value |
|------------|-------|
| 800 K concurrent | |
| 50 KB effective state offloaded to Redis | Heap mostly request buffers |
| 200 MB baseline + 2 KB × in-flight (5 K/pod) | Size heap **512 MB–1 GB** per pod if stateless |
| Pod count from QPS | Separate from session RAM |

## 8. Eviction when memory is full

| Policy | Evicts | Best when |
|--------|--------|-----------|
| **LRU** | Least recently used | Uniform access; sessions |
| **LFU** | Least frequently used | Power-law hot keys |
| **TTL** | After idle timeout | Predictable session expiry |
| **maxmemory-policy** | Redis: `allkeys-lru`, `volatile-lru`, etc. | Match key TTL strategy |

**Pair TTL + LRU:** expire idle sessions; LRU handles bursts when at `maxmemory`.

## 9. Scaling strategies

| Strategy | Memory effect |
|----------|---------------|
| **Vertical** | Bigger RAM per node — quick until hardware cap |
| **Horizontal** | Shard by `user_id` hash — spreads working set |
| **Consistent hash ring** | Add node → minimal key remapping |
| **Tiered cache** | RAM for hot; SSD for warm |
| **Compress values** | Snappy/LZ4 in Redis — CPU ↔ RAM trade |
| **Offload to client** | JWT stateless — less server RAM, other trade-offs |

## 10. Common mistakes

| Mistake | Fix |
|---------|-----|
| Use **DAU** instead of **concurrent** | Apply concurrency factor |
| Count entire DB size as “memory need” | Only hot/working set in cache |
| Ignore **replication** | Primary + replica each hold data — plan both |
| 100% RAM utilisation target | Keep **30%+** free |
| Same bytes for web and WebSocket | Long-lived connections need buffer budget |

## 11. Interview checklist

- [ ] State DAU, concurrency %, derive concurrent users
- [ ] Itemise bytes per user (session, cache, feed)
- [ ] Multiply → working set GB
- [ ] ×2 headroom; divide by usable node RAM
- [ ] Mention eviction (LRU/TTL) and sharding if TB-scale
- [ ] Note what is **not** in RAM (full DB on disk)

**Related:** Part I capacity estimation, **Classic designs** (feed, URL shortener), **Bottleneck analysis → CPU & memory**.
