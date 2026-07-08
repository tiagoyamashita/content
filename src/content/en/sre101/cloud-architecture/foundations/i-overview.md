---
label: "I"
subtitle: "Overview"
group: "Cloud architecture"
order: 1
---
Foundations — overview
Before patterns and scale, understand **what cloud providers offer**: service models, regions, compute, storage, networking, and how to design for **failure and recovery**.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Service models](ii-service-models.md) | IaaS, PaaS, SaaS, shared responsibility |
| [Regions, AZs & edge](iii-regions-azs-and-edge.md) | Regions, AZs, CDN edge, data residency |
| [Compute options](iv-compute-options.md) | VMs, containers/K8s, serverless, cold starts |
| [Storage & databases](v-storage-and-databases.md) | Object, block, file storage; SQL and NoSQL |
| [Networking, VPC & LB](vi-networking-vpc-and-lb.md) | VPC, subnets, load balancers, DNS, firewalls |
| [HA & disaster recovery](vii-ha-and-disaster-recovery.md) | RTO/RPO, multi-AZ, DR tiers |
| [Well-Architected Framework](viii-well-architected-framework.md) | Six pillars with cloud examples |

**Next:** **Patterns & design** submenu — scalability, microservices, events, observability, cost.

## Cloud stack at a glance

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Cloud foundation layers compute storage network">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Build blocks every architecture uses</text>
  <rect x="12" y="40" width="80" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="28" y="60" fill="#e4e4e7" font-size="9">Compute</text>
  <rect x="108" y="40" width="80" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="124" y="60" fill="#e4e4e7" font-size="9">Storage</text>
  <rect x="204" y="40" width="80" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="220" y="60" fill="#e4e4e7" font-size="9">Network</text>
  <rect x="300" y="40" width="80" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="60" fill="#e4e4e7" font-size="9">Security</text>
  <text x="12" y="88" fill="#71717a" font-size="9">All run inside regions · spread across AZs for HA</text>
</svg></figure>

## Rehearsal

- IaaS vs PaaS vs SaaS — one example each?
- Why deploy across **≥ 2 AZs**?
- Object vs block storage — when to use each?
- RTO vs RPO — which is downtime vs data loss?
