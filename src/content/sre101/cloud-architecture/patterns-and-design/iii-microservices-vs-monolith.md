---
label: "III"
subtitle: "Microservices vs monolith"
group: "Cloud architecture"
order: 3
---
Microservices vs monolith
**Monolith** — one deployable unit. **Microservices** — independent services per domain. Most teams should start simpler and extract services only when friction justifies complexity.

## 1. Comparison

| | Monolith | Microservices |
|---|----------|---------------|
| **Deploy** | Single artifact | Per-service pipelines |
| **Scale** | Whole app | Per service |
| **Debug** | Single process stack trace | Distributed tracing required |
| **Data** | Shared DB, ACID transactions | Database per service, eventual consistency |
| **Team** | Shared codebase | Team owns service end-to-end |
| **Latency** | In-process calls | Network hops |

## 2. Monolith advantages

```text
┌─────────────────────────────────┐
│         Monolith (one JAR)       │
│  ┌─────┐ ┌─────┐ ┌──────────┐  │
│  │Auth │ │Orders│ │Inventory │  │
│  └──┬──┘ └──┬──┘ └────┬─────┘  │
│     └───────┴─────────┘         │
│           shared DB              │
└─────────────────────────────────┘
```

- Fast local development — no service mesh to run
- Simple transactions across modules
- One deployment artifact for small teams

## 3. Microservices advantages

```text
     ┌─────────┐     ┌─────────┐     ┌──────────┐
     │  Auth   │     │ Orders  │     │ Inventory│
     │ service │     │ service │     │ service  │
     └────┬────┘     └────┬────┘     └────┬─────┘
          │    HTTP/gRPC   │               │
          └────────────────┴───────────────┘
                    message bus (optional)
```

- Scale **orders** service during peak without scaling auth
- Deploy inventory fix without redeploying entire platform
- Clear **bounded context** ownership (DDD)

## 4. Modular monolith — middle path

Structure code as modules with **clear boundaries** inside one deployable:

```text
src/
  auth/       ← package boundary, no direct DB access from orders
  orders/
  inventory/
  shared-kernel/   ← minimal shared types only
```

| Rule | Enforce |
|------|---------|
| No cross-module DB tables | Module owns its schema |
| Public API per module | Internal classes private |
| Integration tests at seams | Before extracting service |

Extract to microservice when: **independent release cadence**, **different scaling profile**, or **team ownership** boundary is stable.

## 5. When to migrate

| Signal | Action |
|--------|--------|
| Deploy blocked by unrelated team changes | Extract stable domain |
| One module needs 10× CPU | Extract and scale separately |
| Different SLAs (payments vs catalog) | Separate service + SLO |
| Premature split "because Netflix" | Stay modular monolith |

**Strangler fig:** route `%` of traffic to new service via gateway; migrate incrementally.

## 6. Distributed data challenges

| Monolith | Microservice |
|----------|--------------|
| `BEGIN; UPDATE orders; UPDATE inventory; COMMIT` | Saga or outbox pattern |
| Join across tables | API composition or read model |
| Strong consistency | Eventual consistency + idempotency |

See [Event-driven architecture](iv-event-driven-architecture.md) for sagas.

## 7. Operational cost

Microservices require:

- **CI/CD** per service (or monorepo with path filters)
- **Observability** — traces across calls [Observability, SLI & SLO](vi-observability-slo-and-slis.md)
- **Service discovery** — K8s DNS, Consul, cloud LB
- **Versioning** — backward-compatible APIs, consumer-driven contracts

## 8. Decision checklist

| Question | Monolith OK if |
|----------|----------------|
| Team size < 10? | Often yes |
| Single release train? | Yes |
| Domains still shifting? | Yes — avoid early split |
| Proven scaling bottleneck in one domain? | Consider extract |

## 9. Example evolution

| Phase | Architecture |
|-------|--------------|
| MVP | Single Spring Boot app + Postgres |
| Growth | Modular monolith + Redis + read replica |
| Scale | Extract payments (PCI scope), orders (peak load) |
| Mature | Service mesh, event bus, independent SLOs |

**Related:** [Event-driven architecture](iv-event-driven-architecture.md), [API Gateway & service mesh](v-api-gateway-and-service-mesh.md).
