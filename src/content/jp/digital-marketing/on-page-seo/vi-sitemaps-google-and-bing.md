---
label: "VI"
subtitle: "Sitemaps — Google & Bing"
group: "Digital marketing"
order: 6
---
Sitemaps — Google & Bing
A **sitemap** lists the URLs you want crawled. Submitting it to **Google Search Console** and **Bing Webmaster Tools** does not guarantee indexation — it tells each engine where to look, and it flags errors when the file breaks.

Internal links still matter more than the sitemap. Use both. See [Technical checklist](v-technical-checklist.md) for the rest of crawl health.

## 1. What to submit

| Item | Detail |
|------|--------|
| **URL** | Production HTTPS, preferred host (`www` or apex — match GSC/Bing property) |
| **Path** | Usually `https://example.com/sitemap.xml` |
| **Contents** | Canonical, indexable URLs only — no `noindex`, staging, or thank-you pages |
| **Size** | ≤ 50,000 URLs / 50 MB per file; use a sitemap index if larger |
| **`robots.txt`** | Add `Sitemap: https://example.com/sitemap.xml` so bots find it without the dashboards |

Confirm the file returns **200** and is valid XML before you submit.

## 2. Google Search Console

1. Open [Google Search Console](https://search.google.com/search-console) and pick the **exact** property (https + www or non-www).
2. Left nav → **Sitemaps**.
3. Under **Add a new sitemap**, enter the path only (`sitemap.xml` or `sitemap_index.xml`) — GSC prefixes your property URL.
4. **Submit**. Status should move to **Success** after Google fetches it.
5. Open the sitemap row to see **discovered URLs** vs errors.

| Status | Meaning | Action |
|--------|---------|--------|
| **Success** | Google fetched the file | Wait for crawl; check Indexing → Pages |
| **Couldn't fetch** | 404, block, or auth | Fix URL, robots, or HTTPS |
| **Has errors** | Invalid URLs or XML | Open the report; remove bad entries |

**Update after launch:** when you add important URLs, rebuild the sitemap (keep `lastmod` honest) and submit the **same** path again. GSC treats a resubmit as “re-read this file,” not a new sitemap. Do not spam “Request indexing” for every page — fix discovery first, then inspect a few priority URLs.

GSC reports and weekly routine: [Search Console & rank tracking](../analytics/ii-search-console-and-rank-tracking.md).

## 3. Bing Webmaster Tools

Bing does not automatically use your GSC sitemap. Submit it separately (or import the site from GSC, then still confirm Sitemaps).

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters).
2. Add the site and **verify** (HTML file, meta tag, or CNAME). You can **Import from Google Search Console** to skip a second verification if both properties match.
3. **Sitemaps** → submit the full sitemap URL (`https://example.com/sitemap.xml`).
4. Check **Discovered URLs** and error counts after Bing fetches it.

Resubmit the same URL when the file changes (new sections, URL migrations). Bing also accepts **IndexNow** for faster URL notification after publishes — that complements the sitemap; it does not replace it.

## 4. When to resubmit

| Change | Google | Bing |
|--------|--------|------|
| New section or many new URLs | Rebuild sitemap + submit same path | Same |
| One new blog post, already linked | Usually wait — crawl via links | Optional IndexNow |
| HTTP → HTTPS or www change | New property + new sitemap URL | New site + new sitemap |
| Removed URLs | Drop from sitemap; 301 or 404 the old URLs | Same |

A sitemap is a **hint**. Orphan URLs with no internal links may still sit in “discovered, not indexed.”

## 5. Common mistakes

| Mistake | Fix |
|---------|-----|
| Submitting `http://` or the non-canonical host | Match the verified property |
| Listing `noindex` or paginated junk | Filter the generator |
| Forgetting Bing | Same file, second dashboard |
| New sitemap filename every deploy | Keep a stable `/sitemap.xml` (or a stable index) |
| Blocking the file in robots.txt | Allow `/sitemap.xml` |

## 6. Rehearsal questions

- What does submitting a sitemap *not* guarantee?
- How do you resubmit after adding URLs — new filename or the same path?
- Why verify Bing even if GSC already has the sitemap?

**Next:** [Content strategy — Overview](../content-strategy/i-overview.md).
