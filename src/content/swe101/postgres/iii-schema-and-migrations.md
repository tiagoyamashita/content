---
label: "III"
subtitle: "スキーマと移行"
group: "ポストグレ"
order: 3
---
Postgres — スキーマと移行

**DDL** でテーブルを定義し、**制約**でルールを適用し、**バージョン管理された移行** を通じてスキーマを進化させます。追跡されたスクリプトを使用せずに本番環境を手動で編集する必要はありません。

## 1. DDL ビルディング ブロック

```sql
CREATE TABLE accounts (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email         TEXT NOT NULL,
  display_name  TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'suspended', 'closed')),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT accounts_email_unique UNIQUE (email)
);

CREATE TABLE posts (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  account_id  BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  body        TEXT NOT NULL,
  published   BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX posts_account_id_idx ON posts (account_id);
```

|制約 |を防ぐ |
|-----------|----------|
| **`PRIMARY KEY`** | ID が重複しています |
| **`NOT NULL`** |必須フィールドが欠落しています |
| **`UNIQUE`** |重複メール、スラッグ |
| **`CHECK`** |無効な列挙型の値です。
| **`REFERENCES`** |孤立した外部キ​​ー |

## 2. 移行ワークフロー

```text
V1__create_accounts.sql   →  applied once, recorded in history table
V2__add_posts.sql         →  runs on next deploy
V3__index_posts.sql       →  additive, backward-compatible when possible
```

|ルール |なぜ |
|------|-----|
| **ファイルごとに一方向** |アップマイグレーションは契約です。ダウンはオプションです |
| **ツールが許可する場合は冪等** |一部のフローのインデックスの場合は `IF NOT EXISTS` |
| **拡張→デプロイ→契約** | NULL 可能な列を追加 → バックフィル → NOT NULL を設定 → 古いものを削除 |
| **適用された履歴を書き換えないでください** |新しい移行で修正を進めます |

一般的なツール: **Flyway**、**Liquibase**、**Alembic** (Python)、**Rails 移行**、**Prisma 移行**、**golang-maigrate**。

### フライウェイの例

```sql
-- V1__create_accounts.sql
CREATE TABLE accounts (
  id    BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE
);
```

```bash
flyway -url=jdbc:postgresql://localhost:5432/myapp_dev \
  -user=myapp -password=secret migrate
```

Flyway は **`flyway_schema_history`** を作成し、新しいバージョンのみを適用します。

## 3. 安全な列変更

|変更 |より安全なパターン |
|------|------|
| **列を追加** | `ADD COLUMN col TYPE DEFAULT value` — null 許容 + デフォルトの最近の Postgres でのテーブル全体の書き換えを回避します。
| **列の名前を変更** |両方の名前を読み取る移行 + アプリのデプロイ、またはロックステップでデプロイ |
| **列を削除** |書き込みの停止 → デプロイ → 読み取りの停止 → 移行が中止される |
| **タイプの変更** |新しい列 `col_new`、バックフィル、2 つのリリースでの名前の交換 |

トラフィックのピーク時にホット テーブルで **`ACCESS EXCLUSIVE`** の長時間ロックを避けてください。インデックスの作成には **`CONCURRENTLY`** を使用します ([インデックスと EXPLAIN](iv-indexes-and-explain.md) を参照)。

## 4. 形状が柔軟な場合 `JSONB`

```sql
ALTER TABLE products ADD COLUMN metadata JSONB NOT NULL DEFAULT '{}';
CREATE INDEX products_metadata_gin ON products USING GIN (metadata);

SELECT id, title FROM products
WHERE metadata @> '{"category": "electronics"}';
```

リレーショナル モデル内のクエリ可能なドキュメント フィールドには、**`JSON`** (読み取りごとのテキスト解析) ではなく **`JSONB`** (バイナリ、インデックス可能) を使用します。

## 5. `updated_at` のトリガー (一般的なパターン)

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER accounts_updated_at
  BEFORE UPDATE ON accounts
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

多くのチームは、代わりにアプリケーション コードで `updated_at` を設定することを好みます。これにより、DB 層での驚きが少なくなります。

## 6. シードと移行

| |移行 |種子 |
|---|-----------|----------|
| **目的** |スキーマ構造 |開発/デモデータ |
| **本番環境で実行** |はい |通常はいいえ |
| **例** | `CREATE TABLE` | `INSERT INTO roles …` |

本番データを移行ファイルに含めないようにしてください。

＃＃ 次

[インデックスと説明](iv-indexes-and-explain.md) に進み、運用環境でクエリを高速かつ読みやすくします。
