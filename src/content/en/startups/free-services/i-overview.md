---
label: "I"
subtitle: "Overview"
group: "Startups"
order: 1
---
Free services — overview
Curated **free tiers** useful for an early-stage product. Limits change — always check the vendor site before relying on a number in production.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Email & mailing](ii-email-and-mailing.md) | Transactional email, newsletters, DNS — **start here** |
| [Hosting, domains & CDN](iii-hosting-domains-and-cdn.md) | Static sites, serverless, DNS, TLS |
| [Database, auth & storage](iv-database-auth-and-storage.md) | Postgres, auth, files, secrets |
| [Monitoring, analytics & devtools](v-monitoring-analytics-and-devtools.md) | Errors, uptime, analytics, CI |

## Do not run your own mail server

```text
❌  EC2 + Postfix on port 25  →  spam folder, blacklists, ops pain
✅  Resend / Brevo / SES API  →  they handle reputation + bounces
```

You still **own your domain** and add **SPF, DKIM, DMARC** records the provider gives you.

## Quick pick by need

| Need | Free starting point |
|------|---------------------|
| Password reset / welcome email | Resend, Brevo, SendGrid |
| Marketing newsletter | Brevo, MailerLite, Buttondown |
| Forward `hello@` to Gmail | Cloudflare Email Routing |
| Web app hosting | Vercel, Netlify, Cloudflare Pages |
| Database + auth | Supabase, Firebase |
| File uploads | Cloudflare R2 (free egress to CF), Supabase Storage |
| Error tracking | Sentry (dev tier), GlitchTip (self-host) |
| Uptime check | UptimeRobot, Better Stack free |

## Cost reality

| Usually free at MVP | Usually paid |
|---------------------|--------------|
| Hobby hosting, small DB | Custom domain email seats (Google Workspace) |
| Low email volume | High-volume mail, dedicated IP |
| Community support | Contract + SLA |

## Rehearsal

- Transactional vs marketing email — same provider?
- What three DNS records help email deliverability?
