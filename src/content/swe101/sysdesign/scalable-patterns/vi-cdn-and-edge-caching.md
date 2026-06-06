---
label: "VI"
subtitle: "CDN とエッジ キャッシュ"
group: "システム設計"
order: 6
---
CDN とエッジ キャッシュ

**CDN (コンテンツ配信ネットワーク)** は、ユーザーの近くの **エッジ PoP** にコンテンツをキャッシュします。これにより、オリジンの遅延と負荷が軽減されます。

## 1. リクエストの流れ

<figure class="notes-diagram"><svg xmlns="10 viewBox="0 0 480 120" role="img" aria-label="CDN cache hit vs miss to origin">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">CDN pull model</text>
  <rect x="12" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="60" fill="#e4e4e7" font-size="9">User EU</text>
  <path d="M68 56 H108" stroke="#86efac" stroke-width="1.5"/>
  <rect x="108" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.15)" stroke="#fbbf24"/>
  <text x="118" y="56" fill="#fbbf24" font-size="8" font-weight="600">Edge PoP</text>
  <text x="118" y="68" fill="#86efac" font-size="7">HIT → fast</text>
  <path d="M172 56 H212" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="212" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="220" y="60" fill="#e4e4e7" font-size="9">Origin</text>
  <text x="108" y="92" fill="#a1a1aa" font-size="9">MISS: PoP fetches once, caches with TTL, serves next user from edge</text>
</svg></figure>

|ステップ |イベント |
|------|----------|
| 1 |クライアントのリクエスト `cdn.example.com/app.v3.js` |
| 2 | DNS は **最も近い PoP** (エニーキャストまたは地域 DNS) に解決されます。
| 3 | **キャッシュ ヒット** → エッジから戻る |
| 4 | **キャッシュミス** → **オリジン**からPoP GET → 保存 → 応答 |

## 2. CDN に属するもの

|資産タイプ |キャッシュ可能性 |メモ |
|-----------|--------------|------|
|静的JS/CSS/画像 |高 |長い TTL + バージョン付き URL |
|ビデオセグメント |高 | HLS/DASH チャンク |
|パブリック API GET |中 |短い TTL。認証ヘッダーを監視する |
|パーソナライズされた HTML |低い | `Vary: Cookie` またはバイパス CDN |
|投稿/挿入/削除 |いいえ |原点にパススルー |

## 3. キャッシュ制御

|メカニズム |どのように |いつ |
|-----------|-----|------|
| **TTL** | `Cache-Control: max-age=3600` |デフォルト;古いことを受け入れるウィンドウ |
| **バージョン付き URL** | `/app.v3.js` vs `/app.v2.js` |永遠に不変の資産 |
| **API をパージ** |すべての PoP で URL を無効にする |緊急のセキュリティ修正 |
| **再検証中に失効する** |新鮮なものを取り出しながら、古くなったものを提供する |スムーズなトラフィックスパイク |

## 4. プル CDN とプッシュ CDN

| |プル |プッシュ |
|---|------|------|
|セットアップ |発信元の URL; CDN はミス時にフェッチします。 CDN ストレージにアップロードします |
|コールドスタート |リージョン内の最初のユーザーの速度が遅い |起動前に事前にウォームアップ |
|使用 | Web アプリ、キャッシュ ヘッダーを備えた API |大容量ファイルの配布、ライブイベント |

## 5. 無効化戦略

```text
Immutable:  /assets/logo.a1b2c3.png     max-age=31536000, immutable
HTML shell: /index.html                 max-age=60, must-revalidate
API:        /v1/public/config         max-age=300 + ETag
```

**キャッシュキー**には、URL + 関連ヘッダーが含まれます(`Accept-Language`、`Authorization`は通常、パブリックキャッシュから**除外**)。

## 6. 落とし穴

|落とし穴 |修正 |
|----------|-----|
|プライベート データのキャッシュ | `Cache-Control: private` または無店舗 |
|クエリ文字列は無視されました | `?v=` | を含むようにキャッシュ キーを構成します。
|エッジでの HTTPS 証明書 | CDN は TLS を終了します。発信元証明書は非公開にすることができます。
|動的な地理コンテンツ |エッジ ワーカー / 短い TTL |

**関連:** パート I (キャッシュ層)、ネットワーキング DNS/地域 (パート IV ～ V)。
