---
label: "II"
subtitle: "インストールと psql"
group: "Postgres"
order: 2
---
Postgres — インストールと psql


Run Postgres locally, connect with **`psql`**, and inspect databases before wiring an application.

## 1. オプションのインストール

| Method | When to use |
|--------|-------------|
| **Docker** | Reproducible version, easy reset, matches CI |
| **Native package** | macOS (`brew`), Linux (`apt`/`dnf`), Windows installer |
| **Managed cloud** | Neon, Supabase, RDS — no local daemon |

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

| Part | Typical local value |
|------|---------------------|
| **USER** | `postgres` |
| **PASSWORD** | value from `POSTGRES_PASSWORD` |
| **HOST** | `localhost` |
| **PORT** | `5432` |
| **DATABASE** | `postgres` (default DB) or one you create |

## 3. `psql` essentials

接続する：

```bash
psql "postgresql://postgres:dev@localhost:5432/postgres"
# or
psql -h localhost -U postgres -d postgres
```

| Command | Action |
|---------|--------|
| `\l` | List databases |
| `\c mydb` | Connect to database `mydb` |
| `\dt` | List tables in current schema |
| `\d users` | Describe table `users` |
| `\du` | List roles |
| `\timing` | Show query execution time |
| `\q` | Quit |

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

**Principle of least privilege in production:** app role gets `SELECT/INSERT/UPDATE/DELETE` on needed tables — not `SUPERUSER`.

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

| File | Purpose |
|------|---------|
| **`postgresql.conf`** | Memory, connections, logging |
| **`pg_hba.conf`** | Who can connect from which host (auth rules) |

Docker では、オーバーライドをマウントしない限り、構成はコンテナー内にあります。ローカルチューニングの場合、ロードテストを行うまでデフォルトを変更する必要はほとんどありません。

## 7. __​​IT0__ クライアント (オプション)

|ツール |メモ |
|------|------|
| **pgAdmin** |フル機能を備え、多くのインストーラーが付属 |
| **Dビーバー** |クロス DB、優れた ER 図 |
| **TablePlus / DataGrip** |有料、洗練された UX |

`psql` stays worth learning — scripts, CI, and production debugging often happen in the shell.

＃＃ 次

Continue with [Schema & migrations](iii-schema-and-migrations.md) for versioned DDL and safe schema evolution.
