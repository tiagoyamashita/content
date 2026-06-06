---
label: "VII"
subtitle: "Web crawler"
group: "System design"
order: 7
---
Web crawler
**Search-engine-style** crawler: discover URLs, fetch HTML, feed **index pipeline**, respect **politeness** rules.

## 1. Components

| Component | Role |
|-----------|------|
| **URL frontier** | Priority queue of URLs to fetch |
| **Fetcher** | HTTP GET; robots.txt, rate limits |
| **Parser** | Extract links, text, metadata |
| **Dupe filter** | Skip seen URLs / duplicate content |
| **Storage** | Raw HTML → object store; text → search index |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="Web crawler pipeline frontier fetch parse index">
  <rect x="12" y="44" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Frontier</text>
  <path d="M76 60 H116" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="116" y="44" width="56" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="128" y="64" fill="#e4e4e7" font-size="9">Fetcher</text>
  <path d="M172 60 H212" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="212" y="44" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="224" y="64" fill="#e4e4e7" font-size="9">Parser</text>
  <path d="M268 60 H308" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="308" y="44" width="56" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="320" y="64" fill="#e4e4e7" font-size="9">Index</text>
  <rect x="380" y="44" width="72" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="388" y="64" fill="#e4e4e7" font-size="9">S3 archive</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Crawl loop</text>
  <text x="12" y="96" fill="#71717a" font-size="9">New links → frontier · Bloom filter skips revisits</text>
</svg></figure>

## 2. Scale estimate

| Metric | Value |
|--------|-------|
| Pages indexed | 1 B |
| Avg page size | 100 KB |
| Storage | ~100 TB raw HTML |
| Sustained crawl | 1B / (30×86400) ≈ **400 pages/s** |

## 3. Politeness

| Rule | Implementation |
|------|----------------|
| **robots.txt** | Cache per host; honor `Disallow` |
| **Crawl-delay** | Min interval between requests to same host |
| **Per-domain limit** | Token bucket keyed by domain |

## 4. Distributed frontier

**Consistent hash on domain** → one worker owns `example.com`:

| Benefit | |
|---------|--------|
| Centralized per-host rate limit | |
| No duplicate concurrent fetch to same host | |

Priority: sitemap URLs, PageRank, recrawl freshness signals.

## 5. De-duplication

| Layer | Structure | Trade-off |
|-------|-----------|-----------|
| **URL seen** | **Bloom filter** | Tiny memory; small false-positive → skip unfetched URL rarely |
| **Content near-dup** | **Simhash** | Detect template-heavy mirrors |

Bloom filter: “definitely not seen” or “probably seen” — no false negatives.

## 6. Failure handling

- **429/503** → backoff + re-queue frontier.
- **Redirect chains** → cap depth; normalize final URL.
- **Poison URLs** → max size, timeout, MIME allowlist.

**Related:** [Search systems](../scalable-patterns/v-search-systems.md), [Rate limiting](../scalable-patterns/iv-rate-limiting.md).
