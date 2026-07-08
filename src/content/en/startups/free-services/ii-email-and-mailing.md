---
label: "II"
subtitle: "Email & mailing"
group: "Startups"
order: 2
---
Email & mailing
For a startup, **email** means two jobs: **transactional** (password reset, receipts, alerts) and **marketing** (newsletters, announcements). Use an **API provider** — not a self-hosted SMTP server on a VPS.

## 1. Transactional vs marketing

| Type | Trigger | Examples | Requirements |
|------|---------|----------|--------------|
| **Transactional** | User action | Sign-up verify, reset password, invoice | High deliverability, fast API |
| **Marketing** | Campaign | Weekly digest, product launch | Unsubscribe link, list consent (GDPR/CAN-SPAM) |

Many providers do both; some teams split vendors (e.g. Resend + MailerLite) to isolate reputation.

## 2. Recommended free-tier providers (transactional)

| Provider | Free tier (typical) | Best for |
|----------|---------------------|----------|
| **[Resend](https://resend.com)** | ~3,000 emails/month | Developer-first API, React Email, good DX |
| **[Brevo](https://www.brevo.com)** (Sendinblue) | ~300 emails/day | Transactional + marketing in one |
| **[SendGrid](https://sendgrid.com)** | ~100 emails/day forever | Mature API, wide docs |
| **[Mailjet](https://www.mailjet.com)** | ~200 emails/day | EU-friendly option |
| **[Amazon SES](https://aws.amazon.com/ses/)** | Very low cost; free tier with EC2 | Already on AWS; sandbox until verified |

Always confirm current limits on the vendor pricing page.

## 3. Example — send with Resend (Node)

```javascript
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: "Acme <onboarding@mail.yourdomain.com>",
  to: ["user@example.com"],
  subject: "Verify your email",
  html: "<p>Click <a href='https://app.example.com/verify?token=...'>here</a>.</p>",
});
```

Store **`RESEND_API_KEY`** in env vars — never commit keys (see CI/CD secrets notes).

## 4. Example — SendGrid (HTTP API sketch)

```bash
curl -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{"to": [{"email": "user@example.com"}]}],
    "from": {"email": "noreply@yourdomain.com"},
    "subject": "Password reset",
    "content": [{"type": "text/plain", "value": "Reset link: ..."}]
  }'
```

## 5. DNS — deliverability essentials

Add records at your DNS host (Cloudflare, Route 53, etc.) **exactly** as the email provider specifies.

| Record | Purpose |
|--------|---------|
| **SPF** (TXT) | Which servers may send mail for your domain |
| **DKIM** (TXT/CNAME) | Cryptographic signature per message |
| **DMARC** (TXT) | Policy for failed SPF/DKIM + reporting |

```text
Example (conceptual — use provider's exact values):

yourdomain.com   TXT   v=spf1 include:_spf.resend.com ~all
resend._domainkey.yourdomain.com   CNAME   ... (from Resend dashboard)
_dmarc.yourdomain.com   TXT   v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

Start DMARC with **`p=none`** while monitoring; tighten to **`quarantine`** / **`reject`** once confident.

## 6. From-address and domains

| Pattern | Notes |
|---------|--------|
| `noreply@yourdomain.com` | OK for transactional; don't expect replies |
| `hello@yourdomain.com` | Use for support — monitor inbox |
| Shared sandbox domain | Provider default (e.g. `onboarding@resend.dev`) — **dev only** |
| Custom domain | Required for production trust |

Verify domain in provider UI before sending production traffic.

## 7. Inbound email (free options)

| Service | What you get | Cost |
|---------|--------------|------|
| **[Cloudflare Email Routing](https://developers.cloudflare.com/email-routing/)** | Forward `you@domain` → Gmail | Free with CF DNS |
| **Zoho Mail** | Limited free mailboxes on custom domain | Free tier (check seat limits) |
| **ImprovMX** | Forward-only aliases | Free tier available |

**Google Workspace** is paid for custom-domain Gmail — many startups forward to personal Gmail via Cloudflare instead until revenue supports seats.

## 8. Newsletters & mailing lists

| Provider | Free tier (typical) | Notes |
|----------|---------------------|-------|
| **Brevo** | Daily send cap includes marketing | Same account as transactional possible |
| **MailerLite** | Subscribers limit on free | Good for simple newsletters |
| **Buttondown** | Small list free | Markdown newsletters, indie-friendly |
| **ConvertKit / Beehiiv** | Limited free tiers | Creator-focused |

Legal basics:

- **Opt-in only** — no bought lists
- **Unsubscribe** link in every marketing email
- Store **consent timestamp** if EU users (GDPR)

## 9. What to avoid at MVP

| Anti-pattern | Why |
|--------------|-----|
| Postfix on a $5 VPS | IP reputation, port 25 blocks, no time for it |
| Sending from `@gmail.com` via API | Forgery filters, ToS issues |
| Same domain cold outreach + product mail | Marketing spam hurts transactional deliverability |
| No bounce handling | Providers throttle or suspend you |

Use webhooks for **bounces** and **complaints**; stop mailing those addresses.

## 10. Minimal email checklist

- [ ] Domain verified with provider
- [ ] SPF + DKIM + DMARC published
- [ ] Transactional templates (verify, reset, welcome)
- [ ] API key in secrets manager / env — not in repo
- [ ] Unsubscribe for any marketing list
- [ ] Test with [mail-tester.com](https://www.mail-tester.com) or similar before launch

## 11. When to upgrade

| Signal | Move to paid / dedicated |
|--------|--------------------------|
| Hitting daily/monthly caps | Next tier or SES volume |
| Landing in spam consistently | Dedicated IP, deliverability consultant |
| Need SLA or dedicated support | Enterprise plan |
| High-volume product email | SES + configuration sets, or Postmark |

**Related:** [Hosting, domains & CDN](iii-hosting-domains-and-cdn.md) (DNS host), networking DNS notes, CI/CD secrets.
