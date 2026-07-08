---
label: "I"
subtitle: "概要"
group: "Postgres"
order: 1
---
Postgres — 概要

**PostgreSQL** (Postgres) は、強力な **ACID** トランザクション、豊富な **SQL**、拡張可能なタイプ、成熟したツールなど、多くの実稼働アプリケーションのデフォルトの **リレーショナル** データベースです。このトラックでは、**ソフトウェア エンジニア**として必要なこと、つまりスキーマ設計、移行、クエリ パフォーマンス、アプリの統合、2 日目の操作に焦点を当てます。

For the general database landscape (NoSQL, CAP, polyglot persistence), see [Databases overview](../../CS101/databases/i-overview.md). For relational theory and SQL fundamentals, see [Relational (SQL)](../../CS101/databases/ii-relational.md).

## このトラックの地図

| Part | Focus |
|------|--------|
| **I — Overview** | Why Postgres, architecture mental model |
| **II — Install & psql** | Local setup, `psql`, basic admin |
| **III — Schema & migrations** | DDL, constraints, versioned schema changes |
| **IV — Indexes & EXPLAIN** | B-tree indexes, query plans, slow-query triage |
| **V — App integration** | JDBC, connection pools, Spring Data JPA |
| **VI — Operations & backups** | Roles, `pg_dump`, replication basics |
| **VII — Database optimizations** | Triage workflow, query rewrites, scaling checklist |

## Postgres を使用する理由 (アプリの場合)

| Strength | What it means in practice |
|----------|---------------------------|
| **ACID transactions** | Multi-row updates (order + inventory) succeed or roll back together |
| **Rich SQL** | `JOIN`, window functions, CTEs, `JSONB`, full-text search |
| **Constraints** | `UNIQUE`, `CHECK`, foreign keys enforced in the DB — not only in app code |
| **Extensions** | `pgcrypto`, PostGIS, `pgvector` — add capabilities without switching stores |
| **Ecosystem** | Managed offerings (RDS, Cloud SQL, Supabase, Neon), ORMs, migration tools |

## アーキテクチャ (メンタルモデル)

```text
Application  →  connection pool  →  Postgres server
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
              shared_buffers      WAL (durability)   background workers
              (cache pages)       (crash recovery)  (vacuum, checkpointer)
```

| Component | Role |
|-----------|------|
| **Database** | Namespace for schemas; one cluster hosts many databases |
| **Schema** | Default `public`; holds tables, views, functions |
| **Table / index** | On-disk structures; indexes are separate B-trees |
| **WAL** | Write-ahead log — commits are durable before data pages flush |
| **Vacuum** | Reclaims dead tuple space; updates planner statistics |

## Postgres vs 「SQLite だけを使う」

| | SQLサイト | Postgres |
|---|--------|----------|
| **展開** |埋め込みファイル、ゼロサーバー |クライアント/サーバープロセス |
| **同時実行性** |シングルライター |多数の同時リーダー/ライター |
| **こんな用途に最適** |ローカル ツール、モバイル、テスト |マルチユーザー Web アプリ、共有状態 |
| **作戦** |ファイルをコピーします |バックアップ、ロール、レプリケーション、モニタリング |

ローカルの開発テストと単体テストには SQLite を使用します。複数のアプリ インスタンスまたはユーザーが 1 つのデータベースを共有する場合は、Postgres を使用します。

## 名前とタイプ (簡単な規則)

- Prefer **`snake_case`** table and column names — matches SQL tradition and most ORMs.
- Use **`BIGSERIAL` / `GENERATED … AS IDENTITY`** for surrogate primary keys.
- Prefer **`TIMESTAMPTZ`** over `TIMESTAMP` — stores UTC, displays in session timezone.
- Use **`TEXT`** instead of `VARCHAR(n)` unless you have a hard business limit (Postgres treats them similarly; `TEXT` is simpler).

＃＃ 次

Continue with [Install & psql](ii-install-and-psql.md) to run Postgres locally and connect from the shell.
