---
label: "IV"
subtitle: "セットアップと原点"
group: "CDN"
order: 4
---
CDN — セットアップと原点

**オリジン**を選択し、**ディストリビューション**を作成し、**DNS**をポイントし、CDNのみがプライベート バケットをフェッチできるようにオリジン アクセスをロックすることにより、CDNを接続します。

## 1. 一般的なアーキテクチャ

```text
                    ┌─────────────┐
  cdn.example.com   │  CloudFront │─── OAI/OAC ───► S3 bucket (private)
  (or CF proxy)     │  / CF / etc │
                    └──────┬──────┘
                           │ cache miss
                    ┌──────▼──────┐
                    │ ALB / app   │  (optional second origin for API)
                    └─────────────┘
```

|原点タイプ |使用 |
|---------------|-----|
| **S3 / GCS / R2** |静的サイト、構築された SPA、ダウンロード |
| **ロードバランサ** |動的アプリ、混合静的 + API |
| **カスタム ドメイン** | nginx、オリジンサーバー |
| **サーバーレス URL** | API Gateway、ラムダ関数 URL |

## 2. AWS CloudFront + S3 (パターン)

1. Create **private** S3 bucket with built assets.
2. Create **CloudFront distribution** — origin = bucket.
3. Enable **Origin Access Control (OAC)** — bucket policy allows only CloudFront.
4. Attach **ACM certificate** (us-east-1 for CloudFront) for `cdn.example.com`.
5. CNAME **`cdn.example.com`** → `dxxxxx.cloudfront.net`.

S3 オブジェクトのメタデータ:

```text
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

CI 経由でアップロード:

```bash
aws s3 sync dist/ s3://myapp-assets-prod/ --cache-control "public,max-age=31536000,immutable"
aws cloudfront create-invalidation --distribution-id E123456 --paths "/index.html"
```

## 3. クラウドフレア（パターン）

1. サイトをCloudflareに追加します — レジストラーのネームサーバー。
2. DNS レコード上の **オレンジ色のクラウド (プロキシ)** → CDN を経由するトラフィック。
3. **SSL/TLS** → オリジン証明書付きの完全 (厳密)。
4. **キャッシュ ルール** — パス TTL がオーバーライドされます。
5. **R2 + CDN** または、origin = サーバーの IP/ホスト名。

Free tier includes CDN + TLS — common for startups ([Hosting & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md)).

## 4. オリジンのセキュリティ

|メカニズム |目的 |
|----------|----------|
| **OAC / OAI (AWS)** | S3 は公共のインターネットではありません |
| **署名付き URL / Cookie** |プライベート オブジェクトへの時間制限付きアクセス |
| **オリジンシークレットヘッダー** | CDN はヘッダーを追加します。オリジンが他のものを拒否する |
| **IP 許可リスト** |オリジンは CDN 出力 IP のみを受け入れます。

爆発範囲を理解せずに、個人の資産を **パブリック** バケットに残さないでください。

## 5. 複数の起源/動作

1 つのディストリビューションでパスごとに分割します。

| Path | Origin | Cache |
|------|--------|-------|
| `/assets/*` | S3 | Long TTL |
| `/api/*` | ALB | Short or no cache |
| `/` | S3 `index.html` | Short TTL |

CloudFront **動作**、Cloudflare **ルール**、Fastly **条件** — 同じ考えです。

## 6. HTTPS と HSTS

- User → CDN: **TLS 1.2+**, modern ciphers.
- Enable **HSTS** at CDN once HTTPS stable: `Strict-Transport-Security: max-age=31536000`.
- Redirect HTTP → HTTPS at edge.

## 7. ローカル開発と本番環境の比較

| Environment | CDN |
|-------------|-----|
| **Localhost** | No CDN — Vite/webpack dev server |
| **Staging** | Separate distribution or prefix `staging-cdn.example.com` |
| **Production** | Full CDN; stricter cache on hashed assets only |

CURL を使用してキャッシュ ヘッダーをテストします。

```bash
curl -I https://cdn.example.com/assets/main.js
curl -I -H "Accept-Encoding: gzip" https://cdn.example.com/assets/main.js
```

Check **`Cache-Control`**, **`Age`** (time in CDN cache), **`X-Cache`** / **`CF-Cache-Status`** (provider-specific hit/miss).

＃＃ 次

Continue with [Static assets & SPAs](v-static-assets-and-spas.md) for build output and deploy pipelines.
