---
label: "VII"
subtitle: "パフォーマンスと最適化"
group: "Redis"
order: 7
---
Redis — パフォーマンスと最適化






Redis はすでに高速です。最適化は、*ラウンドトリップの減少**、*適切なサイズの値**、*メモリ**、**ホットキーの回避**に重点を置いています。パターンは [パターンと使用例] にあります(iv-patterns-and-use-cases.md); [データベース最適化 (Postgres)]( での SQL 側のチューニング../postgres/vii-database-optimizations.md）。

## 1. 最適化ワークフロー

```text
1. Measure latency     (app metrics, Redis SLOWLOG, latency doctor)
2. Count round trips   (one request → how many commands?)
3. Shrink values       (compression, hash vs JSON blob)
4. Fix hot keys        (shard, local cache, read replicas)
5. Tune memory/eviction
6. Re-measure under load
```

```text
SLOWLOG GET 10
LATENCY DOCTOR
INFO stats    # keyspace hits/misses if tracked
```

## 2. ラウンドトリップが主流

パイプライン化されていない限り、各コマンドはネットワーク RTT に支払います。

|アンチパターン |修正 |
|--------------|-----|
|のループ`GET`アプリ内 | **`MGET`** またはパイプライン |
|のループ`SET`| **`MSET`** またはパイプライン |
| N 個の連続した待機 |パイプライン/トランザクションによるバッチ |

```text
MGET cache:product:1 cache:product:2 cache:product:3
```

春： **`RedisTemplate.executePipelined`**。 Python: **`pipeline()`**。

一括キャッシュ読み取りの対象は、数百の連続呼び出しではなく、**リクエストごとに 1 つのパイプライン** です。

## 3. メモリの最適化

|テクニック |詳細 |
|----------|----------|
| **短いキー** |`c:p:8812`vs 200 文字のキー — 合計すると何百万ものキーになります |
| **オブジェクトのハッシュ** |多くの場合、小さなオブジェクトの場合は JSON 文字列よりもメモリ効率が高くなります。
| **TTL どこでも** |キャッシュキーの有効期限が切れる必要がある - 無制限の増加を防ぐ |
| **大きな値を圧縮** |以前のアプリの Snappy/LZ4`SET`— CPU と RAM のトレードオフ |
| **`UNLINK`対`DEL`** |大きな値に対して非同期は発生しません (非ブロッキング) |

大きなキーを検査します (開発/ステージング):

```text
redis-cli --bigkeys
MEMORY USAGE cache:product:8812
```

## 4. ホットキーの問題

1 つのキー (ウイルス製品、グローバル カウンター) がクラスター内の単一の Redis コアを飽和させます。

|緩和 |アイデア |
|-----------|------|
| **ローカルのインプロセス キャッシュ** |最もホットなキーの Redis の前にカフェイン/グアバ |
| **スプリットカウンター** |`INCR views:8812:shard0`…`shardN`— アプリ内の合計 |
| **リードレプリカ** | GET 負荷を分散する — ラグを受け入れる |
| **事前計算** |バックグラウンド ジョブが実体化されたキャッシュ キーを書き込む |

## 5. キャッシュヒット率

アプリケーションで追跡:

```text
hit_rate = cache_hits / (cache_hits + cache_misses)
```

|ヒット率が低い原因 |修正 |
|---------------------|-----|
| TTL が短すぎます |古い場合は増加します OK |
|ランダム ID ごとのキー |ホットエンティティのみをキャッシュする |
|無効化が積極的すぎる |特定のキーを無効にするのではなく、`FLUSHDB`|
|間違ったレイヤー | 1 回限りのクエリをキャッシュしない |

## 6. 慎重に使用するコマンド

|コマンド |リスク |
|-------|------|
| **`KEYS pattern`** | O(N) — ブロック — ** を使用`SCAN`** |
| **`FLUSHALL`/`FLUSHDB`** |生産停止 |
| **`MONITOR`** |サーバーが遅くなる |
| **`SMEMBERS`巨大なセット** |大きな応答 - ** でページ付けする`SSCAN`** |
| **`LRANGE`膨大なリスト** |同じ — 範囲を使用する |

## 7. クラスターとハッシュタグ

マルチキー操作にはクラスター内の同じスロットが必要です。

```text
{user:42}:profile
{user:42}:sessions
```

中括弧 **`{user:42}`** 同じハッシュ スロットを強制します — アトミックなマルチキー操作が必要な場合のみ。

## 8. Redis がボトルネックではない場合

DB書き込みが優勢な場合:

- 最適化 [Postgres](../postgres/vii-database-optimizations.md) または [MongoDB](../mongodb/vii-database-optimizations.md） 初め。
- **測定後**にキャッシュを追加します。キャッシュが早期に行われると、無効化のバグが追加されます。

## 9. チェックリスト

- [ ] パイプライン /`MGET`一括読み取り用
- すべてのキャッシュ キーの [ ] TTL
- [ ] **`maxmemory`** + エビクションポリシーセット
- [ ] いいえ`KEYS`製品コード内で
- [ ] 遅いログを監視しています
- [ ] 負荷テストでホットキーが特定されました
- [ ] Redis が利用できない場合のフォールバック パス (DB に低下)
- [ ] セッション/キャッシュ回復計画が文書化されました ([操作](vi-operations-and-persistence.md))

## 関連メモ

- [キーと値のストア](../../CS101/databases/iii-key-value.md) — 概念的なパターン
- [パターンと使用例](iv-patterns-and-use-cases.md) — キャッシュアサイド、レート制限
- [データベースの最適化 (MongoDB)](../mongodb/vii-database-optimizations.md) — ドキュメント ストアのチューニング
