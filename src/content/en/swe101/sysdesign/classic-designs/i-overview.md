---
label: "I"
subtitle: "Overview"
group: "System design"
order: 1
---
Classic designs — overview
Canonical **interview and production** problems that combine **Part I** (caching, DBs, sharding) and **Scalable patterns** (APIs, queues, CDN, search).

## Map of this submenu

| Note | System | Core tension |
|------|--------|--------------|
| [URL shortener](ii-url-shortener.md) | Bitly-style redirects | Read-heavy; key generation; 301 vs 302 |
| [News feed & timeline](iii-news-feed-timeline.md) | Twitter/Instagram feed | Fan-out on write vs read; celebrities |
| [Chat & realtime messaging](iv-chat-realtime-messaging.md) | WhatsApp/Slack-style chat | WebSockets; presence; message order |
| [Video streaming](v-video-streaming.md) | YouTube/Netflix-style video | Upload/transcode pipeline vs CDN playback |
| [Ride-sharing & location](vi-ride-sharing-location.md) | Uber/Lyft-style matching | High-frequency GPS; geospatial index |
| [Web crawler](vii-web-crawler.md) | Googlebot-style crawler | Politeness; frontier; deduplication |

## How designs connect

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 160" role="img" aria-label="Classic design problems mapped to building blocks">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Shared building blocks across classic designs</text>
  <rect x="12" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="9">Cache (Redis)</text>
  <rect x="108" y="36" width="88" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="120" y="54" fill="#e4e4e7" font-size="9">Queue (Kafka)</text>
  <rect x="204" y="36" width="88" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="216" y="54" fill="#e4e4e7" font-size="9">CDN / object store</text>
  <rect x="300" y="36" width="88" height="28" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="312" y="54" fill="#e4e4e7" font-size="9">Search index</text>
  <rect x="396" y="36" width="88" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="408" y="54" fill="#e4e4e7" font-size="9">Sharded DB</text>
  <text x="12" y="82" fill="#a1a1aa" font-size="9">URL shortener → cache + shard · Feed → Redis ZSET · Video → CDN · Crawler → frontier + Bloom</text>
  <text x="12" y="110" fill="#d4d4d8" font-size="10" font-weight="600">Interview flow</text>
  <text x="12" y="128" fill="#71717a" font-size="9">Requirements → estimate QPS/storage → high-level diagram → deep dive hot path → bottlenecks</text>
  <text x="12" y="148" fill="#71717a" font-size="9">Part I → Scalable patterns → Classic designs → Bottleneck analysis</text>
</svg></figure>

## Rehearsal questions

- URL shortener data model and read scaling?
- Fan-out write vs read — hybrid for celebrities?
- WebSocket vs long polling for chat?
- Snowflake ID properties?
- Video upload → transcode → HLS playback path?
- Geohash vs S2 for ride matching?
- Bloom filter role in crawlers?
