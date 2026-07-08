---
label: "III"
subtitle: "CPU とメモリ"
group: "システム設計"
order: 3
---
CPU とメモリのボトルネック

コンピューティングおよび RAM の制限は、**負荷に応じたレイテンシのスケーリング**、**OOM**、および **GC の一時停止**として表示されます。

## 1. CPU — シグナル

| Signal | Tool / indicator |
|--------|------------------|
| Sustained **> 80%** all cores | `top`, cloud metrics |
| Run queue **r > # CPUs** | `vmstat` |
| Latency ∝ load (no headroom) | APM p99 vs QPS |

## 2. CPU — 原因と解決策

|原因 |修正 |
|------|-----|
| O(n²) アルゴリズム |プロファイル (pprof、perf、py-spy);より良いアルゴリズム |
| **GIL** / グローバル ロック (Python) |マルチプロセス、非同期 I/O、Rust/ホット パス用の Go |
| JSON は高い QPS でエンコード/デコードします | Protobuf、msgpack;解析されたオブジェクトをキャッシュする |
|スレッド/ゴルーチンの爆発 |制限されたワーカー プール。非同期 I/O とリクエストごとのスレッド |
|リクエストごとに正規表現をコンパイルする |プリコンパイル。再利用 |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 80" role="img" aria-label="Profile before optimize CPU hot path">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Profiler-driven fixes only</text>
  <text x="12" y="40" fill="#86efac" font-size="9">measure → flame graph → fix top 1–2 frames → re-measure</text>
  <text x="12" y="58" fill="#f87171" font-size="9">avoid optimising cold paths</text>
</svg></figure>

## 3. メモリ — 信号

|信号 |意味 |
|--------|--------|
| **OOM を殺す** |プロセスが cgroup 制限を超えました |
| **スワップ > 0** | RAM が使い果たされました — ディスク速度 RAM |
| **GC 一時停止スパイク** | JVM / ストップ・ザ・ワールドに行きましょう |
| Redis **evicted_keys** ↑ | RAM にはキャッシュが大きすぎます |

## 4. メモリ — 原因と解決策

| Cause | Fix |
|-------|-----|
| Memory leak | Heap profiler; fix lifecycle / listeners |
| Over-caching | TTL, maxmemory policy, smaller values |
| Large copies | Pointers, streaming, zero-copy where possible |
| Allocation churn | Object pools; reduce short-lived allocations |
| JVM heap too small/large | Tune `-Xmx`; G1/ZGC for latency |

## 5. CPU とメモリの相互作用

|パターン |症状 |
|----------|----------|
| CPU バウンド + メモリ不足 | CPU インスタンスをスケールアウトする |
|メモリ制限 + 低 CPU |大きい RAM;キャッシュ層。漏れの修正 |
| GC スラッシング |高い CPU + 高い割り当て率 - 最初に割り当てを減らす |

## 6. 簡単なチェックリスト

- [ ] 最もホットなエンドポイントのフレーム グラフ
- [ ] RSS が無制限に増大する場合のヒープ ダンプ
- [ ] 1 つの変更前と変更後の p99 を比較
- [ ] 予想ピークの 2 倍での負荷テスト

**Related:** [Identifying bottlenecks](ii-identifying-bottlenecks.md), application hot keys [Application-level](vii-application-level.md).
