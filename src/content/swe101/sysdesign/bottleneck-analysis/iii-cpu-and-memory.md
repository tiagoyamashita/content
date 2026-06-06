---
label: "III"
subtitle: "CPUとメモリ"
group: "システム設計"
order: 3
---
CPUとメモリのボトルネック

コンピューティングと RAM の制限は、**負荷に応じたレイテンシー スケーリング**、**OOM**、**GC 一時停止**として表示されます。

## 1. CPU — 信号

|信号 |ツール/インジケーター |
|------|------|
|すべてのコアで **> 80%** を維持 | `top`、クラウド メトリクス |
|実行キュー **r > # CPUs** | `vmstat` |
|レイテンシー ∝ 負荷 (ヘッドルームなし) | APM p99 対 QPS |

## 2. CPU — 原因と解決策

|原因 |修正 |
|------|-----|
| O(n²) アルゴリズム |プロファイル (pprof、perf、py-spy);より良いアルゴリズム |
| **GIL** / グローバル ロック (Python) |マルチプロセス、非同期 I/O、ホット パス用の Rust/Go |
|高い QPS での JSON エンコード/デコード | Protobuf、msgpack;解析されたオブジェクトをキャッシュする |
|スレッド/ゴルーチンの爆発 |制限されたワーカー プール。非同期 I/O とリクエストごとのスレッド |
|リクエストごとに正規表現をコンパイルする |プリコンパイル。再利用 |

<figure class="notes-diagram"><svg xmlns="3 viewBox="0 0 420 80" role="img" aria-label="Profile before optimize CPU hot path">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Profiler-driven fixes only</text>
  <text x="12" y="40" fill="#86efac" font-size="9">measure → flame graph → fix top 1–2 frames → re-measure</text>
  <text x="12" y="58" fill="#f87171" font-size="9">avoid optimising cold paths</text>
</svg></figure>

## 3. メモリ — 信号

|信号 |意味 |
|--------|--------|
| **OOM キル** |プロセスが cgroup 制限を超えました |
| **スワップ > 0** | RAM が使い果たされました — ディスク速度の RAM |
| **GC 一時停止のスパイク** | JVM / ストップ・ザ・ワールドに行く |
| Redis **evicted_keys** ↑ |キャッシュが RAM に対して大きすぎます |

## 4. メモリ — 原因と解決策

|原因 |修正 |
|------|-----|
|メモリリーク |ヒーププロファイラー。ライフサイクル/リスナーを修正する |
|オーバーキャッシュ | TTL、maxmemory ポリシー、より小さい値 |
|大量コピー |ポインタ、ストリーミング、可能な場合はゼロコピー |
|割り当てのチャーン |オブジェクトプール。有効期間の短い割り当てを減らす |
| JVM ヒープが小さすぎる/大きすぎる | `-Xmx`を調整します。遅延のための G1/ZGC |

## 5. CPU とメモリの相互作用

|パターン |症状 |
|----------|----------|
| CPU バウンド + メモリ不足 | CPU インスタンスのスケールアウト |
|メモリ制限 + 低 CPU |より大きなRAM。キャッシュ層。漏れの修正 |
| GC スラッシング |高い CPU + 高い割り当てレート - 最初に割り当てを減らします |

## 6. 簡単なチェックリスト

- [ ] 最もホットなエンドポイントのフレーム グラフ
- [ ] RSS が無制限に増大する場合のヒープ ダンプ
- [ ] 1 つの変更前と変更後の p99 を比較
- [ ] 予想ピークの 2 倍での負荷テスト

**関連:** [ボトルネックの特定](ii-identifying-bottlenecks.md)、アプリケーション ホット キー [アプリケーション レベル](vii-application-level.md)。
