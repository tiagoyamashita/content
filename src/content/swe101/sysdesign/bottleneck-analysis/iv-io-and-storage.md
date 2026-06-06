---
label: "IV"
subtitle: "I/Oとストレージ"
group: "システム設計"
order: 4
---
I/O とストレージのボトルネック

**ディスクおよびオブジェクト ストレージ**は、CPU よりも先にデータベース、ログ、メディア パイプラインを制限することがよくあります。

## 1. ディスク I/O — 信号

|信号 |ツール |
|------|------|
|高 **iowait** | `top`、`mpstat` |
| **%util → 100%** | `iostat -x` |
| SSD 上のランダム読み取り **> 1 ミリ秒** |レイテンシのヒストグラム |
|書き込みキューの深さが増加 | iostatの`await` |

## 2. ディスク — 原因と修正

|原因 |修正 |
|------|-----|
|ランダムな小さな読み取り |順次アクセス。先読み。インデックス |
|同期ログ |非同期追加。集中ログエージェント |
|フルテーブルスキャン | WHERE / JOIN 列のインデックス |
|行ごとの fsync |バッチ書き込み。 WAL バッチ処理 |
| OLTP用HDD | **NVMe SSD**; Linux 上の io_uring |

<figure class="notes-diagram"><svg xmlns="5 viewBox="0 0 440 100" role="img" aria-label="Sequential vs random disk access">
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

## 3. オブジェクト ストレージ (S3 スタイル)

|ボトルネック |修正 |
|-----------|-----|
| **プレフィックス ホット スポット** |キープレフィックスをランダム化します。スプレッドパーティション |
|大規模なアップロード | **マルチパート** アップロード (5 MB ～ 5 GB のパート) |
|多数の小さなリスト |巨大なプレフィックスをリストすることは避けてください。 DB 内のインデックスメタデータ |
|下りコスト | CDN が前にあります。同じリージョンの読み取り |

## 4. WAL とチェックポイント (データベース)

|問題 |チューニング |
|------|----------|
| WAL fsync 遅延 |より高速なディスク。グループコミット |
|チェックポイントスパイク | `checkpoint_completion_target` スプレッド |
|レプリケーションの遅延 |ネットワーク + WAL 送信速度 |

## 5. ストレージ層をエスカレーションする場合

|ワークロード |階層 |
|----------|------|
| OLTP プライマリ | NVMe SSD / プロビジョンド IOPS |
|分析スキャン |列ストア / オブジェクト + Spark |
|アーカイブ |コールド オブジェクト ストレージ |
|ログ |アグリゲーターにストリームします。永久にローカルディスクではありません |

**関連:** [データベース](vi-database.md)、クラシック デザインのビデオ ストリーミング (S3)。
