---
label: "IV"
subtitle: "I/O とストレージ"
group: "システム設計"
order: 4
---
I/O とストレージのボトルネック

**ディスクとオブジェクト ストレージ**は、CPU より先にデータベース、ログ、メディア パイプラインを制限することがよくあります。

## 1. ディスク I/O — 信号

| Signal | Tool |
|--------|------|
| High **iowait** | `top`, `mpstat` |
| **%util → 100%** | `iostat -x` |
| Random read **> 1 ms** on SSD | Latency histogram |
| Write queue depth growing | `await` in iostat |

## 2. ディスク — 原因と修正

|原因 |修正 |
|------|-----|
|ランダムな小さな読み取り |順次アクセス。先読み。インデックス |
|同期ログ |非同期追加。集中ログエージェント |
|フルテーブルスキャン | WHERE / JOIN 列のインデックス |
|行ごとの fsync |バッチ書き込み。 WAL バッチ処理 |
| OLTP の HDD | **NVMe SSD**; Linux 上の io_uring |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Sequential vs random disk access">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Access pattern matters</text>
  <text x="12" y="40" fill="#86efac" font-size="9">Sequential scan of index range — SSD friendly</text>
  <text x="12" y="56" fill="#f87171" font-size="9">Random lookups across huge table — IOPS limit</text>
  <rect x="12" y="64" width="200" height="12" rx="2" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="220" y="74" fill="#a1a1aa" font-size="8">contiguous</text>
  <rect x="12" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="80" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="160" y="80" width="40" height="12" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="220" y="90" fill="#a1a1aa" font-size="8">scattered</text>
</svg></figure>

## 3. オブジェクトストレージ (S3-style)

|ボトルネック |修正 |
|-----------|-----|
| **プレフィックス ホット スポット** |キープレフィックスをランダム化します。スプレッドパーティション |
|大規模なアップロード | **マルチパート** アップロード (5 MB–5 GB パート) |
|多くの小さな LIST |巨大なプレフィックスをリストすることは避けてください。 DB のインデックス メタデータ |
|下りコスト | CDN が前にあります。同じリージョンの読み取り |

## 4. WAL とチェックポイント (データベース)

| Issue | Tuning |
|-------|--------|
| WAL fsync latency | Faster disk; group commit |
| Checkpoint spike | `checkpoint_completion_target` spread |
| Replication lag | Network + WAL send rate |

## 5. ストレージ層をエスカレーションする場合

|ワークロード |階層 |
|----------|------|
| OLTP プライマリ | NVMe SSD / プロビジョニング済み IOPS |
|分析スキャン |列ストア / オブジェクト + Spark |
|アーカイブ |コールド オブジェクト ストレージ |
|ログ |アグリゲーターにストリームします。永久にローカルディスクではありません |

**Related:** [Database](vi-database.md), classic designs video streaming (S3).
