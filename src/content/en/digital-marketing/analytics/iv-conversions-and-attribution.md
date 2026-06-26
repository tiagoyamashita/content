---
label: "IV"
subtitle: "Conversions & attribution"
group: "Digital marketing"
order: 4
---
Conversions & attribution
A **conversion** is the action you optimize for. **Attribution** is how you assign credit when multiple touchpoints precede that action.

## 1. Define primary conversion

Pick **one** north-star conversion per site (secondary conversions optional):

| Business | Primary conversion |
|----------|-------------------|
| SaaS | Trial start or qualified signup |
| E-commerce | Purchase |
| Lead gen | Demo request or contact form |
| Content | Email subscribe (if monetization path exists) |

Document: event name, URL, value (if known).

## 2. Funnel tracking

```text
Landing  →  engage  →  start signup  →  complete signup
```

| Step | Event / page |
|------|--------------|
| Landing | `page_view` on `/pricing/` |
| Intent | `click_cta` |
| Start | `sign_up_start` |
| Complete | `sign_up` (conversion) |

Drop-off between steps tells you **what to fix** (copy, form, speed).

## 3. UTM parameters

Append to campaign URLs for GA4 source attribution:

```text
https://yoursite.com/guide?utm_source=newsletter&utm_medium=email&utm_campaign=march_launch
```

| Parameter | Example | Rule |
|-----------|---------|------|
| `utm_source` | `linkedin`, `google` | Platform or sender |
| `utm_medium` | `email`, `cpc`, `social` | Channel type |
| `utm_campaign` | `spring_promo` | Campaign name |
| `utm_content` | `hero_cta` | Optional A/B variant |

**Convention:** lowercase, underscores, documented in a shared sheet.

## 4. Attribution models (basics)

| Model | Credit |
|-------|--------|
| **Last click** | All credit to final touch before conversion |
| **First click** | All credit to discovery touch |
| **Linear / data-driven** | Split across touches (GA4 paid features) |

No model is "true" — use last-click for ops simplicity; data-driven when budget is large.

## 5. Assisted conversions (intuition)

Blog post may not be last click but still **introduced** the buyer. Check:

| Signal | Tool |
|--------|------|
| Landing page before signup | GA4 path exploration |
| Organic growth + direct conversions | Brand search rising |

This justifies [Content strategy](../content-strategy/i-overview.md) beyond last-touch ROI.

## 6. Offline and CRM join (B2B)

Web analytics alone undercounts B2B if sales closes offline.

```text
Form hidden field: utm params
  →  CRM (HubSpot, Salesforce)
  →  report CAC by source
```

## 7. Rehearsal questions

- What is a primary conversion?
- Name the three core UTM parameters.
- Why can last-click attribution undervalue content marketing?

**Next:** [Reporting & experiments](v-reporting-and-experiments.md).
