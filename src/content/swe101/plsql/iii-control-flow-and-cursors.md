---
label: "III"
subtitle: "Control flow & cursors"
group: "PL/SQL"
order: 3
---
PL/SQL — control flow & cursors
Branch with **`IF`**, iterate with **`LOOP`**, and process result sets with **cursors** — explicit or implicit.

## 1. IF / ELSIF / ELSE

```sql
DECLARE
  v_salary employees.salary%TYPE;
  v_band VARCHAR2(20);
BEGIN
  SELECT salary INTO v_salary FROM employees WHERE employee_id = 100;
  IF v_salary >= 10000 THEN
    v_band := 'high';
  ELSIF v_salary >= 5000 THEN
    v_band := 'mid';
  ELSE
    v_band := 'entry';
  END IF;
  DBMS_OUTPUT.PUT_LINE(v_band);
END;
/
```

## 2. Loops

**Basic loop** (exit required):

```sql
DECLARE
  v_i NUMBER := 0;
BEGIN
  LOOP
    v_i := v_i + 1;
    EXIT WHEN v_i > 3;
  END LOOP;
END;
/
```

**WHILE:**

```sql
DECLARE
  v_i NUMBER := 0;
BEGIN
  WHILE v_i < 3 LOOP
    v_i := v_i + 1;
  END LOOP;
END;
/
```

**FOR (integer):**

```sql
BEGIN
  FOR i IN 1..5 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
  END LOOP;
END;
/
```

**FOR (cursor)** — preferred for query loops:

```sql
BEGIN
  FOR r IN (SELECT employee_id, last_name FROM employees WHERE department_id = 30) LOOP
    DBMS_OUTPUT.PUT_LINE(r.employee_id || ' ' || r.last_name);
  END LOOP;
END;
/
```

Oracle opens, fetches, and closes the cursor automatically.

## 3. Implicit cursor (`SQL%`)

After DML, **`SQL%ROWCOUNT`**, **`SQL%FOUND`**, **`SQL%NOTFOUND`** reflect the last statement:

```sql
BEGIN
  UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;
  DBMS_OUTPUT.PUT_LINE('Updated rows: ' || SQL%ROWCOUNT);
END;
/
```

Do not assume `%ROWCOUNT` persists after `COMMIT` or unrelated SQL — read it immediately.

## 4. Explicit cursor

When you need row-by-row control or parameters:

```sql
DECLARE
  CURSOR c_dept(p_dept_id employees.department_id%TYPE) IS
    SELECT employee_id, last_name, salary
    FROM employees
    WHERE department_id = p_dept_id
    ORDER BY salary DESC;
  v_id   employees.employee_id%TYPE;
  v_name employees.last_name%TYPE;
  v_sal  employees.salary%TYPE;
BEGIN
  OPEN c_dept(30);
  LOOP
    FETCH c_dept INTO v_id, v_name, v_sal;
    EXIT WHEN c_dept%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE(v_name || ': ' || v_sal);
  END LOOP;
  CLOSE c_dept;
END;
/
```

| Attribute | Meaning |
|-----------|---------|
| **`%FOUND`** | Last fetch returned a row |
| **`%NOTFOUND`** | Last fetch failed (end of set) |
| **`%ROWCOUNT`** | Rows fetched so far |

Always **`CLOSE`** cursors you **`OPEN`** (or use `FOR` loop).

## 5. Cursor FOR UPDATE (locking)

```sql
DECLARE
  CURSOR c IS
    SELECT employee_id, salary FROM employees
    WHERE department_id = 20
    FOR UPDATE OF salary;
BEGIN
  FOR r IN c LOOP
    UPDATE employees SET salary = r.salary * 1.1 WHERE CURRENT OF c;
  END LOOP;
END;
/
```

Locks selected rows until commit/rollback — use sparingly; prefer set-based **`UPDATE … WHERE`** when possible.

## 6. Set-based vs row-by-row

| Approach | When |
|----------|------|
| **Single SQL** (`UPDATE …`, `MERGE`, `INSERT … SELECT`) | Default — let optimizer work |
| **Cursor loop** | Row-specific logic that SQL cannot express cleanly |
| **Bulk** (see Part VI) | Large loops — reduce context switches |

Anti-pattern: cursor updating one row per iteration when one **`UPDATE`** suffices.

```sql
-- Prefer
UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;

-- Not (unless per-row rule differs)
FOR r IN (SELECT …) LOOP
  UPDATE employees SET salary = r.salary * 1.05 WHERE employee_id = r.employee_id;
END LOOP;
```

## Next

Continue with [Procedures & functions](iv-procedures-and-functions.md) to persist logic as schema objects.
