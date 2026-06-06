---
label: "III"
subtitle: "ニュースフィードとタイムライン"
group: "システム設計"
order: 3
---
ニュースフィードとタイムライン

**Twitter / Instagram スタイル**のホーム タイムライン: **フォローしている**人の最近の投稿を時間またはスコアでランク付けして表示します。

## 1. 配信モデル

|モデル |ポスト上 |読み取り時 |こんな方に最適 |
|----------|-----------|----------|----------|
| **書き込み時のファンアウト (プッシュ)** |投稿 ID をすべてのフォロワーのフィード キャッシュに書き込みます |事前に構築されたリストを読み取る — O(1) |一般ユーザー、適度なフォロワー |
| **読み取り（プル）時のファンアウト** |投稿テーブルのみを書き込みます | N 人のフォロワーの投稿を結合 |ライトチープ。高価な本を読む |
| **ハイブリッド** |ほとんどの場合はプッシュします。有名人のためのプル |プッシュ キャッシュと有名人のプルをマージ |プロダクションソーシャルグラフ |

<figure class="notes-diagram"><svg xmlns="14 viewBox="0 0 460 130" role="img" aria-label="Fan-out on write vs hybrid with celebrity">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Fan-out on write (normal user)</text>
  <rect x="12" y="32" width="48" height="24" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="20" y="48" fill="#e4e4e7" font-size="8">Post</text>
  <path d="M60 44 H100" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="100" y="28" width="56" height="32" rx="2" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="108" y="48" fill="#e4e4e7" font-size="8">fan-out</text>
  <rect x="168" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="212" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="256" y="32" width="40" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="68" fill="#a1a1aa" font-size="8">follower feeds</text>
  <text x="12" y="92" fill="#fbbf24" font-size="9">Celebrity (10M followers): skip fan-out → fetch on read only</text>
</svg></figure>

## 2. 書き込み増幅

|フォロワー |ポストごとのファンアウト書き込み |
|----------|-----------|
| 500 | 500 Redis ZADD |
| 10M | 1,000 万回の書き込み — 受け入れられない |

**しきい値ルール:** `followers > X` (例: 10 K) の場合、**有名人**として扱います — プッシュ ファンアウトはありません。

## 3. データモデル

**投稿 (真実の情報源)**

|コラム |タイプ |
|------|------|
| `post_id` | BIGINT (スノーフレーク) |
| `author_id` |ビッグINT |
| `content` |テキスト |
| `media_ids` | JSON |
| `created_at` |タイムスタンプ |

**フィード キャッシュ (Redis)**

- キー: `feed:{user_id}`
- タイプ: **ソートセット** — メンバー = `post_id`、スコア = `created_at` エポック ミリ秒
- 最後の K エントリまでトリミング (例: 1000)

**グラフをたどる**

| `follower_id` | `followee_id` | `created_at` |

## 4. 読み取りパス (ハイブリッド)

```text
1. ZREVRANGE feed:{user_id} 0 49          → pushed posts
2. For each celebrity followee: fetch recent posts (cached)
3. Merge + dedupe + rank → return page
```

ページネーション: カーソル = `(score, post_id)` タプル。

## 5. スケール戦術

|コンポーネント |戦術 |
|----------|----------|
|ファンアウトワーカー |ポストイベントごとのキュー。バッチ Redis パイプライン |
|ホットユーザー |専用キャッシュ パーティション |
|ランク付けされたフィード |スコアを非同期で事前計算します。 ZSET に保存 |

**関連:** スケーラブルなパターン [メッセージ キューと非同期](../scalable-patterns/iii-message-queues-and-async.md)、パート I Redis。
