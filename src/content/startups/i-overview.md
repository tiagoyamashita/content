---
label: "I"
subtitle: "Overview"
group: "Startups"
order: 1
---
Startups — overview
Practical notes for **building a company on a budget**: free tiers, sensible defaults, and when to pay. Assumes you can write code and deploy — not legal or fundraising advice.

## Map of this track

| Submenu / note | Focus |
|----------------|--------|
| **Free services** | Email, hosting, DB, auth, monitoring on $0 tiers |
| *(future)* | Incorporation checklist, MVP scope, go-to-market |

Start here: **Free services** → `free-services/i-overview.md`.

## Principles

| Principle | Why |
|-----------|-----|
| **Don't self-host email on day one** | Deliverability (SPF/DKIM/DMARC) is hard; use a transactional provider |
| **Use managed free tiers** | Your time is the scarce resource |
| **Tag resources by project** | Know what to delete when an experiment ends |
| **Read ToS and limits** | "Free" often means caps, not unlimited production |
| **Plan the upgrade path** | Pick services that scale without a rewrite |

## Typical zero-cost MVP stack

```text
Domain (paid ~$10/yr) + Cloudflare DNS (free)
  → Vercel / Cloudflare Pages (free hosting)
  → Supabase or Firebase (free DB + auth)
  → Resend / Brevo (free transactional email)
  → GitHub (free private repos) + Actions minutes
  → Sentry / UptimeRobot (free errors + uptime)
```

You still pay for a **domain name**; almost everything else can start at $0.

## When free tiers break

| Signal | Action |
|--------|--------|
| Email bounces or spam folder | Verify DNS records; warm domain; upgrade plan |
| DB size or connection limits | Paid tier or dedicated instance |
| Need SLA or support | Move to paid / enterprise |
| Compliance (HIPAA, etc.) | Free tiers usually exclude — pick compliant vendors |

**Related:** CI/CD **Tools & platforms**, cloud **Foundations**, **Terraform** for later infra.
