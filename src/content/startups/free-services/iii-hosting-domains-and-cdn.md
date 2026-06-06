---
label: "III"
subtitle: "Hosting, domains & CDN"
group: "Startups"
order: 3
---
Hosting, domains & CDN
Most MVPs need a **domain**, **HTTPS**, and a place to run the **frontend** or **API**. These free tiers cover early traffic without a dedicated server.

## 1. Domain names

| Registrar | Notes |
|-----------|--------|
| Cloudflare Registrar | At-cost pricing, pairs with free DNS |
| Namecheap, Porkbun | Often cheap first year |
| Google Domains → Squarespace | Check current product |

Budget **~$10–15/year** for `.com` — rarely free except promotions.

## 2. DNS & TLS (free)

| Service | Free includes |
|---------|---------------|
| **[Cloudflare](https://www.cloudflare.com)** | DNS, CDN, TLS, DDoS basics, Email Routing |
| Route 53 | Not free — pay per hosted zone |
| Registrar DNS | Often free with domain |

Point nameservers to Cloudflare → manage A/CNAME/TXT (email records) in one place.

## 3. Static & frontend hosting

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

## 4. Backend / API hosting

| Platform | Free tier | Notes |
|----------|-----------|-------|
| **Vercel / Netlify functions** | Limited invocations | Good for light APIs |
| **[Railway](https://railway.app)** | Trial credit then usage | Full containers |
| **[Render](https://render.com)** | Free web service (sleeps) | Docker or native |
| **[Fly.io](https://fly.io)** | Small VM allowance | Global edge |
| **AWS Lambda + API Gateway** | Always-free tier limits | More setup |

Cold starts and **sleep on idle** are acceptable for demos; not for latency-sensitive prod without paid tier.

## 5. CDN

Included with Cloudflare, Vercel, Netlify. Cache static assets; set **`Cache-Control`** headers. See system design **CDN** note for patterns.

## 6. Checklist

- [ ] Domain purchased
- [ ] DNS on Cloudflare (or provider)
- [ ] HTTPS working on custom domain
- [ ] Deploy hook from GitHub
- [ ] Staging subdomain (`staging.app.com`) optional

**Related:** `ii-email-and-mailing.md` (DNS records), cloud foundations **edge**.
