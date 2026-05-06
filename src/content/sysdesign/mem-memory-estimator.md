---
label: "Mem"
subtitle: "Memory Estimator"
group: "System design"
order: 5
---
System Design — Memory Estimation
How much RAM does your system need as users grow?

## 1. The core formula

Memory needed = concurrent_users × bytes_per_session

Not ALL users are concurrent — use a concurrency factor:
- Web apps:        ~5-10% of DAU at peak
- Real-time apps:  ~20-40% of DAU at peak

Example:
10 M DAU × 8% concurrency × 50 KB/session = 40 GB

## 2. What lives in memory?

Layer             Typical size
─────────────────────────────
HTTP session       1–20 KB
JWT / auth token   < 1 KB
User object cache  5–50 KB
Feed / timeline    50–500 KB
Full page cache    100 KB–2 MB

## 3. System memory breakdown

Component         Typical allocation
──────────────────────────────────────
App servers        session working set + heap overhead (~30%)
Redis / Memcached  hot data set + ~25% fragmentation headroom
Database buffers   PostgreSQL: shared_buffers = 25% of RAM
OS + kernel        always reserve ~512 MB–2 GB

## 4. Capacity planning rule of thumb

Total RAM needed = working_set × 2          (2× headroom for GC, spikes)
Nodes needed     = ceil(total_RAM / node_RAM)

Never run above ~70% utilisation in steady state.
OOM kills happen fast — add nodes before you hit 80%.

## 5. Eviction when memory is full

LRU  (Least Recently Used)  — evict coldest session first.
Good for: uniform access patterns.

LFU  (Least Frequently Used) — evict least-popular keys.
Good for: skewed access (power-law / hot keys).

TTL-based — expire sessions after N minutes of inactivity.
Simple, predictable, pairs well with LRU.

## 6. Scaling strategies

Vertical scaling   — bigger nodes (quick, has a ceiling).
Horizontal scaling — more nodes behind a consistent-hash ring.
Tiered caching     — hot tier in RAM, warm tier on SSD, cold in DB.
Data partitioning  — shard sessions by user ID to avoid hot spots.

## 7. Interactive estimator
Use the graph in Preview mode to drag sliders and instantly see
how session size, node count, and RAM per node affect capacity.
