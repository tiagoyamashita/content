---
label: "V"
subtitle: "クラス・アクティビティ・状態"
group: "PlantUML"
order: 5
---
PlantUML — Part V
**Class** diagrams model **types and relationships**. **Activity** diagrams model **steps and decisions**. **State** diagrams model **lifecycle transitions**. Use them for domain design, onboarding, and clarifying business rules — not as a substitute for auto-generated code diagrams.

## 1. Class diagrams

```plantuml
@startuml
class Order {
  +id: UUID
  +status: OrderStatus
  +totalCents: int
  +place()
  +cancel()
}

class LineItem {
  +sku: String
  +qty: int
  +unitPriceCents: int
}

enum OrderStatus {
  DRAFT
  PAID
  SHIPPED
  CANCELLED
}

Order "1" *-- "many" LineItem
Order --> OrderStatus
@enduml
```

| Syntax | Meaning |
|--------|---------|
| **`+` / `-` / `#`** | public / private / protected |
| **`*--`** | Composition |
| **`o--`** | Aggregation |
| **`-->`** | Association |
| **`<|--`** | Inheritance |
| **`..|>`** | Implementation |

### Interfaces and abstracts

```plantuml
@startuml
interface PaymentGateway {
  +charge(amount: Money): Receipt
}

abstract class AbstractPayment {
  #merchantId: String
}

class StripeGateway {
  +charge(amount: Money): Receipt
}

PaymentGateway <|.. StripeGateway
AbstractPayment <|-- StripeGateway
@enduml
```

**Tip:** generate class diagrams from code with **IDE plugins** or tools when the codebase is the source of truth; hand-drawn classes are best for **early design** and **bounded-context** discussions.

## 2. Activity diagrams

```plantuml
@startuml
start
:Receive order;
if (inventory available?) then (yes)
  :Reserve stock;
  :Charge payment;
  if (payment ok?) then (yes)
    :Confirm order;
    stop
  else (no)
    :Release stock;
    :Notify customer;
    stop
  endif
else (no)
  :Backorder or cancel;
  stop
endif
@enduml
```

| Element | Syntax |
|---------|--------|
| **Action** | `:Label;` |
| **Decision** | `if () then () else () endif` |
| **Fork/join** | `fork` / `end fork` |
| **Swimlanes** | `|Lane name|` before actions |
| **Partition** | `partition Name { ... }` |

Swimlane example:

```plantuml
@startuml
|Customer|
start
:Submit return request;
|Support|
:Review request;
|Warehouse|
:Receive item;
:Issue refund;
|Customer|
:Notification sent;
stop
@enduml
```

Activity diagrams complement **sequence** diagrams: activity = **business process**; sequence = **message-level** interactions.

## 3. State diagrams

```plantuml
@startuml
[*] --> Draft
Draft --> Paid : payment_success
Draft --> Cancelled : user_cancel
Paid --> Shipped : carrier_pickup
Paid --> Refunded : chargeback
Shipped --> Delivered : pod_scan
Delivered --> [*]
Cancelled --> [*]
Refunded --> [*]
@enduml
```

| Syntax | Meaning |
|--------|---------|
| **`[*]`** | Start / end pseudo-state |
| **`State --> State : event`** | Transition on event |
| **`state "Long Name" as SN`** | Alias long states |

### Composite states

```plantuml
@startuml
state Processing {
  state Validating
  state Charging
  Validating --> Charging
}
[*] --> Processing
Processing --> Succeeded
Processing --> Failed
@enduml
```

Map states to **enum values** or **status columns** in the database — reviewers can verify code and diagram agree.

## 4. ER diagrams (data model sketch)

PlantUML can sketch **entity-relationship** models alongside SQL migrations:

```plantuml
@startuml
entity users {
  * id : uuid
  --
  email : varchar
  created_at : timestamptz
}

entity orders {
  * id : uuid
  --
  user_id : uuid
  status : text
}

users ||--o{ orders
@enduml
```

Pair with [Postgres schema notes](../postgres/iii-schema-and-migrations.md) when documenting table design.

## 5. When to use which

| Diagram | Best for |
|---------|----------|
| **Class** | Domain nouns, service boundaries, ORM mapping discussions |
| **Activity** | Multi-step workflows, approval chains, ETL pipelines |
| **State** | Order status, job lifecycle, connection state machines |
| **ER** | Table relationships before writing migrations |

## Next

Continue with [Docs, repos & CI](vi-docs-repos-and-ci.md) to embed diagrams in Markdown and validate them in pipelines.
