---
label: "I"
subtitle: "Overview"
group: "PL/SQL"
order: 1
---
PL/SQL — overview
**PL/SQL** (Procedural Language/SQL) is Oracle’s procedural extension to **SQL**. You run it inside the **Oracle Database** — anonymous blocks, stored **procedures**, **functions**, **packages**, and **triggers** — close to the data for batch jobs, legacy enterprise apps, and rules that must hold regardless of which client connects.

This track assumes you know relational basics from [Relational (SQL)](../../CS101/databases/ii-relational.md). For open-source Postgres patterns, see the [Postgres](../postgres/i-overview.md) track — syntax differs, but procedural-in-the-DB tradeoffs are similar.

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | When PL/SQL, Oracle tooling, block structure |
| **II — Blocks & variables** | `DECLARE`/`BEGIN`/`END`, types, `%TYPE`, `%ROWTYPE` |
| **III — Control flow & cursors** | `IF`, loops, implicit and explicit cursors |
| **IV — Procedures & functions** | Parameters, return values, calling from SQL |
| **V — Packages & triggers** | Spec/body, state, `BEFORE`/`AFTER` triggers |
| **VI — Exceptions & bulk SQL** | `EXCEPTION`, `BULK COLLECT`, `FORALL`, pragmas |
| **VII — Database optimizations** | Set-based SQL, plans, binds, bulk tuning checklist |

## When PL/SQL makes sense

| Use PL/SQL in the DB | Prefer application code |
|----------------------|-------------------------|
| Complex multi-step SQL on large sets (ETL, reporting) | HTTP APIs, UI, orchestration |
| Rules that every client must obey (constraints + triggers) | Business logic that changes often |
| Nightly batch close / ledger posting | Microservices with separate deploy cycles |
| Legacy Oracle Forms, EBS, custom ERP modules | Greenfield cloud-native services |

**Default for new services:** keep most logic in the app; use PL/SQL where Oracle is the system of record and teams already maintain packages.

## Where code runs

```text
Client (Java, Python, SQL*Plus, SQL Developer)
        │
        ▼
   Oracle Database
        ├── SQL engine (SELECT, DML, DDL)
        └── PL/SQL engine (blocks, procedures, packages, triggers)
                    │
                    └── Shared buffer cache & undo — same transaction as SQL
```

PL/SQL and SQL share **one transaction** in a session — `COMMIT`/`ROLLBACK` apply to both.

## Tooling

| Tool | Role |
|------|------|
| **SQL Developer** | Free GUI — run scripts, debug, browse objects |
| **SQL*Plus / SQLcl** | CLI — scripts, CI, DBA tasks |
| **Oracle Live SQL** | Browser sandbox (oracle.com/livesql) |
| **JDBC / OCI** | App calls: `{ call pkg.proc(?) }` |

Example anonymous block in SQL Developer or SQLcl:

```sql
SET SERVEROUTPUT ON
BEGIN
  DBMS_OUTPUT.PUT_LINE('Hello from PL/SQL');
END;
/
```

## Block anatomy (preview)

Every PL/SQL unit follows:

```text
[DECLARE   -- optional declarations]
BEGIN     -- executable statements
  ...
EXCEPTION -- optional handlers
  ...
END;
/
```

The slash (`/`) tells SQL*Plus/SQLcl to execute the block; SQL Developer often uses **Run Script** (F5) vs **Run Statement** (Ctrl+Enter).

## Oracle vs Postgres procedural SQL

| | Oracle PL/SQL | Postgres PL/pgSQL |
|---|---------------|-------------------|
| **Language** | Proprietary, mature in Oracle stack | Open source, Postgres-native |
| **Packages** | Yes (`SPEC` + `BODY`) | Schemas + functions, no package keyword |
| **Trigger syntax** | `:NEW` / `:OLD` row triggers | `NEW` / `OLD` record |
| **Typical employer context** | Banking, ERP, government Oracle estates | Startups, cloud-native, Supabase/Neon |

Knowing PL/SQL helps you maintain Oracle systems; it does not replace learning SQL and your app stack.

## Next

Continue with [Blocks & variables](ii-blocks-and-variables.md) for declarations, anchors, and assignment.
