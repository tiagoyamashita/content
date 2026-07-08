---
label: "II"
subtitle: "Blocks & variables"
group: "PL/SQL"
order: 2
---
PL/SQL — blocks & variables
Anonymous blocks, scalar variables, **anchor types** (`%TYPE`, `%ROWTYPE`), and assignment — the foundation for every procedure and package.

## 1. Anonymous block

```sql
DECLARE
  v_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_count FROM employees WHERE department_id = 10;
  DBMS_OUTPUT.PUT_LINE('Dept 10 headcount: ' || v_count);
END;
/
```

| Section | Purpose |
|---------|---------|
| **`DECLARE`** | Variables, constants, cursors, nested procedures |
| **`BEGIN`** | Executable statements |
| **`EXCEPTION`** | Handle errors without aborting the whole session |
| **`END`** | Closes the block |

Enable output in SQL*Plus/SQLcl: **`SET SERVEROUTPUT ON`**.

## 2. Common scalar types

| PL/SQL type | Maps to SQL | Notes |
|-------------|-------------|-------|
| **`NUMBER`** | `NUMBER` | Integers and decimals |
| **`VARCHAR2(n)`** | `VARCHAR2` | Variable-length text |
| **`DATE` / `TIMESTAMP`** | Same | Use `TIMESTAMP WITH TIME ZONE` when needed |
| **`BOOLEAN`** | *(none)* | PL/SQL only — not storable in a table column |
| **`CLOB` / `BLOB`** | Large objects | Stream or chunk in loops |

Constants:

```sql
DECLARE
  c_tax_rate CONSTANT NUMBER(5,4) := 0.0825;
BEGIN
  NULL; -- placeholder
END;
/
```

## 3. Anchor types (stay in sync with schema)

**`%TYPE`** — column type:

```sql
DECLARE
  v_email employees.email%TYPE;
BEGIN
  SELECT email INTO v_email FROM employees WHERE employee_id = 100;
END;
/
```

**`%ROWTYPE`** — whole row:

```sql
DECLARE
  r_emp employees%ROWTYPE;
BEGIN
  SELECT * INTO r_emp FROM employees WHERE employee_id = 100;
  DBMS_OUTPUT.PUT_LINE(r_emp.last_name);
END;
/
```

When a column type changes, anchored variables follow — fewer silent mismatches after migrations.

## 4. Assignment and expressions

```sql
DECLARE
  v_a NUMBER := 10;
  v_b NUMBER;
BEGIN
  v_b := v_a * 2;
  v_a := v_a + 1;
END;
/
```

| Operator / construct | Example |
|----------------------|---------|
| **Concatenation** | `'Hi ' \|\| name |
| **Comparison** | `=`, `<>`, `IS NULL`, `BETWEEN` |
| **CASE** | `CASE dept WHEN 10 THEN … END` |
| **`SELECT … INTO`** | Single-row fetch; raises **`NO_DATA_FOUND`** if zero rows |

## 5. `SELECT … INTO` rules

```sql
DECLARE
  v_name employees.last_name%TYPE;
BEGIN
  SELECT last_name INTO v_name
  FROM employees
  WHERE employee_id = 99999;  -- no row → NO_DATA_FOUND
END;
/
```

| Rows returned | Result |
|---------------|--------|
| **0** | `NO_DATA_FOUND` |
| **1** | Success |
| **>1** | `TOO_MANY_ROWS` |

For optional single row, use a cursor or `SELECT … INTO … WHERE …` with exception handler (see [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md)).

## 6. Nested blocks and scope

```sql
DECLARE
  v_x NUMBER := 1;
BEGIN
  DECLARE
    v_x NUMBER := 2;  -- inner v_x shadows outer
  BEGIN
    DBMS_OUTPUT.PUT_LINE(v_x);  -- prints 2
  END;
  DBMS_OUTPUT.PUT_LINE(v_x);    -- prints 1
END;
/
```

Label blocks when you need **`<<exit_block>>`** jumps in complex scripts (rare in application code).

## 7. NULL semantics

```sql
DECLARE
  a NUMBER := NULL;
  b NUMBER := 5;
BEGIN
  IF a = b THEN           -- unknown, not TRUE
    DBMS_OUTPUT.PUT_LINE('never');
  END IF;
  IF a IS NULL THEN
    DBMS_OUTPUT.PUT_LINE('a is null');
  END IF;
END;
/
```

Use **`IS NULL` / `IS NOT NULL`**, not `= NULL`.

## Next

Continue with [Control flow & cursors](iii-control-flow-and-cursors.md) for `IF`, loops, and row-by-row processing.
