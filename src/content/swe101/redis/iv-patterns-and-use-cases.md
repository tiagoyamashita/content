---
label: "IV"
subtitle: "パターンと使用例"
group: "Redis"
order: 4
---
Redis — パターンとユースケース


Production Redis usage centers on a few **repeatable patterns**. Each assumes a durable store ([Postgres](../postgres/i-overview.md), [MongoDB](../mongodb/i-overview.md)) holds source of truth unless noted.

## 1. キャッシュアサイド

```text
READ:
  1. GET cache:key
  2. hit  → return
  3. miss → load from DB → SET cache:key EX ttl → return

WRITE:
  1. UPDATE database
  2. DEL cache:key   (or SET new value)
```

```text
GET cache:product:8812
# miss
SET cache:product:8812 "{...json...}" EX 600
```

| Pitfall | Fix |
|---------|-----|
| **Stale cache** | Invalidate on write; or short TTL + accept staleness |
| **Thundering herd** | Lock key `SET lock:… NX EX` while one worker rebuilds |
| **Caching null** | Cache short “not found” to protect DB |

**TTL** を鮮度のニーズに応じて定義します (製品カタログ 10 分、ユーザー プロファイル 1 分、構成 5 秒)。

## 2. セッションストア

Web アプリは **セッション ID** を Cookie に保存します。サーバーは BLOB を Redis に保存します。

```text
SET session:sess_abc123 "{\"userId\":42,\"roles\":[\"user\"]}" EX 86400
GET session:sess_abc123
DEL session:sess_abc123    # logout
```

利点: スティッキーセッションなしの**水平スケール**。 **DEL** 経由で即時にログアウトします。

Spring Session Redis and similar libraries handle serialization and cookie wiring — see [App integration](v-app-integration.md).

## 3. レート制限

**固定ウィンドウ** — シンプル:

```text
INCR ratelimit:api:10.0.0.1:2026051914
EXPIRE ratelimit:api:10.0.0.1:2026051914 60
# if count > 100 → 429 Too Many Requests
```

**スライディング ウィンドウ** — スコアとしてタイムスタンプを含む **ソート セット**を使用し、古いエントリをトリミングし、メンバーをカウントします。 – より正確で、より複雑です。

API ゲートウェイの場合は、専用のリミッター (Kong、Envoy) を検討してください。Redis は依然としてアプリ層で一般的です。

## 4. 分散ロック（注意）

```text
SET lock:import:20260519 worker-7 NX EX 30
# do work
DEL lock:import:20260519   # only if value matches (use Lua script)
```

|リスク |緩和 |
|------|-----------|
| **作業が完了する前にロックの有効期限が切れます** | TTL をウォッチドッグで拡張します。タスクを短くする |
| **間違ったホルダーのロックを解除** |トークンの値を比較します。 Redisson スタイルのライブラリを使用する |
| **スプリット ブレイン** | Redlock については議論があります。可能であれば DB 制約を使用するか、単一のコンシューマでキューを作成することを推奨します。

ロックは慎重に使用してください。Postgres の **冪等** ジョブと **一意の制約** は、分散ロックよりも優れていることがよくあります。

## 5. パブリッシュ/サブスクライブ

ファイアアンドフォーゲットブロードキャスト — 耐久性がない:

```text
SUBSCRIBE notifications
PUBLISH notifications "{\"type\":\"deploy\",\"env\":\"staging\"}"
```

購読者はオンラインである必要があります。メッセージは再生されません。耐久性のあるファンアウトには、**Streams**、Kafka、または SQS を使用します。

## 6. ストリーム (軽量キュー)

```text
XADD jobs * type email to ada@example.com
XREAD COUNT 10 BLOCK 5000 STREAMS jobs 0
XGROUP CREATE jobs workers $ MKSTREAM
XREADGROUP GROUP workers consumer1 COUNT 1 STREAMS jobs >
XACK jobs workers <message-id>
```

消費者団体は、**少なくとも 1 回** ack 付きで配信します。これは、中程度のジョブ量に適しています。保留リストの長さを監視します。

## 7. 機能フラグと構成

```text
HSET config:flags dark_mode on beta_checkout off
HGET config:flags dark_mode
```

Pub/sub **`CONFIG`** channel to notify apps to refresh — or poll with short TTL cache in app memory.

## 8. Redis に入れてはいけないもの

|避ける |代わりに使用してください |
|------|-----------|
|財務記録の唯一のコピー | Postgres + 監査ログ |
|大きな BLOB (> 少数の MB) |オブジェクト ストレージ (S3) |
|エンティティにわたる複雑なクエリ | SQL / MongoDB |
|長期的な分析 |倉庫 |

＃＃ 次

Continue with [App integration](v-app-integration.md) for Lettuce, Spring Data Redis, and redis-py.
