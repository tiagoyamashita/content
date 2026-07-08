---
label: "I"
subtitle: "Overview"
group: "CDN"
order: 1
---
CDN — overview
A **CDN (Content Delivery Network)** serves copies of your content from **edge locations** close to users — lower latency, less load on origin, and better resilience under traffic spikes. Most production web apps put **static assets** (JS, CSS, images, video segments) behind a CDN; many also cache **selected GET APIs**.

For system-design framing (pull vs push, invalidation), see [CDN & edge caching](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md). For regions and edge vs cloud regions, see [Regions, AZs & edge](../../sre101/cloud-architecture/foundations/iii-regions-azs-and-edge.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | What a CDN does, where it sits in the stack |
| **II — How CDNs work** | DNS, PoPs, cache hit/miss, pull vs push |
| **III — Cache headers & TTL** | `Cache-Control`, ETag, versioning |
| **IV — Setup & origin** | Origin config, TLS, major providers |
| **V — Static assets & SPAs** | Hashed filenames, S3 + CDN, deploy flow |
| **VI — APIs & dynamic content** | Cacheable GETs, `Vary`, purge, edge logic |
| **VII — Operations & troubleshooting** | Purge, monitoring, common failures |
| **VIII — CDN & API gateway together** | How CDN and gateway split work at the edge |

## Where CDN fits

```text
User  →  DNS  →  CDN edge (PoP)  →  [cache HIT → response]
                              └──→  [cache MISS → origin (S3, ALB, app)]
```

| Layer | Role |
|-------|------|
| **CDN edge** | Cache bytes close to user; terminate TLS |
| **Origin** | Source of truth — S3 bucket, load balancer, app server |
| **App cache ([Redis](../redis/i-overview.md))** | Session, DB query cache — different layer, often together |
| **Database** | Not behind CDN — origin only |

CDN caches **HTTP responses** (files, JSON). Redis caches **application objects** inside your stack. Use both.

## What to put on a CDN

| Content | CDN? | Notes |
|---------|------|-------|
| JS/CSS/fonts (hashed) | Yes | Long TTL, immutable |
| Images, video segments | Yes | HLS/DASH chunks |
| Public read-only API GET | Sometimes | Short TTL + cache keys |
| HTML (SPA shell) | Careful | Short TTL or stale-while-revalidate |
| Authenticated/private API | Usually no | `private`, `no-store` |
| POST/PUT/DELETE | No | Always to origin |

## Why engineers care

| Benefit | Explanation |
|---------|-------------|
| **Latency** | Edge in hundreds of cities vs one origin region |
| **Scale** | Edge absorbs flash traffic; origin sees fewer requests |
| **Cost** | Cheaper egress at edge; smaller origin fleet |
| **Security** | DDoS absorption, WAF at edge (provider-dependent) |

## Common providers

| Provider | Typical use |
|----------|-------------|
| **Cloudflare** | DNS + CDN + TLS; free tier for small sites |
| **Amazon CloudFront** | AWS origins (S3, ALB, API Gateway) |
| **Fastly** | Fine-grained purge, edge compute |
| **Azure CDN / Front Door** | Azure and multi-cloud |
| **Google Cloud CDN** | GCS / LB backends |

Managed platforms (**Vercel**, **Netlify**, **Cloudflare Pages**) include CDN automatically — see [Hosting, domains & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md) for MVP options.

## Next

Continue with [How CDNs work](ii-how-cdns-work.md) for DNS routing, PoPs, and cache hit/miss flow.
