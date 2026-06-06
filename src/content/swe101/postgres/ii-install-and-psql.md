---
label: "II"
subtitle: "インストールと psql"
group: "ポストグレ"
order: 2
---
Postgres — インストールと psql

Postgres をローカルで実行し、**`psql`** に接続して、アプリケーションを接続する前にデータベースを検査します。

## 1. オプションのインストール

|方法 |いつ使用するか |
|----------|---------------|
| **ドッカー** |再現可能なバージョン、簡単なリセット、CI と一致 |
| **ネイティブ パッケージ** | macOS (`brew`)、Linux (`apt`/`dnf`)、Windows インストーラー |
| **マネージド クラウド** | Neon、Supabase、RDS — ローカル デーモンなし |

### Docker (学習用に推奨)

```bash
docker run --name pg-dev -e POSTGRES_PASSWORD=dev -p 5432:5432 -d postgres:16
docker exec -it pg-dev psql -U postgres
```

データは削除されるまでコンテナ内に保持されます。名前付きボリュームの場合:

```bash
docker run --name pg-dev -e POSTGRES_PASSWORD=dev -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data -d postgres:16
```

## 2. 接続文字列

```text
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

ローカル Docker の例:

```text
postgresql://postgres:dev@localhost:5432/postgres
```

|パート |典型的なローカル値 |
|------|---------------------|
| **ユーザー** | `postgres` |
| **パスワード** | `POSTGRES_PASSWORD`からの値 |
| **ホスト** | `localhost` |
| **ポート** | `5432` |
| **データベース** | `postgres` (デフォルト DB) または自分で作成したもの |

## 3. `psql` の必需品

接続する：

```bash
psql "postgresql://postgres:dev@localhost:5432/postgres"
# or
psql -h localhost -U postgres -d postgres
```

|コマンド |アクション |
|----------|----------|
| `\l` |データベースのリスト |
| `\c mydb` |データベース `mydb` に接続します |
| `\dt` |現在のスキーマ内のテーブルをリストする |
| `\d users` |表 `users` について説明する |
| `\du` |役割のリスト |
| `\timing` |クエリの実行時間を表示 |
| `\q` |やめる |

ファイルから SQL を実行します。

```bash
psql -U postgres -d myapp -f schema.sql
```

## 4. 開発データベースとロールを作成する

```sql
CREATE DATABASE myapp_dev;
CREATE USER myapp WITH PASSWORD 'local-only-secret';
GRANT ALL PRIVILEGES ON DATABASE myapp_dev TO myapp;

\c myapp_dev
GRANT ALL ON SCHEMA public TO myapp;
```

**運用環境における最小特権の原則:** アプリ ロールは、必要なテーブルに対して 28 ではなく 27 を取得します。

## 5. 最初のテーブル (煙テスト)

```sql
CREATE TABLE todos (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  done       BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO todos (title) VALUES ('Learn psql'), ('Read migrations note');
SELECT * FROM todos WHERE NOT done;
```

## 6. 設定ファイル (存在することを確認)

|ファイル |目的 |
|-----|----------|
| **`postgresql.conf`** |メモリ、接続、ロギング |
| **`pg_hba.conf`** |誰がどのホストから接続できるか (認証ルール) |

Docker では、オーバーライドをマウントしない限り、config はコンテナー内にあります。ローカルチューニングの場合、ロードテストを行うまでデフォルトを変更する必要はほとんどありません。

## 7. GUI クライアント (オプション)

|ツール |メモ |
|------|------|
| **pgAdmin** |フル機能を備え、多くのインストーラーが付属 |
| **Dビーバー** |クロス DB、優れた ER 図 |
| **TablePlus / DataGrip** |有料の洗練された UX |

`psql` stays worth learning — scripts, CI, and production debugging often happen in the shell.

＃＃ 次

バージョン管理された DDL と安全なスキーマの進化については、[スキーマと移行](iii-schema-and-migrations.md) に進みます。
