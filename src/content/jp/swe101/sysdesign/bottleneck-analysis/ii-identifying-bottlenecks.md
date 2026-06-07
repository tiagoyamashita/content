---
label: "II"
subtitle: "ボトルネックの特定"
group: "システム設計"
order: 2
---
ボトルネックの特定

ランダム レイヤーを最適化する前に、スループットを制限する **1 つのリソース**を見つけます。

## 1. 定義

**ボトルネック** = コンポーネントの使用率は **~100%** ですが、他のコンポーネントには余裕があります。他の場所に容量を追加しても、このリソースが解放されるまでシステムのスループットは向上しません。

## 2. リトルの法則

```text
L = λ × W

L = average requests in system (queue + in-flight)
λ = arrival rate (requests/s)
W = average time in system (seconds)
```

|観察 |意味 |
|-----------|-----------|
| **W** は定数 **λ** で上昇します。バックアップ — キューが増大中 |
| **L** が上昇 |遅延または同時実行の増加 |
|固定容量、より高い **λ** |最終的に **W** は爆発します |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 90" role="img" aria-label="Queue grows when service time exceeds capacity">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Saturation → queue</text>
  <rect x="12" y="32" width="120" height="20" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="24" y="46" fill="#e4e4e7" font-size="8">waiting requests ↑</text>
  <rect x="140" y="32" width="80" height="20" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="152" y="46" fill="#e4e4e7" font-size="8">processing</text>
  <text x="12" y="72" fill="#71717a" font-size="9">λ &gt; service capacity → W and L grow without bound</text>
</svg></figure>

## 3. ユニバーサル スケーラビリティの法則 (USL)

```text
X(N) = N / (1 + α(N−1) + βN(N−1))
```

|用語 |意味 |
|-----|----------|
| **α** |競合 — シリアルセクション (ロック、単一ライター) |
| **β** |コヒーレンシ — キャッシュの無効化、ゴシップコスト |
| **N** |ワーカー/ノード |

「完璧な」水平スケールであっても、連続分数では **アムダール** の制限に達します。

## 4. 体系的な探索 (5 つのステップ)

|ステップ |アクション |
|------|----------|
| 1 |有害な指標の定義: レイテンシー、スループット、エラー |
| 2 | **エンドツーエンド プロファイル** — APM トレース、スパン ウォーターフォール |
| 3 | **使用状況**を確認してください: CPU、メモリ、ディスク、ネットワーク、DB |
| 4 | **100%** に最も近いリソースが持続 → ボトルネックの可能性がある |
| 5 |修正 → **再測定** — 次のボトルネック表面 |

## 5. USE メソッド (インフラストラクチャ)

**各リソース** (CPU、ディスク、NIC、DB 接続):

|手紙 |質問 |
|----------|----------|
| **U** — 使用率 | % ビジー (例: CPU > 70% 継続 = 警告) |
| **S** — 彩度 |キューの深さ、待機時間 > 0? |
| **E** — エラー |再試行、タイムアウト、パケットのドロップ |

## 6. RED メソッド (サービス)

|手紙 |メトリック |
|----------|----------|
| **R** — レート | 1 秒あたりのリクエスト |
| **E** — エラー |エラー率 |
| **D** — 期間 |レイテンシー分布 (p50/p95/p99) |

**結合:** インフラ上の USE + 各サービス境界上の RED。

## 7. トレースファーストのワークフロー

```text
Slow request → trace_id → waterfall → longest span → USE/RED on that hop
```

| Span type | Next drill |
|-----------|------------|
| DB query | [Database](vi-database.md) |
| HTTP client | [Network](v-network.md), [Application-level](vii-application-level.md) |
| CPU-bound compute | [CPU & memory](iii-cpu-and-memory.md) |

**Related:** [Elimination playbook](viii-elimination-playbook.md), scalable patterns observability.
