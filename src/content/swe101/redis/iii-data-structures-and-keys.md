---
label: "III"
subtitle: "データ構造とキー"
group: "レディス"
order: 3
---
Redis — データ構造とキー

Redis 値は文字列だけではありません。アクセス パターンに一致する **タイプ** を選択してください。 **キー設計** と **TTL** は、[Key-value ストア](../../CS101/databases/iii-key-value.md) と同じくらい重要です。

## 1. キーの命名

**名前空間** プレフィックスを使用します。ログ内で読みやすく、grep に適しています。

```text
cache:product:8812
session:sess_abc123
ratelimit:api:192.168.1.1:2026051914
user:42:profile
```

|大会 |例 |
|-----------|-----------|
| **`:` セパレーター** |ネストされたフォルダーのない階層 |
| **安定した ID** |電子メールが変更された場合、`user:ada` ではなく `user:42` |
| **バージョンの接尾辞** | `cache:product:v2:8812` キャッシュの形状が変化するとき |

あいまいな名前 (`data`、`temp`、`x`) を持つ 1 つの巨大なキースペースは避けてください。

## 2. 文字列

デフォルトのタイプ — JSON BLOB、カウンター、フラグ:

```text
SET feature:dark_mode "on"
GET feature:dark_mode

SET page:home HTML_EX 300
INCR stats:pageviews:home
INCRBY stats:bytes:served 4096
```

**`SET` オプション:**

|オプション |意味 |
|--------|--------|
| **`EX seconds`** | TTL |
| **`NX`** |キーが見つからない場合にのみ設定 (ロック、重複排除) |
| **`XX`** |キーが存在する場合にのみ設定 |

```text
SET lock:job:import worker-1 NX EX 30
```

## 3. ハッシュ

1 つのキーの下のフィールド マップ — コンパクトなユーザー/セッション オブジェクト:

```text
HSET user:42 name Ada email ada@example.com plan pro
HGET user:42 email
HGETALL user:42
HMGET user:42 name email
HINCRBY cart:42 item_count 1
```

BLOB 全体を解析せずに個々のフィールドを更新する場合は、JSON 文字列よりも **ハッシュ** を優先します。

## 4. リスト

リンクされたリスト — キュー、最近のアイテム (境界付き):

```text
LPUSH events:recent "login" "purchase"
LRANGE events:recent 0 9
LTRIM events:recent 0 99    # keep last 100
```

**`BLPOP`** - 単純なワーカー キューのポップをブロックします (コンシューマ グループの **Streams** を考慮してください)。

## 5. セットとソートされたセット

**セット** — 一意のメンバー、タグ、プレゼンス:

```text
SADD online:users 42 99 101
SISMEMBER online:users 42
SMEMBERS online:users
```

**ソートセット (ZSET)** — スコア + メンバー — リーダーボード、時間順のランク:

```text
ZADD leaderboard 9850 "player:ada"
ZADD leaderboard 9200 "player:grace"
ZREVRANGE leaderboard 0 9 WITHSCORES
ZRANK leaderboard "player:ada"
```

|タイプ |使用 |
|------|-----|
| **設定** |独自タグ、相互フォロー（注意） |
| **ZSET** |タイムスタンプ スコア別の遅延ジョブのランキング |

## 6. TTL と有効期限

```text
SET session:tok EX 3600
EXPIRE cache:product:1 300
PERSIST session:tok          # remove TTL
TTL session:tok              # seconds remaining; -1 no TTL; -2 missing
```

**遅延 + 定期的** 有効期限 — 削除の正確な秒数に依存しないでください。キーが短時間残っても安全になるようにキーを設計します。

## 7. その他のタイプ (認識)

|タイプ |使用 |
|------|-----|
| **ストリーム** |ログ、コンシューマ グループ — [パターンと使用例](iv-patterns-and-use-cases.md) を参照してください。
| **ハイパーログログ** |おおよその一意のカウント |
| **ビットマップ** |ユーザー ID ごとの機能フラグ、毎日のアクティブ ビット |
| **地理** |位置半径のクエリ |

## 8. シリアル化

アプリがすでに JSON を話す場合は、**JSON** を文字列に保存します。

```text
SET cache:product:8812 "{\"title\":\"Keyboard\",\"price\":129.99}"
```

部分的な更新には **ハッシュ** を使用します。サイズが重要な場合は **MessagePack** を使用してください。サービス レイヤーでエンコーディングを必ず文書化してください。

＃＃ 次

キャッシュアサイド、セッション、およびレート制限については、[パターンと使用例](iv-patterns-and-use-cases.md) に進みます。
