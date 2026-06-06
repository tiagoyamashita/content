---
label: "IV"
subtitle: "Git運用と運用"
group: "SRE"
order: 4
---
SRE ツール — Kubernetes: GitOps と運用

2 日目の習慣: マニフェストを運用コードのように扱う安全なロールアウト、訓練、パイプライン。

## 1. GitOps の考え方

- Manifests live in Git (**Flux**, **Argo CD**, **Terraform Kubernetes provider**, etc.)—peer review + CI validation precedes cluster reconcile.
- Avoid silent **`kubectl apply`** hotfixes without backporting YAML—drift becomes undebuggable during incidents.

## 2. 安全なロールアウトとエスカレーション

```text
kubectl apply -k overlays/prod
kubectl rollout undo deployment/checkout-api -n prod        # rollback RS
kubectl cordon node/ip-10-0-3-42                             # stop new placements
kubectl drain node/ip-10-0-3-42 --ignore-daemonsets --delete-emptydir-data
```

**PodDisruptionBudgets** とクラウド メンテナンス期間を使用してドレインを調整します。

## 3. RBAC 衛生管理

- Separate **`cluster-admin`** break-glass from everyday **`Role`**/`RoleBinding` scoped to namespaces.
- Prefer **OIDC** integration over long-lived static **`kubeconfig`** tokens where possible.

## 4. 失敗の訓練

爆発範囲がわかったら、制御された演習を実行します。

- ノードの非常遮断/ドレイン + ワークロードの再スケジュール。
- kube-apiserver/etcd フォロワーの損失 (インフラチームによる)。
- AZ/地域クラスターのネットワーク パーティション シミュレーション。

結果を Runbook に文書化します。**Prometheus/Grafana** からのアラート/SLO 書き込みダッシュボードを結び付けます。

## 5. 可観測性フック

- **DaemonSets** はノードレベルのメトリック/ログ (Promtail/Fluent Bit、ノード エクスポーター) を提供します。
- **アドミッション Webhook** は、ラベル、リソースのデフォルト、イメージ署名を適用し、メトリクスを介して Webhook レイテンシーを表面化します。

## 6. ペアリング

Prometheus scrapes Pod endpoints; Grafana dashboards pivot on **`namespace`**, **`deployment`**, **`pod`**, **`node`** labels—align label conventions across metrics and Kubernetes labels (`prometheus.io/*` annotations vs **`ServiceMonitor`**).
