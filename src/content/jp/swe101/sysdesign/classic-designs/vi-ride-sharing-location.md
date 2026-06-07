---
label: "VI"
subtitle: "ライドシェアリングとロケーション"
group: "システム設計"
order: 6
---
ライドシェアリングと位置情報サービス

**Uber / Lyft スタイル** マッチング: **高頻度 GPS** を取り込み、**近くのドライバー**を見つけ、**ETA-ランク付けされた** 配車を割り当てます。

## 1. スケールスケッチ

|仮定 |レート |
|-----------|------|
| 100 万人のアクティブドライバー | |
| GPS 4 秒ごと | **250,000 のロケーション書き込み/秒** |

書き込みが優勢です。読み取りは、ホット リージョンに対する地理空間クエリです。

## 2. 位置情報の取り込み

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="Driver GPS to Redis geo and Kafka analytics">
  <rect x="12" y="40" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="58" fill="#e4e4e7" font-size="9">Driver app</text>
  <path d="M68 54 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="40" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="58" fill="#e4e4e7" font-size="9">Redis GEO</text>
  <path d="M180 54 H220" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="220" y="40" width="64" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="228" y="58" fill="#e4e4e7" font-size="9">Kafka</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Dual write: hot index + analytics log</text>
  <text x="12" y="88" fill="#71717a" font-size="9">GEOADD driver_id lat lng · stream for history/replay</text>
</svg></figure>

| Store | Purpose |
|-------|---------|
| **Redis Geo** (`GEOADD`, `GEORADIUS`) | Live matching — O(log N) |
| **Kafka** | History, surge pricing, ML features |

## 3. 地理空間インデックス

|インデックス |アイデア |使用者 |
|------|------|-----------|
| **ジオハッシュ** |緯度/経度 → Base32 文字列;プレフィックス = 近くのセル |簡単な半径検索 |
| **S2 セル** |階層的な球体タイリング |グーグル、ウーバー |
| **四分木** | 2 次元再帰的分割 |不均一な密度 |
| **PostGIS** | SQL 拡張機能 |小規模 / 管理者 |

**Geohash に関する注意事項:** エッジ セルには **近隣** ルックアップが必要です。1 つのハッシュ セル ≠ 完全な円です。

## 4. マッチングの流れ

|ステップ |アクション |
|------|----------|
| 1 |送迎付きのライダーリクエスト（緯度/経度） |
| 2 | **GEORADIUS** (または S2 クエリ) - R km 以内のドライバー、利用可能なステータス |
| 3 |ルートグラフから**ETA**によるランク(直線距離ではない) |
| 4 |トップドライバーへのオファータイムアウト → 次の候補 |
| 5 |受け入れる→トリップ状態マシン。ライブ位置を共有する |

## 5. トリップ状態（簡略化）

```text
REQUESTED → DRIVER_ASSIGNED → IN_PROGRESS → COMPLETED
                  ↓ timeout
              RE_OFFER
```

二重代入を防ぐために、受け入れ時に **冪等性** を使用してください。

## 6. 故障モード

|問題 |緩和 |
|------|-----------|
|古いドライバーの場所 |心拍数。更新がない場合は利用不可とマークする |
|バーの近くで雷鳴の群れ | 写真 バーの近くで雷鳴の群れリクエストの急増 + キューリクエスト |
|スプリットブレイン割り当て |ドライバーのステータスを楽観的にロック |

**関連:** パート I レプリケーション、スケーラブル パターンのリージョンごとのレート制限。
