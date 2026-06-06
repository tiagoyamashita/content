---
label: "memory-estimator"
group: "システム設計"
order: 99
---
システム設計 — メモリ推定 (対話型)

**プレビュー モードのグラフ**を使用して、セッション サイズ、ノード数、およびノー​​ドごとの RAM のスライダーをドラッグします。

**完全な書き込み** — 数式、同時実行テーブル、実行されたシナリオ、および図: **[メモリ推定ツール](mem-memory-estimator.md)**。

## クイックリファレンス

```text
concurrent_users = DAU × concurrency_factor
working_set      = concurrent_users × bytes_per_user
total_RAM        ≈ working_set × 2
nodes            = ceil(total_RAM / usable_RAM_per_node)
```

|アプリの種類 |ピーク同時 |
|----------|------|
|ウェブ | DAU の 5 ～ 10% |
|リアルタイム | DAU の 20 ～ 40% |

## 対話型推定器

プレビューでスライダーを調整して次のことを確認します。

- アクティブ ユーザーごとの **セッション/キャッシュ バイト数**
- クラスター内の **ノード数**
- **RAM/ノード** (マイナスOS予約)

**ヘッドルーム** と **シャーディング** が OOM の前に安全な容量をどのように変更するかを見てください。
