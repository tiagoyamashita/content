---
label: "II"
subtitle: "API design"
group: "System design"
order: 2
---
API design — REST, gRPC, GraphQL
How clients and services exchange data at scale: **resource-oriented HTTP**, **binary RPC**, and **flexible queries**.

## 1. REST (Representational State Transfer)

**REST** models resources as URLs; HTTP verbs express intent. Servers stay **stateless** — session state lives in tokens or client storage, not server memory per connection.

| Method | Path | Semantics | Idempotent? |
|--------|------|-----------|-------------|
| **GET** | `/users/{id}` | Read resource | Yes |
| **POST** | `/users` | Create (server assigns id) | No |
| **PUT** | `/users/{id}` | Full replace | Yes |
| **PATCH** | `/users/{id}` | Partial update | No* |
| **DELETE** | `/users/{id}` | Remove | Yes |

\*PATCH idempotency depends on patch document design.

**Status codes (subset)**

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | GET/PUT/PATCH success with body |
| 201 | Created | POST created resource |
| 204 | No content | DELETE success |
| 400 | Bad request | Validation failed |
| 401 / 403 | Auth / forbidden | Missing or insufficient credentials |
| 404 | Not found | Unknown resource id |
| 409 | Conflict | Duplicate create, version clash |
| 429 | Too many requests | Rate limited |
| 500 | Server error | Unhandled failure |

### Versioning

| Strategy | Example | Trade-off |
|----------|---------|-----------|
| URL path | `/v1/users` | Explicit; easy routing at gateway |
| Header | `Accept-Version: 1` | Clean URLs; harder to cache |
| Query | `/users?api-version=1` | Rare in public APIs |

**Rule:** never break existing clients on a version — add fields, deprecate, then sunset.

### Pagination

| Style | Query | Pros | Cons |
|-------|-------|------|------|
| **Offset** | `?offset=100&limit=20` | Simple SQL `OFFSET` | Skips/dupes if rows inserted/deleted while paging |
| **Cursor** | `?cursor=eyJpZCI6…}&limit=20` | Stable under live feeds | Opaque cursor; harder “jump to page 50” |

Cursor pattern: `WHERE (created_at, id) > (:last_ts, :last_id) ORDER BY created_at, id LIMIT 20`.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="Offset pagination vs cursor pagination under concurrent inserts">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Offset vs cursor (live feed)</text>
  <text x="12" y="38" fill="#f87171" font-size="9">Offset page 2: row inserted at top → duplicate or skip</text>
  <text x="12" y="54" fill="#86efac" font-size="9">Cursor after id=105 → always next rows by sort key</text>
  <rect x="12" y="64" width="48" height="20" rx="2" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="22" y="78" fill="#e4e4e7" font-size="8">new</text>
  <rect x="64" y="64" width="48" height="20" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="78" y="78" fill="#e4e4e7" font-size="8">101</text>
  <rect x="116" y="64" width="48" height="20" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="130" y="78" fill="#e4e4e7" font-size="8">102</text>
  <text x="180" y="78" fill="#fbbf24" font-size="9">← cursor "after 102"</text>
</svg></figure>

## 2. gRPC

**gRPC** uses **Protocol Buffers** over **HTTP/2**: binary, typed contracts, streaming.

| Feature | REST/JSON | gRPC |
|---------|-----------|------|
| Payload | Text JSON | Binary protobuf |
| Contract | OpenAPI (optional) | `.proto` required |
| Streaming | Uncommon | Native (server/client/bidi) |
| Browser | Native | Needs grpc-web proxy |
| Best for | Public HTTP APIs | Internal service mesh |

**Streaming modes**

| Mode | Use case |
|------|----------|
| Unary | Single request → single response |
| Server streaming | Large download, live updates |
| Client streaming | Upload batch |
| Bidirectional | Chat, collaborative editing |

```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);
}
```

## 3. GraphQL

Client sends one **query** describing the exact response shape.

| Pros | Cons |
|------|------|
| No over-fetching fields | **N+1** queries if resolvers naïve |
| One round trip for related data | Caching harder than REST URLs |
| Strong typing via schema | Complexity limits, depth attacks |

**N+1 fix:** **DataLoader** batches `userIds` → one `SELECT WHERE id IN (…)`.

## 4. Choosing an API style

| Scenario | Prefer |
|----------|--------|
| Public mobile/web REST ecosystem | **REST** + OpenAPI |
| Internal microservices, low latency | **gRPC** |
| Multiple clients, different field needs | **GraphQL** |
| File upload, simple CRUD | **REST** |

## 5. Cross-cutting API concerns

- **Idempotency-Key** header on POST (payments) — safe retries.
- **Correlation-Id** / trace headers — observability across services.
- **HATEOAS** — optional; hypermedia links in responses for discoverability.

**Related:** [Rate limiting](iv-rate-limiting.md) (429), [Distributed transactions](vii-distributed-transactions.md) (idempotency).
