---
label: "V"
subtitle: "パッケージとトリガー"
group: "PL/SQL"
order: 5
---
PL/SQL — パッケージとトリガー

**パッケージ**は、関連するプロシージャ、関数、型、**パッケージ レベルの変数**をグループ化します。 **トリガー**は、テーブル イベントまたはセッション アクションで PL/SQL を自動的に実行します。

## 1. パッケージ構造

```text
PACKAGE spec     — public interface (what callers see)
PACKAGE body     — implementation + private helpers
```

**仕様：**

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

**体：**

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

電話：

```sql
BEGIN
  emp_mgmt.hire('Chen', 30);
END;
/
```

## 2. パッケージを使用する理由

|メリット |説明 |
|----------|---------------|
| **名前空間** | `emp_mgmt.hire` 対 数十のスタンドアロン手順 |
| **カプセル化** |民間のヘルパーは体だけで生きています |
| **セッション状態** |パッケージ変数はセッションの間保持されます (慎重に使用してください)。
| **パフォーマンス** |最初の呼び出しでは本体がロードされます。後続の呼び出しでは解析されたツリーを再利用します。

接続プールされたアプリでクロスリクエスト状態のパッケージ グローバルを悪用しないでください。各 JDBC 借用は異なるセッションである可能性があります。

## 3. 行レベルのトリガー

**`BEFORE INSERT OR UPDATE`** — 列を検証またはデフォルトにします:

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

|疑似記録 |役割 |
|---------------|------|
| **`:NEW`** |受信行 (INSERT/UPDATE) |
| **`:OLD`** |前の行 (更新/削除) |

**`AFTER`** トリガーは監査行を書き込むことがよくあります。

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

## 4. ステートメントレベルと行レベル

| | **`FOR EACH ROW`** |行句がありません (ステートメント) |
|---|-------------------|--------------------------|
| **火災** |影響を受ける行ごとに 1 回 |ステートメントごとに 1 回 |
| **使用** |列のデフォルト、行の監査 |バルクガード、ロギングカウント |

**テーブルの変更:** `employees` の行トリガーは同じステートメントで `employees` をクエリすることはできません。回避策 - 監査テーブルを設計するか、複雑な場合には複合トリガーを使用してください。

## 5. トリガータイミング

```text
BEFORE statement → BEFORE each row → DML → AFTER each row → AFTER statement
```

検証には **`BEFORE`** を優先します。 **`AFTER`** 変更自体を妨げない副作用については。

## 6. トリガーを使用しない場合

|トリガーヘビー |アプリ層の代替 |
|---------------|----------------------|
|隠されたビジネスルール |サービスメソッド、ドメインイベント |
|クロステーブル オーケストレーション |トランザクション送信ボックス、ジョブ キュー |
|毎週変更されるロジック |バージョン管理されたアプリのデプロイ |

トリガーはテストが難しく、スタック トレースに表示されないため、単純な DML を期待する ORM を驚かせます。

## 7. コンパイルと依存関係

```sql
SELECT object_name, object_type, status
FROM user_objects
WHERE object_name = 'EMP_MGMT';

ALTER PACKAGE emp_mgmt COMPILE;
ALTER TRIGGER trg_employees_biur COMPILE;
```

テーブル DDL の後、無効なオブジェクトを再コンパイルします。

```sql
BEGIN
  DBMS_UTILITY.COMPILE_SCHEMA(user, FALSE);
END;
/
```

＃＃ 次

構造化エラー処理と大量の DML については、[例外と一括 SQL](vi-exceptions-and-bulk-sql.md) に進みます。
