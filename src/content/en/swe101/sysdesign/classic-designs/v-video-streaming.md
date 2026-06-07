---
label: "V"
subtitle: "Video streaming"
group: "System design"
order: 5
---
Video streaming
**YouTube / Netflix-style** systems split **upload + transcoding** (write-heavy, batch) from **playback** (read-heavy, CDN).

## 1. Two paths

| Path | Dominant concern | Components |
|------|------------------|------------|
| **Upload / transcode** | CPU, queue depth, storage | S3, SQS, workers |
| **Playback** | Bandwidth, latency | CDN, HLS/DASH |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 140" role="img" aria-label="Video upload pipeline and CDN playback">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Upload pipeline</text>
  <rect x="12" y="32" width="48" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="48" fill="#e4e4e7" font-size="8">Upload</text>
  <path d="M60 44 H88" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="88" y="32" width="48" height="24" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="96" y="48" fill="#e4e4e7" font-size="8">S3 raw</text>
  <path d="M136 44 H164" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="164" y="32" width="48" height="24" rx="2" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="172" y="48" fill="#e4e4e7" font-size="8">Queue</text>
  <path d="M212 44 H240" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="240" y="32" width="56" height="24" rx="2" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="248" y="48" fill="#e4e4e7" font-size="8">Transcode</text>
  <path d="M296 44 H324" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="324" y="32" width="48" height="24" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="332" y="48" fill="#e4e4e7" font-size="8">S3 HLS</text>
  <text x="12" y="78" fill="#d4d4d8" font-size="11" font-weight="600">Playback</text>
  <rect x="12" y="90" width="48" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="106" fill="#e4e4e7" font-size="8">Player</text>
  <path d="M60 102 H120" stroke="#86efac" stroke-width="1.5"/>
  <rect x="120" y="90" width="56" height="24" rx="2" fill="rgba(251,191,36,0.15)" stroke="#fbbf24"/>
  <text x="128" y="106" fill="#e4e4e7" font-size="8">CDN edge</text>
  <text x="188" y="106" fill="#a1a1aa" font-size="8">segments + manifest · ABR switches 360p–4K</text>
</svg></figure>

## 2. Upload pipeline (step by step)

| Step | Action |
|------|--------|
| 1 | Client requests **pre-signed URL** → upload raw file to **object storage** |
| 2 | Upload complete event → **job queue** (SQS, Kafka) |
| 3 | **Transcode workers** (GPU spot instances) produce renditions |
| 4 | Output **HLS** segments + `master.m3u8` manifest to storage |
| 5 | Metadata row: title, owner, duration, status=ready |

**Renditions (example)**

| Tier | Resolution | Bitrate |
|------|------------|---------|
| 360p | 640×360 | ~800 kbps |
| 720p | 1280×720 | ~2.5 Mbps |
| 1080p | 1920×1080 | ~5 Mbps |

## 3. Playback path

1. Client loads manifest from **CDN**.
2. Player measures bandwidth → **ABR** (adaptive bitrate) picks segment quality.
3. **99%+** requests served from edge; origin on miss only.

## 4. Metadata store

| Data | Store |
|------|-------|
| Video title, uploader, views | PostgreSQL or DynamoDB |
| View counts (high QPS) | Counter cache + async flush |
| Comments | Sharded SQL or NoSQL |

## 5. Scale and cost

| Lever | Why |
|-------|-----|
| CDN | Offloads bytes; global latency |
| Segment caching | Small files cache well |
| GPU transcode fleet | Parallelize; spot for cost |
| Separate read/write paths | Don’t transcode on play request |

**Related:** [CDN & edge caching](../scalable-patterns/vi-cdn-and-edge-caching.md), classic designs web crawler (object storage at scale).
