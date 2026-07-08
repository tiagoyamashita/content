---
label: "IV"
subtitle: "コンピューティングオプション"
group: "クラウドアーキテクチャ"
order: 4
---
コンピューティングオプション

クラウド **コンピューティング**は、完全な **VM** から **機能**まで多岐にわたります。制御、移植性、トラフィック パターン、運用能力に基づいて選択してください。

## 1. 抽象化のスペクトル

```text
More control                                                          Less ops
    │                                                                      │
    VM ──▶ Container (K8s) ──▶ PaaS (managed runtime) ──▶ FaaS (Lambda)
```

|オプション |請求 |こんな方に最適 |
|----------|----------|----------|
| **VM (IaaS)** |実行中の 1 秒/時間あたり |リフトアンドシフト、ステートフル、カスタム OS |
| **コンテナ** |クラスター + ノード |マイクロサービス、ポータブル ワークロード |
| **サーバーレス** |呼び出しごと + 期間 |イベント駆動型の散発的なトラフィック |

## 2. 仮想マシン

完全な OS インスタンス — 永続的、常時オン (停止しない限り)。

|クラウド |サービス |
|------|-----------|
| AWS | EC2 |
|アズール |仮想マシン |
| GCP |コンピューティング エンジン |

```text
EC2 instance
  ├── instance type: t3.micro, m6i.xlarge (CPU/RAM profile)
  ├── AMI: Amazon Linux, Ubuntu, Windows
  ├── EBS volume: root + data disks
  └── security group + subnet
```

|強さ |弱点 |
|----------|----------|
|フルコントロール | OS にパッチを適用し、インスタンスのサイズを |
|あらゆるソフトウェアスタック |コンテナ/サーバーレスよりもスケールアウトが遅い |
|安定した負荷を予測可能 |アイドル状態のときに支払う |

**次の場合に使用します:** レガシー アプリ、ライセンスされたソフトウェア、GPU ワークロード、強力な分離が必要な場合。

## 3. コンテナーと Kubernetes

**Docker** アプリ + 依存関係をパッケージ化します。 **Kubernetes** はノード全体でコンテナーをスケジュールします。

|マネージド K8 |プロバイダーはコントロール プレーンを実行します |
|-----------|----------------------------|
| **EKS** | AWS |
| **AKS** |アズール |
| **GKE** | GCP |

```yaml
# Simplified Deployment — 3 replicas across AZs
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: registry.example.com/api:1.2.3
          resources:
            requests: { cpu: "250m", memory: "512Mi" }
            limits:   { cpu: "500m", memory: "1Gi" }
```

|強さ |弱点 |
|----------|----------|
|ポータブル画像 | K8s の学習曲線 |
|ノード上の高密度パッキング |マニフェスト/Helm を管理する |
|高速スケール ポッド |クラスター操作 (マネージドも含む) |

**次の場合に使用します:** マイクロサービス、環境間でのポータブルなデプロイが必要、チームが K8s スキルを持っている。

**より軽量な代替案:** ECS Fargate、Cloud Run、Azure Container Apps — YAML を減らし、より独自性を高めます。

## 4. サーバーレス/FaaS

**関数**をアップロードします。プロバイダーはランタイム、スケーリング、パッチ適用を処理します。

|クラウド |サービス |
|------|-----------|
| AWS |ラムダ |
|アズール |機能 |
| GCP | Cloud Functions / Cloud Run (コンテナベース) |

```python
# AWS Lambda handler (conceptual)
def handler(event, context):
    order_id = event["orderId"]
    process_order(order_id)
    return {"statusCode": 200}
```

**料金:** 呼び出しごと + GB- 秒のメモリ x 期間。

## 5. コールドスタート

アイドル後の最初の呼び出しでは追加の待ち時間が発生します。プロバイダーは次のことを行う必要があります。

1.サンドボックスの割り当て
2. デプロイメントパッケージのダウンロード / コンテナーの起動
3. ランタイムを初期化します (JVM が特に遅い)

|ランタイム |典型的なコールドスタート |
|----------|--------|
| Node.js / Python | ~100 ～ 300 ミリ秒 |
| Java / .NET | ~500 ミリ秒 – 2 秒 |
| VPC-添付ラムダ | + ENI セットアップ (歴史的に遅い) |

|緩和 |どのように |
|-----------|-----|
| **プロビジョニングされた同時実行性** | N 個のインスタンスをウォームに保つ |
| **小型パッケージ** |依存関係をトリミングする |
| **SnapStart** (Lambda 上の Java) |スナップショットの開始フェーズ |
| **必要な場合を除き、VPC** は避けてください。または、新しい超平面 ENI を使用してください。

**次の場合にサーバーレスを使用します。** イベント トリガー (S3 アップロード、キュー メッセージ、API 散発的なトラフィック)、グルー/ETL、Webhook。

**次の場合は避けてください:** 常に 10 ミリ秒未満の厳密なレイテンシ、長時間実行されるコンピューティング、メモリの重い状態。

## 6. 比較表

| | VM | K8sポッド |ラムダ |
|---|-----|--------|--------|
|スケール速度 |分 (ASG) |秒 |ミリ秒 |
|最大持続時間 |無制限 |無制限 | 15 分 (ラムダ) |
|状態 |ローカルディスク |一時的な |一時的な |
|トラフィックゼロ時のコスト |まだ支払い中 |ノードのベースライン | ~$0 |

## 7. 意思決定の流れ

```text
Need custom OS/kernel?     → VM
Team on K8s, many services? → EKS/GKE/AKS
HTTP API with variable traffic? → Lambda or Cloud Run
Batch nightly job?          → Spot VM or Lambda
```

## 8. アーキテクチャの組み合わせの例

|コンポーネント |コンピューティングの選択 |
|----------|----------------|
|パブリック REST API |ラムダ + API Gateway OR K8s + ALB |
|バックグラウンドワーカー | SQS の K8s デプロイメントまたは Lambda |
| PostgreSQL | RDS (マネージド VM) — Lambda ではありません |
| Redis キャッシュ | ElastiCache (マネージド) |

**関連:** [サービス モデル](ii-service-models.md)、パターン [スケーラビリティとキャッシュ](../patterns-and-design/ii-scalability-and-caching.md)。
