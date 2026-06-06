---
label: "III"
subtitle: "Regions, AZs & edge"
group: "Cloud architecture"
order: 3
---
Regions, AZs & edge
Cloud capacity is organized **geographically**. Design choices here affect **latency**, **compliance**, and **fault tolerance**.

## 1. Region

A **region** is an independent geographic area (e.g. `us-east-1`, `eu-west-1`, `ap-southeast-1`).

| Property | Detail |
|----------|--------|
| Isolation | Resources in one region do **not** auto-replicate to another |
| Latency | Choose region close to users |
| Compliance | Data residency (GDPR — EU region) |
| Services | Not every service exists in every region |

```text
AWS (example)
  us-east-1 (N. Virginia)
  eu-west-1 (Ireland)
  ap-northeast-1 (Tokyo)
```

## 2. Availability Zone (AZ)

An **AZ** is one or more physically separate data centers within a region, linked by **low-latency private fiber**.

```text
Region: eu-west-1
  ├── eu-west-1a   (datacenter campus A)
  ├── eu-west-1b   (datacenter campus B)
  └── eu-west-1c   (datacenter campus C)
```

| Rule | Why |
|------|-----|
| Deploy across **≥ 2 AZs** | Survive single DC failure |
| Same region, different AZ | Low latency, synchronous options |
| Don't assume AZ names match across accounts | `1a` in account A ≠ same building as `1a` in account B |

## 3. Mental model diagram

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 110" role="img" aria-label="Region with three AZs">
  <rect x="12" y="24" width="376" height="72" rx="4" fill="none" stroke="#52525b"/>
  <text x="20" y="40" fill="#d4d4d8" font-size="10" font-weight="600">Region (eu-west-1)</text>
  <rect x="28" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="52" y="72" fill="#e4e4e7" font-size="9">AZ-a</text>
  <rect x="152" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="176" y="72" fill="#e4e4e7" font-size="9">AZ-b</text>
  <rect x="276" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="300" y="72" fill="#e4e4e7" font-size="9">AZ-c</text>
  <text x="12" y="108" fill="#71717a" font-size="9">Load balancer spans AZs · RDS Multi-AZ standby in another AZ</text>
</svg></figure>

## 4. Edge / PoP (Point of Presence)

**CDN edge nodes** cache content close to users — not full regions, but globally distributed (100s of locations).

| Service | Provider |
|---------|----------|
| CloudFront | AWS |
| Azure CDN / Front Door | Azure |
| Cloud CDN | GCP |
| Cloudflare | Multi-cloud edge |

**Use for:** static assets (JS, CSS, images), cacheable API GET responses, TLS termination at edge.

## 5. Multi-region vs multi-AZ

| | Multi-AZ | Multi-region |
|---|----------|--------------|
| Protects against | Single DC failure | Entire region outage |
| Latency | Same region (~1–2 ms between AZs) | Cross-region higher |
| Complexity | Standard HA | DNS failover, replication lag |
| Cost | Moderate | Higher (duplicate infra + transfer) |

Start with **multi-AZ**; add **multi-region** when RTO/RPO or compliance requires it [HA & disaster recovery](vii-ha-and-disaster-recovery.md).

## 6. Data residency example

| Requirement | Design |
|-------------|--------|
| EU personal data stays in EU | Deploy in `eu-west-1`, restrict replication |
| Global product, local compliance | Per-region stacks + geo-routing |
| DR in second region | Async replication — understand RPO |

## 7. Local Zones and Wavelength (AWS context)

| Extension | Purpose |
|-----------|---------|
| **Local Zone** | Extension of region — ultra-low latency to city |
| **Wavelength** | 5G edge — mobile/game latency |

Specialized — use when milliseconds matter to specific metro.

## 8. Choosing a region checklist

- [ ] Latency to primary users
- [ ] Required services available
- [ ] Legal / data residency
- [ ] Pricing (varies by region)
- [ ] DR region paired or chosen explicitly

**Related:** [Networking, VPC & LB](vi-networking-vpc-and-lb.md), [HA & disaster recovery](vii-ha-and-disaster-recovery.md), patterns **CDN** note.
