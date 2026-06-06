---
label: "VI"
subtitle: "例外と一括SQL"
group: "PL/SQL"
order: 6
---
PL/SQL — 例外とバルク SQL

**`EXCEPTION`** で Oracle エラーを処理し、**`RAISE_APPLICATION_ERROR`** でアプリ エラーを発生させ、**`BULK COLLECT`** および **`FORALL`** で大規模なループを高速化します。

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
| **`NO_DATA_FOUND`** | `SELECT INTO` は 0 行を返しました |
| **`TOO_MANY_ROWS`** | `SELECT INTO` は 2 行以上を返しました |
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

## 3. トランザクションと例外

ブロック内の未処理例外は、事前に**`COMMIT`**しない限り、そのブロック内の**のみ** DML をロールバックします (プロシージャでの部分的なコミットは避けてください)。

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

財務ロジックを 1 つのトランザクション境界に保ち、アプリの `@Transactional` セマンティクスに一致させます。

## 4. 一括収集

1 回の往復で多くの行をコレクションにフェッチします。

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

大きなセットをページングするには、カーソルで **`LIMIT`** を使用します。

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

**`FORALL`** は SQL エンジンにバッチを送信します。ループ内で行ごとに **`UPDATE`** するよりもはるかに高速です。

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

**`AUTONOMOUS_TRANSACTION`** は、外部トランザクションがロールバックした場合でも監査をコミットします。強力ですが、悪用しやすいです。

## 7. テストと保守性

|練習 |なぜ |
|----------|-----|
| **utPLSQL または SQL Developer を使用した単体テスト** |パッケージ内のリグレッションをキャッチする |
| ****`DBMS_APPLICATION_INFO`** のログ | AWR/ASH でのトレースセッション |
| **Flyway/Liquibase のバージョン スクリプト** | [Postgres の移行](../postgres/iii-schema-and-migrations.md) と同じ分野 |
| **ドキュメント `RAISE_APPLICATION_ERROR` コード** |アプリは -20001.. を HTTP エラーにマッピングできます。

## 8. Oracle からの移行

PL/SQLを置き換える場合:

1. 在庫 **`USER_SOURCE`** / **`ALL_PROCEDURES`** — 誰が何を電話するか。
2. 読み取りの多いレポートをウェアハウスに移動します。ルールをアプリサービスに移動します。
3. 可能な場合は、トリガーをアプリバリデーターまたは DB 制約に置き換えます。
4. 段階的に移植する — パッケージには、長年にわたるエッジケースが隠蔽されていることがよくあります。

## 関連メモ

- [リレーショナル (SQL)](../../CS101/databases/ii-relational.md) — SQL 基礎
- [データベース最適化](vii-database-optimizations.md) — AWR/V$SQLワークフロー、セットベースSQL、チェックリスト
- [Postgres の概要](../postgres/i-overview.md) — オープンソースの代替スタック
- [データベース最適化 (Postgres)](../postgres/vii-database-optimizations.md) — 並列チューニング ガイド
- [アプリ統合 (Postgres)](../postgres/v-app-integration.md) — Oracle ドライバーにも適用される JDBC パターン
