---
label: "V"
subtitle: "Measurement & pitfalls"
group: "Digital marketing"
order: 5
---
Measurement & pitfalls
Link building without measurement is guesswork. Track **referring domains**, **referral traffic**, and **rankings** — and know when links hurt instead of help.

## 1. KPIs that matter

| KPI | What it tells you | Tool |
|-----|-------------------|------|
| **New referring domains** | Growth of unique sites linking to you | Search Console, Ahrefs, Semrush |
| **Referral sessions** | Real visitors from backlinks | Analytics (GA4, Plausible) |
| **Landing page rankings** | SEO impact for target keywords | Search Console, rank trackers |
| **Indexed pages** | Crawl benefit from internal + external links | Search Console |
| **Conversions from referral** | Business value (signups, sales) | Analytics goals / events |

**Leading indicator:** outreach sent → reply rate → links earned.

**Lagging indicator:** rankings and organic traffic (weeks to months).

## 2. Google Search Console (free baseline)

| Report | Use |
|--------|-----|
| **Links → External links** | Top linked pages, top linking sites |
| **Links → Top linking text** | Anchor text distribution |
| **Performance** | Queries and pages gaining impressions |

Export monthly snapshots to spot **spikes** (good PR) or **suspicious domains** (spam attacks).

## 3. Analytics setup

Tag referral traffic so you know which links convert:

```text
Acquisition → Traffic acquisition → Session source/medium = referral
  → filter by landing page
  → segment by campaign (UTM on links you control)
```

For links you do not control, UTM is impossible — use **referral domain** reports instead.

| UTM use case | Example |
|--------------|---------|
| Guest bio link | `?utm_source=site&utm_medium=guest_post` |
| Newsletter sponsorship | `utm_campaign=spring2026` |

## 4. Outreach funnel metrics

| Stage | Benchmark (varies by niche) |
|-------|------------------------------|
| Emails sent | Volume |
| Open rate | 40–60% if list is warm; lower for cold |
| Reply rate | 5–15% for good personalized outreach |
| Positive reply | 1–5% |
| Link placed | 1–3% of initial sends |

Low reply rate usually means **weak list**, **generic copy**, or **weak asset** — not "email doesn't work."

## 5. Toxic links & negative SEO

**Toxic links** come from spam, hacks, or attacks (competitor blasting your URL on bad sites).

| Signal | Action |
|--------|--------|
| Sudden thousands of gambling/pharma links | Audit; likely attack or bad vendor |
| Manual action in Search Console | Fix cause; submit reconsideration |
| No penalty but junk links | Often ignore; Google discounts spam |

**Disavow file** (`disavow.txt` via Search Console): tell Google to ignore specific domains. Use **sparingly** — only when you have evidence of harm or a manual action. Incorrect disavow can hurt legitimate links.

```text
# disavow.txt example (domain-level)
domain:spam-example.com
domain:cheap-links.net
```

## 6. Penalties and manual actions

| Type | Cause | Recovery |
|------|-------|----------|
| **Manual action** | Human reviewer flags manipulation | Remove bad links / disavow; document cleanup; request review |
| **Algorithmic demotion** | Link spam systems (e.g. Penguin-style) | Stop toxic tactics; earn clean links over time |

Prevention beats recovery: no bought links, no PBNs, no automated blasts.

## 7. Link velocity and patterns

| Pattern | Risk |
|---------|------|
| 0 links for years → 500 in one week | Unnatural |
| Steady growth with content launches | Normal |
| All exact-match commercial anchors | Over-optimization |
| All links to homepage only | Thin; diversify to deep pages |

Launch PR or viral content can cause **legitimate spikes** — context matters.

## 8. Tool landscape

| Tool | Strength |
|------|----------|
| **Google Search Console** | Official link data, free |
| **Ahrefs / Semrush / Moz** | Competitor analysis, prospecting, alerts |
| **Hunter.io** | Find email addresses |
| **Check My Links** (extension) | Broken link prospecting on page |
| **Wayback Machine** | See what broken URLs used to cover |
| **Spreadsheet** | CRM for outreach — underrated |

No tool replaces **judgment** on link quality ([Link quality & evaluation](ii-link-quality-and-evaluation.md)).

## 9. Reporting template (monthly)

```text
Month: March 2026

New referring domains:     12 (+4 vs Feb)
Total referring domains:   847
Top new link:              example.com/review (DR 72, in-content)
Referral sessions:         1,240 (+18%)
Organic clicks (GSC):      8,900 (+6%)
Outreach:                  45 sent, 6 replies, 3 links live

Notes: Guest post on [site] drove 400 referral sessions.
       Disavowed 2 spam domains from negative SEO test.
Next:  Broken link campaign on [topic] resource pages.
```

Share with stakeholders in **business terms** (traffic, conversions), not just DR.

## 10. Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Chasing DR only | Prioritize relevance and traffic |
| Linking only to homepage | Deep links to best assets |
| Ignoring nofollow | Track referral value separately |
| Stopping after first wins | Link building is ongoing |
| Outsourcing to black-hat agencies | Audit their methods; you own the penalty |
| No alignment with content calendar | Plan assets before outreach sprints |

## 11. Integration with other marketing

```text
Content marketing  →  assets worth linking
PR / social        →  amplifies reach, earns mentions
Paid ads           →  does not replace links; test landing pages that earn organic links later
Email              →  nurtures audience; rarely builds SEO links directly
```

Links compound: today's guest post becomes tomorrow's **referring domain** that makes the next pitch easier ("as seen on…").

## 12. Rehearsal questions

- Name three KPIs for link building.
- When should you consider a disavow file?
- What does a healthy anchor text profile look like?

**Back to:** [Link building — Overview](i-overview.md) · [Digital marketing — Overview](../i-overview.md).
