---
label: "I"
subtitle: "概要"
group: "MongoDB"
order: 1
---
MongoDB — 概要


**MongoDB** is a **document database**: records are **BSON/JSON documents** in **collections**, queried through drivers, **`mongosh`**, or ODMs like Spring Data MongoDB. This track covers what you need as a **software engineer** — modeling, queries, indexes, app integration, ops, and tuning.

For document-store concepts (embedding vs referencing, when to choose documents), see [Document](../../CS101/databases/iv-document.md). For relational patterns and ACID tradeoffs, see [Postgres](../postgres/i-overview.md) and [Relational (SQL)](../../CS101/databases/ii-relational.md).

## このトラックの地図

| Part | Focus |
|------|--------|
| **I — Overview** | Why MongoDB, core vocabulary, when to use it |
| **II — Install & mongosh** | Local/Atlas setup, connection strings, shell basics |
| **III — Schema & modeling** | Embed vs reference, validation, migrations |
| **IV — Queries & indexes** | `find`, aggregation, index types |
| **V — App integration** | Java Spring Data, Python PyMongo patterns |
| **VI — Operations & backups** | Replica sets, `mongodump`, Atlas ops |
| **VII — Database optimizations** | Triage, explain, schema/query checklist |

## MongoDB を使用する理由 (アプリの場合)

| Strength | What it means in practice |
|----------|---------------------------|
| **Document model** | One read returns nested JSON — fits many REST/API shapes |
| **Flexible schema** | New fields without `ALTER TABLE` — still plan migrations |
| **Horizontal scale** | Sharded cluster by shard key (when you outgrow one node) |
| **Rich queries** | Filters, aggregation pipeline, text/geo indexes |
| **Managed Atlas** | Backups, monitoring, global clusters without running your own ops |

## 主要な語彙

```text
Cluster
  └── Database (e.g. myapp)
        └── Collection (e.g. products)   ← like a table, schema-flexible
              └── Document { _id, ... }  ← like a row, but nested
```

| Term | Role |
|------|------|
| **`_id`** | Primary key — `ObjectId` by default if omitted |
| **Collection** | Named bag of documents |
| **Database** | Namespace for collections + users/roles |
| **Replica set** | Primary + secondaries — minimum for production transactions |
| **Shard** | Horizontal partition when data/throughput exceeds one machine |

## MongoDB が適合する場合

|良いフィット感 |悪いデフォルト |
|----------|--------------|
|さまざまな属性を持つカタログ |大量の JOIN レポートを備えた厳密なマルチテーブル台帳 |
|コンテンツ、ユーザー プロファイル、IoT イベント |すべてが 1 つの店舗にある「NoSQL だから」 |
|スキーマ チャーンを伴うプロトタイプ |複雑なアドホック分析 (多くの場合、ウェアハウス + SQL) |
| **多言語永続性** Postgres と並行 |モデリングのトレードオフなしで Postgres を置き換える |

お金と不変条件には **Postgres を使用します**、柔軟なドキュメントには **MongoDB を使用します** - 多くのチームが両方を実行しています。

## ドキュメントのサイズと書き込み

- **16 MB** 最大ドキュメント サイズ - 無制限の埋め込み配列はアンチパターンです。
- 可能な場合は **単一ドキュメントの更新** を推奨します。マルチドキュメント **トランザクション** は存在します (4.0 以降) が、1 ドキュメントのアトミック性よりもコストがかかります。

＃＃ 次

Continue with [Install & mongosh](ii-install-and-mongosh.md) to run MongoDB locally or on Atlas and connect from the shell.
