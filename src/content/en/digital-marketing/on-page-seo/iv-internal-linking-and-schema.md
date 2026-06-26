---
label: "IV"
subtitle: "Internal linking & schema"
group: "Digital marketing"
order: 4
---
Internal linking & schema
**Internal links** distribute authority and help users (and crawlers) discover pages. **Schema** (structured data) clarifies page type for rich results — optional but high leverage on key templates.

## 1. Site architecture (shallow beats deep)

```text
Homepage
  ├── Category / pillar hub
  │     ├── Article A
  │     └── Article B
  └── Product / pricing
```

**Goal:** important pages reachable in **≤3 clicks** from homepage. Deep orphan pages rank poorly.

## 2. Internal linking tactics

| Tactic | Example |
|--------|---------|
| **Hub → spoke** | Pillar guide links to cluster articles |
| **Spoke → hub** | Each article links back to pillar |
| **Contextual in-body links** | "See our [title tag guide](...)" in relevant paragraph |
| **Nav + footer** | Stable paths to pricing, docs, top content |
| **Related posts block** | 3–5 genuinely related URLs |

Use **descriptive anchor text** — "link building outreach templates" beats "click here."

## 3. PageRank flow (intuition)

External backlinks inject authority; internal links **pass** it to other URLs on your site.

```text
High-authority blog post (many backlinks)
  →  internal link  →  trial signup page
```

When you earn a new backlink, link from that page (or updates) to **money pages** where appropriate.

## 4. Orphan and dead-end pages

| Problem | Fix |
|---------|-----|
| Page not linked anywhere | Add from hub, sitemap, related block |
| Page only in sitemap | Add contextual links |
| 404 on internal links | Fix or redirect |

Audit quarterly with a crawler (Screaming Frog free tier, Sitebulb, etc.) or Search Console coverage reports.

## 5. Breadcrumbs

Breadcrumbs show hierarchy and often appear in SERPs.

```text
Home > Digital marketing > On-page SEO > Internal linking
```

Implement visible breadcrumbs + `BreadcrumbList` schema where your stack allows.

## 6. Schema.org basics

JSON-LD in `<head>` or body — validates in [Google Rich Results Test](https://search.google.com/test/rich-results).

| Schema type | Use on |
|-------------|--------|
| **Organization / WebSite** | Homepage |
| **Article / BlogPosting** | Blog posts |
| **FAQPage** | FAQ sections (only if visible on page) |
| **Product** | Product pages (accurate price/availability) |
| **HowTo** | Step-by-step guides |

**Rules:** schema must match **visible** content; misleading markup can cause manual actions.

## 7. Canonical tags

When duplicate or near-duplicate URLs exist:

```html
<link rel="canonical" href="https://yoursite.com/preferred-url/" />
```

Use for: HTTP→HTTPS, www vs non-www, parameterized URLs, syndicated copies pointing to original.

## 8. Pagination and faceted navigation

| Scenario | Approach |
|----------|----------|
| Blog page 2, 3… | Often fine indexed; canonical page 1 optional for thin archives |
| E-commerce filters | `noindex` low-value filter combos; canonical to parent category |

Avoid infinite crawl traps from uncontrolled filter parameters.

## 9. Rehearsal questions

- Why link from high-authority posts to money pages?
- What is an orphan page?
- What must FAQ schema match on the page?

**Next:** [Technical checklist](v-technical-checklist.md).
