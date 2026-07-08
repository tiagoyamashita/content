---
label: "III"
subtitle: "CPU & memory"
group: "System design"
order: 3
---
CPU and memory bottlenecks
Compute and RAM limits show up as **latency scaling with load**, **OOM**, and **GC pauses**.

## 1. CPU — signals

| Signal | Tool / indicator |
|--------|------------------|
| Sustained **> 80%** all cores | `top`, cloud metrics |
| Run queue **r > # CPUs** | `vmstat` |
| Latency ∝ load (no headroom) | APM p99 vs QPS |

## 2. CPU — causes and fixes

| Cause | Fix |
|-------|-----|
| O(n²) algorithm | Profile (pprof, perf, py-spy); better algorithm |
| **GIL** / global lock (Python) | Multiprocess, async I/O, Rust/Go for hot path |
| JSON encode/decode at high QPS | Protobuf, msgpack; cache parsed objects |
| Thread/goroutine explosion | Bounded worker pool; async I/O vs thread-per-request |
| Regex compile per request | Pre-compile; reuse |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 80" role="img" aria-label="Profile before optimize CPU hot path">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Profiler-driven fixes only</text>
  <text x="12" y="40" fill="#86efac" font-size="9">measure → flame graph → fix top 1–2 frames → re-measure</text>
  <text x="12" y="58" fill="#f87171" font-size="9">avoid optimising cold paths</text>
</svg></figure>

## 3. Memory — signals

| Signal | Meaning |
|--------|---------|
| **OOM kill** | Process exceeded cgroup limit |
| **Swap > 0** | RAM exhausted — disk-speed RAM |
| **GC pause spikes** | JVM / Go stop-the-world |
| Redis **evicted_keys** ↑ | Cache too large for RAM |

## 4. Memory — causes and fixes

| Cause | Fix |
|-------|-----|
| Memory leak | Heap profiler; fix lifecycle / listeners |
| Over-caching | TTL, maxmemory policy, smaller values |
| Large copies | Pointers, streaming, zero-copy where possible |
| Allocation churn | Object pools; reduce short-lived allocations |
| JVM heap too small/large | Tune `-Xmx`; G1/ZGC for latency |

## 5. CPU vs memory interaction

| Pattern | Symptom |
|---------|---------|
| CPU-bound + low memory | Scale out CPU instances |
| Memory-bound + low CPU | Larger RAM; cache tier; leak fix |
| GC thrashing | High CPU + high alloc rate — reduce allocations first |

## 6. Quick checklist

- [ ] Flame graph on hottest endpoint
- [ ] Heap dump if RSS grows unbounded
- [ ] Compare p99 before/after one change
- [ ] Load test at 2× expected peak

**Related:** [Identifying bottlenecks](ii-identifying-bottlenecks.md), application hot keys [Application-level](vii-application-level.md).
