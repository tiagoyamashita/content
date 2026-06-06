---
label: "IV"
subtitle: "セットアップと原点"
group: "CDN"
order: 4
---
CDN — セットアップとオリジン

**オリジン**を選択し、**ディストリビューション**を作成し、**DNS**をポイントし、CDNのみがプライベート バケットをフェッチできるようにオリジン アクセスをロックすることで CDN を接続します。

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
| **ロードバランサー** |動的アプリ、静的 + API の混合 |
| **カスタム ドメイン** | nginx、オリジンサーバー |
| **サーバーレス URL** | API ゲートウェイ、Lambda 関数 URL |

## 2. AWS CloudFront + S3 (パターン)

1. 構築されたアセットを含む **プライベート** S3 バケットを作成します。
2. **CloudFront ディストリビューション** — オリジン = バケットを作成します。
3. **オリジン アクセス コントロール (OAC)** を有効にする — バケット ポリシーは CloudFront のみを許可します。
4. **ACM 証明書** (CloudFront の場合は us-east-1) を `cdn.example.com` に添付します。
5. CNAME **`cdn.example.com`** → `dxxxxx.cloudfront.net`。

S3 オブジェクトのメタデータ:

```text
Content-Type: application/javascript
Cache-Control: public, max-age=31536000, immutable
```

CI経由でアップロード:

```bash
aws s3 sync dist/ s3://myapp-assets-prod/ --cache-control "public,max-age=31536000,immutable"
aws cloudfront create-invalidation --distribution-id E123456 --paths "/index.html"
```

## 3. クラウドフレア（パターン）

1. サイトをCloudflareに追加します — レジストラーのネームサーバー。
2. DNS レコード上の **オレンジ色のクラウド (プロキシ)** → CDN 経由のトラフィック。
3. **SSL/TLS** → オリジン証明書を使用した完全 (厳密)。
4. **キャッシュ ルール** — パス TTL の上書き。
5. **R2 + CDN** またはオリジン = サーバーの IP/ホスト名。

無料利用枠には CDN + TLS が含まれます。これはスタートアップに一般的です ([ホスティング & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md))。

## 4. オリジンのセキュリティ

|メカニズム |目的 |
|----------|----------|
| **OAC / OAI (AWS)** | S3 は公共のインターネットではありません |
| **署名付き URL / Cookie** |プライベート オブジェクトへの時間制限付きアクセス |
| **オリジンシークレットヘッダー** | CDN はヘッダーを追加します。オリジンが他のものを拒否する |
| **IP 許可リスト** |オリジンは CDN エグレス IP のみを受け入れます。

爆発範囲を理解せずに、個人の資産を **パブリック** バケットに残さないでください。

## 5. 複数の起源/動作

1 つのディストリビューション上でパスごとに分割します。

|パス |由来 |キャッシュ |
|------|--------|------|
| `/assets/*` | S3 |長い TTL |
| `/api/*` | ALB |キャッシュが不足しているかキャッシュがない |
| `/` | S3 `index.html` |短い TTL |

CloudFront **動作**、Cloudflare **ルール**、Fastly **条件** — 同じ考えです。

## 6. HTTPS と HSTS

- ユーザー → CDN: **TLS 1.2+**、最新の暗号。
- HTTPS が安定したら、CDN で **HSTS** を有効にします: `Strict-Transport-Security: max-age=31536000`。
- エッジで HTTP → HTTPS にリダイレクトします。

## 7. ローカル開発と本番環境の比較

|環境 | CDN |
|---------------|-----|
| **ローカルホスト** | CDN なし — Vite/webpack 開発サーバー |
| **ステージング** |個別のディストリビューションまたはプレフィックス `staging-cdn.example.com` |
| **生産** |完全な CDN。ハッシュ化されたアセットのみのキャッシュを厳格化 |

CURL を使用してキャッシュ ヘッダーをテストします。

```bash
curl -I https://cdn.example.com/assets/main.js
curl -I -H "Accept-Encoding: gzip" https://cdn.example.com/assets/main.js
```

**`Cache-Control`**、**`Age`** (CDN キャッシュ内の時間)、**`X-Cache`** / **`CF-Cache-Status`** (プロバイダー固有のヒット/ミス) を確認します。

＃＃ 次

[静的アセットと SPA](v-static-assets-and-spas.md) に進み、出力をビルドし、パイプラインをデプロイします。
