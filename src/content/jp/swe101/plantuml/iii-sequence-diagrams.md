---
label: "III"
subtitle: "シーケンス図"
group: "PlantUML"
order: 3
---
PlantUML — Part III
**Sequence diagrams** show **who talks to whom, in what order** — ideal for HTTP calls, queue handoffs, auth flows, and failure paths. They are the default choice in design docs and incident writeups.

## 1. Basic syntax

```plantuml
@startuml
actor Client
participant "Order API" as API
database "Postgres" as DB

Client -> API: POST /orders
API -> DB: INSERT ...
DB --> API: row id
API --> Client: 201 + JSON
@enduml
```

| Arrow | Meaning |
|-------|---------|
| **`->`** | Solid line — call / request |
| **`-->`** | Dashed line — return / response |
| **`->>`** | Open arrow — async message (style) |
| **`Client ->> API`** | Same semantics; visual emphasis |

Define participants once; alias with **`as`** for shorter references.

## 2. Participant types

```plantuml
@startuml
actor User
boundary Web
control Service
entity Order
database DB
collections Cache
@enduml
```

| Keyword | Use |
|---------|-----|
| **`actor`** | Human or external system |
| **`boundary`** | UI, API gateway edge |
| **`control`** | Application / orchestration logic |
| **`entity`** | Domain object or record |
| **`database`** | SQL, document store |
| **`collections`** | Cache, in-memory structure |

Stereotypes and colors: `participant "API" as API <<Service>>` — pair with `skinparam` or shared include files.

## 3. Activation bars

```plantuml
@startuml
Client -> API: request
activate API
API -> DB: query
activate DB
DB --> API: rows
deactivate DB
API --> Client: response
deactivate API
@enduml
```

**`activate` / `deactivate`** (or `++` / `--` shorthand on arrows) show when a participant is busy — helpful for nested calls.

## 4. Notes and grouping

```plantuml
@startuml
Client -> API: login
note right of API: validate JWT
group Happy path
  API -> DB: fetch user
  DB --> API: user
end
Client <-- API: 200
@enduml
```

| Block | Purpose |
|-------|---------|
| **`note left/right of X`** | Annotate a participant |
| **`note over A, B`** | Span multiple participants |
| **`group` / `end`** | Label a section (non-semantic) |
| **`alt` / `else` / `end`** | Conditional branches |
| **`opt`** | Optional fragment |
| **`loop`** | Repeated steps |
| **`par`** | Parallel fragments |

### `alt` example (error path)

```plantuml
@startuml
Client -> API: GET /account
alt account exists
  API -> DB: SELECT
  DB --> API: row
  API --> Client: 200
else not found
  API --> Client: 404
end
@enduml
```

Document **both** happy and unhappy paths — reviewers catch missing error handling early.

## 5. Lifelines, delays, and references

```plantuml
@startuml
A -> B: start
...
hnote over B: processing
B --> A: done
@enduml
```

| Feature | Syntax |
|---------|--------|
| **Delay** | `...` on its own line |
| **Hanging note** | `hnote over` |
| **Reference another diagram** | `ref over A, B : see checkout.puml` |
| **Create/destroy** | `create B` / `destroy B` |

## 6. Realistic API + cache flow

```plantuml
@startuml
actor User
participant CDN
participant "API GW" as GW
participant "User Svc" as SVC
database "Postgres" as PG
collections "Redis" as R

User -> CDN: GET /users/42
alt cache HIT
  CDN --> User: 200 JSON
else cache MISS
  CDN -> GW: forward
  GW -> SVC: GET /internal/users/42
  SVC -> R: GET user:42
  alt Redis hit
    R --> SVC: cached
  else Redis miss
    SVC -> PG: SELECT ...
    PG --> SVC: row
    SVC -> R: SETEX user:42
  end
  SVC --> GW: 200
  GW --> CDN: 200
  CDN --> User: 200
end
@enduml
```

Cross-link concepts: [CDN overview](../cdn/i-overview.md), [Redis patterns](../redis/iv-patterns-and-use-cases.md), [API gateway overview](../api-gateway/i-overview.md).

## 7. Style tips

| Tip | Why |
|-----|-----|
| **Left-to-right flow** | `left to right direction` for wide diagrams |
| **Consistent naming** | Match service names in code and Terraform |
| **One scenario per file** | `checkout-happy.puml`, `checkout-payment-fail.puml` |
| **Number steps in prose** | Use `autonumber` for incident timelines |

```plantuml
@startuml
autonumber
Alice -> Bob: authentication request
Bob --> Alice: authentication response
@enduml
```

## Next

Continue with [Component & deployment](iv-component-and-deployment.md) for structural and runtime topology diagrams.
