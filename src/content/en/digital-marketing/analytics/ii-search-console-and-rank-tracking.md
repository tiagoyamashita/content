---
label: "II"
subtitle: "Search Console & rank tracking"
group: "Digital marketing"
order: 2
---
Search Console & rank tracking
**Google Search Console (GSC)** is free, first-party data on how Google sees your site — queries, pages, index status, and links. Use it before paying for rank trackers.

## 1. Core GSC reports

| Report | Use |
|--------|-----|
| **Performance** | Queries, impressions, clicks, CTR, average position |
| **Pages** | Which URLs earn search traffic |
| **Indexing → Pages** | Indexed vs not indexed and why |
| **Sitemaps** | Submit and monitor crawl |
| **Links** | Top linked pages, external links, anchor text sample |

Verify property for **exact** host (https + www or non-www).

## 2. Reading Performance data

| Metric | Meaning |
|--------|---------|
| **Impressions** | Times your URL appeared in search |
| **Clicks** | Times users clicked through |
| **CTR** | Clicks ÷ impressions |
| **Position** | Average rank (rough — not exact per user) |

Filter by **query**, **page**, **country**, **device** to diagnose.

## 3. Quick wins from GSC

| Pattern | Action |
|---------|--------|
| High impressions, low CTR | Improve title/meta — [Titles, meta & structure](../on-page-seo/ii-titles-meta-and-structure.md) |
| Position 4–15 for valuable query | Expand content, internal links, links |
| Page indexed but zero impressions | Intent mismatch or very low volume |
| "Discovered – currently not indexed" | Quality, duplication, or crawl — improve page |

## 4. Index coverage troubleshooting

| Status | Typical fix |
|--------|-------------|
| **Excluded by noindex** | Remove tag on prod |
| **Soft 404** | Add substance or return 404 |
| **Duplicate without canonical** | Add canonical |
| **Crawled – currently not indexed** | Strengthen content & links |

Use **URL Inspection** → "Request indexing" only after fixing root cause.

## 5. Links report (SEO)

GSC shows **sample** of external links — complement with Ahrefs/Semrush for prospecting ([Link quality](../link-building/ii-link-quality-and-evaluation.md)).

| View | Action |
|------|--------|
| Top linked pages | Ensure they convert; internal link out |
| New links | Thank / nurture relationships |
| Weird anchors | Audit for spam |

## 6. Rank tracking beyond GSC

GSC is lagged and averaged. Paid tools track daily position for keyword lists.

| When to pay | When GSC is enough |
|-------------|-------------------|
| Competitive SEO program | Early site, few target queries |
| Client reporting | Founder doing own marketing |
| Many locales | Single market |

Track **20–50 priority queries** — not thousands.

## 7. Weekly GSC routine (15 min)

```text
1. Performance last 28 days vs prior — clicks down?
2. Top queries — any new opportunities?
3. Indexing errors — new exclusions?
4. Manual actions / security — must be zero
```

## 8. Rehearsal questions

- What is the difference between impressions and clicks in GSC?
- What might you do for a query with high impressions and low CTR?
- Why verify the exact domain property in GSC?

**Next:** [GA4 & events](iii-ga4-and-events.md).
