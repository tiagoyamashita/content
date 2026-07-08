---
label: "V"
subtitle: "Attribution & privacy"
group: "Digital marketing"
order: 5
---
Attribution & privacy
**Tracking** connects ad clicks to conversions. **Privacy** changes (iOS, cookies, regulation) mean platforms and analytics **under-report** — plan for modeled data and first-party signals.

## 1. Tracking stack (modern)

```text
Browser pixel (Meta, Google tag)
  +  GA4 events
  +  UTM parameters
  +  Conversion API / server-side (recommended at scale)
  →  CRM join for offline sales
```

## 2. Platform pixels

| Platform | Tag | Events |
|----------|-----|--------|
| **Google Ads** | gtag / GTM | Purchase, lead, signup |
| **Meta** | Meta Pixel + **CAPI** | ViewContent, Lead, Purchase |
| **LinkedIn** | Insight Tag | Conversions |

Verify events in each platform's **event manager** before spending.

## 3. Conversion API (server-side)

Browser pixels miss users with:

| Blocker | Effect |
|---------|--------|
| Ad blockers | No client pixel fire |
| iOS ATT | Limited Meta mobile tracking |
| Cookie consent decline | No marketing cookies |

**Server-side** sends events from your backend (signup webhook → Meta CAPI). Reduces gap — does not fix everything.

## 4. Consent mode (EU / UK)

| Practice | Detail |
|----------|--------|
| Consent banner | Before non-essential tags |
| **Google Consent Mode v2** | Adjusts tag behavior by consent |
| Document choices | Privacy policy |

Work with legal for your jurisdictions — not legal advice here.

## 5. Attribution gaps to expect

| Phenomenon | Response |
|------------|----------|
| Platform ROAS > GA4 revenue | Platform claims view-through; compare on **blended** MER |
| **MER** (marketing efficiency ratio) | Total revenue ÷ total marketing spend — sanity check |
| Cross-device | User clicks mobile, converts desktop — last-click may miss |

Use [UTMs](../analytics/iv-conversions-and-attribution.md) + CRM for B2B truth.

## 6. First-party data strategy

| Asset | Use in ads |
|-------|------------|
| **Email list** | Customer match uploads (hashed) |
| **Site behavior** | Retargeting segments |
| **Purchase history** | Exclude customers from prospecting |

Email + SEO compound; paid **amplifies** retargeting pools.

## 7. iOS / cookieless direction

| Trend | Implication |
|-------|-------------|
| Less third-party data | Creative and landing page quality matter more |
| Modeled conversions | Platforms estimate — treat as directional |
| Server-side + CRM | First-party becomes primary |

## 8. Rehearsal questions

- Why add server-side conversion tracking?
- What is MER and why use it?
- Name one reason browser pixels under-count conversions.

**Next:** Return to [Digital marketing — Overview](../i-overview.md) or iterate channels with [Reporting & experiments](../analytics/v-reporting-and-experiments.md).
