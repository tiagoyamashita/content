---
label: "IV"
subtitle: "Procedures & functions"
group: "PL/SQL"
order: 4
---
PL/SQL — procedures & functions
Store reusable units as **procedures** (no return value in the signature) and **functions** (return one value). Call them from SQL, other PL/SQL, or application code.

## 1. Procedure

```sql
CREATE OR REPLACE PROCEDURE raise_salary (
  p_employee_id IN employees.employee_id%TYPE,
  p_pct         IN NUMBER DEFAULT 0.05
) IS
BEGIN
  UPDATE employees
  SET salary = salary * (1 + p_pct)
  WHERE employee_id = p_employee_id;

  IF SQL%ROWCOUNT = 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Employee not found: ' || p_employee_id);
  END IF;
END raise_salary;
/
```

Execute:

```sql
BEGIN
  raise_salary(100, 0.10);
  COMMIT;
END;
/
```

## 2. Function

```sql
CREATE OR REPLACE FUNCTION dept_avg_salary (
  p_dept_id IN employees.department_id%TYPE
) RETURN NUMBER
IS
  v_avg employees.salary%TYPE;
BEGIN
  SELECT AVG(salary) INTO v_avg FROM employees WHERE department_id = p_dept_id;
  RETURN v_avg;
END dept_avg_salary;
/
```

Call from SQL (must be **`DETERMINISTIC`** or satisfy purity rules for some contexts):

```sql
SELECT department_id, dept_avg_salary(department_id) AS avg_sal
FROM departments;
```

Call from PL/SQL:

```sql
DECLARE
  v NUMBER;
BEGIN
  v := dept_avg_salary(30);
  DBMS_OUTPUT.PUT_LINE(v);
END;
/
```

## 3. Parameter modes

| Mode | Caller can pass | Inside procedure |
|------|-----------------|------------------|
| **`IN`** | Literal, variable | Read-only input |
| **`OUT`** | Variable only | Assign before return; caller sees result |
| **`IN OUT`** | Initialized variable | Read and replace |

```sql
CREATE OR REPLACE PROCEDURE swap (
  p_a IN OUT NUMBER,
  p_b IN OUT NUMBER
) IS
  v_tmp NUMBER;
BEGIN
  v_tmp := p_a;
  p_a := p_b;
  p_b := v_tmp;
END;
/
```

Prefer **`IN`** defaults over many **`OUT`** parameters — consider returning a **`RECORD`** or ref cursor for multiple values.

## 4. Function return restrictions in SQL

Functions used in **`SELECT`** must not commit/rollback or execute DML on mutating tables (historical **purity** rules). Mark **`DETERMINISTIC`** only when results depend solely on inputs (same args → same result).

For side effects, use a **procedure** invoked from the app, not a function in a query.

## 5. Calling from Java (JDBC)

```java
try (var conn = dataSource.getConnection();
     var cs = conn.prepareCall("{ call raise_salary(?, ?) }")) {
  cs.setLong(1, 100L);
  cs.setBigDecimal(2, new BigDecimal("0.08"));
  cs.execute();
  conn.commit();
}
```

Use **`{ call name(?, ?) }`** for procedures; functions may use **`? = call func(?)`** depending on driver.

## 6. `AUTHID DEFINER` vs `AUTHID CURRENT_USER`

```sql
CREATE OR REPLACE PROCEDURE report_sensitive
  AUTHID CURRENT_USER
IS
BEGIN
  -- Runs with invoker's privileges — respects invoker's row-level security
  NULL;
END;
/
```

| | **`DEFINER`** (default) | **`CURRENT_USER`** |
|---|-------------------------|---------------------|
| **Runs as** | Owner who compiled it | Caller |
| **Risk** | Over-privileged if owner is schema admin | Safer for multi-tenant apps |

Audit **`DEFINER`** procedures carefully — they bypass caller permissions.

## 7. Drop and replace

```sql
DROP PROCEDURE raise_salary;
-- or
CREATE OR REPLACE PROCEDURE raise_salary ...  -- keeps grants if signature unchanged
```

Changing parameter list may invalidate dependent objects — recompile dependents or use **`ALTER … COMPILE`**.

## Next

Continue with [Packages & triggers](v-packages-and-triggers.md) for grouped APIs and event-driven logic.
