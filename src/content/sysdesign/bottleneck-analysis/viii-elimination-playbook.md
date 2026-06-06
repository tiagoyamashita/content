---
label: "VIII"
subtitle: "Elimination playbook"
group: "System design"
order: 8
---
Bottleneck elimination playbook
Repeatable process for **incidents** and **design reviews** — measure first, fix in **impact order**, validate, prevent recurrence.

## 1. Five phases

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="Five phase bottleneck playbook cycle">
  <rect x="12" y="40" width="72" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="28" y="58" fill="#e4e4e7" font-size="8">1 Measure</text>
  <path d="M84 54 H108" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="108" y="40" width="72" height="28" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="124" y="58" fill="#e4e4e7" font-size="8">2 Isolate</text>
  <path d="M180 54 H204" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="204" y="40" width="56" height="28" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="214" y="58" fill="#e4e4e7" font-size="8">3 Fix</text>
  <path d="M260 54 H284" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="284" y="40" width="72" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="296" y="58" fill="#e4e4e7" font-size="8">4 Validate</text>
  <path d="M356 54 H380" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="380" y="40" width="72" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="392" y="58" fill="#e4e4e7" font-size="8">5 Prevent</text>
</svg></figure>

### Phase 1 — Measure, don't guess

| Collect | Tools |
|---------|-------|
| p50 / p95 / p99 latency | APM, Prometheus |
| Throughput, error rate | RED dashboards |
| Per-resource USE | CPU, disk, NIC, DB |
| Trace waterfall | Jaeger, Tempo, X-Ray |

### Phase 2 — Isolate

| Question | Narrows cause |
|----------|---------------|
| One endpoint or all? | Route-specific bug vs shared infra |
| Correlated with deploy / cron / spike? | Change vs load |
| One AZ, shard, host? | Localised failure |

### Phase 3 — Fix by impact / cost

| Priority | Tactic | Cost |
|----------|--------|------|
| 1 | Query + index optimisation | Low |
| 2 | Cache layer, TTL tuning | Low–medium |
| 3 | Async / queue off hot path | Medium |
| 4 | Scale out instances | Medium |
| 5 | Sharding / partitioning | High |
| 6 | Architecture rewrite | Very high |

### Phase 4 — Validate

- Load test (**k6**, Locust, Gatling) before vs after
- Watch **p99** and **error budget** post-deploy
- Canary / gradual rollout

### Phase 5 — Prevent

| Action | |
|--------|---|
| Alert on symptom that caught incident | |
| Load test in CI/CD for regression | |
| Runbook: symptom → cause → fix | |
| Post-incident review (blameless) | |

## 2. Runbook snippet template

```markdown
## Alert: High p99 on POST /orders
- Dashboard: [link]
- Likely: DB lock wait, pool exhaustion, downstream payment timeout
- Steps: 1) trace sample 2) pg_stat_activity 3) pool metrics
- Mitigation: scale pooler, disable non-critical job, circuit-break payment
- Escalation: DBA on-call
```

## 3. Interview answer shape

1. **Metric** hurting (p99 latency)
2. **Trace** → DB span 800 ms
3. **EXPLAIN** → seq scan → add index
4. **Validate** with load test
5. **Prevent** — slow query log alert

**Related:** [Identifying bottlenecks](ii-identifying-bottlenecks.md), scalable patterns observability, SRE tooling.
