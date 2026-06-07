---
label: "VII"
subtitle: "HA & disaster recovery"
group: "Cloud architecture"
order: 7
---
High availability & disaster recovery
Systems fail. **HA** minimizes downtime within a region; **DR** prepares for region-wide or major disasters. Define **RTO** and **RPO** before picking a strategy.

## 1. Key metrics

| Metric | Definition | Example |
|--------|------------|---------|
| **RTO** | Recovery **Time** Objective — max acceptable **downtime** | 4 hours |
| **RPO** | Recovery **Point** Objective — max acceptable **data loss** (time window) | 15 minutes |

```text
Failure at T0 ───────────────────────────▶ Service restored
              │◀──── RTO (downtime) ────▶│

Last good backup ──▶ Failure
              │◀──── RPO (data lost) ───▶│
```

Lower RTO/RPO → higher cost and complexity.

## 2. Failure scopes

| Scope | Mitigation |
|-------|------------|
| Single instance | Auto Scaling replacement, LB health checks |
| Single AZ | Multi-AZ deployment |
| Whole region | Multi-region DR |
| Operator error | Backups, IaC, change review |

## 3. Multi-AZ patterns

### Active-active (preferred for stateless tiers)

```text
        ┌── AZ-a: app instances ──┐
  ALB ──┤                         ├── all receive traffic
        └── AZ-b: app instances ──┘
```

Traffic load-balanced across AZs **at all times**.

### Active-passive (common for databases)

```text
RDS Primary (AZ-a) ──sync──▶ Standby (AZ-b)
         │
    failover on AZ-a failure → promote standby
```

Higher **RTO** than active-active app tier (~minutes for DB failover).

### Auto Scaling Group

- Replace unhealthy instances automatically.
- Spread across AZs via launch template.
- Pair with ALB health checks [Networking, VPC & LB](vi-networking-vpc-and-lb.md).

## 4. DR tiers (cheapest → lowest RTO)

| Tier | Description | RTO | RPO | Cost |
|------|-------------|-----|-----|------|
| **Backup & restore** | Periodic snapshots to S3; rebuild on disaster | Hours–days | Hours | $ |
| **Pilot light** | Minimal core (DB replica, AMIs) always on; scale up rest | Hours | Minutes–hours | $$ |
| **Warm standby** | Scaled-down full stack running; scale on failover | Minutes–hours | Minutes | $$$ |
| **Active-active multi-region** | Full capacity in 2+ regions | Seconds–minutes | Near zero | $$$$ |

```text
Backup & restore:     [snapshots in S3] ──on DR──▶ rebuild everything

Pilot light:          [DB replica] + [AMIs] ──on DR──▶ launch full fleet

Warm standby:         [small running env in DR region] ──scale up──▶

Active-active:        [Region A: 100%] + [Region B: 100%] via Route 53
```

## 5. Backup best practices

| Resource | Backup method |
|----------|---------------|
| RDS | Automated backups + manual snapshots |
| EBS | Snapshots |
| S3 | Versioning + cross-region replication |
| K8s | Velero, etcd backup (managed control plane handled) |
| IaC | Git is source of truth — rebuild env from Terraform |

**Test restores** — untested backups are wishful thinking.

## 6. Multi-region considerations

| Topic | Detail |
|-------|--------|
| **Replication** | Async cross-region — non-zero RPO |
| **DNS failover** | Route 53 health checks + failover routing |
| **Data sovereignty** | Some data cannot leave primary region |
| **Split brain** | Avoid dual-write without conflict resolution |

## 7. Example RTO/RPO targets

| Business | RTO | RPO | Strategy |
|----------|-----|-----|----------|
| Internal admin tool | 24 h | 24 h | Backup & restore |
| B2B SaaS | 4 h | 1 h | Warm standby |
| Payments API | 15 min | 1 min | Multi-AZ + cross-region replica |
| Global social app | 1 min | ~0 | Active-active multi-region |

## 8. Runbook essentials

| Step | Action |
|------|--------|
| 1 | Detect (monitoring, health checks) |
| 2 | Declare incident, assign commander |
| 3 | Failover DNS / promote standby |
| 4 | Verify SLO, communicate status |
| 5 | Post-incident review, fix root cause |

## 9. HA checklist

- [ ] App tier in **≥ 2 AZs** behind LB
- [ ] Database **Multi-AZ** or equivalent
- [ ] Health checks + auto replacement
- [ ] Backups with retention + **tested restore**
- [ ] DR strategy documented with RTO/RPO
- [ ] Runbook rehearsed annually

**Related:** [Regions, AZs & edge](iii-regions-azs-and-edge.md), patterns [Scalability & caching](../patterns-and-design/ii-scalability-and-caching.md), [Well-Architected Framework](viii-well-architected-framework.md).
