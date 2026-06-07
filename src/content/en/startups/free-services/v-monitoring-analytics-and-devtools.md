---
label: "V"
subtitle: "Monitoring, analytics & devtools"
group: "Startups"
order: 5
---
Monitoring, analytics & devtools
Free tiers for **knowing when things break** and **shipping code** — enough for MVP, upgrade when on-call becomes real.

## 1. Error tracking

| Service | Free tier | Notes |
|---------|-----------|-------|
| **[Sentry](https://sentry.io)** | Developer plan | Stack traces, releases, alerts |
| **[GlitchTip](https://glitchtip.com)** | Self-host OSS | Sentry-compatible API |
| **Highlight.io** | Session replay + errors | Frontend-heavy apps |

```javascript
// Sentry (conceptual)
Sentry.init({ dsn: process.env.SENTRY_DSN, environment: "production" });
```

## 2. Uptime & status

| Service | Free |
|---------|------|
| **[UptimeRobot](https://uptimerobot.com)** | ~50 monitors, 5-min interval |
| **[Better Stack](https://betterstack.com)** | Uptime + incident basics |
| **GitHub Actions cron** | DIY HTTP ping |

Monitor **`/health`** endpoint — not just homepage.

## 3. Analytics

| Service | Privacy / notes |
|---------|-----------------|
| **[Plausible](https://plausible.io)** | Paid but lightweight; trial |
| **[Umami](https://umami.is)** | Self-host or cloud — OSS |
| **Cloudflare Web Analytics** | Free, no cookie banner in many cases |
| **Google Analytics** | Free; heavier, consent banners in EU |

Product analytics (funnels): **PostHog** cloud free tier for small volume.

## 4. CI/CD & code

| Service | Free for startups |
|---------|-------------------|
| **GitHub** | Private repos, Actions minutes/month |
| **GitLab** | Free tier CI |
| **Dependabot / Renovate** | Dependency updates |

See **CI/CD** track for pipeline patterns.

## 5. Design & collaboration

| Tool | Free |
|------|------|
| **Figma** | Starter files |
| **Notion** | Personal/small team |
| **Linear** | Free for small teams |
| **Discord / Slack** | Free tiers |

## 6. Minimal ops stack

```text
Deploy (Vercel) → Sentry (errors) → UptimeRobot (ping)
                → Cloudflare Analytics (traffic)
                → GitHub Actions (test on PR)
```

## 7. When to pay

| Need | Upgrade |
|------|---------|
| On-call paging 24/7 | PagerDuty, Better Stack paid |
| Log retention > 7 days | Datadog, Axiom, CloudWatch paid |
| SOC2 / audit | Enterprise plans |

**Related:** CI/CD **security & observability**, cloud patterns **SLO** note.
