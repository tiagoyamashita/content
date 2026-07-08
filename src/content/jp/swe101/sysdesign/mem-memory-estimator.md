---
label: "Mem"
subtitle: "メモリ推定器"
group: "システム設計"
order: 5
---
システム設計 - メモリの見積もり

セッション、キャッシュ、アプリ ヒープの基本的な **RAM** のサイジング - インスタンスを購入する前、または **OOM** に到達する前のインタビューとキャパシティ プランニングに不可欠です。

## 1. なぜメモリを見積もるのでしょうか?

|質問 |メモリ推定の答え |
|----------|----------------------|
| **Redis** ノードはいくつですか? |ホット データ セット + オーバーヘッド |
|アプリの**ヒープ**サイズ/ポッド制限? |セッション + 飛行中のオブジェクト |
|ピーク時には **OOM** するでしょうか? |同時ユーザー数 × ユーザーあたりのバイト数 |
|スケールは**垂直**ですか、**水平**ですか? |ワーキング セットと単一ノードの RAM の上限 |

多くの場合、明らかな CPU ボトルネックを修正した後の最初のハード制限はメモリです。**ボトルネック分析→ CPU とメモリ**を参照してください。

## 2. コアフォーミュラ

```text
RAM_working_set ≈ concurrent_users × bytes_per_active_user
```

**DAU** ではありません — ピーク時に **同時にアクティブになる**ユーザーのみです。

```text
concurrent_users = DAU × concurrency_factor

Example:
  10_000_000 DAU × 0.08 × 50 KB ≈ 40 GB working set (sessions/cache only)
```

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="DAU to concurrent users to RAM">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Peak memory chain</text>
  <rect x="12" y="36" width="80" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="54" fill="#e4e4e7" font-size="9">DAU</text>
  <path d="M92 50 H112" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="96" y="44" fill="#71717a" font-size="7">× factor</text>
  <rect x="112" y="36" width="96" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="120" y="54" fill="#e4e4e7" font-size="9">concurrent</text>
  <path d="M208 50 H228" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="210" y="44" fill="#71717a" font-size="7">× bytes</text>
  <rect x="228" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="244" y="54" fill="#e4e4e7" font-size="9">RAM (GB)</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Add 2× headroom before dividing by node RAM (§6).</text>
</svg></figure>

## 3. 同時実行係数 (ピーク)

|アプリの種類 |ピーク同時実行数 (DAU の %) |メモ |
|----------|----------------------------|----------|
|ウェブ/電子商取引全般 | **5 ～ 10%** |昼食 + 夕方のピーク |
|ソーシャル / フィード (モバイル) | **10 ～ 20%** |長いセッション |
|リアルタイム (チャット、ゲーム、コラボ) | **20–40%** | WebSocket は開いたまま |
| B2B SaaS (営業時間) | **WAU** の **15 ～ 25%** | DAU がスパースの場合は、毎週アクティブを使用します。
|バッチ / API のみ | **無視できるセッション RAM** |代わりにリクエストバッファあたりのサイズ |

**インタビューのヒント:** 仮定を明確に述べてください — 「1,000 万 DAU、ピーク時の同時実行数 8% → 同時実行数 800 K と仮定します。」

## 4. アクティブ ユーザーあたりのバイト数 (カウントする内容)

|インメモリ項目 |典型的なサイズ | | の場合にカウントします。
|--|--------------|-----------|
| HTTP セッション (サーバー側) | 1–20 KB |スティッキーセッション、カート |
|メモリ内の JWT (解析されたクレーム) |< 1 KB | Usually stateless — **don’t** multiply by DAU |
| Cached user profile | 5–50 KB | Redis `user:{id}` |
| Home feed / timeline slice | 50–500 KB | Push model precomputed feed |
| Full page HTML fragment | 100 KB – 2 MB | Edge/page cache |
| WebSocket connection buffers | 4–16 KB+ | Chat, live updates |
| In-flight request context | 1–10 KB | Per concurrent request on app |

**Stack only what you store in RAM** — not everything in the database.

### Example session breakdown (50 KB total)

| Field | Size |
|-------|------|
| `user_id`, roles | 200 B |
| Cart (10 line items) | 8 KB |
| Recent views | 12 KB |
| CSRF + flash messages | 2 KB |
| Framework overhead | ~28 KB |
| **Total** | **~50 KB** |

## 5. Full-system RAM budget

One region at peak — allocate **per layer**:

| Component | What to size | Rule of thumb |
|-----------|--------------|---------------|
| **App servers** | Heap + native + threads | `working_set × 1.3` heap overhead (JVM/Go) |
| **Redis / Memcached** | Hot keys | Data + **~25%** fragmentation (`mem_fragmentation_ratio`) |
| **PostgreSQL** | Buffer cache | `shared_buffers` ≈ **25%** of DB instance RAM |
| **OS + kernel** | — | Reserve **512 MB – 2 GB** per node |
| **Sidecars / agents** | mesh, logs | 128–512 MB each |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 160" role="img" aria-label="Tiered memory from hot RAM to cold disk">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Tiered data temperature</text>
  <rect x="12" y="36" width="120" height="32" rx="3" fill="rgba(248,113,113,0.15)" stroke="#f87171"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="9">Hot — Redis RAM</text>
  <rect x="12" y="76" width="120" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="96" fill="#e4e4e7" font-size="9">Warm — SSD cache</text>
  <rect x="12" y="116" width="120" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="136" fill="#e4e4e7" font-size="9">Cold — DB disk</text>
  <text x="148" y="56" fill="#a1a1aa" font-size="9">Size with concurrent × bytes (§2)</text>
  <text x="148" y="96" fill="#a1a1aa" font-size="9">Less frequently accessed keys</text>
  <text x="148" y="136" fill="#a1a1aa" font-size="9">Source of truth — not in session RAM</text>
</svg></figure>

## 6. Headroom and node count

```text
total_RAM_required = working_set × 2        # GC, spikes, fragmentation
nodes              = ceil(total_RAM / RAM_per_node_usable)

usable_per_node    = node_RAM − OS_reserve − other_daemons
```

| Utilisation | Guidance |
|-------------|----------|
| **< 70%** steady | Healthy — room for spikes |
| **70–80%** | Plan scale event |
| **>80%** | OOM リスク — Linux キラーは高速です |

**例 — Redis クラスター**

|入力 |値 |
|------|------|
|ワーキングセット | 40 GB |
| 2倍のヘッドルーム付き | 80 GB |
|ノードサイズ | 32 GB RAM、2 GB OS → **30 GB 使用可能** |
|ノード |`ceil(80 / 30)`= **3** Redis シャード/レプリカ |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 90" role="img" aria-label="Split working set across three nodes">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">80 GB target → 3 × ~27 GB shards</text>
  <rect x="12" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="36" y="58" fill="#e4e4e7" font-size="9">Node A</text>
  <rect x="120" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="144" y="58" fill="#e4e4e7" font-size="9">Node B</text>
  <rect x="228" y="36" width="100" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="252" y="58" fill="#e4e4e7" font-size="9">Node C</text>
</svg></figure>

## 7. 成功したシナリオ

### A — セッション ストア (Redis)

|仮定 |値 |
|-----------|----------|
| DAU | 5分 |
|同時実行性 | 10% → **500,000** |
|セッションサイズ | 8 KB |
|生 | 500 K × 8 KB = **4 GB** |
| +25% Redis オーバーヘッド | **5 GB** |
| ×2 ヘッドルーム | **10 GB** Redis フリート |

### B — 事前計算されたニュース フィード (クラシック デザイン)

|仮定 |値 |
|-----------|----------|
| DAU | 20M |
|ファンアウト キャッシュ: 30% のユーザーがプッシュ フィードを取得 | 6 M フィードが保存されました (フル DAU ではありません) |
| Redis のフィード スライスあたり 200 KB | 6M × 200 KB ≈ **1.2 TB** |
|緩和 |上位 500 件の投稿をトリミングします。圧縮する。引くべき階層の有名人 |

**書き込み時のファンアウト**は書き込み増幅だけではなく**メモリ**の問題であることを示しています。

### C — JVM API ポッド

|仮定 |値 |
|-----------|----------|
| 800 K 同時 | |
| 50 KB 有効状態が Redis にオフロードされる |ヒープは主にバッファを要求します。
| 200 MB ベースライン + 2 KB × 飛行中 (5 K/pod) |ステートレスの場合、ポッドあたりヒープのサイズ **512 MB–1 GB** |
| QPS からのポッド数 |セッション RAM から分離 |

## 8. メモリがいっぱいの場合のエビクション

|ポリシー |立ち退き |最適な時期 |
|----------|----------|----------|
| **LRU** |最も最近使用されていない |均一なアクセス。セッション |
| **LFU** |最も使用頻度の低い |べき乗則ホットキー |
| **TTL** |アイドルタイムアウト後 |予測可能なセッションの有効期限 |
| **maxmemory-policy** | Redis:`allkeys-lru`、`volatile-lru`、など |マッチキー TTL 戦略 |

**TTL + LRU のペア:** アイドル状態のセッションを期限切れにします。 LRU は、次の場合にバーストを処理します。`maxmemory`。

## 9. スケーリング戦略

|戦略 |メモリー効果 |
|----------|--------------|
| **垂直** |ノードあたりの RAM を大きくする - ハードウェアの上限まですぐ |
| **水平** |シャードの作成者`user_id`ハッシュ — スプレッド ワーキング セット |
| **一貫性のあるハッシュ リング** |ノードの追加 → 最小限のキーの再マッピング |
| **階層型キャッシュ** | RAM ホット。 SSD 暖かい |
| **値を圧縮** | Redis の Snappy/LZ4 — CPU ↔ RAM 取引 |
| **クライアントへのオフロード** | JWT ステートレス — サーバーの削減 RAM、その他のトレードオフ |

## 10. よくある間違い

|間違い |修正 |
|----------|-----|
| **同時**の代わりに**DAU**を使用してください。同時実行係数を適用する |
| DB サイズ全体を「必要なメモリ」としてカウントします。キャッシュ内のホット/ワーキング セットのみ |
| **レプリケーション**を無視する |プライマリとレプリカはそれぞれデータを保持します - 両方を計画する |
| 100% RAM 使用率目標 | **30%+** を無料で維持 |
| Web と WebSocket で同じバイト |存続期間の長い接続にはバッファ バジェットが必要です。

## 11. 面接チェックリスト

- [ ] 状態 DAU、同時実行率 %、同時ユーザーを導出
- [ ] ユーザーごとのバイト数の項目 (セッション、キャッシュ、フィード)
- [ ] 乗算 → ワーキングセット GB
- [ ] ×2 ヘッドルーム;使用可能なノード RAM で除算
- [ ] エビクション (LRU/TTL) と TB-scale の場合のシャーディングについて言及する
- [ ] RAM に **ない**ことに注意してください (ディスク上の完全な DB)

**関連:** パート I の容量見積もり、**クラシックな設計** (フィード、URL 短縮機能)、**ボトルネック分析 → CPU およびメモリ**。
