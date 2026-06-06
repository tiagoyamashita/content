---
label: "IV"
subtitle: "パターンと使用例"
group: "レディス"
order: 4
---
Redis — パターンとユースケース

本番環境での Redis の使用は、いくつかの**反復可能なパターン**に重点を置いています。それぞれは、注記がない限り、耐久性ストア ([Postgres](../postgres/i-overview.md)、[MongoDB](../mongodb/i-overview.md)) が信頼できる情報源を保持していることを前提としています。

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

|落とし穴 |修正 |
|----------|-----|
| **古いキャッシュ** |書き込み時に無効化します。または短い TTL + 古いことを受け入れる |
| **雷鳴の群れ** | 1 人のワーカーが再構築している間、キー `SET lock:… NX EX` をロックします。
| **キャッシュ null** | DB を保護するためのキャッシュ不足が「見つかりません」 |

**TTL** を鮮度のニーズに応じて定義します (製品カタログ 10 分、ユーザー プロファイル 1 分、構成 5 秒)。

## 2. セッションストア

Web アプリは **セッション ID** を Cookie に保存します。サーバーは Redis に BLOB を保存します。

```text
SET session:sess_abc123 "{\"userId\":42,\"roles\":[\"user\"]}" EX 86400
GET session:sess_abc123
DEL session:sess_abc123    # logout
```

利点: スティッキーセッションなしの**水平スケール**。 **DEL** による即時ログアウト。

Spring Session Redis および同様のライブラリは、シリアル化と Cookie ワイヤリングを処理します。「アプリの統合」(v-app-integration.md) を参照してください。

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
| **作業が完了する前にロックの有効期限が切れます** |ウォッチドッグで TTL を延長します。タスクを短くする |
| **間違ったホルダーのロックを解除** |トークンの値を比較します。 Redisson スタイルのライブラリを使用する |
| **スプリット ブレイン** | Redlock については議論が行われています。可能であれば、DB 制約または単一コンシューマのキューを推奨します。

ロックは慎重に使用してください。Postgres の **冪等** ジョブと **一意の制約** は、分散ロックよりも優れていることがよくあります。

## 5. パブリッシュ/サブスクライブ

ファイアアンドフォーゲットブロードキャスト — 耐久性がない:

```text
SUBSCRIBE notifications
PUBLISH notifications "{\"type\":\"deploy\",\"env\":\"staging\"}"
```

購読者はオンラインである必要があります。メッセージは再生されません。耐久性のあるファンアウトを実現するには、**Streams**、Kafka、または SQS を使用します。

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

Pub/sub **`CONFIG`** チャネルを使用してアプリに更新を通知するか、アプリ メモリ内の短い TTL キャッシュを使用してポーリングします。

## 8. Redis に入れてはいけないもの

|避ける |代わりに使用してください |
|------|-----------|
|財務記録の唯一のコピー | Postgres + 監査ログ |
|大きな BLOB (> 数 MB) |オブジェクトストレージ (S3) |
|エンティティにわたる複雑なクエリ | SQL / MongoDB |
|長期的な分析 |倉庫 |

＃＃ 次

Lettuce、Spring Data Redis、redis-py の [アプリ統合](v-app-integration.md) に進みます。
