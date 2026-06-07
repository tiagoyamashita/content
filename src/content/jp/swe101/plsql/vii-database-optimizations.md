---
label: "VII"
subtitle: "データベースの最適化"
group: "PL/SQL"
order: 7
---
PL/SQL — データベースの最適化


How to optimize **Oracle** workloads that use PL/SQL: prefer set-based SQL, reduce round trips, read execution plans, and avoid hidden row-by-row cost. Bulk primitives are in [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md); Postgres equivalents in [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md).

## 1. 最適化ワークフロー

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

常に **本番規模** の行数に対して最適化します。100 行の開発スキーマはテーブル全体のスキャンを隠します。

## 2. 黄金律: 最初にセットベースの SQL

カーソル ループを調整する前に、1 つの SQL ステートメントで十分かどうかを確認してください。

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

**各行に異なる手続きロジックが必要**で、SQL では表現できない場合 (デフォルトの CRUD としてではなく) PL/SQL ループを使用します。

## 3. PL/SQL での一括操作

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

## 4. バインド変数と共有 SQL

Literal values in dynamic SQL cause **hard parses** and fill **`V$SQL`**:

```sql
-- Bad: unique SQL per id
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = ' || p_id;

-- Good: bind
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = :id'
  INTO v_sal USING p_id;
```

Apps using JDBC **`PreparedStatement`** get binds automatically; dynamic PL/SQL must use **`USING`** or native binding.

チャーンをチェックします。

```sql
SELECT sql_text, executions, parse_calls
FROM v$sql
WHERE sql_text LIKE '%employees%'
ORDER BY parse_calls DESC;
```

High **`parse_calls`** relative to **`executions`** → binding or cursor reuse problem.

## 5. 実行計画

```sql
EXPLAIN PLAN FOR
  SELECT e.last_name, d.department_name
  FROM employees e
  JOIN departments d ON d.department_id = e.department_id
  WHERE e.department_id = 30;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

|操作 |懸念事項 |
|----------|----------|
| **TABLE ACCESS FULL** |大きなテーブル、有用なインデックスがない |
| **NESTED LOOPS** | OK 内部インデックス検索の場合。内部がフルスキャンの場合は悪い |
| **HASH JOIN** |結合キーにインデックスのない大きなセット |
| **CARTESIAN** |結合条件がありません |

**推定行と実際の行**を比較します (12c+ 適応プラン、SQL モニター) - 統計が古い → 結合順序が間違っています。

一括ロード後に統計を更新します。

```sql
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(ownname => USER, tabname => 'EMPLOYEES');
END;
/
```

## 6. インデックス (SQL 層)

Same ideas as Postgres — match **`WHERE`**, **`JOIN`**, and **`ORDER BY`**:

```sql
CREATE INDEX emp_dept_sal_idx ON employees (department_id, salary DESC);
```

| PL/SQL-specific note | Detail |
|----------------------|--------|
| **`FOR UPDATE` cursors** | Lock only needed rows; keep transactions short |
| **Function-based index** | `CREATE INDEX … ON employees (UPPER(email))` for case-insensitive search |
| **Invisible / partial** | Test index before exposing to all sessions |

「念のため」すべての列にインデックスを付けることは避けてください。一括ジョブの DML の速度が低下します。

## 7. __​​IT0__ ↔ SQL コンテキスト スイッチを減らす

PL/SQL からの各スタンドアロン SQL にはオーバーヘッドがあります。バッチ作業:

| Anti-pattern | Better |
|--------------|--------|
| `SELECT … INTO` inside loop | **`BULK COLLECT`** once |
| `UPDATE` per iteration | **`FORALL`** or one **`UPDATE`** |
| Commit every row | Commit per batch (business rules permitting) |
| **`DBMS_OUTPUT` in hot loop** | Remove or guard with debug flag |

**`PRAGMA UDF`** (12c+) can inline small functions in SQL — use for pure computation, not DML.

## 8. 並列処理と分割 (認識)

**パーティション プルーニング** — パーティション キーを使用したクエリは無関係なセグメントをスキップします。

```sql
SELECT COUNT(*) FROM sales
WHERE sale_date >= DATE '2026-05-01'
  AND sale_date <  DATE '2026-06-01';
```

**Parallel DML/query** (`PARALLEL` hint or table degree) — DBA territory; can saturate I/O; test off-peak.

夜間の PL/SQL ジョブの場合は、競合が少ない時間帯にスケジュールを設定します。 **エンキュー待機**と**元に戻す**の使用状況を監視します。

## 9. トリガーとパッケージ

| Risk | Mitigation |
|------|------------|
| Row trigger fires per row | Move to statement-level or set-based validation |
| **`AUTHID DEFINER`** + hidden DML | Audit; keep triggers thin |
| Package state assumptions | Pool-friendly apps may not share session state |

「最適化」のためのトリガーを追加する前にプロファイルを作成します。多くの場合、各 DML に遅延が追加されます。

## 10. チェックリスト

- [ ] Hottest SQL identified (`V$SQL`, AWR, or app trace)
- [ ] **`EXPLAIN PLAN`** reviewed for full scans and bad joins
- [ ] Row-by-row loops replaced with set SQL or **`BULK COLLECT`/`FORALL`**
- [ ] Binds used in dynamic SQL
- [ ] Stats refreshed after large loads
- [ ] Indexes align with predicates (not redundant copies)
- [ ] Commits scoped to business batches, not per row

## 関連メモ

- [Control flow & cursors](iii-control-flow-and-cursors.md) — when loops are justified
- [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md) — `BULK COLLECT`, `FORALL`, errors
- [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md) — `pg_stat_statements`, vacuum, keyset pagination
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — caching, replicas, sharding
