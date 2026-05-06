---
label: "memory-estimator"
group: "System Design"
order: 99
---
# System Design — Memory Estimation

How much RAM does your system need as users grow?

---

## 1. The core formula

```
Memory needed = concurrent_users × bytes_per_session
```

Not ALL users are concurrent — use a **concurrency factor**:

| App type       | Concurrency at peak |
|----------------|---------------------|
| Web apps       | ~5–10 % of DAU      |
| Real-time apps | ~20–40 % of DAU     |

**Example:** 10 M DAU × 8 % × 50 KB/session = **40 GB**

---

## 2. What lives in memory?

| Layer             | Typical size    |
|-------------------|-----------------|
| HTTP session      | 1–20 KB         |
| JWT / auth token  | < 1 KB          |
| User object cache | 5–50 KB         |
| Feed / timeline   | 50–500 KB       |
| Full page cache   | 100 KB – 2 MB   |

---

## 3. System memory breakdown

| Component          | Typical allocation                              |
|--------------------|-------------------------------------------------|
| App servers        | session working set + heap overhead (~30 %)     |
| Redis / Memcached  | hot data set + ~25 % fragmentation headroom     |
| Database buffers   | PostgreSQL: `shared_buffers` = 25 % of RAM      |
| OS + kernel        | always reserve ~512 MB – 2 GB                  |

---

## 4. Capacity planning rule of thumb

```
Total RAM needed = working_set × 2        ← 2× headroom for GC & spikes
Nodes needed     = ceil(total_RAM / node_RAM)
```

> Never run above **~70 % utilisation** in steady state.
> OOM kills happen fast — add nodes before you hit 80 %.

---

## 5. Eviction when memory is full

**LRU — Least Recently Used**
Evict the coldest session first. Good for uniform access patterns.

**LFU — Least Frequently Used**
Evict least-popular keys. Good for skewed / power-law access (hot keys).

**TTL-based**
Expire sessions after N minutes of inactivity. Simple, predictable — pairs well with LRU.

---

## 6. Scaling strategies

| Strategy             | Description                                                |
|----------------------|------------------------------------------------------------|
| Vertical scaling     | Bigger nodes — quick win, but has a ceiling.               |
| Horizontal scaling   | More nodes behind a consistent-hash ring.                  |
| Tiered caching       | Hot tier in RAM, warm tier on SSD, cold in DB.             |
| Data partitioning    | Shard sessions by user ID to avoid hot spots.              |

---

## 7. Interactive estimator

Use the graph in **Preview** mode to drag the sliders and instantly see
how session size, node count, and RAM per node affect capacity.
