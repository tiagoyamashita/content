---
label: "VI"
subtitle: "データベース"
group: "システム設計"
order: 6
---
データベースのボトルネック

**データベース**は、Web システムで最も一般的なボトルネックです (読み取り、書き込み、ロック、**接続プール**)。

## 1. 読み取りのボトルネック

| Problem | Signal | Fix |
|---------|--------|-----|
| Full table scan | `EXPLAIN` → Seq Scan | Index on predicates |
| **N+1 queries** | ORM: 1 + N queries | JOIN, batch `IN`, DataLoader |
| Replica lag | Stale reads on replica | Critical reads → primary; monitor lag |
| Long transactions block reads | Lock waits | Short txs; READ COMMITTED / MVCC |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="N plus 1 query problem vs batched query">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">N+1 vs batch</text>
  <text x="12" y="38" fill="#f87171" font-size="9">1 query parents + N queries children</text>
  <text x="12" y="54" fill="#86efac" font-size="9">1 query parents + 1 WHERE id IN (...)</text>
  <text x="12" y="78" fill="#71717a" font-size="9">ORM lazy load is a common hidden bottleneck</text>
</svg></figure>

## 2. 書き込みのボトルネック

|問題 |修正 |
|----------|-----|
|単一プライマリ上限 (~10K ～ 50K 書き込み/秒 Postgres) |シャード;非同期キュー; CQRS |
|インデックス書き込み増幅 |インデックスが少なくなります。部分インデックス |
|デッドロック |一貫したロック順序。楽観的ロック (CAS) |
| WAL / ディスク |より高速なストレージ。チェックポイントを調整する |

## 3. 接続プールの枯渇

```text
500 pods × 10 connections = 5 000  →  DB max_connections = 100  →  crash
```

|修正 |役割 |
|-----|------|
| **PgBouncer** / **RDS プロキシ** |多数のアプリ接続 → 少数の DB 接続を多重化 |
|適切なサイズのプール |経験則: ~(2 × CPU コア) + インスタンスあたりのディスク スピンドル |
|短いクエリ |すぐに接続を解除してください |

## 4. クエリ最適化チェックリスト

- [ ] `EXPLAIN (ANALYZE, BUFFERS)` on slow queries
- [ ] Composite index for multi-column WHERE / ORDER BY
- [ ] **Covering index** — index-only scan
- [ ] **Partial index** — `WHERE active = true`
- [ ] Materialised view for heavy aggregates
- [ ] **Partition** by date for prune + archival

## 5. インデックスが追加されましたが、まだ遅いですか?

| Check | |
|-------|---|
| Wrong column order in composite index | |
| Function on column (`WHERE LOWER(email)`) — needs expression index | |
| Statistics stale — `ANALYZE` | |
| Row count wrong estimate — increase stats target | |
| Sort spills to disk — work_mem / index for ORDER BY | |
| Lock wait, not query plan | |

## 6. 読み取りと書き込みのスケーリング パス

|パス |いつ |
|------|----------|
|リードレプリカ |読み取りが多い。ラグを許容する |
|キャッシュ (Redis) |ホットキー、繰り返し読み取り |
|シャーディング |書き込みスケールが単一プライマリを超える |
|非正規化 |読み取りパスが安くなります。複雑さを書き出す |

**Related:** [Core building blocks](../i-core-building-blocks.md) (replication), [Database sharding](../scalable-patterns/ix-database-sharding.md), [Application-level](vii-application-level.md) (hot partition).
