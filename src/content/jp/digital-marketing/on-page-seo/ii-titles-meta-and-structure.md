---
label: "II"
subtitle: "Titles, meta & structure"
group: "Digital marketing"
order: 2
---
Titles, meta & structure
Search engines and users both scan **titles**, **headings**, and **URLs** to decide relevance. Small edits here often move **CTR** before rankings change.

## 1. Title tag (`<title>`)

The **title tag** is the primary headline in search results (often — Google may rewrite it).

| Rule | Detail |
|------|--------|
| **One primary topic** | Match the page's main query intent |
| **Front-load keywords** | Important words early, not stuffed |
| **Brand at end** | `Primary Topic \| Brand` |
| **Unique per page** | No duplicate titles sitewide |
| **Length** | ~50–60 characters visible — longer may truncate |

```html
<title>Link Building Guide for SaaS (2026) | Acme</title>
```

## 2. Meta description

Not a direct ranking factor for most queries — but affects **CTR**.

| Do | Don't |
|----|-------|
| Summarize benefit in ~150–160 chars | Duplicate across pages |
| Include a soft CTA ("Learn how…") | Keyword spam |
| Match page content | Promise what the page doesn't deliver |

If omitted, Google often generates a snippet from page body.

## 3. Heading hierarchy

```html
<h1>One per page — main topic</h1>
  <h2>Major sections</h2>
    <h3>Subsections</h3>
```

| Mistake | Fix |
|---------|-----|
| Multiple `<h1>` for styling | One H1; use CSS for size |
| Skipping levels (H1 → H4) | Keep logical outline |
| Vague H2s ("Introduction") | Descriptive ("Why links matter") |

Headings help accessibility and clarify structure for crawlers.

## 4. URL structure

| Good | Weak |
|------|------|
| `/digital-marketing/link-building/` | `/p?id=3847` |
| Short, lowercase, hyphens | Dates in URL unless news site |
| Stable — avoid frequent changes | Keyword-stuffed paths |

**Redirects:** 301 old URLs when you must change paths; update internal links.

## 5. On-page content structure

```text
Above fold: answer the query in 1–2 sentences (BLUF)
H2 sections: subquestions users ask
Lists/tables: scannable comparisons
Internal links: related guides, money pages
CTA: next step matched to intent
```

Thin pages (few words, no unique value) struggle to rank — pair structure with depth from [Content strategy](../content-strategy/i-overview.md).

## 6. SERP snippet preview checklist

Before publish, ask:

| Question | |
|----------|---|
| Would I click this title vs top 3 results? | |
| Does meta description differentiate us? | |
| Does H1 match title intent (not necessarily identical)? | |
| Is the URL shareable and readable? | |

## 7. Common CMS pitfalls

| Issue | Fix |
|-------|-----|
| Site name prepended to every title | Template: `%page title \| brand` not `brand \| %page` on all |
| Auto-generated titles from H1 + date | Override for money pages |
| Missing meta on paginated archives | `noindex` thin archive pages or canonical to page 1 |

## 8. Rehearsal questions

- What is the purpose of the title tag vs meta description?
- Why use only one H1 per page?
- Name two qualities of a good URL.

**Next:** [Keywords & search intent](iii-keywords-and-search-intent.md).
