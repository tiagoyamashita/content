---
label: "V"
subtitle: "ビデオストリーミング"
group: "システム設計"
order: 5
---
ビデオストリーミング

**YouTube / Netflix スタイル** システムは、**アップロード + トランスコーディング** (書き込みが多い、バッチ) と **再生** (読み取りが多い、CDN) を分割します。

## 1. 2 つのパス

|パス |主要な懸念事項 |コンポーネント |
|------|-------|-----------|
| **アップロード/トランスコード** | CPU、キューの深さ、ストレージ | S3、SQS、労働者 |
| **再生** |帯域幅、遅延 | CDN、HLS/DASH |

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

## 2. パイプラインのアップロード (ステップバイステップ)

| Step | Action |
|------|--------|
| 1 | Client requests **pre-signed URL** → upload raw file to **object storage** |
| 2 | Upload complete event → **job queue** (SQS, Kafka) |
| 3 | **Transcode workers** (GPU spot instances) produce renditions |
| 4 | Output **HLS** segments + `master.m3u8` manifest to storage |
| 5 | Metadata row: title, owner, duration, status=ready |

**レンディション（例）**

|階層 |解像度 |ビットレート |
|------|-----------|----------|
| 360p | 640×360 | ～800kbps |
| 720p | 1280×720 | ～2.5Mbps |
| 1080p | 1920×1080 | ～5Mbps |

## 3. 再生パス

1. クライアントは **CDN** からマニフェストを読み込みます。
2. プレーヤーが帯域幅を測定 → **ABR** (適応ビットレート) がセグメントの品質を選択します。
3. **99%+** リクエストはエッジから処理されます。ミス時のみの原点。

## 4. メタデータ ストア

|データ |ストア |
|------|------|
|動画のタイトル、アップローダー、再生回数 | PostgreSQL または DynamoDB |
|閲覧数 (高い QPS) |カウンターキャッシュ + 非同期フラッシュ |
|コメント |シャード化された SQL または NoSQL |

## 5. 規模とコスト

|レバー |なぜ |
|------|-----|
| CDN |バイトをオフロードします。グローバルレイテンシ |
|セグメントキャッシュ |小さなファイルは適切にキャッシュされます。
| GPU トランスコード フリート |並列化します。費用のスポット |
|個別の読み取り/書き込みパス |再生リクエスト時にトランスコードしない |

**Related:** [CDN & edge caching](../scalable-patterns/vi-cdn-and-edge-caching.md), classic designs web crawler (object storage at scale).
