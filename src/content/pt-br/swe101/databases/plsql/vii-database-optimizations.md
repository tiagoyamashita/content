---
label: "VII"
subtitle: "Database optimizations"
group: "PL/SQL"
order: 7
---
PL/SQL — database optimizations
How to optimize **Oracle** workloads that use PL/SQL: prefer set-based SQL, reduce round trips, read execution plans, and avoid hidden row-by-row cost. Bulk primitives are in [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md); Postgres equivalents in [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md).

## 1. Optimization workflow

```text
1. Find slow SQL / jobs     (AWR, ASH, V$SQL, app traces)
2. EXPLAIN PLAN + DBMS_XPLAN
3. Fix SQL shape first      (set-based, fewer round trips)
4. Fix PL/SQL loop structure (BULK COLLECT, FORALL)
5. Index / stats / partition as needed
6. Re-measure on representative volume
```

| Tool | Purpose |
|------|---------|
| **AWR / ASH** | Top SQL, wait events (DBA + licensed options vary) |
| **`V$SQL` / `GV$SQL`** | Executions, elapsed time, buffer gets |
| **SQL Developer** | Explain plan, trace, profiler |
| **`DBMS_PROFILER` / PL/Scope** | Line-level PL/SQL time (dev) |

Always optimize against **production-scale** row counts — 100-row dev schemas hide full table scans.

## 2. Golden rule: set-based SQL first

Before tuning a cursor loop, ask whether one SQL statement suffices:

```sql
-- Slow: row-by-row in PL/SQL
BEGIN
  FOR r IN (SELECT employee_id FROM employees WHERE department_id = 50) LOOP
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = r.employee_id;
  END LOOP;
END;
/

-- Fast: one statement
UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;
```

| Pattern | Prefer |
|---------|--------|
| Per-row DML in loop | Single **`UPDATE`/`DELETE`/`MERGE`** |
| Loop + `SELECT INTO` | Join or subquery in one statement |
| Manual aggregation | **`GROUP BY`**, analytic functions |

Use PL/SQL loops when **each row needs different procedural logic** that SQL cannot express — not as default CRUD.

## 3. Bulk operations in PL/SQL

When you must loop, batch fetches and DML — see [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md).

```sql
DECLARE
  TYPE emp_rec IS TABLE OF employees%ROWTYPE;
  v_rows emp_rec;
  CURSOR c IS SELECT * FROM employees WHERE department_id = 50;
BEGIN
  OPEN c;
  LOOP
    FETCH c BULK COLLECT INTO v_rows LIMIT 1000;
    EXIT WHEN v_rows.COUNT = 0;

    FORALL i IN 1 .. v_rows.COUNT
      INSERT INTO employees_archive VALUES v_rows(i);

    v_rows.DELETE;
  END LOOP;
  CLOSE c;
END;
/
```

| Technique | Saves |
|-----------|-------|
| **`BULK COLLECT … LIMIT n`** | SQL→PL/SQL round trips on fetch |
| **`FORALL`** | PL/SQL→SQL round trips on DML |
| **`FORALL SAVE EXCEPTIONS`** | Partial success on bulk errors |

Tune **`LIMIT`** (500–5000) — balance memory vs round trips.

## 4. Bind variables and shared SQL

Literal values in dynamic SQL cause **hard parses** and fill **`V$SQL`**:

```sql
-- Bad: unique SQL per id
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = ' || p_id;

-- Good: bind
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = :id'
  INTO v_sal USING p_id;
```

Apps using JDBC **`PreparedStatement`** get binds automatically; dynamic PL/SQL must use **`USING`** or native binding.

Check for churn:

```sql
SELECT sql_text, executions, parse_calls
FROM v$sql
WHERE sql_text LIKE '%employees%'
ORDER BY parse_calls DESC;
```

High **`parse_calls`** relative to **`executions`** → binding or cursor reuse problem.

## 5. Execution plans

```sql
EXPLAIN PLAN FOR
  SELECT e.last_name, d.department_name
  FROM employees e
  JOIN departments d ON d.department_id = e.department_id
  WHERE e.department_id = 30;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

| Operation | Concern |
|-----------|---------|
| **TABLE ACCESS FULL** | Large table, no useful index |
| **NESTED LOOPS** | OK if inner index lookup; bad if inner is full scan |
| **HASH JOIN** | Large sets without index on join key |
| **CARTESIAN** | Missing join condition |

Compare **estimated vs actual rows** (12c+ adaptive plans, SQL Monitor) — stale stats → wrong join order.

Refresh stats after bulk load:

```sql
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(ownname => USER, tabname => 'EMPLOYEES');
END;
/
```

## 6. Indexes (SQL layer)

Same ideas as Postgres — match **`WHERE`**, **`JOIN`**, and **`ORDER BY`**:

```sql
CREATE INDEX emp_dept_sal_idx ON employees (department_id, salary DESC);
```

| PL/SQL-specific note | Detail |
|----------------------|--------|
| **`FOR UPDATE` cursors** | Lock only needed rows; keep transactions short |
| **Function-based index** | `CREATE INDEX … ON employees (UPPER(email))` for case-insensitive search |
| **Invisible / partial** | Test index before exposing to all sessions |

Avoid indexing every column “just in case” — DML in bulk jobs slows down.

## 7. Reduce PL/SQL ↔ SQL context switches

Each standalone SQL from PL/SQL has overhead. Batch work:

| Anti-pattern | Better |
|--------------|--------|
| `SELECT … INTO` inside loop | **`BULK COLLECT`** once |
| `UPDATE` per iteration | **`FORALL`** or one **`UPDATE`** |
| Commit every row | Commit per batch (business rules permitting) |
| **`DBMS_OUTPUT` in hot loop** | Remove or guard with debug flag |

**`PRAGMA UDF`** (12c+) can inline small functions in SQL — use for pure computation, not DML.

## 8. Parallelism and partitioning (awareness)

**Partition pruning** — queries with partition key skip irrelevant segments:

```sql
SELECT COUNT(*) FROM sales
WHERE sale_date >= DATE '2026-05-01'
  AND sale_date <  DATE '2026-06-01';
```

**Parallel DML/query** (`PARALLEL` hint or table degree) — DBA territory; can saturate I/O; test off-peak.

For nightly PL/SQL jobs, schedule during low contention; watch **enqueue waits** and **undo** usage.

## 9. Triggers and packages

| Risk | Mitigation |
|------|------------|
| Row trigger fires per row | Move to statement-level or set-based validation |
| **`AUTHID DEFINER`** + hidden DML | Audit; keep triggers thin |
| Package state assumptions | Pool-friendly apps may not share session state |

Profile before adding triggers for “optimization” — they often add latency to every DML.

## 10. Checklist

- [ ] Hottest SQL identified (`V$SQL`, AWR, or app trace)
- [ ] **`EXPLAIN PLAN`** reviewed for full scans and bad joins
- [ ] Row-by-row loops replaced with set SQL or **`BULK COLLECT`/`FORALL`**
- [ ] Binds used in dynamic SQL
- [ ] Stats refreshed after large loads
- [ ] Indexes align with predicates (not redundant copies)
- [ ] Commits scoped to business batches, not per row

## Related notes

- [Control flow & cursors](iii-control-flow-and-cursors.md) — when loops are justified
- [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md) — `BULK COLLECT`, `FORALL`, errors
- [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md) — `pg_stat_statements`, vacuum, keyset pagination
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — caching, replicas, sharding
