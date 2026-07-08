---
label: "VI"
subtitle: "操作と永続性"
group: "Redis"
order: 6
---
Redis — 操作と永続性

データが **メモリ内**にあるため、Redis は高速です。運用トラフィックの前に、**メモリ制限**、**永続性**、**高可用性**を計画してください。

## 1. メモリ管理

```text
INFO memory
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```

| Policy | Behavior when `maxmemory` reached |
|--------|-----------------------------------|
| **`noeviction`** | Writes fail — safe if Redis is required store |
| **`allkeys-lru`** | Evict any key — typical **cache** |
| **`volatile-lru`** | Evict keys with TTL only |
| **`allkeys-lfu`** | Evict least frequently used (Redis 4+) |

Set **`maxmemory`** below host RAM — leave headroom for OS and replication buffers.

## 2. RDB (スナップショット)

ポイントインタイムのバイナリ スナップショット:

```conf
# redis.conf
save 900 1      # if 1 key changed in 900 sec
save 300 10
save 60 10000
dbfilename dump.rdb
dir /data
```

| Pros | Cons |
|------|------|
| Compact backup file | Between snapshots, recent writes can be lost |
| Fast restarts | `SAVE` blocks; `BGSAVE` forks (copy-on-write memory spike) |

Copy **`dump.rdb`** for cold backup when traffic is low or after **`BGSAVE`**.

## 3. AOF (追加専用ファイル)

すべての書き込みをログに記録します - より耐久性があります:

```conf
appendonly yes
appendfsync everysec   # balance; always | everysec | no
auto-aof-rewrite-percentage 100
```

| `appendfsync` | Trade-off |
|---------------|-----------|
| **`always`** | Safest; slowest |
| **`everysec`** | At most ~1s loss on crash — common default |
| **`no`** | OS buffer — faster, riskier |

多くのチームは、マネージド Redis (ElastiCache、Redis クラウド) で **RDB + AOF** の両方を使用しています。

## 4. レプリケーション

```text
Primary (read/write)  ──stream──►  Replica (read, failover)
```

レプリカを構成します。

```conf
replicaof primary-host 6379
```

|使用 |メモ |
|-----|------|
| **読み取りスケーリング** |読み取り専用キャッシュの GET をレプリカにルーティング — レプリケーションの遅延を監視する |
| **フェイルオーバー** | Sentinel またはマネージド フェールオーバーはレプリカをプロモートします。

**レプリカ上のキャッシュ:** 古い読み取りの可能性があります。通常はキャッシュとして許容されます。不用意にロックしないでください。

## 5. センチネルとクラスター (認識)

| Mode | When |
|------|------|
| **Single instance** | Dev only |
| **Primary + replicas + Sentinel** | HA failover for one shard |
| **Redis Cluster** | Data sharded across nodes — key must hit same slot; multi-key ops need same hash tag `{user:42}:profile` |

ほとんどのアプリ キャッシュは、メモリが 1 台のマシンを超えるまで、**1 つのプライマリ + レプリカ**に適合します。

## 6. セキュリティ

- **`requirepass`** or **ACL users** — never expose Redis to public internet unauthenticated.
- **TLS** (`rediss://`) on managed services and between AZs when required.
- Disable **`FLUSHALL`**, **`CONFIG`** for app users via ACL.
- Bind **`127.0.0.1`** in dev; VPC security groups in cloud.

## 7. バックアップと復元

| Method | Steps |
|--------|--------|
| **RDB file** | Stop or `BGSAVE` → copy `dump.rdb` → restore to new instance data dir |
| **Managed snapshot** | ElastiCache/Redis Cloud automated backups + PITR where offered |
| **Rebuild from DB** | Cache empty → warm from Postgres — valid DR for cache-only data |

**復元のテスト** — 特にセッションを Redis に保存する場合 (ユーザーは損失時にログアウトします)。

## 8. モニタリングチェックリスト

- [ ] Memory usage vs **`maxmemory`**
- [ ] Evicted keys per second (`INFO stats`)
- [ ] Connected clients vs **`maxclients`**
- [ ] Replication lag (`INFO replication`)
- [ ] Slow log (`SLOWLOG GET 10`)
- [ ] Hit rate for cache (app metric: hits / (hits + misses))

## 関連メモ

- [Performance & optimizations](vii-performance-and-optimizations.md) — pipelines, hot keys
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — cache in system design
- [Postgres operations](../postgres/vi-operations-and-backups.md) — source-of-truth backup mindset
