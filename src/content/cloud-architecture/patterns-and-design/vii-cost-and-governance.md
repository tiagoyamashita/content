---
label: "VII"
subtitle: "Cost & governance"
group: "Cloud architecture"
order: 7
---
Cost & governance
Cloud bills scale with usage. **FinOps** aligns engineering and finance; **governance** enforces guardrails so speed does not become sprawl.

## 1. Pricing models

| Model | Commitment | Discount | Best for |
|-------|------------|----------|----------|
| **On-Demand** | None | 0% (baseline) | Spiky, unpredictable, dev/test |
| **Reserved / Savings Plans** | 1–3 years | 30–70% | Steady-state prod workloads |
| **Spot / Preemptible** | Can be reclaimed | Up to ~90% | Batch, ML training, stateless workers |
| **Committed use (GCP)** | 1–3 yr | Similar to RIs | Stable compute |

```text
On-Demand:  $$$$  full flexibility
Reserved:   $$    predictable baseline capacity
Spot:       $     interruptible — checkpoint & retry
```

## 2. When to use Spot instances

| Good fit | Bad fit |
|----------|---------|
| Kubernetes batch jobs with retry | Single-node stateful DB |
| Video transcoding queue | Long single-thread job with no checkpoint |
| CI build agents | Monolithic app with no redundancy |
| Flink / Spark workers | Legacy app that cannot tolerate kill |

**Pattern:** Spot fleet + on-demand baseline; on Spot interruption, work returns to queue.

## 3. FinOps practices

| Practice | Action |
|----------|--------|
| **Tagging** | `team`, `env`, `project`, `cost-center` on every resource |
| **Budgets & alerts** | Alert at 80% of monthly budget |
| **Right-sizing** | Compare CloudWatch CPU/RAM vs instance size |
| **Idle cleanup** | Detached EBS, old snapshots, unused ELBs, idle NAT Gateway |
| **Storage tiering** | S3 Standard → IA → Glacier for cold data |
| **Showback/chargeback** | Monthly report per team tag |

```text
Required tags (example policy):
  Environment: dev | staging | prod
  Owner: team-payments
  Application: checkout-api
```

Untagged resources → deny at deploy (policy) or auto-remind.

## 4. Cost optimization by service

| Service | Tip |
|---------|-----|
| **EC2 / VM** | Reserved for baseline; Spot for burst |
| **RDS** | Right-size; stop dev instances nights/weekends |
| **S3** | Lifecycle rules; delete incomplete multipart uploads |
| **NAT Gateway** | Expensive — VPC endpoints for S3/DynamoDB |
| **Data transfer** | Same-region; CDN for egress-heavy content |
| **Lambda** | Right-size memory (affects CPU and cost) |

## 5. Governance hierarchy

```text
Organization (AWS Org / Azure MG)
  ├── SCP / Policy — deny root login, restrict regions
  ├── Account: production
  ├── Account: staging
  └── Account: sandbox
        └── IAM roles per workload (least privilege)
```

| Mechanism | Purpose |
|-----------|---------|
| **AWS Organizations / Azure Management Groups** | Multi-account structure |
| **SCP / Azure Policy** | Guardrails even for admins |
| **IAM / RBAC** | Least privilege per role |
| **CloudTrail / Activity Log** | Immutable API audit |
| **Config / Policy compliance** | Detect public S3 buckets |

## 6. IAM least privilege

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::myapp-uploads-prod/user-uploads/*"
}
```

| Avoid | Prefer |
|-------|--------|
| `"Action": "*"` | Scoped actions |
| `"Resource": "*"` | Resource ARN prefix |
| Long-lived access keys | IAM roles, OIDC for CI |
| Shared root credentials | SSO + assumed roles |

## 7. Policy examples

**Deny unencrypted S3 upload:**

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "AES256"
    }
  }
}
```

**Restrict regions (SCP):**

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["us-east-1", "eu-west-1"]
    }
  }
}
```

## 8. Well-Architected cost pillar (summary)

| Review question | Action |
|-----------------|--------|
| Do we know top 5 cost drivers? | Cost Explorer / billing export |
| Are dev resources shut down off-hours? | Lambda scheduler, Instance Scheduler |
| Are we paying for unused capacity? | Trusted Advisor, Compute Optimizer |
| Is architecture using managed services? | Less ops, often better $/value |

## 9. Anti-patterns

| Anti-pattern | Cost impact |
|--------------|-------------|
| Always on-demand prod at scale | 30–50% overspend vs reserved |
| No tags | Cannot allocate or optimize |
| Oversized "just in case" instances | 2× spend with 10% CPU |
| NAT Gateway per private subnet | High fixed hourly + data processing |

## 10. Rehearsal answers

- **Spot** — cheap spare capacity; can be reclaimed; needs fault-tolerant workload.
- **SLI/SLO** — see [Observability, SLI & SLO](vi-observability-slo-and-slis.md); SLA adds customer contract.
- **SCP** — organization-level deny that applies even to account admins.
- **Stateless + auto scaling** — see [Scalability & caching](ii-scalability-and-caching.md).

**Related:** **Foundations** submenu → [Well-Architected Framework](../foundations/viii-well-architected-framework.md), CI/CD Terraform for IaC guardrails.
