---
label: "IV"
subtitle: "手順と機能"
group: "PL/SQL"
order: 4
---
PL/SQL — プロシージャと関数

再利用可能なユニットを **プロシージャ** (シグネチャに戻り値なし) および **関数** (1 つの値を返す) として保存します。 SQL、他の PL/SQL、またはアプリケーション コードから呼び出します。

## 1.手順

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

実行する：

```sql
BEGIN
  raise_salary(100, 0.10);
  COMMIT;
END;
/
```

## 2. 機能

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

SQL からの電話 (** である必要があります)`DETERMINISTIC`** または一部のコンテキストの純粋性ルールを満たす):

```sql
SELECT department_id, dept_avg_salary(department_id) AS avg_sal
FROM departments;
```

PL/SQL からの電話:

```sql
DECLARE
  v NUMBER;
BEGIN
  v := dept_avg_salary(30);
  DBMS_OUTPUT.PUT_LINE(v);
END;
/
```

## 3.パラメータモード

|モード |発信者は通過できます |内部手順 |
|------|---------------|------|
| **`IN`** |リテラル、変数 |読み取り専用入力 |
| **`OUT`** |変数のみ |返却前に割り当てます。呼び出し側は結果を確認します |
| **`IN OUT`** |初期化された変数 |読んで置き換える |

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

好む **`IN`** 多くの場合にデフォルトが発生します **`OUT`** パラメータ — ** を返すことを検討してください`RECORD`** または複数の値の場合は ref カーソル。

## 4. SQL における関数の戻り値の制限

**で使用される関数`SELECT`** は、変更テーブルに対してコミット/ロールバックまたは DML を実行してはなりません (歴史的な **純粋性** ルール)。マーク **`DETERMINISTIC`** 結果が入力のみに依存する場合のみ (同じ引数→同じ結果)。

副作用を考慮して、クエリ内の関数ではなく、アプリから呼び出される **プロシージャ** を使用してください。

## 5. Java (JDBC) からの呼び出し

```java
try (var conn = dataSource.getConnection();
     var cs = conn.prepareCall("{ call raise_salary(?, ?) }")) {
  cs.setLong(1, 100L);
  cs.setBigDecimal(2, new BigDecimal("0.08"));
  cs.execute();
  conn.commit();
}
```

使用 **`{ call name(?, ?) }`** 手順について。関数は ** を使用できます`? = call func(?)`** ドライバーによって異なります。

＃＃６。`AUTHID DEFINER`対`AUTHID CURRENT_USER`

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

| | **`DEFINER`** (デフォルト) | **`CURRENT_USER`** |
|---|---------|----------|
| **として実行** |コンパイルしたオーナー |発信者 |
| **リスク** |所有者がスキーマ管理者の場合、過剰な権限が与えられます。マルチテナント アプリの安全性を高める |

監査 **`DEFINER`** 手順は慎重に行ってください。呼び出し元のアクセス許可がバイパスされます。

## 7. 削除して置き換える

```sql
DROP PROCEDURE raise_salary;
-- or
CREATE OR REPLACE PROCEDURE raise_salary ...  -- keeps grants if signature unchanged
```

パラメータリストを変更すると、依存オブジェクトが無効になる可能性があります - 依存オブジェクトを再コンパイルするか、** を使用してください`ALTER … COMPILE`**。

＃＃次

[パッケージとトリガー](v-packages-and-triggers.md) グループ化された API およびイベント駆動型ロジックの場合。
