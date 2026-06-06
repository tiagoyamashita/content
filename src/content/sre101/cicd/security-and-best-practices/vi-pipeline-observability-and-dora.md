---
label: "VI"
subtitle: "パイプラインの可観測性と DORA"
group: "CI/CD"
order: 6
---
パイプラインの可観測性と DORA

パイプラインは **分散システム** であり、本番環境と同様に測定します。 **DORA メトリクス** は配信速度と信頼性を結び付けます。

## 1. DORA の 4 つの主要な指標

|メトリック |対策 |より良い方向へ |
|----------|----------|----------|
| **展開頻度** |本番環境に発送する頻度 |高レベル (成熟したチーム向け) |
| **変更のリードタイム** |コミット→本番環境で実行 |下 |
| **失敗率の変更** | % デプロイによりインシデント/ロールバックが発生します |下 |
| **MTTR** |障害後の平均復元時間 |下 |

エリート パフォーマー: オンデマンドでのデプロイ、1 日未満のリードタイム、15% 未満の CFR、1 時間未満の MTTR — 目標はドメイン (銀行か SaaS) によって異なります。

## 2. CI/CD データへのメトリクスのマッピング

| DORA メトリック | CI/CD信号 |
|---------------|--------------|
|導入頻度 |デプロイワークフローは `main` / prod タグで実行されます |
|リードタイム | `commit timestamp` → `deploy job end` |
|故障率の変更 |導入後、24 時間以内にロールバックまたはホットフィックスを実行 |
| MTTR |インシデントオープン → 本番環境が復元 (PagerDuty + デプロイログ) |

```yaml
# Tag deploy job for analytics
deploy:
  environment:
    name: production
  steps:
    - name: Record deploy metadata
      run: |
        echo "deploy_sha=${{ github.sha }}" >> $GITHUB_STEP_SUMMARY
        echo "deploy_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_STEP_SUMMARY
```

データ ウェアハウス (BigQuery、Snowflake) または **Haystack**、**LinearB**、**Swarmia** などのツールにエクスポートします。

## 3. パイプラインの健全性メトリクス

|メトリック |なぜ追跡するのか |
|----------|----------|
| **P50 / P95 の期間** | deps またはキャッシュミスによる速度低下をキャッチ |
| **待ち時間** |ランナーのキャパシティ プランニング |
| **キャッシュ ヒット率** |コストとスピード |
| **不安定なテスト率** |質の高い負債 |
| **段階別の故障率** |どこに投資するか |

```yaml
# GitHub — job timing in summary
- run: echo "duration=${SECONDS}s" >> $GITHUB_STEP_SUMMARY
```

## 4. アラート

|警告 |チャンネル |重大度 |
|----------|-----------|----------|
| `main` パイプラインが失敗しました |スラック `#ci-alerts` |高 |
|本番環境のデプロイに失敗しました | PagerDuty |クリティカル |
|夜間のセキュリティ スキャン CVE | Slack + チケット |中 |
| P95 持続時間 > ベースラインの 2 倍 |スラック |低い |

```yaml
- name: Notify on failure
  if: failure() && github.ref == 'refs/heads/main'
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {"text": "Main CI failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"}
```

アラート疲労を回避します — **本番パス** の失敗に関するページのみを表示します。

## 5. OpenTelemetry トレース

分散トレースのカスタム ステップを計測します。

```yaml
- name: Run integration tests
  env:
    OTEL_SERVICE_NAME: ci-integration
    OTEL_EXPORTER_OTLP_ENDPOINT: https://otel.example.com
  run: |
    otel-cli exec -- mvn -Pintegration verify
```

**Honeycomb**、**Grafana Tempo**、または **Jaeger** でスパンを表示し、遅い実行を並べて比較します。

## 6. ダッシュボードの例 (何をグラフ化するか)

|パネル |クエリのアイデア |
|------|-----------|
|デプロイ/週 |製品デプロイ イベントを数える |
|リードタイムの​​傾向 |コミット→デプロイ時間の中央値 |
| CI期間 P95 |ワークフローによるジョブ終了 - ジョブ開始 |
|メインブランチの成功率 % |緑のラン / 総ラン |
|キューの深さ |自己ホスト型プール上の保留中のジョブ |

## 7. CI と CD の可観測性

|フェーズ |フォーカス |
|------|------|
| **CI** (ビルド/テスト) |高速フィードバック、フレーク検出、キャッシュ |
| **CD** (展開) | DORA メトリクス、ロールバック時間、爆発範囲 |

CI グリーンを CD デプロイに接続します。グリーン ビルドがデプロイされない場合でも、**リード タイム**はかかります。

## 8. リハーサルの答え

- **リードタイム** — コードのコミットから本番までの時間。
- **変更失敗率** — 単体テストの失敗率ではありません。ユーザーに損害を与えるデプロイ。
- **CI をトレースする理由** — 合計時間が 2 倍になったときにどのステージが後退したかを調べます。
- **MTTR** — 検出、修正、再展開が含まれます。

**関連:** [テスト戦略](v-testing-strategy.md)、[ゲートとロールバックのリリース](vii-release-gates-and-rollbacks.md)、パート I の基礎。
