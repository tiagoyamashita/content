---
label: "VIII"
subtitle: "Well-Architected Framework"
group: "Cloud architecture"
order: 8
---
Well-Architected Framework
AWS **Well-Architected Framework** (applies conceptually to Azure/GCP too) defines **six pillars** for reviewing workloads. Use it in design reviews and post-incident retrospectives.

## 1. Pillars overview

| # | Pillar | Question it answers |
|---|--------|---------------------|
| 1 | **Operational Excellence** | Can we run and improve the system? |
| 2 | **Security** | Is data and infrastructure protected? |
| 3 | **Reliability** | Does it recover from failure and meet demand? |
| 4 | **Performance Efficiency** | Are we using resources well? |
| 5 | **Cost Optimization** | Are we avoiding waste? |
| 6 | **Sustainability** | Are we minimizing environmental impact? |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 100" role="img" aria-label="Six Well-Architected pillars">
  <text x="12" y="18" fill="#d4d4d8" font-size="11" font-weight="600">Six pillars — no single pillar wins alone</text>
  <rect x="12" y="32" width="52" height="22" rx="2" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="16" y="47" fill="#e4e4e7" font-size="7">Ops</text>
  <rect x="70" y="32" width="52" height="22" rx="2" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="74" y="47" fill="#e4e4e7" font-size="7">Security</text>
  <rect x="128" y="32" width="52" height="22" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="132" y="47" fill="#e4e4e7" font-size="7">Reliable</text>
  <rect x="186" y="32" width="52" height="22" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="190" y="47" fill="#e4e4e7" font-size="7">Perf</text>
  <rect x="244" y="32" width="52" height="22" rx="2" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="248" y="47" fill="#e4e4e7" font-size="7">Cost</text>
  <rect x="302" y="32" width="52" height="22" rx="2" fill="rgba(45,212,191,0.12)" stroke="#2dd4bf"/>
  <text x="306" y="47" fill="#e4e4e7" font-size="7">Sustain</text>
  <text x="12" y="78" fill="#71717a" font-size="9">Trade-offs: stricter security may add latency; higher availability adds cost</text>
</svg></figure>

## 2. Operational Excellence

Run and monitor systems; continuously improve.

| Practice | Cloud example |
|----------|---------------|
| **Infrastructure as Code** | Terraform, CloudFormation |
| **Small reversible changes** | Feature flags, blue/green deploy |
| **Runbooks** | DR failover steps documented |
| **Observability** | Logs, metrics, traces, alarms |

```text
Change → CI/CD → automated test → staged deploy → monitor → rollback if SLO burn
```

**Anti-pattern:** Manual console changes with no audit trail.

## 3. Security

Protect information, systems, and assets.

| Practice | Cloud example |
|----------|---------------|
| **Least privilege IAM** | Role per workload, no wildcards |
| **Encryption** | TLS in transit, KMS at rest |
| **Audit** | CloudTrail, Config, GuardDuty |
| **Network isolation** | Private subnets, security groups |

See patterns `vii-cost-and-governance.md` for IAM/SCP detail.

## 4. Reliability

Recover from failures and meet demand.

| Practice | Cloud example |
|----------|---------------|
| **Multi-AZ** | ASG + ALB across AZs |
| **Auto scaling** | Target tracking on CPU/RPS |
| **Health checks** | LB + Route 53 |
| **Graceful degradation** | Circuit breakers, cached fallbacks |

Foundations: `vii-ha-and-disaster-recovery.md`. Patterns: event-driven, circuit breakers.

## 5. Performance Efficiency

Use computing resources efficiently as demand changes.

| Practice | Cloud example |
|----------|---------------|
| **Right-sizing** | Compute Optimizer recommendations |
| **Managed services** | RDS vs self-managed Postgres on EC2 |
| **Caching** | CloudFront, Redis |
| **Benchmark** | Load test before launch |

| Review | Question |
|--------|----------|
| Wrong instance family | CPU-bound on memory-optimized? |
| Missing CDN | Static assets hitting origin? |
| Sync where async fits | Queue decoupling |

## 6. Cost Optimization

Avoid unnecessary spend while meeting requirements.

| Practice | Cloud example |
|----------|---------------|
| **Reserved / Savings Plans** | Steady baseline capacity |
| **Spot** | Batch, fault-tolerant workers |
| **Auto scaling in** | Remove idle capacity |
| **Tagging & budgets** | Cost allocation by team |

Full detail: patterns `vii-cost-and-governance.md`.

## 7. Sustainability

Minimize environmental impact of cloud workloads.

| Practice | Effect |
|----------|--------|
| **Right-size** | Less wasted CPU cycles |
| **Higher utilization** | Fewer physical servers overall |
| **Managed services** | Provider optimizes hardware efficiency |
| **Graviton / ARM instances** | Better perf/watt for compatible apps |
| **Delete idle resources** | No ghost EC2 or unattached EBS |

Often aligns with **cost** optimization — efficient usually means greener.

## 8. Well-Architected Review (WAR)

Structured questionnaire per pillar — run:

- Before major launch
- After serious incident
- Annually for critical workloads

Output: **HRIs** (high-risk issues) prioritized for remediation.

## 9. Pillar trade-offs

| Tension | Balance |
|---------|---------|
| Security vs performance | mTLS adds latency — worth it for east-west |
| Reliability vs cost | Multi-region doubles infra — need business case |
| Speed vs ops excellence | Automate even under deadline pressure |
| Cost vs reliability | Spot for batch, on-demand for critical path |

## 10. Map pillars to this track

| Pillar | Foundations note | Patterns note |
|--------|------------------|---------------|
| Ops | `vii-ha-and-disaster-recovery.md` | observability, CI/CD |
| Security | `vi-networking-vpc-and-lb.md` | governance |
| Reliability | multi-AZ, DR | scaling, circuit breakers |
| Performance | compute, storage | caching |
| Cost | — | FinOps |
| Sustainability | right-size compute | utilization |

## 11. Rehearsal answers

- **Six pillars** — Ops, Security, Reliability, Performance, Cost, Sustainability.
- **Reliability vs HA** — reliability is pillar; HA is multi-AZ technique.
- **IaC** — supports Ops + Security (reviewable changes).

**Related:** `i-overview.md`, **Patterns & design** submenu, CI/CD Terraform submenu.
