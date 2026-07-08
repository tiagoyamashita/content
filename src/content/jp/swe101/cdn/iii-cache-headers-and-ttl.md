---
label: "III"
subtitle: "キャッシュヘッダーと TTL"
group: "CDN"
order: 3
---
CDN — キャッシュヘッダーと TTL

ブラウザと CDN のキャッシュは **HTTP キャッシュ ヘッダー** に基づいています。 **元の応答** (または CDN オーバーライド ルール) から動作を制御します。

## 1. コアヘッダー

| Header | Meaning |
|--------|---------|
| **`Cache-Control: max-age=3600`** | Fresh for 3600 seconds at CDN/browser |
| **`Cache-Control: public`** | Shared caches (CDN) may store |
| **`Cache-Control: private`** | Only end-user browser — not CDN |
| **`Cache-Control: no-store`** | Do not cache at all |
| **`Cache-Control: no-cache`** | Cache but must revalidate before use |
| **`Cache-Control: immutable`** | Content never changes (with hashed URL) |
| **`ETag: "abc123"`** | Validator for conditional GET |
| **`Last-Modified`** | Time-based validator |

例 - 長期間存続する資産:

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

例 — API 構成:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=300
ETag: "config-v7"
```

## 2. 再検証

TTL の有効期限が切れると、Edge は完全にダウンロードせずに **再検証**する場合があります。

```http
GET /v1/public/config HTTP/1.1
If-None-Match: "config-v7"

HTTP/1.1 304 Not Modified
```

**304** は帯域幅を節約します。オリジンは引き続きリクエストを取得します。TTL を調整して、鮮度とオリジンの負荷のバランスをとります。

## 3. バージョン管理された URL (静的アセットに最適)

パージする代わりに、新しいファイル名を送信します。

```text
/app.v2.js   →  max-age=1 year, immutable
/app.v3.js   →  new deploy; old cache harmless
```

ビルド ツールはハッシュを生成します。

```text
/assets/main-Dk3f9a2b.js
/assets/main-Cx8e1f0c.css
```

HTML は新しいハッシュを参照します。デプロイ時に JS/CSS に CDN パージは必要ありません。

## 4. HTML および SPA シェル

`index.html` often **should not** cache forever — it points at hashed assets:

```http
Cache-Control: public, max-age=60, must-revalidate
```

または：

```http
Cache-Control: no-cache
```

**`stale-while-revalidate`** — serve stale HTML while fetching fresh (smooth spikes):

```http
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

## 5. CDN の動作とオリジンヘッダーの比較

プロバイダーを使用すると、エッジで**オーバーライド**できます。

| Rule | Example |
|------|---------|
| Path pattern | `/assets/*` → 1 year TTL |
| File type | `*.jpg` → 7 days |
| Query string | Ignore `utm_*` in cache key |
| Origin missing headers | Default TTL 86400 |

**オリジン** でヘッダーを設定することを優先します (S3 メタデータ、アプリ ミドルウェア)。これにより、CDN を変更しても動作が一貫します。

## 6. 危険な間違い

| Mistake | Consequence |
|---------|-------------|
| `public, max-age=3600` on `/api/me` | User A’s data served to User B |
| Caching `Set-Cookie` responses | Broken sessions |
| Ignoring `Authorization` in cache key | Leaked private JSON |
| Long TTL on unversioned `/app.js` | Users stuck on old bundle after deploy |

Default sensitive routes to **`Cache-Control: private, no-store`**.

## 7. 早見表

| Asset | Typical policy |
|-------|----------------|
| Hashed JS/CSS | `public, max-age=31536000, immutable` |
| Images (versioned path) | `public, max-age=604800` |
| `index.html` | `max-age=0, must-revalidate` or short TTL |
| Public GET API | `public, max-age=60–300` + ETag |
| Authenticated API | `private, no-store` |

＃＃ 次

Continue with [Setup & origin](iv-setup-and-origin.md) for CloudFront, Cloudflare, and origin patterns.
