---
label: "VII"
subtitle: "データベースの最適化"
group: "PL/SQL"
order: 7
---
PL/SQL — データベースの最適化

PL/SQL を使用する **Oracle** ワークロードを最適化する方法: セットベースの SQL を優先し、ラウンドトリップを削減し、実行計画を読み取り、隠れた行ごとのコストを回避します。バルクプリミティブは[例外とバルクSQL](vi-exceptions-and-bulk-sql.md)にあります。 [データベース最適化 (Postgres)](../postgres/vii-database-optimizations.md) の Postgres と同等のもの。

## 1. 最適化ワークフロー

```text
1. Find slow SQL / jobs     (AWR, ASH, V$SQL, app traces)
2. EXPLAIN PLAN + DBMS_XPLAN
3. Fix SQL shape first      (set-based, fewer round trips)
4. Fix PL/SQL loop structure (BULK COLLECT, FORALL)
5. Index / stats / partition as needed
6. Re-measure on representative volume
```

|ツール |目的 |
|-----|----------|
| **AWR / アッシュ** |上位の SQL、待機イベント (DBA + ライセンス オプションは異なります) |
| **`V$SQL` / `GV$SQL`** |実行数、経過時間、バッファーの取得 |
| **SQL 開発者** |プラン、トレース、プロファイラーの説明 |
| **`DBMS_PROFILER` / PL/範囲** |行レベルのPL/SQL時間(開発) |

常に **本番規模** の行数に対して最適化します。100 行の開発スキーマはテーブル全体のスキャンを隠します。

## 2. 黄金律: 最初にセットベースの SQL

カーソル ループを調整する前に、1 つの SQL ステートメントで十分かどうかを確認してください。

```sql
-- Slow: row-by-row in PL/SQL
BEGIN
  FOR r IN (SELECT employee_id FROM employees WHERE department_id = 50) LOOP
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = r.employee_id;
  END LOOP;
END;
/

-- Fast: one statement
UPDATE employees SET salary = salary * 1.05 WHERE department_id = 50;
```

|パターン |優先する |
|----------|----------|
|ループ内の行ごとの DML |シングル **`UPDATE`/`DELETE`/`MERGE`** |
|ループ + `SELECT INTO` | 1 つのステートメントで結合またはサブクエリを実行する |
|手動集計 | **`GROUP BY`**、分析関数 |

**各行に SQL で表現できない異なる手続きロジックが必要**な場合、デフォルトの CRUD としてではなく、PL/SQL ループを使用します。

## 3. PL/SQL での一括操作

ループ、バッチフェッチ、および DML を実行する必要がある場合は、[例外と一括 SQL](vi-exceptions-and-bulk-sql.md) を参照してください。

```sql
DECLARE
  TYPE emp_rec IS TABLE OF employees%ROWTYPE;
  v_rows emp_rec;
  CURSOR c IS SELECT * FROM employees WHERE department_id = 50;
BEGIN
  OPEN c;
  LOOP
    FETCH c BULK COLLECT INTO v_rows LIMIT 1000;
    EXIT WHEN v_rows.COUNT = 0;

    FORALL i IN 1 .. v_rows.COUNT
      INSERT INTO employees_archive VALUES v_rows(i);

    v_rows.DELETE;
  END LOOP;
  CLOSE c;
END;
/
```

|テクニック |保存 |
|----------|----------|
| **`BULK COLLECT … LIMIT n`** |フェッチ時の SQL→PL/SQL ラウンドトリップ |
| **`FORALL`** | DML での PL/SQL→SQL ラウンドトリップ |
| **`FORALL SAVE EXCEPTIONS`** |一括エラーで部分的に成功 |

**`LIMIT`** (500–5000) を調整 — メモリとラウンドトリップのバランスをとります。

## 4. バインド変数と共有 SQL

動的 SQL のリテラル値は **ハード解析**を引き起こし、**`V$SQL`** を埋めます。

```sql
-- Bad: unique SQL per id
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = ' || p_id;

-- Good: bind
EXECUTE IMMEDIATE 'SELECT salary FROM employees WHERE employee_id = :id'
  INTO v_sal USING p_id;
```

JDBC **`PreparedStatement`** を使用するアプリは自動的にバインドされます。動的PL/SQLは**`USING`**またはネイティブ・バインディングを使用する必要があります。

チャーンをチェックします。

```sql
SELECT sql_text, executions, parse_calls
FROM v$sql
WHERE sql_text LIKE '%employees%'
ORDER BY parse_calls DESC;
```

**`executions`** と比較して **`parse_calls`** が高い → バインディングまたはカーソルの再利用の問題。

## 5. 実行計画

```sql
EXPLAIN PLAN FOR
  SELECT e.last_name, d.department_name
  FROM employees e
  JOIN departments d ON d.department_id = e.department_id
  WHERE e.department_id = 30;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

|操作 |懸念事項 |
|----------|----------|
| **テーブルアクセスがいっぱいです** |大きなテーブル、有用なインデックスがない |
| **ネストされたループ** |内部インデックス検索の場合は OK。内部がフルスキャンの場合は悪い |
| **ハッシュ結合** |結合キーにインデックスのない大きなセット |
| **デカルト** |結合条件がありません |

**推定行と実際の行**を比較します (12c 以降のアダプティブ プラン、SQL モニター) - 古い統計 → 間違った結合順序。

一括ロード後に統計を更新します。

```sql
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(ownname => USER, tabname => 'EMPLOYEES');
END;
/
```

## 6. インデックス (SQL 層)

Postgres と同じ考え方 — **`WHERE`**、**`JOIN`**、および **`ORDER BY`** に一致します。

```sql
CREATE INDEX emp_dept_sal_idx ON employees (department_id, salary DESC);
```

| PL/SQL 固有の注意事項 |詳細 |
|---------------------|----------|
| **`FOR UPDATE` カーソル** |必要な行のみをロックします。トランザクションを短くする |
| **関数ベースのインデックス** |大文字と小文字を区別しない検索の場合は `CREATE INDEX … ON employees (UPPER(email))` |
| **非表示/部分的** |すべてのセッションに公開する前にインデックスをテストする |

「念のため」すべての列にインデックスを作成することは避けてください。一括ジョブでの DML は速度が低下します。

## 7. PL/SQL ↔ SQL コンテキストの切り替えを減らす

PL/SQL の各スタンドアロン SQL にはオーバーヘッドがあります。バッチ作業:

|アンチパターン |より良い |
|--------------|----------|
| `SELECT … INTO` ループ内 | **`BULK COLLECT`** 1 回 |
|反復あたり `UPDATE` | **`FORALL`** または 1 つの **`UPDATE`** |
|すべての行をコミット |バッチごとにコミット (ビジネス ルールが許可する) |
| **`DBMS_OUTPUT` ホット ループ中** |デバッグフラグを使用して削除または保護する |

**`PRAGMA UDF`** (12c+) は SQL で小さな関数をインライン化できます。DML ではなく純粋な計算に使用します。

## 8. 並列処理と分割 (認識)

**パーティション プルーニング** — パーティション キーを使用したクエリは無関係なセグメントをスキップします。

```sql
SELECT COUNT(*) FROM sales
WHERE sale_date >= DATE '2026-05-01'
  AND sale_date <  DATE '2026-06-01';
```

**並列 DML/クエリ** (`PARALLEL` ヒントまたはテーブル次数) — DBA の領域。 I/O が飽和状態になる可能性があります。オフピーク時にテストします。

夜間のPL/SQLジョブの場合は、競合が少ない時間帯にスケジュールしてください。 **エンキュー待機**と**元に戻す**の使用状況を監視します。

## 9. トリガーとパッケージ

|リスク |緩和 |
|------|-----------|
|行トリガーは行ごとに起動します。ステートメントレベルまたはセットベースの検証に移行 |
| **`AUTHID DEFINER`** + 非表示 DML |監査;トリガーを薄く保つ |
|パッケージ状態の仮定 |プール対応アプリはセッション状態を共有できない可能性があります |

「最適化」のためのトリガーを追加する前にプロファイルを作成します。多くの場合、トリガーによりすべての DML に待ち時間が追加されます。

## 10. チェックリスト

- [ ] 最もホットな SQL が特定されました (`V$SQL`、AWR、またはアプリ トレース)
- [ ] **`EXPLAIN PLAN`** フルスキャンと不正な結合についてレビュー済み
- [ ] 行ごとのループは set SQL または **`BULK COLLECT`/`FORALL`** に置き換えられます
- [ ] 動的 SQL で使用されるバインド
- [ ] 大量のロード後に統計が更新されました
- [ ] インデックスは述語と一致します (冗長コピーではありません)。
- [ ] 行ごとではなく、ビジネス バッチにスコープを設定したコミット

## 関連メモ

- [制御フローとカーソル](iii-control-flow-and-cursors.md) — ループが両端揃えの場合
- [例外と一括SQL](vi-exceptions-and-bulk-sql.md) — `BULK COLLECT`、`FORALL`、エラー
- [データベース最適化 (Postgres)](../postgres/vii-database-optimizations.md) — `pg_stat_statements`、バキューム、キーセット ページネーション
- [データベースのボトルネック](../sysdesign/bottleneck-analysis/vi-database.md) — キャッシュ、レプリカ、シャーディング
