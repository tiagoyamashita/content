---
label: "V"
subtitle: "静的資産と SPA"
group: "CDN"
order: 5
---
CDN — 静的資産と SPA

シングルページ アプリ (React、Vue、Svelte) には、**ハッシュされた静的ファイル** と小さな **HTML シェル**が同梱されています。 CDN は、静的レイヤーをグローバルに提供することに優れています。

## 1. 出力レイアウトを構築する

```text
dist/
  index.html              ← entry, short cache TTL
  assets/
    main-Dk3f9a2b.js      ← hashed, long TTL
    main-Cx8e1f0c.css
    logo-3f2a1b.png
```

Vite/Webpack/Next static export emit **content hashes** in filenames — safe **`immutable`** caching.

## 2. パイプラインをデプロイする

```text
git push tag v1.2.0
  → CI: npm run build
  → sync dist/assets/* to S3 with long Cache-Control
  → sync index.html with short Cache-Control
  → optional: invalidate /index.html only
  → users get new shell → load new hashed JS
```

```bash
# Long cache for hashed assets
aws s3 sync dist/assets/ s3://bucket/assets/ \
  --cache-control "public,max-age=31536000,immutable"

# Short cache for shell
aws s3 cp dist/index.html s3://bucket/index.html \
  --cache-control "public,max-age=60,must-revalidate" \
  --content-type "text/html"
```

## 3. デプロイ時にすべてをパージしないのはなぜですか

| Approach | Downside |
|----------|----------|
| Purge `/*` | Origin spike; slower global rollout |
| Versioned filenames | Old JS stays cached but unused — **preferred** |
| Same `/app.js` forever | Users on stale code until purge |

Only **`index.html`** (and service worker, if any) needs frequent invalidation.

## 4. サービスワーカー (PWA)

Service Worker は積極的にキャッシュします。**ブラウザーで CDN** をオーバーライドできます。

| Practice | Why |
|----------|-----|
| Version SW file name or hash | Force update on deploy |
| `skipWaiting` + `clients.claim` | Careful — understand UX |
| Cache bust on activate | Delete old caches |

SW が正しく構成されていないと、CDN がパージされているにもかかわらず、「デプロイされているがユーザーに古いアプリが表示される」という問題が発生します。

## 5. 画像とメディア

| Type | CDN pattern |
|------|-------------|
| **Responsive images** | `srcset` same CDN; multiple widths in `/assets/` |
| **Video** | HLS/DASH segments — each `.ts` chunk long TTL |
| **User uploads** | Separate origin/path; shorter TTL; auth via signed URLs |

ビルド時または CDN **イメージ最適化** (Cloudflare Polish、CloudFront イメージ ハンドラー) 経由で、最新の形式 (**WebP**、**AVIF**) を使用します。

## 6. 圧縮

CDN またはオリジンで **Brotli/gzip** を有効にします。

```http
Content-Encoding: br
Vary: Accept-Encoding
```

キャッシュ キーには **エンコーディング** が含まれている必要があります。そうでない場合、gzip クライアントは br バイトを取得します。

## 7. サブリソースの整合性 (オプション)

CDN のサードパーティ スクリプトの場合:

```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-…"
        crossorigin="anonymous"></script>
```

SRI はファイルの内容を検証します。サプライ チェーンに適しています。独自のハッシュ化されたアセットはすでに URL によって固定されています。

## 8. プラットフォーム管理の CDN

|プラットフォーム |あなたが管理します |
|----------|-----------|
| **Vercel / Netlify / CF ページ** | Git プッシュ;プラットフォームはヘッダーを設定します。
| **S3 + CloudFront** |フル コントロール — ヘッダー、無効化、OAC |

マネージド プラットフォームにはベスト プラクティスがコード化されています。カスタム S3+CDN は、基礎となるノブを教えます。

＃＃ 次

Continue with [APIs & dynamic content](vi-apis-and-dynamic-content.md) for cacheable GET endpoints and edge logic.
