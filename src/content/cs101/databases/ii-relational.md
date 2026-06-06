---
label: "II"
subtitle: "リレーショナル (SQL)"
group: "データベース"
order: 2
---
リレーショナル データベース (SQL)

**リレーショナル** データベースは、**テーブル** (リレーション) にデータを保存します。これは、**キー** によってリンクされた、型指定された**列**を持つ行です。 **SQL** (宣言型 **SELECT**、**JOIN**、**GROUP BY**) を使用してクエリを実行し、複数の行またはテーブルを同時に変更する必要がある場合は **ACID トランザクション** に依存します。

## 1. データモデル

```text
users                          orders
┌────┬─────────┬──────────┐    ┌────┬─────────┬────────┬────────┐
│ id │ name    │ email    │    │ id │ user_id │ total  │ status │
├────┼─────────┼──────────┤    ├────┼─────────┼────────┼────────┤
│  1 │ Ada     │ a@…      │◄───│ 10 │    1    │  49.99 │ paid   │
│  2 │ Grace   │ g@…      │    │ 11 │    1    │  12.00 │ open   │
└────┴─────────┴──────────┘    └────┴─────────┴────────┴────────┘
         ▲                              │
         └──────── foreign key ──────────┘
```

|コンセプト |役割 |
|-------|------|
| **主キー (PK)** |一意の行 ID (`id`) |
| **外部キー (FK)** |別のテーブルの PK (`orders.user_id → users.id`) を参照します。
| **制約** | `NOT NULL`、`UNIQUE`、`CHECK`、`REFERENCES` — DB によって強制されます。
| **スキーマ** | DDL 時にテーブル定義を修正 (アプリでの移行) |

## 2. 1 パスの SQL

**DDL** — 構造体を定義します。

```sql
CREATE TABLE users (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  email      TEXT UNIQUE NOT NULL
);

CREATE TABLE orders (
  id         BIGSERIAL PRIMARY KEY,
  user_id    BIGINT NOT NULL REFERENCES users(id),
  total      NUMERIC(10, 2) NOT NULL,
  status     TEXT NOT NULL DEFAULT 'open'
);
```

**DML** — 読み取り/書き込み:

```sql
INSERT INTO users (name, email) VALUES ('Ada', 'ada@example.com');

SELECT u.name, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'paid';

UPDATE orders SET status = 'shipped' WHERE id = 10;

DELETE FROM orders WHERE status = 'cancelled' AND created_at < NOW() - INTERVAL '90 days';
```

**JOIN** はキーに基づいてテーブルを結合します。これが、エンティティが多対多の関係にある場合に SQL を選択する主な理由です。

## 3. ACID トランザクション

|プロパティ |意味 |
|----------|----------|
| **原子性** |トランザクション内のすべてのステートメントがコミットされるか、すべてロールバックされます。
| **一貫性** |コミット後に制約が保持される |
| **孤立** |同時トランザクションは互いのビューを破壊しません (レベル: コミット読み取り、反復読み取り、シリアル化可能) |
| **耐久性** |コミットされたデータはクラッシュしても存続します (WAL + fsync) |

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK; if anything fails
```

アプリケーション コード (JDBC / Spring) は同じ境界をラップします。

```java
// Compile: javac --release 22 …
// Spring @Transactional on a service method achieves the same boundary
connection.setAutoCommit(false);
try {
  debit(stmt, from, amount);
  credit(stmt, to, amount);
  connection.commit();
} catch (SQLException e) {
  connection.rollback();
  throw e;
}
```

## 4. インデックスとクエリ プラン

インデックスを使用しない場合、**`WHERE email = ?`** はすべての行 (**O(n)**) をスキャンします。 `email` の **B ツリー** インデックスは、おおよそ **O(log n)** でポイント検索を行います。

```sql
CREATE INDEX idx_users_email ON users (email);
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'ada@example.com';
```

経験則:

- よく使用する **WHERE**、**JOIN**、**ORDER BY** 述語の列にインデックスを付けます。
- インデックスが多すぎると **INSERT/UPDATE** が遅くなります (各インデックスを更新する必要があります)。
- **複合インデックス** `(user_id, status)` は `WHERE user_id = ? AND status = ?` に役立ちます。

## 5. 正規化 (なぜ複数のテーブルがあるのか​​)

|標準形 |アイデア |
|---------------|------|
| **1NF** |アトミック列 (繰り返しグループなし) |
| **2NF** |複合 PK への部分的な依存性はありません |
| **3NF** |非キー列は別の非キー列に依存しません。

**非正規化** - 意図的にデータを重複させる - ストレージと更新の複雑さを引き換えに読み取り速度を実現します (分析では一般的ですが、OLTP では必要性が確認されるまではまれです)。

## 6. 強みと限界

**強み**

- 柔軟な **アドホック クエリ** および **JOIN**
- 強力な**整合性** (FK、制約)
- 成熟した**トランザクション**、バックアップ、ツール

**制限**

- 1 つの巨大なテーブルに対する **スケールアウト書き込み** は困難です (シャーディングは手動または NewSQL 経由で行われます)
- **スキーマの移行**により、非常に急速な形状の変化が遅くなります (ドキュメント DB がここで競合します)
- **グラフ トラバーサル** 多くのホップ - 再帰的 CTE を使用する SQL では可能ですが、大規模な場合は扱いにくい

## 7. リレーショナルを選択する場合

- 注文、請求、在庫、アカウント — お金と不変条件が重要
- **多対多**の関係を持つ多くのエンティティ タイプ
- レポートには予測不可能な **JOIN** / **GROUP BY** が必要です
- チームはすでに **PostgreSQL** / **MySQL** を標準化しています

## 8. 例

|エンジン |一般的な使用法 |
|----------|---------------|
| **PostgreSQL** |汎用、JSON 列、拡張機能 |
| **MySQL / MariaDB** | Web アプリ、LAMP スタック |
| **SQLite** |組み込み、モバイル、テスト、単一ファイル |
| **SQL サーバー** |エンタープライズ Windows/.NET スタック |

## 9. 関連

- **概要** — [データベースの概要](i-overview.md)
- **ドキュメント** — ネストされた JSON が広範な正規化に勝る場合 [ドキュメント](iv-document.md)
- **ハッシュ テーブル** — ハッシュ インデックスと B ツリー (データ構造サブメニュー)
