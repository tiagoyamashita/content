---
label: "I"
subtitle: "概要"
group: "CDN"
order: 1
---
CDN — 概要

**CDN (コンテンツ配信ネットワーク)** は、ユーザーに近い **エッジ ロケーション** からコンテンツのコピーを提供します。これにより、遅延が短縮され、オリジンの負荷が軽減され、トラフィックの急増に対する復元力が向上します。ほとんどの実稼働 Web アプリは、**静的アセット** (JS、CSS、画像、ビデオ セグメント) を CDN の背後に置きます。多くは **選択された GET APIs** もキャッシュします。

For system-design framing (pull vs push, invalidation), see [CDN & edge caching](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md). For regions and edge vs cloud regions, see [Regions, AZs & edge](../../sre101/cloud-architecture/foundations/iii-regions-azs-and-edge.md).

## このトラックの地図

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

## CDN が当てはまる場所

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

CDN は **HTTP 応答** (ファイル、JSON) をキャッシュします。 Redis は **アプリケーション オブジェクト**をスタック内にキャッシュします。両方を使用してください。

## CDN に何を付けるか

| Content | CDN? | Notes |
|---------|------|-------|
| JS/CSS/fonts (hashed) | Yes | Long TTL, immutable |
| Images, video segments | Yes | HLS/DASH chunks |
| Public read-only API GET | Sometimes | Short TTL + cache keys |
| HTML (SPA shell) | Careful | Short TTL or stale-while-revalidate |
| Authenticated/private API | Usually no | `private`, `no-store` |
| POST/PUT/DELETE | No | Always to origin |

## エンジニアが気にする理由

|メリット |説明 |
|----------|---------------|
| **レイテンシ** |数百の都市のエッジと 1 つの発信地域のエッジ |
| **スケール** |エッジはフラッシュ トラフィックを吸収します。オリジンで受信されるリクエストが少なくなります。
| **コスト** |エッジでの下り料金が安くなる。より小規模な出発地フリート |
| **セキュリティ** | DDoS 吸収、エッジでの WAF (プロバイダー依存) |

## 一般的なプロバイダー

|プロバイダー |一般的な使用法 |
|----------|---------------|
| **クラウドフレア** | DNS + CDN + TLS;小規模サイトの無料枠 |
| **Amazon CloudFront** | AWS の起源 (S3、ALB、API Gateway) |
| **すぐに** |きめ細かいパージ、エッジ コンピューティング |
| **Azure CDN / フロント ドア** | Azure とマルチクラウド |
| **Google Cloud CDN** | GCS / LB バックエンド |

Managed platforms (**Vercel**, **Netlify**, **Cloudflare Pages**) include CDN automatically — see [Hosting, domains & CDN](../../startups/free-services/iii-hosting-domains-and-cdn.md) for MVP options.

＃＃ 次

Continue with [How CDNs work](ii-how-cdns-work.md) for DNS routing, PoPs, and cache hit/miss flow.
