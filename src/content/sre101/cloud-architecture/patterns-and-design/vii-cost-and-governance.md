---
label: "VII"
subtitle: "コストとガバナンス"
group: "クラウドアーキテクチャ"
order: 7
---
コストとガバナンス

クラウドの料金は使用量に応じて増加します。 **FinOps** はエンジニアリングと財務を連携させます。 **ガバナンス** は速度がスプロールにならないようにガードレールを強化します。

## 1. 価格モデル

|モデル |コミットメント |割引 |こんな方に最適 |
|----------|-----------|----------|----------|
| **オンデマンド** |なし | 0% (ベースライン) |スパイク、予測不能、開発/テスト |
| **予約/節約プラン** | 1 ～ 3 年 | 30～70% |定常状態の本番ワークロード |
| **スポット / プリエンプティブル** |回収可能 |最大 ~90% |バッチ、ML トレーニング、ステートレス ワーカー |
| **確約使用 (GCP)** | 1 ～ 3 歳 | RIに似ている |安定したコンピューティング |

```text
On-Demand:  $$$$  full flexibility
Reserved:   $$    predictable baseline capacity
Spot:       $     interruptible — checkpoint & retry
```

## 2. スポット インスタンスを使用する場合

|良いフィット感 |フィット感が悪い |
|----------|----------|
| Kubernetes 再試行のあるバッチ ジョブ |単一ノードのステートフル DB |
|ビデオトランスコーディングキュー |チェックポイントのない長いシングルスレッド ジョブ |
| CI ビルド エージェント |冗長性のないモノリシック アプリ |
|フリンク / スパークワーカー |キルを許容できないレガシーアプリ |

**パターン:** スポット フリート + オンデマンド ベースライン。スポット中断時には、作業はキューに戻ります。

## 3. FinOps の実践

| Practice | Action |
|----------|--------|
| **Tagging** | `team`, `env`, `project`, `cost-center` on every resource |
| **Budgets & alerts** | Alert at 80% of monthly budget |
| **Right-sizing** | Compare CloudWatch CPU/RAM vs instance size |
| **Idle cleanup** | Detached EBS, old snapshots, unused ELBs, idle NAT Gateway |
| **Storage tiering** | S3 Standard → IA → Glacier for cold data |
| **Showback/chargeback** | Monthly report per team tag |

```text
Required tags (example policy):
  Environment: dev | staging | prod
  Owner: team-payments
  Application: checkout-api
```

タグなしリソース → デプロイ時に拒否 (ポリシー) または自動通知。

## 4. サービス別コストの最適化

|サービス |ヒント |
|----------|-----|
| **EC2 / VM** |ベースライン用に予約されています。バースト用スポット |
| **RDS** |適切なサイズ。夜間/週末に開発インスタンスを停止する |
| **S3** |ライフサイクルルール。不完全なマルチパート アップロードを削除する |
| **NAT ゲートウェイ** |高価 — S3/DynamoDB 用の VPC エンドポイント |
| **データ転送** |同じ地域。出力の多いコンテンツの場合は CDN |
| **ラムダ** |適切なサイズのメモリ (CPU とコストに影響) |

## 5. ガバナンス階層

```text
Organization (AWS Org / Azure MG)
  ├── SCP / Policy — deny root login, restrict regions
  ├── Account: production
  ├── Account: staging
  └── Account: sandbox
        └── IAM roles per workload (least privilege)
```

|メカニズム |目的 |
|----------|----------|
| **AWS 組織 / Azure 管理グループ** |マルチアカウント構造 |
| **SCP / Azure ポリシー** |管理者にもガードレール |
| **IAM / RBAC** |ロールごとの最小権限 |
| **CloudTrail / アクティビティ ログ** |不変の API 監査 |
| **構成 / ポリシーのコンプライアンス** |パブリック S3 バケットを検出する |

## 6. IAM 最小権限

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::myapp-uploads-prod/user-uploads/*"
}
```

| Avoid | Prefer |
|-------|--------|
| `"Action": "*"` | Scoped actions |
| `"Resource": "*"` | Resource ARN prefix |
| Long-lived access keys | IAM roles, OIDC for CI |
| Shared root credentials | SSO + assumed roles |

## 7. ポリシーの例

**暗号化されていない S3 アップロードを拒否します:**

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "AES256"
    }
  }
}
```

**地域の制限 (SCP):**

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["us-east-1", "eu-west-1"]
    }
  }
}
```

## 8. 適切に設計されたコストの柱 (概要)

|質問を確認する |アクション |
|-----------------|----------|
|コスト要因のトップ 5 を知っていますか? | Cost Explorer / 請求書のエクスポート |
|開発リソースは営業時間外にシャットダウンされますか? | Lambda スケジューラ、インスタンス スケジューラ |
|未使用の容量に対して料金を支払うのでしょうか? | Trusted Advisor、コンピューティングオプティマイザー |
|アーキテクチャはマネージド サービスを使用していますか? |操作が少なくなり、多くの場合、$/value が向上します |

## 9. アンチパターン

|アンチパターン |コストへの影響 |
|--------------|---------------|
|常にオンデマンドの大規模な製品 | 30 ～ 50% の超過支出と予約済み |
|タグなし |割り当てまたは最適化ができません |
|特大の「万が一に備えて」インスタンス | 10% CPU で 2 倍の支出 |
| NAT プライベート サブネットごとのゲートウェイ |高固定時間 + データ処理 |

## 10. リハーサルの答え

- **Spot** — cheap spare capacity; can be reclaimed; needs fault-tolerant workload.
- **SLI/SLO** — see [Observability, SLI & SLO](vi-observability-slo-and-slis.md); SLA adds customer contract.
- **SCP** — organization-level deny that applies even to account admins.
- **Stateless + auto scaling** — see [Scalability & caching](ii-scalability-and-caching.md).

**Related:** **Foundations** submenu → [Well-Architected Framework](../foundations/viii-well-architected-framework.md), CI/CD Terraform for IaC guardrails.
