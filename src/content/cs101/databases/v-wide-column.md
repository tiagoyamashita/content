---
label: "V"
subtitle: "Wide-column"
group: "Databases"
order: 5
---
Wide-column (column-family) databases
**Wide-column** stores (also **column-family** or **Bigtable-style**) partition rows by a **partition key** and store **many columns** per row — often sparse (millions of possible column names, only some set per row). They optimize for **massive write throughput** and **linear scale-out**, not arbitrary JOINs.

## 1. Data model

Think **distributed hash map of wide rows**:

```text
Partition key: user_id = 42
Row key (within partition): timestamp or event_id

         column:email     column:last_login    column:pref:theme
row 42   ada@…            2026-05-19T10:00Z    dark
```

In **Cassandra** terms:

```text
PRIMARY KEY ((tenant_id), event_time, event_id)
           └─ partition ─┘  └─ clustering order within partition ─┘
```

All rows with the same **partition key** live on the same node (simplified) — **choose partition keys** to spread load.

## 2. Query pattern drives design

Unlike SQL, you **design tables for queries upfront** (query-first modeling):

| Access need | Table design |
|-------------|--------------|
| Latest 100 events for user | Partition by `user_id`, cluster by `event_time DESC` |
| Events by device per day | Partition by `(device_id, day)` |
| Lookup user by email | **Secondary table** duplicating data keyed by `email` |

**Denormalization is normal** — duplicate rows in multiple tables to match read paths.

## 3. CQL example (Cassandra)

```sql
CREATE TABLE events_by_user (
  user_id      UUID,
  event_time   TIMESTAMP,
  event_id     UUID,
  payload      TEXT,
  PRIMARY KEY ((user_id), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);

INSERT INTO events_by_user (user_id, event_time, event_id, payload)
VALUES (?, ?, ?, ?);

SELECT * FROM events_by_user
WHERE user_id = ?
  AND event_time >= ?
LIMIT 100;
```

**ALLOW FILTERING** without partition key = full cluster scan — avoid in production.

## 4. Tunable consistency

Many wide-column systems let per-query **consistency level**:

| Level | Behavior |
|-------|----------|
| **ONE** | Fast; may read stale replica |
| **QUORUM** | Majority of replicas — common default |
| **ALL** | Slowest; all replicas agree |

Under network partition, **availability** vs **strong consistency** trade off (CAP).

## 5. Replication and ring

Nodes form a **ring** (often **consistent hashing**). Each partition key maps to replicas responsible for that range. Adding nodes **moves** only neighboring key ranges — not the whole dataset.

## 6. Strengths and limits

**Strengths**

- **Huge write rates** (IoT, feeds, logs at scale)
- **Linear horizontal scale** when partition keys are balanced
- **Geographic replication** in some products
- **Time-ordered** data within partition fits naturally

**Limits**

- **No ad-hoc JOIN** — application merges or duplicate tables
- **Hot partitions** if one key gets all traffic (celebrity user, global counter)
- **Learning curve** — wrong partition key is expensive to fix
- **Limited transactions** — often partition-scoped only

## 7. When to choose wide-column

- Event logs, activity streams, messaging metadata at **very large scale**
- **Write-heavy** workloads where SQL single-primary bottlenecks
- You can accept **query-first schema** and **eventual consistency** options
- **Not** first choice for small CRUD apps — PostgreSQL is simpler

## 8. Examples

| Product | Notes |
|---------|--------|
| **Apache Cassandra** | Open source, partition + clustering keys |
| **ScyllaDB** | Cassandra-compatible, C++ engine |
| **HBase** | Hadoop ecosystem, Bigtable model |
| **Google Bigtable** | Managed original; Spanner adds SQL layer |

## 9. Wide-column vs document vs relational

| | Relational | Document | Wide-column |
|---|------------|----------|-------------|
| **Unit** | Row in table | JSON document | Wide row under partition key |
| **Query** | Flexible SQL | Document filter | Partition key + column range |
| **Scale writes** | Harder on one node | Moderate | Designed for it |
| **Schema** | Strict tables | Flexible | Column families per row |

## 10. Related

- **Overview** — [Databases overview](i-overview.md)
- **Time-series** — overlapping use cases; TSDBs add retention/aggregation [Time-series](vii-time-series.md)
- **Key-value** — simpler key model without wide columns [Key-value](iii-key-value.md)
