---
label: "IV"
subtitle: "GitOps と運用"
group: "SRE"
order: 4
---
SRE ツール — Kubernetes: GitOps と運用

2 日目の習慣: マニフェストを運用コードのように扱う安全なロールアウト、訓練、パイプライン。

## 1. GitOps の考え方

- マニフェストは Git 内に存在します (**Flux**、**Argo CD**、**Terraform Kubernetes プロバイダー** など)。ピアレビュー + CI 検証がクラスターの調整に先立ちます。
- YAML をバックポートせずにサイレント **`kubectl apply`** ホットフィックスを回避します。インシデント中にドリフトがデバッグできなくなります。

## 2. 安全なロールアウトとエスカレーション

```text
kubectl apply -k overlays/prod
kubectl rollout undo deployment/checkout-api -n prod        # rollback RS
kubectl cordon node/ip-10-0-3-42                             # stop new placements
kubectl drain node/ip-10-0-3-42 --ignore-daemonsets --delete-emptydir-data
```

**PodDisruptionBudgets** とクラウド メンテナンス期間を使用してドレインを調整します。

## 3. RBAC の衛生管理

- **`cluster-admin`** のブレークグラスを、名前空間を対象とした日常の **`Role`**/`RoleBinding` から分離します。
- 可能であれば、有効期間の長い静的 **`kubeconfig`** トークンよりも **OIDC** 統合を優先します。

## 4. 失敗の訓練

爆発範囲がわかったら、制御された演習を実行します。

- ノードの非常遮断/ドレイン + ワークロードの再スケジュール。
- kube-apiserver/etcd フォロワーの損失 (インフラチームによる)。
- リージョン クラスターの AZ/ネットワーク パーティション シミュレーション。

結果をランブックに文書化します。**Prometheus/Grafana** からのアラート/SLO 書き込みダッシュボードを結び付けます。

## 5. 可観測性フック

- **DaemonSets** はノードレベルのメトリック/ログ (Promtail/Fluent Bit、ノード エクスポーター) を提供します。
- **アドミッション Webhook** は、ラベル、リソースのデフォルト、イメージ署名を適用し、メトリクスを介して Webhook レイテンシーを表面化します。

## 6. ペアリング

Prometheus は Pod エンドポイントをスクレイピングします。 Grafana ダッシュボードは **`namespace`**、**`deployment`**、**`pod`**、**`node`** ラベルを中心に、メトリックと Kubernetes ラベル全体でラベル規則を調整します (`prometheus.io/*` アノテーションと **`ServiceMonitor`**)。
