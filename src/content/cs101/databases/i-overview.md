---
label: "I"
subtitle: "Databases overview"
group: "Databases"
order: 1
---
Databases — overview
A **database** is organized storage plus **operations** to create, read, update, and delete data (**CRUD**), often with **concurrency**, **durability**, and **query** support. Applications rarely keep everything in flat files — they use a **database management system (DBMS)** chosen for the shape of the data and the access patterns.

**Java baseline:** JDBC and Spring Data examples assume **Java SE 22** (`javac --release 22`); they also run on **JDK 21 LTS**.

## 1. Why not just files?

| Files alone | Database |
|-------------|----------|
| You parse and lock manually | Engine handles indexing, caching, locking |
| Whole-file rewrite for small updates | Update one row or document |
| Hard to query across many users | **Query language** or API (SQL, aggregation pipeline) |
| Crash mid-write → corruption | **Transactions**, **WAL**, replication |

## 2. Core vocabulary

| Term | Meaning |
|------|---------|
| **Schema** | Structure: columns, types, constraints, or document shape |
| **Primary key** | Unique identifier for a row/document |
| **Index** | Extra structure (often B-tree or hash) for faster lookups |
| **Transaction** | Group of changes that succeed **all together** or **none** (**ACID** in SQL systems) |
| **Replication** | Copies of data on multiple machines (read scale, failover) |
| **Sharding** | Split data across machines by key range or hash |

## 3. Types of databases (short map)

Real systems often use **more than one** store (**polyglot persistence**): PostgreSQL for orders, Redis for sessions, Elasticsearch for search.

| Type | Data model | Best for | Examples | Deep dive |
|------|------------|----------|----------|-----------|
| **Relational (SQL)** | Tables, rows, typed columns, **JOINs** | Structured data, relationships, strong transactions | PostgreSQL, MySQL, SQLite | [Relational (SQL)](ii-relational.md) |
| **Key-value** | Opaque key → value | Cache, sessions, feature flags, simple lookups | Redis, DynamoDB (single-key), etcd | [Key-value](iii-key-value.md) |
| **Document** | JSON/BSON documents, optional schema | Flexible records, content, catalogs | MongoDB, CouchDB, Firestore | [Document](iv-document.md) |
| **Wide-column** | Row key + many columns; partition by key | Huge write throughput, time-ordered rows at scale | Cassandra, HBase, ScyllaDB | [Wide-column](v-wide-column.md) |
| **Graph** | Vertices + edges + properties | Relationship traversal, recommendations, fraud rings | Neo4j, Amazon Neptune | [Graph](vi-graph.md) |
| **Time-series** | Timestamp + measurements (tags + fields) | Metrics, IoT, monitoring, finance ticks | InfluxDB, TimescaleDB, Prometheus TSDB | [Time-series](vii-time-series.md) |

### Where older models fit

- **Hierarchical / network** (1960s–70s): tree or graph-like models before relational won — mostly historical; ideas survive inside **document** and **graph** stores.
- **Object-oriented DBs**: store language objects directly — niche today; **ORMs** map objects to **relational** tables instead.

### “NewSQL” and distributed SQL (one line)

**CockroachDB**, **Spanner**, **TiDB**: **SQL** interface with **horizontal scaling** — relational semantics across clusters. Start with **[Relational (SQL)](ii-relational.md)**, then read vendor docs when you need global scale.

## 4. SQL vs NoSQL (decision sketch)

```text
Need ad-hoc JOINs across many entities + ACID transactions?
  → Relational (SQL)

Need sub-millisecond key lookup, no joins?
  → Key-value

Schema varies per record, nested JSON, rapid product iteration?
  → Document

Billions of writes, partition by key, tunable consistency?
  → Wide-column

Queries are “friends of friends”, shortest path, pattern match on edges?
  → Graph

Queries are “avg CPU last hour by host”, append-only metrics?
  → Time-series
```

**NoSQL** is not “no SQL ever” — it means **not only relational tables**. Many teams run **PostgreSQL** plus **Redis** plus one specialized store.

## 5. CAP and consistency (preview)

Distributed databases trade **consistency**, **availability**, and **partition tolerance**. SQL primaries with sync replicas lean **CP**; some wide-column stores default to **eventual consistency** for **AP** under partition. Details per type in the linked notes; full distributed story appears in system-design material.

## 6. How data gets on disk (shared idea)

Most stores use:

- **B-tree** (or **B+ tree**) indexes for range scans and point lookups — same family as balanced BSTs in CS101.
- **Write-ahead log (WAL)** — append changes before applying to pages (durability after crash).
- **Buffer pool** — cache hot pages in RAM.

Hash indexes appear in key-value and hash-table-backed stores for **O(1)** point reads.

## 7. Related notes

| Note | Topic |
|------|--------|
| [Relational (SQL)](ii-relational.md) | Tables, SQL, ACID, normalization |
| [Key-value](iii-key-value.md) | Redis, TTL, cache patterns |
| [Document](iv-document.md) | Embedded docs, aggregation |
| [Wide-column](v-wide-column.md) | Partition keys, Cassandra-style modeling |
| [Graph](vi-graph.md) | Cypher/Gremlin, traversal vs JOINs |
| [Time-series](vii-time-series.md) | Retention, downsampling, PromQL-style queries |
| **Hash table** (Data structures submenu) | how hash maps relate to key-value stores |
| **B-tree / BST** (Data structures submenu) | index structure under SQL |
