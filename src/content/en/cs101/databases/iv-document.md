---
label: "IV"
subtitle: "Document"
group: "Databases"
order: 4
---
Document databases
**Document** stores treat each record as a **self-contained document** — usually **JSON** or **BSON** — with an **`_id`** and optional **schema validation**. Nested objects and arrays live **inside** one document instead of many normalized SQL tables.

## 1. Data model

One document = one logical entity (user profile, product, blog post):

```json
{
  "_id": "prod_8812",
  "title": "Mechanical keyboard",
  "price": 129.99,
  "tags": ["hardware", "peripherals"],
  "specs": {
    "switch": "linear",
    "layout": "TKL"
  },
  "reviews": [
    { "user": "ada", "stars": 5, "text": "Great feel" }
  ]
}
```

```text
SQL approach              Document approach
──────────────            ─────────────────
products table            one product document
product_tags join         tags: [ ... ] array inside
reviews table             reviews: [ ... ] embedded
specs columns or EAV      specs: { nested object }
```

## 2. Schema flexibility

| Mode | Trade-off |
|------|-----------|
| **Schema-less** | Fast iteration; app validates shape |
| **JSON Schema validation** | DB rejects bad documents (MongoDB `$jsonSchema`) |
| **Migrations** | Still needed when field meaning changes |

Good fit when **different records have different fields** (catalogs, CMS, user-generated content).

## 3. Querying

Document DBs expose **APIs** or **aggregation pipelines** instead of SQL JOINs across arbitrary tables.

MongoDB-style examples:

```javascript
// Find cheap hardware-tagged products
db.products.find({
  tags: "hardware",
  price: { $lt: 150 }
});

// Aggregation: average price by tag
db.products.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", avgPrice: { $avg: "$price" } } }
]);
```

**Indexes** on nested fields (`specs.switch`) make filters fast — same B-tree idea as SQL, different syntax.

## 4. Embedding vs referencing

| Pattern | Use when |
|---------|----------|
| **Embed** array/object in parent | One-to-few; read together; bounded size |
| **Reference** store `_id` of another doc | One-to-many huge sets; shared sub-documents |

Example reference:

```json
{ "_id": "order_99", "userId": "user_42", "lines": [ ... ] }
{ "_id": "user_42", "name": "Ada", "email": "..." }
```

Application does **two lookups** or **`$lookup`** (left-outer join) — no free relational JOIN optimizer for every shape.

## 5. Transactions and consistency

Modern document DBs (MongoDB 4+) support **multi-document ACID transactions** on a replica set — use for money-like updates, but **design for single-document writes** when possible (simpler, faster).

**Eventual consistency** still appears in **replica reads** if you read from secondaries — same class of bugs as SQL read replicas.

## 6. Strengths and limits

**Strengths**

- **Natural fit** for JSON APIs and mobile clients
- **Horizontal sharding** by `_id` or shard key in many products
- **Flexible schema** for evolving products
- **Nested reads** in one round trip when data is embedded

**Limits**

- **Unbounded arrays** in one document → document size limits (16 MB in MongoDB)
- **Ad-hoc analytics** across entities harder than SQL warehouses
- **Duplicate data** when embedding — update many docs to change shared field
- **Complex many-to-many** reporting often moves to **SQL** or **warehouse**

## 7. When to choose document

- Content platforms, catalogs with varying attributes
- **Backend-for-frontend** storing API-shaped blobs
- Prototypes where schema churn is high
- **NOT** default for strict financial ledger with heavy cross-table invariants — **relational** often wins

## 8. Examples

| Product | Notes |
|---------|--------|
| **MongoDB** | General document store, aggregation framework |
| **CouchDB** | HTTP API, multi-master replication |
| **Firestore** | Managed, mobile/web SDKs, realtime listeners |
| **PostgreSQL JSONB** | Hybrid: SQL + document columns in one engine |

## 9. Java sketch (MongoDB driver)

```java
// Compile: javac --release 22 …
// org.mongodb:mongodb-driver-sync (conceptual)
Document filter = new Document("tags", "hardware")
    .append("price", new Document("$lt", 150));
collection.find(filter).into(new ArrayList<>());
```

Spring Data MongoDB maps **`@Document`** entities similarly to JPA.

## 10. Related

- **Overview** — [Databases overview](i-overview.md)
- **Relational** — when JOINs and strict schema dominate [Relational (SQL)](ii-relational.md)
- **Wide-column** — another NoSQL family for write-heavy wide rows [Wide-column](v-wide-column.md)
