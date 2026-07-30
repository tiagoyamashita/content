---
label: "IV"
subtitle: "Flowcharts & architecture"
group: "Mermaid"
order: 4
---
Mermaid — Part IV
**Flowcharts** show **steps, decisions, and dependencies** — pipelines, request paths, and service graphs. **Subgraphs** group nodes into tiers (web, backend, data) for deployment-style sketches before Terraform or Kubernetes YAML.

For scalable topology patterns, see [Core building blocks](../sysdesign/i-core-building-blocks.md) and [Classic designs](../sysdesign/classic-designs/i-overview.md).

## 1. Flowchart basics

```mermaid
flowchart TD
  A[Client] --> B[API Gateway]
  B --> C[Order Service]
  C --> D[(Postgres)]
  C --> E[Payment Client]
  E --> F[[Stripe]]
```

| Shape | Syntax | Typical meaning |
|-------|--------|-----------------|
| **Rectangle** | `[Label]` | Process, service, step |
| **Rounded** | `(Label)` | Start/end event |
| **Stadium** | `([Label])` | Terminal |
| **Cylinder** | `[(Label)]` | Database |
| **Subroutine** | `[[Label]]` | External system |
| **Diamond** | `{Label}` | Decision |

Direction: **`TD`** top-down, **`LR`** left-right, **`BT`**, **`RL`**.

## 2. Decisions and labels

```mermaid
flowchart TD
  Start([Receive order]) --> Q{Inventory OK?}
  Q -->|yes| Reserve[Reserve stock]
  Q -->|no| Backorder[Backorder or cancel]
  Reserve --> Pay{Payment OK?}
  Pay -->|yes| Confirm[Confirm order]
  Pay -->|no| Release[Release stock]
```

Edge labels after **`-->|text|`** document branch conditions — keep them short.

## 3. Subgraphs (tiers and boundaries)

```mermaid
flowchart LR
  subgraph Public["Public subnet"]
    ALB[ALB]
  end
  subgraph Private["Private subnet"]
    API[Order API]
    PG[(RDS Postgres)]
    R[(ElastiCache)]
  end
  User([User]) --> ALB
  ALB --> API
  API --> PG
  API --> R
```

| Pattern | Use |
|---------|-----|
| **`subgraph id["Title"]`** | VPC, region, bounded context |
| **Nested subgraphs** | Account → VPC → subnet (keep depth ≤ 2 for readability) |
| **`direction LR` inside subgraph** | Control layout per group |

Deployment diagrams in Mermaid are **logical** — they document intent; Terraform state is the operational source of truth.

## 4. Component-style dependency graph

```mermaid
flowchart TB
  subgraph Web["Web tier"]
    SPA[SPA]
    Client[API Client lib]
    SPA --> Client
  end
  subgraph Backend["Backend"]
    REST[REST API]
    Orders[Order Service]
    PayClient[Payment Client]
    Client --> REST
    REST --> Orders
    Orders --> PayClient
  end
  PG[(Postgres)]
  Stripe[[Stripe]]
  Orders --> PG
  PayClient --> Stripe
```

Keep **names aligned** with [sequence diagrams](iii-sequence-diagrams.md) in the same doc set — mismatched labels confuse readers.

## 5. Styling nodes and links

```mermaid
flowchart LR
  Auth[Auth] --> API[API]
  classDef primary fill:#e1f5fe,stroke:#01579b;
  class Auth,API primary;
  linkStyle 0 stroke:#333,stroke-width:2px;
```

| Directive | Effect |
|-----------|--------|
| **`classDef name fill,stroke`** | Reusable style |
| **`class node1,node2 name`** | Apply style |
| **`style node fill:#f9f`** | One-off override |
| **`linkStyle index stroke:...`** | Style nth link (0-based) |

Put shared `classDef` blocks in a **`theme.mmd` fragment** your build prepends before render.

## 6. C4-style context (lightweight)

Mermaid supports **C4** diagrams in recent versions (enable in config). Example **system context**:

```mermaid
C4Context
  title System Context - Ordering

  Person(customer, "Customer", "Places orders")
  System(ordering, "Ordering System", "Takes orders and payments")
  System_Ext(stripe, "Stripe", "Payment processor")

  Rel(customer, ordering, "Uses")
  Rel(ordering, stripe, "Charges cards", "HTTPS")
```

| Level | Question it answers |
|-------|---------------------|
| **Context** | Who uses the system and what external systems exist? |
| **Container** | Major apps and data stores (`C4Container`) |
| **Component** | Modules inside one container (`C4Component`) |

Pin Mermaid version in CI — C4 syntax evolved across releases. For full C4-PlantUML stdlib and pinned includes, see [PlantUML component & deployment](../plantuml/iv-component-and-deployment.md).

## 7. Anti-patterns

| Avoid | Prefer |
|-------|--------|
| One giant flowchart with every microservice | Context diagram + per-domain flowcharts |
| Subgraph nesting deeper than two levels | Multiple linked `.mmd` files |
| Different service names than in sequence diagrams | Shared glossary in doc intro |
| Relying on manual `linkStyle` indices | Named `classDef` and stable node order |

## Next

Continue with [Class, state & ER](v-class-state-and-er.md) for domain models and data sketches.
