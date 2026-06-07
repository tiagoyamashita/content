---
label: "I"
subtitle: "Overview"
group: "Cloud architecture"
order: 1
---
Patterns & design — overview
**Foundations** submenu covers **what cloud gives you** (compute, storage, VPC). This submenu covers **how to architect** for scale, resilience, observability, and cost at application and platform level.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Scalability & caching](ii-scalability-and-caching.md) | Scale up/out, stateless apps, auto scaling, cache tiers |
| [Microservices vs monolith](iii-microservices-vs-monolith.md) | Monolith, modular monolith, microservices trade-offs |
| [Event-driven architecture](iv-event-driven-architecture.md) | Queues, pub/sub, streaming, sagas |
| [API Gateway & service mesh](v-api-gateway-and-service-mesh.md) | North-south vs east-west, circuit breakers |
| [Observability, SLI & SLO](vi-observability-slo-and-slis.md) | Logs, metrics, traces, SLI/SLO/SLA |
| [Cost & governance](vii-cost-and-governance.md) | Pricing models, FinOps, IAM, guardrails |

**Related:** **Foundations** submenu (Well-Architected pillars), system design **scalable-patterns**, networking ingress/CDN notes.

## Architecture layers (mental model)

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="Cloud architecture layers client gateway services data">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Request path — patterns apply at each hop</text>
  <rect x="12" y="40" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="58" fill="#e4e4e7" font-size="8">Client</text>
  <path d="M68 54 H88" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="88" y="40" width="64" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="58" fill="#e4e4e7" font-size="8">CDN / GW</text>
  <path d="M152 54 H172" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="172" y="40" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="180" y="58" fill="#e4e4e7" font-size="8">Services</text>
  <path d="M244 54 H264" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="264" y="40" width="56" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="272" y="58" fill="#e4e4e7" font-size="8">Cache</text>
  <path d="M320 54 H340" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="340" y="40" width="56" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="348" y="58" fill="#e4e4e7" font-size="8">Data</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Scale services horizontally · cache reads · async where possible · observe everything</text>
</svg></figure>

## Well-Architected connection

| Pillar | Patterns in this submenu |
|--------|--------------------------|
| **Reliability** | Auto scaling, circuit breakers, multi-AZ (Foundations) |
| **Performance** | Caching, CDN, right-sizing |
| **Security** | Gateway auth, IAM least privilege, governance |
| **Cost** | Spot, reserved, FinOps tagging |
| **Operational excellence** | Observability, SLOs |

## Rehearsal

- Stateless vs stateful — impact on auto scaling?
- Queue vs pub/sub — one consumer or many?
- SLI vs SLO vs SLA — which is contractual?
