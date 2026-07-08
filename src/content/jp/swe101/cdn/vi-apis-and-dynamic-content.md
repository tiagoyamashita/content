---
label: "VI"
subtitle: "API と動的コンテンツ"
group: "CDN"
order: 6
---
CDN — API と動的コンテンツ

すべての応答が CDN に属するわけではありませんが、**読み取り負荷の高いパブリック GET** (構成、製品カタログ スニペット、OG 画像) は、キャッシュ ルールが厳格な場合、レイテンシとオリジンの負荷を軽減できます。

## 1. キャッシュ可能な GET 基準

すべてが真実である (または意識的に受け入れられている) 必要があります。

- [ ] **No user-specific secrets** in body
- [ ] **Same URL → same bytes** for all users (or `Vary` is correct)
- [ ] **Stale window acceptable** for business
- [ ] **Origin sets explicit** `Cache-Control` (not accidental default)

```http
GET /v1/public/features HTTP/1.1

HTTP/1.1 200 OK
Cache-Control: public, max-age=120
Content-Type: application/json

{"darkMode":true,"minVersion":"2.1.0"}
```

## 2. キャッシュを行わない (デフォルト)

| Route | Header |
|-------|--------|
| `/api/me`, `/cart`, `/orders` | `Cache-Control: private, no-store` |
| Anything with **`Set-Cookie`** | `no-store` |
| POST/PUT/PATCH/DELETE | Not cacheable by HTTP spec |

Authenticate at origin; CDN passes **`Authorization`** through unless you design shared cache keys (usually **don’t** for private data).

## 3. `Vary` header

リクエストヘッダごとにレスポンスが異なる場合：

```http
Vary: Accept-Language
```

CDN は言語ごとに **個別のキャッシュ エントリ**を保存します。ヒット率は低下します。必要な場合にのみ使用してください。

| Header | Common use |
|--------|------------|
| **`Accept-Encoding`** | gzip vs br (often automatic) |
| **`Accept-Language`** | Localized JSON |
| **`Origin`** | CORS — usually not for CDN cache |

Avoid **`Vary: Cookie`** unless you fully understand cache fragmentation.

## 4. GraphQL と POST

デフォルト: **CDN-cache GraphQL POST** — 同じパス、異なる本体。

オプション:

- Public queries via **GET** with persisted query hash (niche)
- **Separate REST** read endpoints for cacheable public data
- Cache at **[Redis](../redis/iv-patterns-and-use-cases.md)** in app layer instead

## 5. パージと無効化

キャッシュされたコンテンツをすぐに削除する必要がある場合:

| Method | Use |
|--------|-----|
| **Path purge** | `/products/8812.json` — security fix, bad deploy |
| **Wildcard purge** | `/assets/*` — expensive; avoid habit |
| **Surrogate keys** (Fastly etc.) | Tag related URLs; purge by tag |
| **Version bump** | Prefer URL/version over purge for static |

```bash
# CloudFront example
aws cloudfront create-invalidation --distribution-id E123 --paths "/v1/public/config"
```

伝播は **世界中で瞬時に行われるわけではありません**。数秒から数分を計画してください。

## 6. エッジ ワーカー / エッジでの計算

PoP で軽量ロジックを実行します。

|プロバイダー |製品 |
|----------|----------|
|クラウドフレア |労働者 |
|早く |コンピューティング@エッジ |
|クラウドフロント | Lambda@Edge、CloudFront 関数 |

ユースケース: A/B ヘッダー、地域リダイレクト、エッジでのトークン検証、HTML 書き換え — **完全なデータベース アクセスではありません**。

エッジ機能を **ステートレス**かつ高速に保ちます (数ミリ秒未満 CPU 制限)。

## 7. 動的なサイトの高速化

一部の CDN **は、本体をキャッシュせずに、オリジンへの最適化されたパス (TCP チューニング、キープアライブ) を介して動的 HTML/API** をルーティングします。これにより、キャッシュのリスクなしでレイテンシーが軽減されます。

**キャッシュ**とは異なります - プロバイダーのドキュメントを読んでください (CloudFront「動的コンテンツ」、Cloudflare「Argo」)。

## 8. OG / ソーシャル プレビュー画像

生成された画像 URL は、適切な CDN 候補です。

```text
GET /og/product/8812.png   →  max-age=3600, purge on product update
```

オリジンでのミス時に生成するか、バッチで事前レンダリングします。

＃＃ 次

Continue with [Operations & troubleshooting](vii-operations-and-troubleshooting.md) for monitoring and debug checklist.
