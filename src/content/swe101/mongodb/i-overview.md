---
label: "I"
subtitle: "Overview"
group: "MongoDB"
order: 1
---
MongoDB — overview
**MongoDB** is a **document database**: records are **BSON/JSON documents** in **collections**, queried through drivers, **`mongosh`**, or ODMs like Spring Data MongoDB. This track covers what you need as a **software engineer** — modeling, queries, indexes, app integration, ops, and tuning.

For document-store concepts (embedding vs referencing, when to choose documents), see [Document](../../CS101/databases/iv-document.md). For relational patterns and ACID tradeoffs, see [Postgres](../postgres/i-overview.md) and [Relational (SQL)](../../CS101/databases/ii-relational.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Why MongoDB, core vocabulary, when to use it |
| **II — Install & mongosh** | Local/Atlas setup, connection strings, shell basics |
| **III — Schema & modeling** | Embed vs reference, validation, migrations |
| **IV — Queries & indexes** | `find`, aggregation, index types |
| **V — App integration** | Java Spring Data, Python PyMongo patterns |
| **VI — Operations & backups** | Replica sets, `mongodump`, Atlas ops |
| **VII — Database optimizations** | Triage, explain, schema/query checklist |

## Why MongoDB (for apps)

| Strength | What it means in practice |
|----------|---------------------------|
| **Document model** | One read returns nested JSON — fits many REST/API shapes |
| **Flexible schema** | New fields without `ALTER TABLE` — still plan migrations |
| **Horizontal scale** | Sharded cluster by shard key (when you outgrow one node) |
| **Rich queries** | Filters, aggregation pipeline, text/geo indexes |
| **Managed Atlas** | Backups, monitoring, global clusters without running your own ops |

## Core vocabulary

```text
Cluster
  └── Database (e.g. myapp)
        └── Collection (e.g. products)   ← like a table, schema-flexible
              └── Document { _id, ... }  ← like a row, but nested
```

| Term | Role |
|------|------|
| **`_id`** | Primary key — `ObjectId` by default if omitted |
| **Collection** | Named bag of documents |
| **Database** | Namespace for collections + users/roles |
| **Replica set** | Primary + secondaries — minimum for production transactions |
| **Shard** | Horizontal partition when data/throughput exceeds one machine |

## When MongoDB fits

| Good fit | Poor default |
|----------|--------------|
| Catalogs with varying attributes | Strict multi-table ledger with heavy JOIN reporting |
| Content, user profiles, IoT events | Everything in one store “because NoSQL” |
| Prototypes with schema churn | Complex ad-hoc analytics (often warehouse + SQL) |
| **Polyglot persistence** alongside Postgres | Replacing Postgres without modeling tradeoffs |

Use **Postgres for money + invariants**, **MongoDB for flexible documents** — many teams run both.

## Document size and writes

- **16 MB** max document size — unbounded embedded arrays are an anti-pattern.
- Prefer **single-document updates** when possible; multi-document **transactions** exist (4.0+) but cost more than one-doc atomicity.

## Next

Continue with [Install & mongosh](ii-install-and-mongosh.md) to run MongoDB locally or on Atlas and connect from the shell.
