---
label: "IV"
subtitle: "CI と実践"
group: "SRE"
order: 4
---
SRE ツール — Terraform: CI とプラクティス


Automate **`plan`** review, reduce drift, and document operational assumptions baked into modules.

## 1. CI ゲート

典型的なパイプラインステージ:

1. **`terraform fmt -check`** — blocks noisy diffs.
2. **`terraform validate`** — catches syntax/provider misconfig early.
3. **`terraform plan`** — upload textual plan to PR; require reviewer acknowledgement before **`apply`** on protected branches.
4. Optional **`tfsec` / `checkov` / `tflint`** — policy-as-code for insecure defaults.

GitOps の負荷が高いフロー (**Atlantis**、Terraform クラウド実行タスク) の場合、承認をチーム RBAC にマップします。

## 2. 規律を保つ

- **`apply`** from CI with OIDC/IAM roles—not long-lived static keys on laptops where avoidable.
- Separate workspaces/backends per environment—never **`apply`** prod stacks accidentally using staging vars.

## 3. ランブックとモジュール

デフォルトが容量の仮定 (**インスタンス サイズ**、**リージョン**、**保持**) をエンコードする場合、運用コンテキストをミラーリングします。

- Module **`README`** — SLIs touched by defaults (e.g. NAT concurrency).
- Linked wiki/runbook URLs inside observability resources provisioned alongside infra.

## 4. ドリフトとインポート

- Schedule **`terraform plan`** against prod weekly—even without merges—to detect manual console edits early.
- **`import`** discovered orphans deliberately instead of letting unmanaged infra linger.

## 5. Kubernetes とのペアリングと可観測性

Provision **EKS/GKE/AKS**, node pools, IAM roles (**IRSA** / workload identity), load balancers, DNS—then layer Helm/`kubernetes_manifest` resources or GitOps controllers.

マネージド Prometheus/Grafana スタックは、Terraform プロバイダーを公開することがよくあります。可能な場合は、**クラスター**、**ネットワーク**、**ダッシュボード**、**Alertmanager** ルートを 1 つのレビュー済みパイプラインで一緒に進化させ続けます。

## 6. Terraform が停止する場所

Day-two workload rollout semantics remain Kubernetes controllers—Terraform provisions clusters/add-ons; **kubectl/Helm/GitOps** handle frequent microservice churn unless you intentionally unify via **`kubernetes_*`** resources (trade-offs on blast radius & plan runtime).

具体的なリポジトリのレイアウトと VPC + EKS モジュールのスケッチについては、**実際のデプロイメント** を参照してください。
