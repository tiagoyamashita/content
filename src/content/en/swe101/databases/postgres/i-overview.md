---
label: "I"
subtitle: "Overview"
group: "Postgres"
order: 1
---
Postgres — overview
**PostgreSQL** (Postgres) is the default **relational** database for many production applications: strong **ACID** transactions, rich **SQL**, extensible types, and mature tooling. This track focuses on what you need as a **software engineer** — schema design, migrations, query performance, app integration, and day-two operations.

For the general database landscape (NoSQL, CAP, polyglot persistence), see [Databases overview](../../CS101/databases/i-overview.md). For relational theory and SQL fundamentals, see [Relational (SQL)](../../CS101/databases/ii-relational.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Why Postgres, architecture mental model |
| **II — Install & psql** | Local setup, `psql`, basic admin |
| **III — Schema & migrations** | DDL, constraints, versioned schema changes |
| **IV — Indexes & EXPLAIN** | B-tree indexes, query plans, slow-query triage |
| **V — App integration** | JDBC, connection pools, Spring Data JPA |
| **VI — Operations & backups** | Roles, `pg_dump`, replication basics |
| **VII — Database optimizations** | Triage workflow, query rewrites, scaling checklist |

## Why Postgres (for apps)

| Strength | What it means in practice |
|----------|---------------------------|
| **ACID transactions** | Multi-row updates (order + inventory) succeed or roll back together |
| **Rich SQL** | `JOIN`, window functions, CTEs, `JSONB`, full-text search |
| **Constraints** | `UNIQUE`, `CHECK`, foreign keys enforced in the DB — not only in app code |
| **Extensions** | `pgcrypto`, PostGIS, `pgvector` — add capabilities without switching stores |
| **Ecosystem** | Managed offerings (RDS, Cloud SQL, Supabase, Neon), ORMs, migration tools |

## Architecture (mental model)

```text
Application  →  connection pool  →  Postgres server
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
              shared_buffers      WAL (durability)   background workers
              (cache pages)       (crash recovery)  (vacuum, checkpointer)
```

| Component | Role |
|-----------|------|
| **Database** | Namespace for schemas; one cluster hosts many databases |
| **Schema** | Default `public`; holds tables, views, functions |
| **Table / index** | On-disk structures; indexes are separate B-trees |
| **WAL** | Write-ahead log — commits are durable before data pages flush |
| **Vacuum** | Reclaims dead tuple space; updates planner statistics |

## Postgres vs “just use SQLite”

| | SQLite | Postgres |
|---|--------|----------|
| **Deployment** | Embedded file, zero server | Client/server process |
| **Concurrency** | Single writer | Many concurrent readers/writers |
| **Best for** | Local tools, mobile, tests | Multi-user web apps, shared state |
| **Ops** | Copy the file | Backups, roles, replication, monitoring |

Use SQLite for local dev and unit tests; use Postgres when multiple app instances or users share one database.

## Naming and types (quick conventions)

- Prefer **`snake_case`** table and column names — matches SQL tradition and most ORMs.
- Use **`BIGSERIAL` / `GENERATED … AS IDENTITY`** for surrogate primary keys.
- Prefer **`TIMESTAMPTZ`** over `TIMESTAMP` — stores UTC, displays in session timezone.
- Use **`TEXT`** instead of `VARCHAR(n)` unless you have a hard business limit (Postgres treats them similarly; `TEXT` is simpler).

## Next

Continue with [Install & psql](ii-install-and-psql.md) to run Postgres locally and connect from the shell.
