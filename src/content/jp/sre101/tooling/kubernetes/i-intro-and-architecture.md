---
label: "I"
subtitle: "イントロとアーキテクチャ"
group: "SRE"
order: 1
---
SRE ツール — Kubernetes: 概要とアーキテクチャ

自動化する宣言型 API を使用して、コンテナーを大規模に実行します。

## 1. 役割

**Kubernetes** は、ノード上にポッドをスケジュールし、望ましい状態 (**Deployments**、**StatefulSets** など) を調整し、安定したネットワーク (**Services**、**Ingress** / Gateway API) を公開し、チームが依存するレイヤー運用プリミティブ (**リソース クォータ**、**NetworkPolicies**、**PodDisruptionBudgets**) を実現します。より安全なアップグレード。

## 2. コントロール プレーンとワークロード

|ピース |責任 |
|------|----------------|
| **kube-apiserver** | REST リクエストを検証します。クラスターの単一調整ファサード。 |
| **etcd** |望ましいクラスター状態を保存します (監視セマンティクス ドライブ コントローラー)。 |
| **kube スケジューラー** |スケジュールされていないポッドを適切なノードに割り当てます。 |
| **kube-controller-manager** | ReplicaSet、デプロイメント、ジョブ、エンドポイント…ループを調整します。 |
| **クラウド コントローラー マネージャー** |有効な場合、ベンダー LB/ ルート統合をブリッジします。 |
| **クベレット** |各ノードで実行 - コンテナー ランタイム経由でポッドを起動し、ステータスを報告します。 |

ワーカーノードはポッドを実行します。コントロール プレーンの障害モードは **クラスター全体**になる傾向があり、それに応じて apiserver/etcd HA トポロジを保護します。

## 3. 名前空間と分離ベースライン

- **`namespaces`** segment RBAC, quotas, DNS zones (**`<svc>.<ns>.svc.cluster.local`**), and operator-managed stacks (**kube-system**, **`monitoring`**, etc.).
- Strong isolation usually adds **NetworkPolicy**, quota enforcement, and admission policy—not namespaces alone.

## 4. 宣言型ワークフロー

You mostly **`kubectl apply -f`** YAML (or Helm/Kustomize manifests). Controllers converge reality toward spec; drift can still happen via broken controllers or manual **`kubectl edit`**—**GitOps** (see **GitOps & operations**) adds audit trail + rollback semantics.

このフォルダー内の **ワークロードと正常性**、**ネットワーキングとポリシー**、**Git運用と運用**、**Dockerアプリの化**に進みます。
