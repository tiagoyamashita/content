---
label: "III"
subtitle: "制御フローとカーソル"
group: "PL/SQL"
order: 3
---
PL/SQL — 制御フローとカーソル

**`IF`** で分岐し、**`LOOP`** で反復し、**カーソル** で結果セットを明示的または暗黙的に処理します。

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

## 2. ループ

**基本ループ** (終了が必要):

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

**その間：**

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

**FOR (整数):**

```sql
BEGIN
  FOR i IN 1..5 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
  END LOOP;
END;
/
```

**FOR (カーソル)** — クエリ ループに推奨されます。

```sql
BEGIN
  FOR r IN (SELECT employee_id, last_name FROM employees WHERE department_id = 30) LOOP
    DBMS_OUTPUT.PUT_LINE(r.employee_id || ' ' || r.last_name);
  END LOOP;
END;
/
```

Oracle はカーソルを自動的に開き、フェッチし、閉じます。

## 3. 暗黙的カーソル (`SQL%`)

DML の後、**`SQL%ROWCOUNT`**、**`SQL%FOUND`**、**`SQL%NOTFOUND`** は最後のステートメントを反映します。

```sql
BEGIN
  UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;
  DBMS_OUTPUT.PUT_LINE('Updated rows: ' || SQL%ROWCOUNT);
END;
/
```

`%ROWCOUNT` が `COMMIT` または無関係な SQL の後も存続するとは考えず、すぐに読んでください。

## 4. 明示的なカーソル

行ごとのコントロールまたはパラメータが必要な場合:

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

|属性 |意味 |
|----------|----------|
| **`%FOUND`** |最後のフェッチでは行が返されました。
| **`%NOTFOUND`** |最後のフェッチに失敗しました (セットの終わり) |
| **`%ROWCOUNT`** |これまでにフェッチされた行 |

常に **`CLOSE`** カーソルを **`OPEN`** に設定します (または `FOR` ループを使用します)。

## 5. カーソル FOR UPDATE (ロック)

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

選択した行をコミット/ロールバックするまでロックします。使用は慎重に行ってください。可能であれば、セットベースの **`UPDATE … WHERE`** を推奨します。

## 6. セットベースと行ごとの比較

|アプローチ |いつ |
|----------|------|
| **単一 SQL** (`UPDATE …`、`MERGE`、`INSERT … SELECT`) |デフォルト — オプティマイザを機能させます |
| **カーソル ループ** | SQL ではきれいに表現できない行固有のロジック |
| **バルク** (パート VI を参照) |大規模なループ - コンテキストの切り替えを減らす |

アンチパターン: 1 **`UPDATE`** で十分な場合、カーソルは反復ごとに 1 行を更新します。

```sql
-- Prefer
UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;

-- Not (unless per-row rule differs)
FOR r IN (SELECT …) LOOP
  UPDATE employees SET salary = r.salary * 1.05 WHERE employee_id = r.employee_id;
END LOOP;
```

＃＃ 次

[プロシージャと関数](iv-procedures-and-functions.md) に進み、ロジックをスキーマ オブジェクトとして永続化します。
