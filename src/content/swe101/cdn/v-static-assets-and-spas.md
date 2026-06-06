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

Vite/Webpack/Next 静的エクスポートはファイル名に **コンテンツ ハッシュ**を生成します - 安全な **`immutable`** キャッシュ。

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

|アプローチ |マイナス面 |
|----------|----------|
|パージ `/*` |原点スパイク。世界的な展開が遅い |
|バージョン管理されたファイル名 |古い JS はキャッシュされたままですが、使用されません — **推奨** |
|永遠に同じ `/app.js` |パージされるまで古いコードを使用するユーザー |

頻繁な無効化が必要なのは **`index.html`** (およびサービス ワーカー (存在する場合)) のみです。

## 4. サービスワーカー (PWA)

Service Worker は積極的にキャッシュします。ブラウザーで **CDN** をオーバーライドできます。

|練習 |なぜ |
|----------|-----|
|バージョン SW ファイル名またはハッシュ |デプロイ時に更新を強制する |
| `skipWaiting` + `clients.claim` |注意 — UX を理解する |
|アクティブ化時のキャッシュバスト |古いキャッシュを削除する |

SW の構成が間違っていると、CDN のパージにもかかわらず「デプロイされているが、ユーザーには古いアプリが表示される」という問題が発生します。

## 5. 画像とメディア

|タイプ | CDN パターン |
|------|---------------|
| **レスポンシブ画像** | `srcset` 同じ CDN。 `/assets/` の複数の幅 |
| **ビデオ** | HLS/DASH セグメント - 各 `.ts` チャンク長の TTL |
| **ユーザーのアップロード** |起点とパスを分離します。 TTL が短い。署名付き URL による認証 |

ビルド時または CDN **画像最適化** (Cloudflare Polish、CloudFront 画像ハンドラー) 経由で最新の形式 (**WebP**、**AVIF**) を使用します。

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

SRI はファイルの内容を検証します。これはサプライ チェーンに適しています。独自のハッシュ化されたアセットは URL によってすでに固定されています。

## 8. プラットフォーム管理の CDN

|プラットフォーム |あなたが管理します |
|----------|-----------|
| **Vercel / Netlify / CF ページ** | Git プッシュ;プラットフォームはヘッダーを設定します。
| **S3 + CloudFront** |フルコントロール — ヘッダー、無効化、OAC |

マネージド プラットフォームにはベスト プラクティスがコード化されています。カスタム S3+CDN は基礎となるノブを教えます。

＃＃ 次

キャッシュ可能な GET エンドポイントとエッジ ロジックについては、[API と動的コンテンツ](vi-apis-and-dynamic-content.md) に進みます。
