---
label: "VI"
subtitle: "Exceptions & bulk SQL"
group: "PL/SQL"
order: 6
---
PL/SQL — exceptions & bulk SQL
Handle Oracle errors with **`EXCEPTION`**, raise app errors with **`RAISE_APPLICATION_ERROR`**, and speed large loops with **`BULK COLLECT`** and **`FORALL`**.

## 1. Built-in exceptions

```sql
DECLARE
  v_name employees.last_name%TYPE;
BEGIN
  SELECT last_name INTO v_name FROM employees WHERE employee_id = -1;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('No employee');
  WHEN TOO_MANY_ROWS THEN
    DBMS_OUTPUT.PUT_LINE('Ambiguous key');
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('SQLCODE=' || SQLCODE || ' ' || SQLERRM);
    RAISE;  -- re-raise to caller
END;
/
```

| Handler | Typical cause |
|---------|---------------|
| **`NO_DATA_FOUND`** | `SELECT INTO` returned 0 rows |
| **`TOO_MANY_ROWS`** | `SELECT INTO` returned 2+ rows |
| **`DUP_VAL_ON_INDEX`** | Unique constraint violation |
| **`OTHERS`** | Catch-all — log and re-raise when unsure |

## 2. User-defined exceptions

```sql
DECLARE
  e_invalid_dept EXCEPTION;
  PRAGMA EXCEPTION_INIT(e_invalid_dept, -20003);
BEGIN
  RAISE_APPLICATION_ERROR(-20003, 'Invalid department');
EXCEPTION
  WHEN e_invalid_dept THEN
    DBMS_OUTPUT.PUT_LINE('Handled app error');
END;
/
```

**`RAISE_APPLICATION_ERROR(code, message)`** — use codes **-20000 .. -20999** for application errors.

## 3. Transaction and exceptions

Unhandled exceptions in a block roll back **only** DML in that block unless you **`COMMIT`** earlier (avoid partial commits in procedures).

```sql
BEGIN
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 999; -- fails
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/
```

Keep financial logic in one transaction boundary — match your app’s `@Transactional` semantics.

## 4. BULK COLLECT

Fetch many rows into a collection in one round trip:

```sql
DECLARE
  TYPE id_tab IS TABLE OF employees.employee_id%TYPE;
  v_ids id_tab;
BEGIN
  SELECT employee_id BULK COLLECT INTO v_ids
  FROM employees
  WHERE department_id = 50;

  DBMS_OUTPUT.PUT_LINE('Count: ' || v_ids.COUNT);
  FOR i IN 1 .. v_ids.COUNT LOOP
    NULL; -- process v_ids(i)
  END LOOP;
END;
/
```

Use **`LIMIT`** on cursors for paging large sets:

```sql
OPEN c;
LOOP
  FETCH c BULK COLLECT INTO v_rows LIMIT 500;
  EXIT WHEN v_rows.COUNT = 0;
  -- process batch
END LOOP;
CLOSE c;
```

## 5. FORALL (bulk DML)

```sql
DECLARE
  TYPE id_tab IS TABLE OF employees.employee_id%TYPE;
  v_ids id_tab := id_tab(101, 102, 103);
BEGIN
  FORALL i IN 1 .. v_ids.COUNT
    UPDATE employees SET salary = salary * 1.02 WHERE employee_id = v_ids(i);
  DBMS_OUTPUT.PUT_LINE('Updated: ' || SQL%ROWCOUNT);
END;
/
```

**`FORALL`** sends batches to the SQL engine — much faster than row-by-row **`UPDATE`** in a loop.

**Save exceptions** (continue on failure):

```sql
FORALL i IN 1 .. v_ids.COUNT SAVE EXCEPTIONS
  DELETE FROM employees WHERE employee_id = v_ids(i);
-- inspect SQL%BULK_EXCEPTIONS after
```

## 6. Pragmas (selected)

```sql
CREATE OR REPLACE PROCEDURE log_action IS
  PRAGMA AUTONOMOUS_TRANSACTION;  -- separate commit scope — use rarely
BEGIN
  INSERT INTO audit_log (msg) VALUES ('action');
  COMMIT;
END;
/
```

**`AUTONOMOUS_TRANSACTION`** commits audit even if outer transaction rolls back — powerful and easy to misuse.

## 7. Testing and maintainability

| Practice | Why |
|----------|-----|
| **Unit test with utPLSQL or SQL Developer** | Catch regressions in packages |
| **Log with **`DBMS_APPLICATION_INFO`** | Trace sessions in AWR/ASH |
| **Version scripts in Flyway/Liquibase** | Same discipline as [Postgres migrations](../postgres/iii-schema-and-migrations.md) |
| **Document `RAISE_APPLICATION_ERROR` codes** | App can map -20001.. to HTTP errors |

## 8. Migration off Oracle

When replacing PL/SQL:

1. Inventory **`USER_SOURCE`** / **`ALL_PROCEDURES`** — who calls what.
2. Move read-heavy reporting to the warehouse; move rules to app services.
3. Replace triggers with app validators or DB constraints where possible.
4. Port incrementally — packages often hide years of edge cases.

## Related notes

- [Relational (SQL)](../../CS101/databases/ii-relational.md) — SQL foundation
- [Database optimizations](vii-database-optimizations.md) — AWR/V$SQL workflow, set-based SQL, checklist
- [Postgres overview](../postgres/i-overview.md) — open-source alternative stack
- [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md) — parallel tuning guide
- [App integration (Postgres)](../postgres/v-app-integration.md) — JDBC patterns that also apply to Oracle drivers
