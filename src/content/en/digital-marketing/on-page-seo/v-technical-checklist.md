---
label: "V"
subtitle: "Technical checklist"
group: "Digital marketing"
order: 5
---
Technical checklist
Technical SEO ensures bots and users can **reach**, **render**, and **trust** your pages. Run this checklist before scaling content or link building.

## 1. Pre-flight (blocking issues)

| Check | How |
|-------|-----|
| **HTTPS everywhere** | No mixed content; redirect HTTP → HTTPS |
| **No accidental `noindex`** | View source / CMS SEO settings on production |
| **Robots.txt** | Not blocking `/` or entire site; allow CSS/JS if needed for rendering |
| **Search Console verified** | Property for correct domain (www vs non-www) |
| **Sitemap submitted** | `/sitemap.xml` in Search Console |

## 2. Crawlability

```text
Can Google discover URLs?  →  internal links + sitemap
Can Google fetch URLs?     →  200 status, not 5xx
Can Google render content? →  JS not required for core text (ideal)
```

| Issue | Signal | Fix |
|-------|--------|-----|
| Soft 404 | Thin page returns 200 | Improve content or return real 404 |
| Redirect chains | Multiple hops | Single 301 |
| 404 spikes | Broken links | Fix or 301 to relevant page |

## 3. Mobile and Core Web Vitals

Google uses **mobile-first indexing**. Test with PageSpeed Insights / Search Console Core Web Vitals.

| Metric | Target (rule of thumb) |
|--------|------------------------|
| **LCP** (largest contentful paint) | ≤ 2.5s good |
| **INP** (interaction) | ≤ 200ms good |
| **CLS** (layout shift) | ≤ 0.1 good |

| Quick wins | |
|------------|---|
| Compress images (WebP/AVIF) | |
| Lazy-load below-fold media | |
| CDN for static assets — see [Hosting & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md) | |
| Defer non-critical JS | |

## 4. Indexation hygiene

| Practice | Why |
|----------|-----|
| Canonical preferred URLs | Consolidate signals |
| `noindex` on staging, admin, thank-you pages | Reduce index bloat |
| Consistency (www, trailing slash) | One version in Search Console |

Use **URL Inspection** in Search Console to test live URL index status.

## 5. International and multi-language (if applicable)

| Setup | When |
|-------|------|
| **`hreflang`** | Same content in multiple languages/regions |
| **Subfolders** `/en/`, `/ja/` | Clear locale separation |
| **Separate domains** | Rare — strong brand reason only |

Incorrect hreflang hurts more than omitting it — validate carefully.

## 6. Security and trust signals

| Signal | Notes |
|--------|-------|
| Valid SSL | Auto via Cloudflare, Vercel, etc. |
| No malware / hacked content | Search Console security issues |
| Clear contact / about on YMYL topics | Your Money Your Life — finance, health |

## 7. Launch checklist (copy-paste)

```text
[ ] HTTPS, single preferred host
[ ] GSC + sitemap
[ ] Title/meta on core pages
[ ] No staging noindex on prod
[ ] Mobile-friendly test pass
[ ] Core pages in nav + internal links
[ ] 404 page helpful
[ ] Analytics + conversion events
```

## 8. When to escalate

| Symptom | Likely need |
|---------|-------------|
| Half of site "Discovered – not indexed" | Quality, duplication, or crawl budget — improve content & architecture |
| Sudden ranking drop sitewide | Manual action, algorithm update, or technical break — check GSC |
| JS-only content missing in cache | SSR or pre-render for critical content |

## 9. Rehearsal questions

- Name three items on the technical pre-flight checklist.
- What are LCP and CLS measuring?
- Why submit a sitemap to Search Console?

**Next:** [Content strategy — Overview](../content-strategy/i-overview.md).
