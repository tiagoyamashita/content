---
label: "II"
subtitle: "Identifying bottlenecks"
group: "System design"
order: 2
---
Identifying bottlenecks
Find the **one resource** limiting throughput before optimizing random layers.

## 1. Definition

**Bottleneck** = component at **~100% utilisation** while others have headroom — adding capacity elsewhere does not raise system throughput until this resource is relieved.

## 2. Little's Law

```text
L = λ × W

L = average requests in system (queue + in-flight)
λ = arrival rate (requests/s)
W = average time in system (seconds)
```

| Observation | Meaning |
|-------------|---------|
| **W** rises at constant **λ** | Backing up — queue growing |
| **L** rises | Latency or concurrency increasing |
| Fixed capacity, higher **λ** | Eventually **W** explodes |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 90" role="img" aria-label="Queue grows when service time exceeds capacity">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Saturation → queue</text>
  <rect x="12" y="32" width="120" height="20" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="24" y="46" fill="#e4e4e7" font-size="8">waiting requests ↑</text>
  <rect x="140" y="32" width="80" height="20" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="152" y="46" fill="#e4e4e7" font-size="8">processing</text>
  <text x="12" y="72" fill="#71717a" font-size="9">λ &gt; service capacity → W and L grow without bound</text>
</svg></figure>

## 3. Universal Scalability Law (USL)

```text
X(N) = N / (1 + α(N−1) + βN(N−1))
```

| Term | Meaning |
|------|---------|
| **α** | Contention — serial sections (locks, single writer) |
| **β** | Coherency — cache invalidation, gossip cost |
| **N** | Workers / nodes |

Even “perfect” horizontal scale hits **Amdahl** limits from serial fractions.

## 4. Systematic hunt (5 steps)

| Step | Action |
|------|--------|
| 1 | Define hurting metric: latency, throughput, errors |
| 2 | **End-to-end profile** — APM trace, span waterfall |
| 3 | Check **utilisation**: CPU, memory, disk, network, DB |
| 4 | Resource nearest **100%** sustained → likely bottleneck |
| 5 | Fix → **re-measure** — next bottleneck surfaces |

## 5. USE method (infrastructure)

For **each resource** (CPU, disk, NIC, DB connections):

| Letter | Question |
|--------|----------|
| **U** — Utilisation | % busy (e.g. CPU > 70% sustained = warning) |
| **S** — Saturation | Queue depth, wait time > 0? |
| **E** — Errors | Retries, timeouts, dropped packets |

## 6. RED method (services)

| Letter | Metric |
|--------|--------|
| **R** — Rate | Requests per second |
| **E** — Errors | Error rate |
| **D** — Duration | Latency distribution (p50/p95/p99) |

**Combine:** USE on infra + RED on each service boundary.

## 7. Trace-first workflow

```text
Slow request → trace_id → waterfall → longest span → USE/RED on that hop
```

| Span type | Next drill |
|-----------|------------|
| DB query | [Database](vi-database.md) |
| HTTP client | [Network](v-network.md), [Application-level](vii-application-level.md) |
| CPU-bound compute | [CPU & memory](iii-cpu-and-memory.md) |

**Related:** [Elimination playbook](viii-elimination-playbook.md), scalable patterns observability.
