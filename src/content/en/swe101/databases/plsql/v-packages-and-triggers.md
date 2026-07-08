---
label: "V"
subtitle: "Packages & triggers"
group: "PL/SQL"
order: 5
---
PL/SQL — packages & triggers
**Packages** group related procedures, functions, types, and **package-level variables**. **Triggers** run PL/SQL automatically on table events or session actions.

## 1. Package structure

```text
PACKAGE spec     — public interface (what callers see)
PACKAGE body     — implementation + private helpers
```

**Specification:**

```sql
CREATE OR REPLACE PACKAGE emp_mgmt AS
  PROCEDURE hire (
    p_last_name IN employees.last_name%TYPE,
    p_dept_id   IN employees.department_id%TYPE
  );
  PROCEDURE fire (p_employee_id IN employees.employee_id%TYPE);
  FUNCTION headcount (p_dept_id IN employees.department_id%TYPE) RETURN NUMBER;
END emp_mgmt;
/
```

**Body:**

```sql
CREATE OR REPLACE PACKAGE BODY emp_mgmt AS
  g_raise_default NUMBER := 0.05;  -- package state (session-scoped)

  PROCEDURE hire (
    p_last_name IN employees.last_name%TYPE,
    p_dept_id   IN employees.department_id%TYPE
  ) IS
  BEGIN
    INSERT INTO employees (employee_id, last_name, department_id, hire_date)
    VALUES (employees_seq.NEXTVAL, p_last_name, p_dept_id, SYSDATE);
  END hire;

  PROCEDURE fire (p_employee_id IN employees.employee_id%TYPE) IS
  BEGIN
    DELETE FROM employees WHERE employee_id = p_employee_id;
  END fire;

  FUNCTION headcount (p_dept_id IN employees.department_id%TYPE) RETURN NUMBER IS
    v_n NUMBER;
  BEGIN
    SELECT COUNT(*) INTO v_n FROM employees WHERE department_id = p_dept_id;
    RETURN v_n;
  END headcount;
END emp_mgmt;
/
```

Call:

```sql
BEGIN
  emp_mgmt.hire('Chen', 30);
END;
/
```

## 2. Why packages

| Benefit | Explanation |
|---------|-------------|
| **Namespace** | `emp_mgmt.hire` vs dozens of standalone procedures |
| **Encapsulation** | Private helpers live only in the body |
| **Session state** | Package variables persist for the session (use carefully) |
| **Performance** | First call loads body; subsequent calls reuse parsed tree |

Avoid abusing package globals for cross-request state in connection-pooled apps — each JDBC borrow may be a different session.

## 3. Row-level triggers

**`BEFORE INSERT OR UPDATE`** — validate or default columns:

```sql
CREATE OR REPLACE TRIGGER trg_employees_biur
  BEFORE INSERT OR UPDATE ON employees
  FOR EACH ROW
BEGIN
  :NEW.last_updated := SYSTIMESTAMP;
  IF :NEW.salary < 0 THEN
    RAISE_APPLICATION_ERROR(-20002, 'Salary cannot be negative');
  END IF;
END;
/
```

| Pseudo-record | Role |
|---------------|------|
| **`:NEW`** | Incoming row (INSERT/UPDATE) |
| **`:OLD`** | Previous row (UPDATE/DELETE) |

**`AFTER`** triggers often write audit rows:

```sql
CREATE OR REPLACE TRIGGER trg_employees_audit
  AFTER UPDATE OF salary ON employees
  FOR EACH ROW
BEGIN
  INSERT INTO emp_salary_audit (employee_id, old_sal, new_sal, changed_at)
  VALUES (:OLD.employee_id, :OLD.salary, :NEW.salary, SYSTIMESTAMP);
END;
/
```

## 4. Statement-level vs row-level

| | **`FOR EACH ROW`** | No row clause (statement) |
|---|-------------------|---------------------------|
| **Fires** | Once per affected row | Once per statement |
| **Use** | Column defaults, row audit | Bulk guard, logging count |

**Mutating table:** a row trigger on `employees` cannot query `employees` in the same statement without workaround — design audit tables or use compound triggers for complex cases.

## 5. Trigger timing

```text
BEFORE statement → BEFORE each row → DML → AFTER each row → AFTER statement
```

Prefer **`BEFORE`** for validation; **`AFTER`** for side effects that should not block the change itself.

## 6. When not to use triggers

| Trigger-heavy | App-layer alternative |
|---------------|----------------------|
| Hidden business rules | Service methods, domain events |
| Cross-table orchestration | Transactional outbox, job queue |
| Logic that changes weekly | Versioned app deploys |

Triggers are hard to test, invisible in stack traces, and surprise ORMs that expect simple DML.

## 7. Compile and dependencies

```sql
SELECT object_name, object_type, status
FROM user_objects
WHERE object_name = 'EMP_MGMT';

ALTER PACKAGE emp_mgmt COMPILE;
ALTER TRIGGER trg_employees_biur COMPILE;
```

After table DDL, recompile invalid objects:

```sql
BEGIN
  DBMS_UTILITY.COMPILE_SCHEMA(user, FALSE);
END;
/
```

## Next

Continue with [Exceptions & bulk SQL](vi-exceptions-and-bulk-sql.md) for structured error handling and high-volume DML.
