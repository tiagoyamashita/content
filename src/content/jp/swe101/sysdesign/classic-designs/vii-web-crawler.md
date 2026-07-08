---
label: "VII"
subtitle: "ウェブクローラー"
group: "システム設計"
order: 7
---
ウェブクローラー

**検索エンジン スタイル** クローラー: URL を検出し、HTML を取得し、**インデックス パイプライン** をフィードし、**礼儀正しさ** ルールを尊重します。

## 1. コンポーネント

|コンポーネント |役割 |
|-----------|------|
| **URL フロンティア** |取得する URL の優先キュー |
| **フェッチャー** | HTTP GET; robots.txt、レート制限 |
| **パーサー** |リンク、テキスト、メタデータを抽出 |
| **重複フィルター** |表示された URL / 重複したコンテンツをスキップする |
| **ストレージ** |生の HTML → オブジェクト ストア。テキスト → 検索インデックス |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="Web crawler pipeline frontier fetch parse index">
  <rect x="12" y="44" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Frontier</text>
  <path d="M76 60 H116" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="116" y="44" width="56" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="128" y="64" fill="#e4e4e7" font-size="9">Fetcher</text>
  <path d="M172 60 H212" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="212" y="44" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="224" y="64" fill="#e4e4e7" font-size="9">Parser</text>
  <path d="M268 60 H308" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="308" y="44" width="56" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="320" y="64" fill="#e4e4e7" font-size="9">Index</text>
  <rect x="380" y="44" width="72" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="388" y="64" fill="#e4e4e7" font-size="9">S3 archive</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Crawl loop</text>
  <text x="12" y="96" fill="#71717a" font-size="9">New links → frontier · Bloom filter skips revisits</text>
</svg></figure>

## 2. 規模の見積もり

|メトリック |値 |
|------|------|
|インデックス付けされたページ | 1B |
|平均ページ サイズ | 100 KB |
|ストレージ | ~100 TB 生 HTML |
|持続的なクロール | 1B / (30×86400) ≈ **400 ページ/秒** |

## 3. 礼儀正しさ

| Rule | Implementation |
|------|----------------|
| **robots.txt** | Cache per host; honor `Disallow` |
| **Crawl-delay** | Min interval between requests to same host |
| **Per-domain limit** | Token bucket keyed by domain |

## 4. 分散フロンティア

**Consistent hash on domain** → one worker owns `example.com`:

|メリット | |
|----------|----------|
|ホストごとの集中レート制限 | |
|同じホストへの重複した同時フェッチはありません | |

優先順位: サイトマップ URL、PageRank、再クロールの鮮度シグナル。

## 5. 重複排除

|レイヤー |構造 |トレードオフ |
|------|-----------|-----------|
| **URL を確認しました** | **ブルーム フィルター** |小さな記憶。小さな誤検知 → フェッチされていない URL をスキップすることはほとんどありません |
| **内容はほぼ重複** | **シムハッシュ** |テンプレートの多いミラーを検出する |

ブルーム フィルター: 「絶対に見られない」または「おそらく見られる」 - 偽陰性なし。

## 6. 障害対応

- **429/503** → バックオフ + フロンティアの再キュー。
- **リダイレクト チェーン** → キャップの深さ;最後の URL を正規化します。
- **有害な URL** → 最大サイズ、タイムアウト、MIME 許可リスト。

**Related:** [Search systems](../scalable-patterns/v-search-systems.md), [Rate limiting](../scalable-patterns/iv-rate-limiting.md).
