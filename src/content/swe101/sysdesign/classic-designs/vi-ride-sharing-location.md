---
label: "VI"
subtitle: "Ride-sharing & location"
group: "System design"
order: 6
---
Ride-sharing and location services
**Uber / Lyft-style** matching: ingest **high-frequency GPS**, find **nearby drivers**, assign **ETA-ranked** rides.

## 1. Scale sketch

| Assumption | Rate |
|------------|------|
| 1 M active drivers | |
| GPS every 4 s | **250 K location writes/s** |

Writes dominate; reads are geospatial queries on hot regions.

## 2. Location ingestion

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="Driver GPS to Redis geo and Kafka analytics">
  <rect x="12" y="40" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="58" fill="#e4e4e7" font-size="9">Driver app</text>
  <path d="M68 54 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="40" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="58" fill="#e4e4e7" font-size="9">Redis GEO</text>
  <path d="M180 54 H220" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="220" y="40" width="64" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="228" y="58" fill="#e4e4e7" font-size="9">Kafka</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Dual write: hot index + analytics log</text>
  <text x="12" y="88" fill="#71717a" font-size="9">GEOADD driver_id lat lng · stream for history/replay</text>
</svg></figure>

| Store | Purpose |
|-------|---------|
| **Redis Geo** (`GEOADD`, `GEORADIUS`) | Live matching — O(log N) |
| **Kafka** | History, surge pricing, ML features |

## 3. Geospatial indexes

| Index | Idea | Used by |
|-------|------|---------|
| **Geohash** | Lat/lng → base32 string; prefix = nearby cells | Simple radius search |
| **S2 cells** | Hierarchical sphere tiling | Google, Uber |
| **Quadtree** | 2-D recursive split | Non-uniform density |
| **PostGIS** | SQL extensions | Smaller scale / admin |

**Geohash caveat:** edge cells need **neighbor** lookup — one hash cell ≠ perfect circle.

## 4. Matching flow

| Step | Action |
|------|--------|
| 1 | Rider request with pickup lat/lng |
| 2 | **GEORADIUS** (or S2 query) — drivers within R km, available status |
| 3 | Rank by **ETA** from route graph (not straight-line distance) |
| 4 | Offer to top driver; timeout → next candidate |
| 5 | Accept → trip state machine; share live location |

## 5. Trip state (simplified)

```text
REQUESTED → DRIVER_ASSIGNED → IN_PROGRESS → COMPLETED
                  ↓ timeout
              RE_OFFER
```

Use **idempotency** on accept to prevent double assignment.

## 6. Failure modes

| Issue | Mitigation |
|-------|------------|
| Stale driver location | Heartbeat; mark unavailable if no update |
| Thundering herd at bar close | Surge + queue requests |
| Split-brain assignment | Optimistic lock on driver status |

**Related:** Part I replication, scalable patterns rate limiting per region.
