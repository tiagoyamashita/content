---
label: "II"
subtitle: "仕事量と健康"
group: "SRE"
order: 2
---
SRE ツール — Kubernetes: ワークロードと健全性

ポッド、コントローラー、プローブ、容量、および中断の予算。

## 1. ポッドとコントローラーのパターン

|種類 |いつ |
|------|------|
| **展開** |ステートレス HTTP ワーカー - その下の ReplicaSet がロールアウトを管理します。 |
| **ステートフルセット** |安定した ID + 順序付けられたロールアウト (クラスター内で操作するデータベース)。 |
| **デーモンセット** |ノードごとに 1 つのポッド - エージェント、ログ フォワーダー、ノード エクスポーター。 |
| **ジョブ/Cronジョブ** |再試行セマンティクスを備えたバッチ/スケジュールされたタスク。 |

## 2. プローブ

- **livenessProbe** — kubelet は、異常な場合にコンテナーを再起動します (フラップを伴う高価なチェックを回避します)。
- **readinessProbe** — 準備が完了するまで (起動時のトラフィック シェーピング)、**Service** エンドポイントからポッドを削除します。
- **startupProbe** — 起動が遅いアプリを保護し、活性化によってアプリが途中で強制終了されないようにします。

Probe **`failureThreshold`** × **`periodSeconds`** drives blast radius—tune with observed startup curves.

## 3. リソースとスケジュール設定

- **`requests`** influence scheduling (kube-scheduler fits Pods onto Nodes with allocatable capacity).
- **`limits`** cap burst usage (CPU throttling vs hard memory **OOMKill** behavior differs—memory limits are not “soft”).
- **QoS classes** (`Guaranteed`, `Burstable`, `BestEffort`) affect eviction ordering under pressure—document assumptions for stateful tiers.

## 4. 水平スケーリングと PDB

- **HorizontalPodAutoscaler** scales Replica counts off metrics (often Prometheus Adapter `custom.metrics.k8s.io`).
- **PodDisruptionBudget** caps simultaneous voluntary disruptions (`maxUnavailable` / `minAvailable`) during node drains or deployments—pair PDBs with sensible **`Deployment.strategy`** (`RollingUpdate` **`maxSurge`/`maxUnavailable`**).

## 5. kubectl のクイック キュー

```text
kubectl rollout status deployment/checkout-api -n prod
kubectl rollout restart deployment/checkout-api -n prod
kubectl describe pod -n prod <pod-name>
kubectl logs -n prod deploy/checkout-api --tail=200 -f
```

次: **ネットワーキングとポリシー**、次に **Git運用と運用**。プローブを調整する前の **Dockerファイル**、画像、信号については、**Dockerアプリの化**を参照してください。
