---
label: "III"
subtitle: "キャッシュヘッダーとTTL"
group: "CDN"
order: 3
---
CDN — キャッシュヘッダーと TTL

ブラウザと CDN は **HTTP キャッシュ ヘッダー** に基づいてキャッシュします。 **元の応答** (または CDN オーバーライド ルール) から動作を制御します。

## 1. コアヘッダー

|ヘッダー |意味 |
|--------|--------|
| **`Cache-Control: max-age=3600`** | CDN/ブラウザで 3600 秒間新鮮 |
| **`Cache-Control: public`** |共有キャッシュ (CDN) には |
| **`Cache-Control: private`** |エンドユーザーのブラウザのみ - CDN ではない |
| **`Cache-Control: no-store`** |キャッシュをまったく行わない |
| **`Cache-Control: no-cache`** |キャッシュしますが、使用前に再検証する必要があります |
| **`Cache-Control: immutable`** |コンテンツは変更されません (ハッシュ化された URL を使用) |
| **`ETag: "abc123"`** |条件付き GET のバリデータ |
| **`Last-Modified`** |時間ベースのバリデータ |

例 - 長期間存続する資産:

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

例 - API 構成:

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

**304** は帯域幅を節約します。オリジンは依然としてリクエストを取得します。新鮮さとオリジンの負荷のバランスを取るために TTL を調整します。

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

HTML は新しいハッシュを参照します。デプロイ時に JS/CSS に対して CDN パージは必要ありません。

## 4. HTML および SPA シェル

`index.html` often **should not** cache forever — it points at hashed assets:

```http
Cache-Control: public, max-age=60, must-revalidate
```

または：

```http
Cache-Control: no-cache
```

**`stale-while-revalidate`** — 新しい (スムーズなスパイク) を取得しながら、古い HTML を提供します。

```http
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

## 5. CDN の動作とオリジンヘッダーの比較

プロバイダーを使用すると、エッジで**オーバーライド**できます。

|ルール |例 |
|-----|----------|
|パスパターン | `/assets/*` → 1 年間 TTL |
|ファイルの種類 | `*.jpg` → 7日 |
|クエリ文字列 |キャッシュ キーの `utm_*` を無視する |
|オリジンにヘッダーがありません |デフォルトの TTL 86400 |

CDN を変更しても動作が一貫しているように、**オリジン** でヘッダーを設定することを優先します (S3 メタデータ、アプリのミドルウェア)。

## 6. 危険な間違い

|間違い |結果 |
|----------|---------------|
| `public, max-age=3600` に `/api/me` |ユーザー A のデータがユーザー B に提供される |
| `Set-Cookie` 応答のキャッシュ |壊れたセッション |
|キャッシュキーの `Authorization` を無視します |プライベート JSON が漏洩 |
|バージョン管理されていない `/app.js` での長い TTL |デプロイ後にユーザーが古いバンドルにスタックする |

デフォルトの機密ルートは **`Cache-Control: private, no-store`** です。

## 7. 早見表

|資産 |典型的なポリシー |
|------|----------------|
|ハッシュ化された JS/CSS | `public, max-age=31536000, immutable` |
|画像 (バージョン管理されたパス) | `public, max-age=604800` |
| `index.html` | `max-age=0, must-revalidate` または短い TTL |
|パブリック GET API | `public, max-age=60–300` + Eタグ |
|認証済み API | `private, no-store` |

＃＃ 次

CloudFront、Cloudflare、およびオリジンパターンの [セットアップとオリジン](iv-setup-and-origin.md) に進みます。
