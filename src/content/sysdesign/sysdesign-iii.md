---
label: "III"
subtitle: "Classic Designs"
group: "System design"
order: 3
---
System Design — Part III: Classic Designs
Apply Parts I & II to canonical interview problems.

## 1. URL shortener
Requirements: create short URL, redirect to original, analytics.
Scale: 100 M URLs created/day; 10 B redirects/day (~115 K reads/s).

Key generation:
- Hash (MD5/SHA-256) → take first 7 chars of base-62 encoding.
Collision probability is low but non-zero; check DB before inserting.
- Pre-generate short codes in a Key Generation Service (KGS).
KGS batch-generates unique keys; app picks from pool — no collision check.

Data model:
short_url  VARCHAR PK
long_url   TEXT
user_id    BIGINT
created_at TIMESTAMP
expires_at TIMESTAMP

Redirect: HTTP 301 (permanent, browser caches → reduces server load)
vs HTTP 302 (temporary, every click hits server → accurate analytics).

Scaling:
- Read-heavy → cache short→long mapping in Redis (cache-aside, LRU).
- Shard DB by short_url hash.
- Analytics: async; write click events to Kafka → Flink → ClickHouse.

## 2. News feed / timeline
Two delivery models:

Fan-out on write (push model):
When user A posts → immediately write to every follower's feed cache.
+ Read is O(1) — just fetch pre-built feed.
− Write amplification for celebrities (10 M followers → 10 M writes).

Fan-out on read (pull model):
When user B opens feed → fetch posts from all people B follows.
+ Write is cheap.
− Read is expensive; must merge and rank N timelines on every load.

Hybrid (Twitter / Instagram approach):
- Normal users: fan-out on write into a feed cache.
- Celebrities (>X followers): fan-out on read only.
- Merge both sources at read time for logged-in user.

Data model: posts table (post_id, author_id, content, media_ids, created_at).
Feed cache: Redis sorted set keyed by user_id; score = timestamp.

## 3. Chat & real-time messaging
Core challenge: push messages to the recipient instantly.

Connection options:
- Short polling: client polls every N seconds — wasteful.
- Long polling: server holds request open until message arrives — better.
- WebSocket: full-duplex persistent TCP connection — best for chat.
- Server-Sent Events (SSE): server → client only; simpler than WebSocket.

Architecture:
Client ↔ Chat Service (WebSocket) ↔ Message Broker (Kafka)
↔ Presence Service
↔ Push Notification Service

Message storage:
- Cassandra: wide-column; keyed by (conversation_id, message_id DESC).
- message_id = Snowflake ID (timestamp + server id + sequence) → sortable.

Presence (online/offline):
- Client heartbeats every 5 s; server marks offline after 30 s silence.
- Store in Redis with TTL = 30 s; renew on heartbeat.

## 4. Video streaming
Key insight: video files are huge; the architecture is split between
the upload/transcoding pipeline and the playback path.

Upload & transcoding pipeline:
1. Client uploads raw video to object storage (S3) via pre-signed URL.
2. Upload completion triggers a job on a transcoding queue (SQS).
3. Transcoding workers convert to multiple resolutions (360p, 720p, 1080p, 4K)
and container formats (HLS segments + manifest).
4. Output segments stored in S3; metadata written to DB.

Playback path:
Client → CDN edge (serves HLS segments) → origin (S3) on miss.
Player chooses resolution based on available bandwidth (ABR — adaptive bitrate).

Scale considerations:
- CDN absorbs 99%+ of traffic; origin rarely hit.
- Transcode with GPU-accelerated spot instances for cost efficiency.
- Metadata DB (video title, views, likes): PostgreSQL or DynamoDB.

## 5. Ride-sharing / location service
Core challenges: real-time location updates at massive scale,
efficient geospatial queries ('find drivers near me').

Location ingestion:
- Drivers send GPS update every 4 s → 1 M active drivers = 250 K writes/s.
- Write to Redis Geo (GEOADD) — in-memory, O(log N) insert.
- Also write to Kafka for downstream analytics / historical replay.

Geospatial indexing:
- Geohash: encode (lat, lng) into a short base-32 string.
Adjacent geohashes are usually nearby; prefix search finds neighbours.
- S2 cells: hierarchical spherical geometry; used by Google, Uber.
- Quadtree: recursive 2-D partitioning; good for non-uniform data.

Matching:
1. Rider requests → find drivers within radius using geospatial index.
2. Rank by ETA (route graph) → offer to nearest available driver.
3. Driver accepts / timeout → re-offer to next candidate.

## 6. Web crawler
Purpose: discover and index web content for search engines.

Components:
- URL frontier (priority queue of URLs to crawl).
- Fetcher: download HTML; respect robots.txt and crawl-delay.
- Parser: extract links; de-duplicate against visited set.
- Storage: raw HTML → object storage; parsed data → index pipeline.

Scale: 1 B pages, avg 100 KB = 100 TB storage; 1 B / (30 days × 86 400 s) ≈ 400 pages/s.

Politeness:
- Per-domain rate limiting — do not hammer a single host.
- Obey robots.txt Disallow rules.

De-duplication:
- URL seen-set: Bloom filter (space-efficient; small false-positive rate).
- Content de-dup: simhash of page content → detect near-duplicates.

Distributed crawler:
- Consistent hashing on domain → assign domain to a specific worker.
→ All requests to a domain go through one worker → easy per-domain rate limit.

## 7. Remember & rehearse
- Design a URL shortener: what is the data model? How do you scale reads?
- Explain fan-out on write vs fan-out on read. When do you use the hybrid?
- Why is WebSocket preferred over polling for chat?
- What is a Snowflake ID and what properties does it have?
- Sketch the video upload + transcoding pipeline end-to-end.
- What geospatial index would you use for a ride-sharing app? Why?
- How does a Bloom filter help a web crawler?
