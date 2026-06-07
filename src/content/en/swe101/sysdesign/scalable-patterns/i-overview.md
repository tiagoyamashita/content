---
label: "I"
subtitle: "Overview"
group: "System design"
order: 1
---
Scalable patterns — overview
Patterns for **APIs**, **async messaging**, **rate limiting**, **search**, **CDN**, **distributed transactions**, and **observability** — the layer above core building blocks (caching, DBs, replication in **Part I**).

## Map of this submenu

| Note | Topic | Core question |
|------|--------|---------------|
| [API design](ii-api-design.md) | REST, gRPC, GraphQL | How do clients talk to services at scale? |
| [Message queues & async](iii-message-queues-and-async.md) | Queues, pub/sub, outbox | How do you decouple and absorb spikes? |
| [Rate limiting](iv-rate-limiting.md) | Token bucket, sliding window | How do you protect backends from overload? |
| [Search systems](v-search-systems.md) | Inverted index, CDC, vectors | How do you serve fast full-text and semantic search? |
| [CDN & edge caching](vi-cdn-and-edge-caching.md) | CDN, cache invalidation | How do you serve static and cacheable content globally? |
| [Distributed transactions](vii-distributed-transactions.md) | Saga, 2PC, idempotency | How do you coordinate writes across services? |
| [Observability at scale](viii-observability-at-scale.md) | SLOs, tracing, chaos | How do you know when scale breaks something? |

## Where these sit in a typical architecture

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" role="img" aria-label="Client through CDN API gateway services queue search and databases">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Request path (simplified)</text>
  <rect x="12" y="36" width="64" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="56" fill="#e4e4e7" font-size="9">Client</text>
  <rect x="88" y="36" width="56" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="98" y="56" fill="#e4e4e7" font-size="9">CDN</text>
  <rect x="156" y="36" width="72" height="32" rx="3" fill="rgba(244,114,182,0.12)" stroke="#f472b6"/>
  <text x="164" y="56" fill="#e4e4e7" font-size="9">API / GW</text>
  <rect x="240" y="36" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="252" y="56" fill="#e4e4e7" font-size="9">Service</text>
  <rect x="316" y="36" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="324" y="56" fill="#e4e4e7" font-size="9">Queue</text>
  <rect x="384" y="36" width="56" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="388" y="56" fill="#e4e4e7" font-size="9">Search</text>
  <rect x="452" y="36" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="460" y="56" fill="#e4e4e7" font-size="9">DB</text>
  <path d="M76 52 H88" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M144 52 H156" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M228 52 H240" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M304 52 H316" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M372 52 H384" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M440 52 H452" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="12" y="92" fill="#71717a" font-size="10">Rate limiting usually sits at API gateway. Async work fans out via queue. Search index syncs from DB (CDC).</text>
  <text x="12" y="120" fill="#d4d4d8" font-size="10" font-weight="600">Study order</text>
  <text x="12" y="138" fill="#a1a1aa" font-size="9">Part I → this submenu → Classic designs submenu → bottleneck analysis</text>
</svg></figure>

## Rehearsal questions

- Cursor vs offset pagination — when does each break?
- Transactional outbox — why not dual-write to DB and broker?
- Token bucket vs leaky bucket — burst behavior?
- Inverted index vs relational table scan?
- Saga choreography vs orchestration?
- Alert on symptoms vs causes — example?
