---
label: "VII"
subtitle: "Application-level"
group: "System design"
order: 7
---
Application-level bottlenecks
Logic and **dependency patterns** limit scale even when infra looks healthy.

## 1. Synchronous blocking

| Pattern | Problem | Fix |
|---------|---------|-----|
| Thread blocked on DB/API | Pool exhaustion | async/await, reactive, virtual threads |
| Serial calls in handler | Latency sums | Parallel `asyncio.gather`, fork-join |

| Model | Examples |
|-------|----------|
| Event loop | Node.js, asyncio |
| Thread pool | JVM servlet pool |
| Goroutines + blocking IO | Go with limits |

## 2. Thundering herd

**Cache expires** → many concurrent **cache miss** → all hit DB.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="Thundering herd on cache expiry">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Thundering herd</text>
  <rect x="12" y="36" width="64" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="9">TTL expires</text>
  <path d="M76 50 H120" stroke="#f87171" stroke-width="1.5"/>
  <rect x="120" y="32" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="120" y="52" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="120" y="72" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="176" y="54" fill="#e4e4e7" font-size="8">N concurrent</text>
  <path d="M224 50 H268" stroke="#f87171" stroke-width="2"/>
  <rect x="268" y="44" width="56" height="32" rx="3" fill="rgba(248,113,113,0.25)" stroke="#f87171"/>
  <text x="276" y="64" fill="#e4e4e7" font-size="9">DB</text>
</svg></figure>

| Mitigation | How |
|------------|-----|
| **Lock on miss** | One refills cache; others wait |
| **Probabilistic early expiry** | Refresh before hard TTL |
| **Background refresh** | Serve stale; async warm |
| **Request coalescing** | Singleflight pattern |

## 3. Hot key / hot partition

| Example | Fix |
|---------|-----|
| Viral tweet id | Local in-process cache; read replicas |
| One Redis key | Shard key: `key#0`…`key#N` |
| One DB shard | Re-shard; celebrity fan-out read model |

## 4. Slow external dependency

| Pattern | Purpose |
|---------|---------|
| **Timeout** | Fail fast |
| **Retry + backoff + jitter** | Transient errors |
| **Circuit breaker** | Stop calling failing dep |
| **Bulkhead** | Isolate pool per dependency |
| **Fallback** | Cached/default response |

```text
Closed → failures ↑ → Open (fail fast) → Half-open probe → Closed
```

## 5. Code-level hotspots

| Smell | Fix |
|-------|-----|
| Serialize in tight loop | Batch; binary format |
| Regex compile per request | Compile once |
| String `+` in loop | `StringBuilder` / `join` |
| Unbounded cache map | TTL + max size |

**Always profile** — never optimise without measurement.

**Related:** scalable patterns rate limiting, distributed transactions (idempotency).
