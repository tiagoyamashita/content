---
label: "VIII"
subtitle: "排除プレイブック"
group: "システム設計"
order: 8
---
ボトルネック解消プレイブック

**インシデント**と**設計レビュー**の反復可能なプロセス - 最初に測定し、**影響の順番**で修正し、検証して再発を防止します。

## 1. 5 つのフェーズ

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="Five phase bottleneck playbook cycle">
  <rect x="12" y="40" width="72" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="28" y="58" fill="#e4e4e7" font-size="8">1 Measure</text>
  <path d="M84 54 H108" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="108" y="40" width="72" height="28" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="124" y="58" fill="#e4e4e7" font-size="8">2 Isolate</text>
  <path d="M180 54 H204" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="204" y="40" width="56" height="28" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="214" y="58" fill="#e4e4e7" font-size="8">3 Fix</text>
  <path d="M260 54 H284" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="284" y="40" width="72" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="296" y="58" fill="#e4e4e7" font-size="8">4 Validate</text>
  <path d="M356 54 H380" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="380" y="40" width="72" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="392" y="58" fill="#e4e4e7" font-size="8">5 Prevent</text>
</svg></figure>

### フェーズ 1 — 推測せずに測定する

|収集 |ツール |
|----------|----------|
| p50 / p95 / p99 レイテンシー | APM、Prometheus |
|スループット、エラー率 | RED ダッシュボード |
|リソースごとの USE | CPU、ディスク、NIC、DB |
|トレース滝 | 写真 トレース滝イェーガー、テンポ、X-Ray |

### フェーズ 2 — 隔離

|質問 |ナローズの原因 |
|----------|--------------|
|エンドポイントは 1 つだけですか、それともすべてですか? |ルート固有のバグと共有インフラ |
|デプロイ/cron/スパイクと相関関係がありますか? |変更と負荷 |
| 1 つの AZ、シャード、ホスト? |局所的な障害 |

### フェーズ 3 — 影響/コストによる修正

|優先順位 |戦術 |コスト |
|----------|----------|------|
| 1 |クエリ + インデックスの最適化 |低い |
| 2 |キャッシュ層、TTL チューニング |低～中 |
| 3 |非同期/キューオフホットパス |中 |
| 4 |スケールアウトインスタンス |中 |
| 5 |シャーディング/パーティショニング |高 |
| 6 |アーキテクチャの書き換え |非常に高い |

### フェーズ 4 — 検証

- 負荷テスト (**k6**、ローカスト、ガトリング) の前後
- デプロイ後に **p99** と **エラー バジェット** を監視する
- カナリア / 段階的なロールアウト

### フェーズ 5 — 防止

|アクション | |
|--------|---|
|インシデントを捉えた症状に関するアラート | |
|回帰のために CI/CD でテストをロードする | |
|ランブック: 症状 → 原因 → 修正 | |
|事件後のレビュー (非難の余地なし) | |

## 2. Runbook スニペット テンプレート

```markdown
## Alert: High p99 on POST /orders
- Dashboard: [link]
- Likely: DB lock wait, pool exhaustion, downstream payment timeout
- Steps: 1) trace sample 2) pg_stat_activity 3) pool metrics
- Mitigation: scale pooler, disable non-critical job, circuit-break payment
- Escalation: DBA on-call
```

＃＃３ 面接の回答形式

1. **メトリクス** が有害 (p99 レイテンシ)
2. **トレース** → DB スパン 800 ミリ秒
3. **EXPLAIN** → シーケンススキャン → インデックスの追加
4. 負荷テストによる **検証**
5. **防止** — 低速クエリ ログ アラート

**Related:** [Identifying bottlenecks](ii-identifying-bottlenecks.md), scalable patterns observability, SRE tooling.
