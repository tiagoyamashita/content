---
label: "VI"
subtitle: "例外とバルク SQL"
group: "PL/SQL"
order: 6
---
PL/SQL — 例外とバルク SQL






** を使用して Oracle エラーを処理する`EXCEPTION`**、** でアプリエラーが発生します`RAISE_APPLICATION_ERROR`**、** を使用して大規模なループを高速化します`BULK COLLECT`** そして **`FORALL`**。

## 1. 組み込みの例外

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

|ハンドラー |典型的な原因 |
|-------|---------------|
| **`NO_DATA_FOUND`** |`SELECT INTO`0 行が返されました |
| **`TOO_MANY_ROWS`** |`SELECT INTO`2 行以上が返されました |
| **`DUP_VAL_ON_INDEX`** |一意の制約違反 |
| **`OTHERS`** |キャッチオール — 不明な場合は記録して再レイズする |

## 2. ユーザー定義の例外

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

**`RAISE_APPLICATION_ERROR(code, message)`** — アプリケーション エラーにはコード **-20000 .. -20999** を使用します。

## 3. 瞬間と例外

** しない限り、ブロック内の未処理例外はそのブロック内の**のみ** DML をロールバックします。`COMMIT`** より早く (プロシージャでの部分的なコミットは避けてください)。

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

財務ロジックを 1 つのトランザクション境界内に維持し、アプリの境界と一致させます。`@Transactional`セマンティクス。

## 4. BULK COLLECT

1回の往復で多くの行をコレクションにフェッチします。

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

使用 **`LIMIT`** 大きなセットをページングするためのカーソル:

```sql
OPEN c;
LOOP
  FETCH c BULK COLLECT INTO v_rows LIMIT 500;
  EXIT WHEN v_rows.COUNT = 0;
  -- process batch
END LOOP;
CLOSE c;
```

## 5. FORALL (バルク DML)

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

**`FORALL`** バッチを SQL エンジンに送信します — 行ごとに送信するよりもはるかに高速です **`UPDATE`** ループ内。

**例外を保存** (失敗しても続行):

```sql
FORALL i IN 1 .. v_ids.COUNT SAVE EXCEPTIONS
  DELETE FROM employees WHERE employee_id = v_ids(i);
-- inspect SQL%BULK_EXCEPTIONS after
```

## 6. プラグマ (選択済み)

```sql
CREATE OR REPLACE PROCEDURE log_action IS
  PRAGMA AUTONOMOUS_TRANSACTION;  -- separate commit scope — use rarely
BEGIN
  INSERT INTO audit_log (msg) VALUES ('action');
  COMMIT;
END;
/
```

**`AUTONOMOUS_TRANSACTION`** 外部トランザクションがロールバックした場合でも監査をコミットします。強力ですが、悪用されやすいです。

## 7. テストと保守性

|練習 |なぜ |
|----------|-----|
| **utPLSQL または SQL 開発者による単体テスト** |パッケージ内のリグレッションをキャッチする |
| ** でログを記録します **`DBMS_APPLICATION_INFO`** | AWR/ASH でセッションをトレースする |
| **Flyway/Liquibase のバージョン スクリプト** | [Postgres 移行](../postgres/iii-schema-and-migrations.md) |
| **書類`RAISE_APPLICATION_ERROR`コード** |アプリは -20001.. を HTTP エラーにマッピングできます。

## 8. Oracleからの移行

PL/SQL を置き換える場合:

1. 在庫 **`USER_SOURCE`** / **`ALL_PROCEDURES`** — 誰が何を呼び出すか。
2. 読み取りの多いレポートをウェアハウスに移動します。ルールをアプリサービスに移動します。
3. 可能であれば、トリガーをアプリバリデーターまたは DB 制約に置き換えます。
4. 段階的に移植する — パッケージには、長年にわたるエッジケースが隠蔽されていることがよくあります。

## 関連メモ

- [リレーショナル (SQL)](../../CS101/databases/ii-relational.md) — SQL 財団
- [データベースの最適化](vii-database-optimizations.md) — AWR/V$SQL ワークフロー、セットベースの SQL、チェックリスト
- [Postgres 概要](../postgres/i-overview.md) — オープンソースの代替スタック
- [データベースの最適化 (Postgres)](../postgres/vii-database-optimizations.md) — パラレルチューニングガイド
- [アプリの統合 (Postgres)](../postgres/v-app-integration.md) — Oracle ドライバーにも適用される JDBC パターン
