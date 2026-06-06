---
label: "III"
subtitle: "ネットワーキングとポリシー"
group: "SRE"
order: 3
---
SRE ツール — Kubernetes: ネットワーキングとポリシー

**NetworkPolicy** を強化するまで、クラスターはデフォルトで **allow-all** ポッド間のトラフィックを許可します。

## 1. サービスと DNS

- **ClusterIP** — クラスター内の仮想 IP。 **`kube-proxy`** (iptables/IPVS) または eBPF データパスは、トラフィックを正常なエンドポイント (準備完了状態を渡すポッド) にルーティングします。
- **NodePort** — すべてのノードでポートを公開します。ラボに便利です。通常、prod は LB/Ingress の前に置かれます。
- **LoadBalancer** — クラウド統合により外部 LB が割り当てられます (実装はプロバイダーによって異なります)。
- **ヘッドレス (`clusterIP: None`)** — ポッドあたりの DNS **`A`** レコード - StatefulSet と共通。

クラスター DNS (**CoreDNS**) は **`my-svc.my-ns.svc.cluster.local`** を解決します。

## 2. Ingress API とゲートウェイ API

- **Ingress** — コントローラー (nginx、contour など) を介した HTTP ルーティング。 **`IngressClass`** は実装を選択します。
- **ゲートウェイ API** - **`Gateway`** / **`HTTPRoute`** CRD を備えたより豊富なルーティング/TLS モデル - サポートされている場合はグリーンフィールドが推奨されます。

TLS 終端は Ingress/LB またはメッシュに存在する可能性があります。環境ごとに 1 つのストーリーを選択してください。

## 3. ネットワークポリシー

ポリシーがなければ、どのポッドも CNI デフォルトで許可されている任意のポッド/CIDR に到達できます。デフォルト拒否ベースラインの例 (例示 - ラベル/CIDR の適応):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

次に、アプリごとに **許可** ポリシーを追加します (`podSelector` + `namespaceSelector` + **`ports`**)。代表的な Pod から **`kubectl exec`** + **`nc`** / **`curl`** で検証します。

## 4. マルチテナンシーノブ

**名前空間**、**ResourceQuota** / **LimitRange**、**RBAC**、**NetworkPolicy**、およびオプションで **PodSecurity** / アドミッション (OPA/Kyverno) を組み合わせて、より安全な共有クラスターを実現します。

## 5. 可観測性とのペアリング

サービス メッシュ/CNI はメトリクスを生成します。Prometheus ターゲットは、**`kube-state-metrics`**、**cAdvisor/node-exporter**、およびアプリ **`ServiceMonitor`** オブジェクトを収集することがよくあります (ツールの **Prometheus → Kubernetes** を参照)。
