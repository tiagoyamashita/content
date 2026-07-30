---
label: "I"
subtitle: "Overview"
group: "System design"
order: 1
---
Bottleneck analysis — overview
A **bottleneck** is the resource whose **saturation** caps overall throughput. Relieve one and the limit often **moves** — systematic measurement beats guessing.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Identifying bottlenecks](ii-identifying-bottlenecks.md) | Little's Law, USL, USE, RED, finding the limiter |
| [CPU & memory](iii-cpu-and-memory.md) | CPU, GC, leaks, caching pressure |
| [I/O & storage](iv-io-and-storage.md) | Disk, SSD, object storage, WAL |
| [Network](v-network.md) | Bandwidth, latency, connections, mesh |
| [Database](vi-database.md) | Reads, writes, pools, indexes |
| [Application-level](vii-application-level.md) | Thundering herd, hot keys, circuit breakers |
| [Elimination playbook](viii-elimination-playbook.md) | Measure → isolate → fix → validate → prevent |

## The whack-a-mole mental model

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Bottleneck moves after each fix">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Throughput limited by one resource at a time</text>
  <rect x="12" y="36" width="72" height="24" rx="3" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="24" y="52" fill="#e4e4e7" font-size="8">DB 100%</text>
  <text x="96" y="52" fill="#a1a1aa" font-size="9">→ add cache</text>
  <rect x="160" y="36" width="72" height="24" rx="3" fill="rgba(251,191,36,0.2)" stroke="#fbbf24"/>
  <text x="172" y="52" fill="#e4e4e7" font-size="8">Redis hot</text>
  <text x="244" y="52" fill="#a1a1aa" font-size="9">→ shard key</text>
  <rect x="308" y="36" width="72" height="24" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="320" y="52" fill="#e4e4e7" font-size="8">CPU 95%</text>
  <text x="12" y="84" fill="#71717a" font-size="9">Profile end-to-end; fix highest-impact constraint; repeat.</text>
</svg></figure>

## Rehearsal questions

- State **Little's Law** — what rises when **W** rises at fixed **λ**?
- **USE** vs **RED** — infrastructure vs service?
- Thundering herd — two mitigations?
- Connection pool exhaustion — role of **PgBouncer**?
- Five phases of the elimination playbook?
