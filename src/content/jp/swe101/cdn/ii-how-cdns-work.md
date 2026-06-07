---
label: "II"
subtitle: "CDN の仕組み"
group: "CDN"
order: 2
---
CDN — CDN の仕組み

CDN は、**オリジン**の前にある**分散キャッシュ**です。ユーザーは最寄りの **PoP (Point of Presence)** と通話します。 **ミス**の場合、PoP はオリジンから一度フェッチし、後のリクエストに備えて応答を保存します。

## 1. リクエスト フロー (CDN をプル)

```text
1. Browser GET https://cdn.example.com/assets/app.a1b2c3.js
2. DNS returns CDN edge IP (Anycast or geo-routed)
3. Edge checks cache for that URL (+ cache key rules)
4. HIT  → 200 from edge (fast)
5. MISS → edge GET from origin → store with TTL → 200 to user
6. Next user in same region → HIT
```

|用語 |意味 |
|-----|----------|
| **PoP / エッジ** |都市/地域の CDN サーバー |
| **起源** |バケット、サーバー、またはロード バランサー |
| **キャッシュ ヒット** |エッジは原点に接触せずに機能します |
| **キャッシュミス** |エッジはオリジンからフェッチし、キャッシュします。
| **TTL** |再検証するまでエッジがコピーを保持する期間 |

Same mental model as [CDN & edge caching](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md).

## 2. DNS ルーティング

| Method | Behavior |
|--------|----------|
| **CNAME to CDN** | `cdn.example.com` → `d111111.cloudfront.net` |
| **Anycast** | One IP; BGP routes to nearest PoP |
| **Geo DNS** | Different answers by user continent |

ユーザーは PoP を選択しません。CDN DNS/ネットワーク層が選択します。

## 3. プルとプッシュ

| | **プル** (ほとんどの Web アプリ) | **プッシュ** |
|---|--------------------------|----------|
| **方法** | CDN は、ミス時にオリジンからフェッチします。ファイルを CDN ストレージにアップロードします。
| **起源** | S3、nginx、ALB、カスタム サーバー | CDN バケット (例: S3 オリジン + OAI、またはプッシュ ゾーン) |
| **コールドスタート** |地域の最初の訪問者が遅くなる |発売前に事前アップロード |
| **こんな用途に最適** |サイト、キャッシュ ヘッダーのある API |大規模なダウンロード、ライブ イベントのシーディング |

最新のセットアップは、オブジェクト ストレージ オリジン (S3 + CloudFront、GCS + Cloud CDN) を使用した **プル** です。

## 4. キャッシュキー

Edge は応答を **キャッシュ キー** に保存します。必ずしも「URL のみ」であるとは限りません。

```text
Default key:  host + path + query string (provider-specific)
Custom key:   include/exclude query params, headers, cookies
```

キーの設定が間違っていると、次のような原因が発生します。

- **間違ったコンテンツ** - 同じ URL、異なるユーザーが同じキャッシュされた JSON を取得します
- **低ヒット率** — ランダムなクエリパラメータにより毎回キャッシュが無効になります

Configure **which query params** matter (`?v=3` yes, `?utm_source=` no).

## 5. TLS の終了

```text
User ──HTTPS──► CDN edge (public cert for cdn.example.com)
                    └──HTTPS or HTTP──► origin (can use private cert)
```

CDN は、ユーザーが信頼する **公開証明書** を保持します。オリジンは、VPC 内の HTTP (署名付きリクエストあり) または HTTPS にすることができます。プロバイダーのドキュメントは異なります (**オリジン アクセス コントロール**、**署名付き URL**)。

## 6. オリジンシールド（オプション）

一部の CDN は、多くの PoP とオリジンの間に **地域中間層キャッシュ** を追加します。これにより、1 つのファイルが世界的に広まったときにオリジンのヒットが減少します。

## 7. __​​IT0__ が実行しないこと

| Not CDN’s job | Where instead |
|---------------|---------------|
| Run your Java/Python API logic | App servers, serverless |
| Replace database | Postgres, MongoDB |
| Session storage | [Redis](../redis/iv-patterns-and-use-cases.md) |
| Write operations | POST always to origin |

＃＃ 次

Continue with [Cache headers & TTL](iii-cache-headers-and-ttl.md) to control what gets stored and for how long.
