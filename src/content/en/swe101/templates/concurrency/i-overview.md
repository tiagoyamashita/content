---
label: "I"
subtitle: "Overview"
group: "Concurrency"
order: 1
---
Concurrency — overview
A REST server handles **many requests at once**. How each stack achieves that differs — OS threads, async event loops, goroutines — but the senior concerns are the same: don't block the request pipeline, don't share mutable state unsafely, and don't exhaust your pools.

Pairs with [Resilience](../resilience/i-overview.md) (timeouts/bulkheads), [HTTP clients](../http-clients/i-overview.md) (outbound fan-out), and [Transactions](../transactions/i-overview.md) (consistency under parallel writes).

## Concurrency models per stack

Same goal — serve concurrent requests — very different runtime.

| Stack | Model | A request runs on | Blocking cost |
|-------|-------|-------------------|---------------|
| **Spring MVC** | Thread-per-request | An OS thread from a pool (Tomcat) | Blocks a whole thread — pool can exhaust |
| **Spring WebFlux** | Event loop (Reactor) | A few event-loop threads | Blocking a loop thread stalls many requests |
| **FastAPI / asyncio** | Single-threaded event loop | The loop (`async def`) | A blocking call freezes the loop — offload it |
| **Express / Node** | Single-threaded event loop | The loop | CPU-bound work blocks everyone |
| **Go net/http** | Goroutine-per-request | A cheap goroutine (M:N scheduler) | Cheap, but shared state still needs locks |

**Mnemonic:** threads (Spring MVC, Go) can block one worker; event loops (Node, asyncio, WebFlux) must **never** block — offload CPU/blocking work.

```mermaid
flowchart TB
  subgraph ThreadPool[Thread-per-request: Spring MVC, Go]
    R1[Req] --> W1[Worker/goroutine]
    R2[Req] --> W2[Worker/goroutine]
  end
  subgraph EventLoop[Event loop: Node, asyncio, WebFlux]
    R3[Req] --> L[Single loop]
    R4[Req] --> L
    L -->|blocking work| Off[Offload: worker pool / executor]
  end
```

## Where concurrency bites

| Hazard | Symptom | Fix |
|--------|---------|-----|
| **Shared mutable state** | Race conditions, corrupted data | Immutability, locks, atomics, per-request scope |
| **Blocking the event loop** | Whole service latency spikes | `async` I/O, or offload to a worker/executor |
| **Thread/connection pool exhaustion** | Requests queue, then time out | Bound pools, timeouts, bulkheads |
| **Unbounded fan-out** | One request spawns 1000 tasks | Cap parallelism (semaphore / worker limit) |
| **Deadlock** | Requests hang forever | Consistent lock ordering; avoid nested locks |
| **Lost updates** | Two writers overwrite each other | DB transactions + optimistic/pessimistic locking |

## Golden rules

1. **Stateless handlers.** Keep per-request data on the stack / request scope — not in shared singletons.
2. **Never block an event loop.** In Node/asyncio, wrap CPU/blocking work in a worker thread/executor.
3. **Bound everything.** Thread pools, connection pools, and fan-out parallelism all need explicit limits.
4. **Make shared state safe.** Prefer immutable data; otherwise use the stack's concurrency primitives (locks, atomics, channels).
5. **Push consistency to the DB.** For concurrent writes, rely on [Transactions](../transactions/i-overview.md) and row locks — not in-memory guards.

## Capacity model per stack

"How many concurrent requests can one instance hold?" has a different answer — and a different **bottleneck** — per stack.

| Stack | Concurrency unit | Rough cost each | Usual capacity ceiling |
|-------|------------------|-----------------|------------------------|
| **Spring MVC (platform threads)** | OS thread | ~1 MB stack + scheduler | Thread pool size (Tomcat default **200**) → memory-bound in the low thousands |
| **Spring MVC (virtual threads)** | Virtual thread | ~hundreds of bytes | Downstream/DB pool + heap → hundreds of thousands |
| **Spring WebFlux** | Reactor subscription | Tiny (few loop threads) | CPU + downstream limits, not thread count |
| **FastAPI / asyncio** | Coroutine on 1 loop | Tiny | 1 CPU core per process → scale with workers |
| **Express / Node** | Callback on 1 loop | Tiny | 1 CPU core per process → scale with cluster/instances |
| **Go net/http** | Goroutine | ~2–8 KB stack | Memory + FDs + downstream → hundreds of thousands |

**Key point:** event-loop runtimes (asyncio, Node) use **one CPU core per process**, so horizontal capacity = **processes × loop concurrency**. Thread/goroutine runtimes (Spring, Go) can use many cores in one process but hit **pool, memory, or file-descriptor** ceilings.

## Capacity changes by language / runtime version

The concurrency ceiling has shifted a lot recently — always state the **minimum version** your capacity assumptions need.

| Runtime | Version that changes capacity | What changed |
|---------|-------------------------------|--------------|
| **Java** | **21 LTS** (Spring Boot **3.2+**) | Virtual threads GA — blocking I/O stops being thread-bound; `spring.threads.virtual.enabled=true` |
| **Python** | **3.12** / **3.13** | 3.12 sub-interpreters (PEP 684); 3.13 experimental **free-threaded** (no-GIL) build — until then threads don't add CPU parallelism |
| **Node** | **12+** / **18+** | `worker_threads` stable (12); global `fetch` + `AbortSignal.timeout` (18) for bounded outbound work |
| **Go** | **1.22** / **1.25** | 1.22 fixed loop-variable capture (safer goroutines in loops); 1.25 makes `GOMAXPROCS` **container-CPU-aware** |

Each stack page has a **Capacity by version** section with the concrete knobs and the math.

## Parallel outbound calls (common need)

Fetching several upstreams for one response? Do it **in parallel with a bounded limit and a timeout** — see each stack page. This is where concurrency and [Resilience](../resilience/i-overview.md) meet.

## Language templates

| Note | Stack |
|------|--------|
| [Java — Spring](ii-java-spring.md) | Thread pools, `@Async`, `CompletableFuture`, `synchronized`/atomics |
| [Python — FastAPI](iii-python-fastapi.md) | `async`/`await`, `asyncio.gather`, `run_in_executor`, semaphore |
| [JavaScript — Express](iv-javascript-express.md) | Event loop, `Promise.all`, `worker_threads`, concurrency cap |
| [Go — net/http](v-go-nethttp.md) | Goroutines, `sync.WaitGroup`, `errgroup`, mutex, channels |

## Notes

| Topic | Practice |
|-------|----------|
| **Don't hand-roll** | Prefer the platform's executor/pool over raw threads |
| **Always timeout** | Parallel work needs a deadline — pair with [Resilience](../resilience/i-overview.md) |
| **Test under load** | Races hide until concurrency is high — load/stress test |
| **Measure** | Track pool saturation and queue depth — see [Observability](../observability/i-overview.md) |

## Next

Pick your stack — start with [Java — Spring](ii-java-spring.md) or [Go — net/http](v-go-nethttp.md).
