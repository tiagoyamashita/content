---
label: "VI"
subtitle: "操作とバックアップ"
group: "MongoDB"
order: 6
---
MongoDB — 操作とバックアップ

実稼働 MongoDB は、**レプリカ セット** (フォールト トレランスのため少なくとも 3 つのメンバー) または **Atlas** (管理対象) として実行されます。 **バックアップ**、**監視**、**復元テスト**を必要になる前に計画してください。

## 1. 展開の形状

|形状 |使用 |
|------|-----|
| **スタンドアロン** |ローカル開発のみ |
| **レプリカセット** |プロダクション HA、トランザクション、oplog |
| **シャード クラスター** | 1 つのレプリカ セットを超えるデータまたはスループット |
| **アトラス** |マネージド レプリカ セット / シャード クラスター |

```text
Replica set (conceptual)
  Primary  ──replication──►  Secondary 1
       │                           │
       └──────────replication──────►  Secondary 2
```

書き込みは **プライマリ** に送られます。セカンダリは **oplog** を複製します。セカンダリからの読み取りには遅延が生じる可能性があります。

## 2. 役割と認証

```javascript
use myapp_dev
db.createUser({
  user: "app_rw",
  pwd: "…",
  roles: [{ role: "readWrite", db: "myapp_dev" }]
})

db.createUser({
  user: "app_ro",
  pwd: "…",
  roles: [{ role: "read", db: "myapp_dev" }]
})
```

| Role | Scope |
|------|-------|
| **`read` / `readWrite`** | Database-level app access |
| **`dbAdmin`** | Indexes, stats — migration job only |
| **`clusterAdmin`** | Break-glass ops — not for apps |

Atlas IAM + データベース ユーザーは、クラウド上での手動セットアップを置き換えます。

## 3. Backup with `mongodump` / `mongorestore`

論理バックアップ (BSON + メタデータ):

```bash
mongodump --uri="mongodb://localhost:27017/myapp_dev" --out=./backup-2026-05-19

mongorestore --uri="mongodb://localhost:27017/myapp_dev_restored" ./backup-2026-05-19/myapp_dev
```

| Method | Pros | Cons |
|--------|------|------|
| **`mongodump`** | Portable, collection-level | Large datasets slower than snapshots |
| **Atlas continuous backup** | Point-in-time restore | Vendor-specific |
| **Volume snapshot** | Fast at scale | Must coordinate with filesystem snapshot API |

**スケジュールに従ってリストアをテスト** - テストされていないバックアップは重要なときに失敗します。

## 4. 信号の監視

| Signal | Action |
|--------|--------|
| **Replication lag** | Secondary falls behind — check load, network, index builds |
| **Opcounters / QPS** | Capacity planning |
| **Slow query log** | Enable `operationProfiling` or Atlas Performance Advisor |
| **Disk usage** | TTL, archival, compaction (WiredTiger) |
| **Connections** | Pool sizing — too many clients |

アトラス: **メトリクス**、**アラート**、**パフォーマンス アドバイザー** (インデックスの提案)。

## 5. 運用環境でのインデックスの構築

大規模なインデックス作成により、古いバージョンへの書き込みがブロックされます。好む：

```javascript
db.products.createIndex({ sku: 1 }, { background: true })  // legacy option; behavior varies by version
```

最近の MongoDB では、インデックス ビルドの同時実行が増加しています。依然として、負荷の高いビルドはオフピークにスケジュールされています。ステージングデータ量を確認します。

## 6. シャーディング (認識)

単一のレプリカ セットが CPU/RAM/disk を最大にすると、次のようになります。

- Choose a **shard key** with high cardinality and even distribution — **hard to change later**.
- Bad key: monotonic `_id` only on one shard → hot shard.
- Good key: compound including tenant id + time, or hashed `_id`.

ほとんどのアプリは、メトリクスによって必要性が証明されるまで、**シャードなし**で開始されます。

## 7. 生産前のチェックリスト

- [ ] **レプリカ セット** または Atlas (スタンドアロンではない)
- [ ] 認証が有効です。アプリは最小権限のユーザーを使用します
- [ ] バックアップ + 文書化された復元ランブック
- [ ] 本番クエリパターンのインデックス
- [ ] すべてのアプリ インスタンスにわたる接続プールのサイズ
- [ ] ディスク上のアラート、レプリケーション ラグ、プライマリ フェールオーバー

## 関連メモ

- [Database optimizations](vii-database-optimizations.md) — slow query triage
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — caching, read scaling
- [Postgres operations](../postgres/vi-operations-and-backups.md) — parallel ops mindset for polyglot stacks
