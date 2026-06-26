---
label: "III"
subtitle: "GA4 & events"
group: "Digital marketing"
order: 3
---
GA4 & events
**Google Analytics 4 (GA4)** tracks sessions, traffic sources, and **events** (actions users take). Configure a handful of meaningful events — not hundreds of noise.

## 1. GA4 mental model

```text
User visits site  →  session starts
User does something  →  event (page_view, click, signup)
Events roll up  →  reports & conversions
```

GA4 is **event-based** (unlike Universal Analytics pageviews-only mindset).

## 2. Must-have events (typical SaaS / lead gen)

| Event | When fired |
|-------|------------|
| `page_view` | Automatic |
| `sign_up` or `generate_lead` | Form submit success |
| `begin_checkout` / `purchase` | E-commerce funnel |
| `click_cta` | Primary button clicks (optional) |
| `scroll` / `file_download` | Engagement (optional) |

Mark **1–3 as conversions** in Admin → Events.

## 3. Key reports

| Report | Question |
|--------|----------|
| **Acquisition → Traffic acquisition** | Which channels bring sessions? |
| **Engagement → Pages and screens** | Top landing pages |
| **Engagement → Events** | Are conversions firing? |
| **User → Tech** | Mobile vs desktop split |

Compare **Organic Search**, **Paid**, **Email**, **Referral** — align with [Channels & funnel](../foundations/ii-channels-and-funnel.md).

## 4. Implementation options

| Method | Best for |
|--------|----------|
| **GA4 gtag.js** | Simple marketing sites |
| **Google Tag Manager (GTM)** | Multiple tags, non-dev updates |
| **Server-side GTM** | Ad blockers, privacy — advanced |

Test with **DebugView** in GA4 while clicking through your site.

## 5. Common setup bugs

| Bug | Symptom |
|-----|---------|
| Double GA tags | Inflated pageviews |
| Conversion on wrong trigger | Button click without form success |
| Missing cross-domain | Checkout on subdomain not attributed |
| No consent mode (EU) | Compliance gap |

## 6. Alternatives

| Tool | When |
|------|------|
| **Plausible / Fathom / Umami** | Privacy-first, simpler dashboards |
| **PostHog** | Product analytics + events |
| **Mixpanel / Amplitude** | Deep funnel product analytics |

Principles (events, conversions, sources) transfer across tools.

## 7. Rehearsal questions

- What is an event in GA4?
- Name two reports you would check weekly.
- Why mark only a few events as conversions?

**Next:** [Conversions & attribution](iv-conversions-and-attribution.md).
