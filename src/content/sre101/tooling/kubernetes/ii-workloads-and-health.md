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

プローブ **`failureThreshold`** × **`periodSeconds`** は爆発半径を制御します。観測された起動曲線に合わせて調整します。

## 3. リソースとスケジュール設定

- **`requests`** はスケジューリングに影響します (kube-scheduler は、割り当て可能な容量を持つノードにポッドを適合させます)。
- **`limits`** キャップ バースト使用量 (CPU スロットリングとハード メモリ **OOMKill** の動作は異なります。メモリ制限は「ソフト」ではありません)。
- **QoS クラス** (`Guaranteed`、`Burstable`、`BestEffort`) は、プレッシャーにさらされた場合のエビクション順序に影響します。ステートフル層の仮定を文書化します。

## 4. 水平スケーリングと PDB

- **horizo​​ntalPodAutoscaler** は、レプリカのカウントをメトリクスからスケーリングします (多くの場合、Prometheus アダプター `custom.metrics.k8s.io`)。
- **PodDisruptionBudget** は、ノードのドレインまたはデプロイメント中の同時自発的中断 (`maxUnavailable` / `minAvailable`) を制限します。PDB を賢明な **`Deployment.strategy`** (`RollingUpdate` **`maxSurge`/`maxUnavailable`**) とペアにします。

## 5. kubectl のクイック キュー

```text
kubectl rollout status deployment/checkout-api -n prod
kubectl rollout restart deployment/checkout-api -n prod
kubectl describe pod -n prod <pod-name>
kubectl logs -n prod deploy/checkout-api --tail=200 -f
```

次: **ネットワーキングとポリシー**、次に **GitOps と運用**。プローブを調整する前の **Dockerfile**、イメージ、および信号については、**Dockerizing アプリ**をご覧ください。
