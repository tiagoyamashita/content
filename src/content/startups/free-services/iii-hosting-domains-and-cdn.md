---
label: "III"
subtitle: "ホスティング、ドメイン、CDN"
group: "スタートアップ"
order: 3
---
ホスティング、ドメイン、CDN

ほとんどの MVP には、**ドメイン**、**HTTPS**、および **フロントエンド** または **API** を実行する場所が必要です。これらの無料枠は、専用サーバーなしで初期のトラフィックをカバーします。

## 1. ドメイン名

|レジストラ |メモ |
|----------|----------|
| Cloudflareレジストラ |原価価格、無料の DNS との組み合わせ |
|名前安い、豚まん |初年度は安いことが多い |
| Google ドメイン → スクエアスペース |現在の製品を確認する |

Budget **~$10–15/year** for `.com` — rarely free except promotions.

## 2. DNS および TLS (無料)

| Service | Free includes |
|---------|---------------|
| **[Cloudflare](https://www.cloudflare.com)** | DNS, CDN, TLS, DDoS basics, Email Routing |
| Route 53 | Not free — pay per hosted zone |
| Registrar DNS | Often free with domain |

ネームサーバーをCloudflareに向けて→ A/CNAME/TXT (電子メールレコード) を 1 か所で管理します。

## 3. 静的およびフロントエンドのホスティング

| Platform | Free tier (typical) | Stack |
|----------|---------------------|-------|
| **[Vercel](https://vercel.com)** | Hobby projects | Next.js, static, serverless functions |
| **[Netlify](https://www.netlify.com)** | Starter | Static, functions, forms |
| **[Cloudflare Pages](https://pages.cloudflare.com)** | Generous | Static, Workers integration |
| **[GitHub Pages](https://pages.github.com)** | Public repos | Static only |

```text
git push main → auto build → https://yourapp.vercel.app
Custom domain: CNAME to provider + verify in dashboard
```

## 4. バックエンド / API ホスティング

| Platform | Free tier | Notes |
|----------|-----------|-------|
| **Vercel / Netlify functions** | Limited invocations | Good for light APIs |
| **[Railway](https://railway.app)** | Trial credit then usage | Full containers |
| **[Render](https://render.com)** | Free web service (sleeps) | Docker or native |
| **[Fly.io](https://fly.io)** | Small VM allowance | Global edge |
| **AWS Lambda + API Gateway** | Always-free tier limits | More setup |

コールド スタートと **アイドル状態でのスリープ**はデモでは許容されます。有料枠のないレイテンシーに敏感な製品には適していません。

## 5. CDN

Included with Cloudflare, Vercel, Netlify. Cache static assets; set **`Cache-Control`** headers. See system design **CDN** note for patterns.

## 6. チェックリスト

- [ ] Domain purchased
- [ ] DNS on Cloudflare (or provider)
- [ ] HTTPS working on custom domain
- [ ] Deploy hook from GitHub
- [ ] Staging subdomain (`staging.app.com`) optional

**Related:** [Email & mailing](ii-email-and-mailing.md) (DNS records), cloud foundations **edge**.
