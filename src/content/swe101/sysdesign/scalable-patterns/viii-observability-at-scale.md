---
label: "VIII"
subtitle: "大規模な可観測性"
group: "システム設計"
order: 8
---
大規模な可観測性

大規模な場合、1 つの遅い依存関係が **カスケード** します。 **メトリクス**、**ログ**、**トレース**に加え、**SLO**と制御された**カオス**により、障害を可視化し、制限を維持します。

＃＃１．３つの柱

|柱 |答え |ツール (例) |
|----------|-----------|---------------------|
| **メトリクス** |いくら？どのくらい速いですか？エラー率? | Prometheus、Datadog、CloudWatch |
| **ログ** |この事例では何が起こったのでしょうか? |ロキ、ELK、クラウド ロギング |
| **痕跡** |このリクエストではどのホップが遅かったですか? |イェーガー、テンポ、ジプキン、X-Ray |

**Correlation:** same `trace_id` / `request_id` across all three.

## 2. 警告 — 症状が原因ではない

|アラートオン (良好) |アラートオン (騒音) |
|-----------------|-----------------|
| 5 分間のエラー率 > 1% | CPU > 80% |
| p99 遅延 > 500 ミリ秒 |単一ポッドの再起動 |
| SLO 燃焼率 14× 予算 |ディスクが 70% 使用されています |

**SLO の例:** 99.9% の可用性 = 月あたり最大 43 分のダウンタイム **エラー バジェット**。 **バーンレート**による予算の消費が速すぎる場合のページ。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Distributed trace waterfall across services">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Trace waterfall (one request)</text>
  <rect x="12" y="36" width="200" height="14" rx="2" fill="rgba(34,197,94,0.3)" stroke="#86efac"/>
  <text x="16" y="47" fill="#e4e4e7" font-size="8">api-gateway 120ms</text>
  <rect x="40" y="54" width="120" height="14" rx="2" fill="rgba(59,130,246,0.3)" stroke="#60a5fa"/>
  <text x="44" y="65" fill="#e4e4e7" font-size="8">orders 80ms</text>
  <rect x="60" y="72" width="280" height="14" rx="2" fill="rgba(248,113,113,0.35)" stroke="#f87171"/>
  <text x="64" y="83" fill="#e4e4e7" font-size="8">postgres query 240ms ← bottleneck</text>
</svg></figure>

## 3. 分散トレーシング

1. **API ゲートウェイ** は、トレース ID (**W3C トレース コンテキスト** ヘッダー) を作成または受け入れます。
2. 各サービスは **スパン** (名前、開始、期間、ステータス) を作成します。
3. 送信 HTTP/gRPC/message メタデータのヘッダーを伝播します。
4. バックエンドストアのスパン。 UI は **ウォーターフォール** を示しています。

| Header | Purpose |
|--------|---------|
| `traceparent` | Trace and span ids (W3C) |
| `tracestate` | Vendor-specific hints |
| `X-Request-Id` | Support correlation (not a full trace) |

## 4. キャパシティプランニング

|メトリック |使用 |
|--------|-----|
| p50 / p95 / p99 レイテンシー |テール レイテンシが UX を引き起こす |
| QPS / スループット |スケールトリガー |
|飽和 (CPU、プール待機) |障害が発生する前のヘッドルーム |

**モデルの成長:** DAU +20%/月の場合、DB 接続プールまたはシャードの制限はいつ破られますか? **打ち上げ前の負荷テスト** (k6、ローカスト、ガトリング)。

## 5. カオスエンジニアリング

**ステージング** (または制御された本番環境) に意図的に障害を挿入します。

|実験 |検証 |
|-----------|----------|
|ランダムポッドをキルする | K8s の再起動 + LB の健全性 |
|依存関係に 500 ミリ秒の遅延を追加 |タイムアウト + サーキット ブレーカー |
|パーティション AZ |フェイルオーバー + レプリカのプロモーション |

ツール: Chaos Monkey、Litmus、AWS FIS。 **すべてのアラート**は**ランブック**にリンクする必要があります。

## 6. ランブックのテンプレート

|セクション |コンテンツ |
|----------|----------|
|症状 |ユーザーに表示されるもの |
|ダッシュボード |グラフへのリンク |
|考えられる原因 |順序付きチェックリスト |
|緩和 |スケール、ロールバック、機能フラグ |
|エスカレーション |次のページに行く人 |

## 7. リハーサル

- 仮想の API (可用性 + 遅延) に対して SLO を定義します。
- 4 つのサービスを介したトレース伝播を描画します。
- CPU ではなく、エラー率に基づいてアラートを発行する理由は何ですか?

**Related:** SRE tooling notes (Prometheus, Alertmanager), **Bottleneck analysis** submenu (`bottleneck-analysis/`).
