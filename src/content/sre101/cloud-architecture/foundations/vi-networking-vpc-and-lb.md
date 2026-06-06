---
label: "VI"
subtitle: "ネットワーキング、VPC、LB"
group: "クラウドアーキテクチャ"
order: 6
---
ネットワーキング、VPC、負荷分散

**VPC** は、クラウド内のプライベート ネットワークです。 **サブネット**、**ロード バランサー**、**ファイアウォール**は、トラフィックがどこに流れるか、誰が何に到達できるかを制御します。

## 1. VPC の基本

**仮想プライベート クラウド** — ユーザーが定義する論理的に分離されたネットワーク。

|クラウド |名前 |
|------|------|
| AWS | VPC |
|アズール |仮想ネットワーク (VNet) |
| GCP | VPC ネットワーク |

```text
VPC CIDR: 10.0.0.0/16
  ├── public subnet  10.0.1.0/24  (AZ-a)  → route to Internet Gateway
  ├── public subnet  10.0.2.0/24  (AZ-b)
  ├── private subnet 10.0.11.0/24 (AZ-a)  → NAT Gateway for outbound
  └── private subnet 10.0.12.0/24 (AZ-b)  → app + DB tiers
```

## 2. パブリックサブネットとプライベートサブネット

| |パブリックサブネット |プライベートサブネット |
|---|--------------|--------------|
| **インターネットへのルート** |インターネットゲートウェイ (IGW) 経由 |インターネットからの直接受信はありません |
| **典型的なリソース** | ALB、要塞 (使用されている場合) |アプリサーバー、データベース |
| **ウェブからのインバウンド** |パブリック層の LB 経由 | LB はプライベート ターゲットに転送します。

```text
Internet ──▶ IGW ──▶ ALB (public subnet)
                         │
                         └──▶ EC2 targets (private subnet)

Private EC2 outbound: private subnet ──▶ NAT GW (public subnet) ──▶ IGW
```

**NAT ゲートウェイ** のコストに関するメモ: 時間 + データ処理 — AWS API トラフィックの NAT を回避するには、S3/DynamoDB に **VPC エンドポイント** を使用します。

## 3. ロードバランサ

**複数の AZ** 内のターゲット間でトラフィックを分散します。

|レイヤー |名前 | | のルートAWSの例 |
|----------|------|---------------|---------------|
| **L4** |輸送 | IP + ポート (TCP/UDP) | NLB |
| **L7** |アプリケーション | HTTP パス、ホストヘッダー | ALB |

```text
Client HTTPS ──▶ ALB (SSL termination)
                    ├── /api/*  → target group A (API pods)
                    └── /*      → target group B (static S3 via IP targets)
```

|特集 | ALB(L7) | NLB (L4) |
|----------|----------|----------|
|パスルーティング |はい |いいえ |
| WebSocket / HTTP/2 |はい | TCP パススルー |
|静的 IP | NLB経由 |はい |
|レイテンシ |やや高め |超低価格 |

**ヘルスチェック** — LB は異常なターゲットを削除します。 Auto Scaling とペアリングします。

## 4.DNS

|クラウド |サービス |特長 |
|----------|-----------|----------|
| AWS |ルート53 |ヘルスチェック、フェイルオーバー、地理的ルーティング |
|アズール | Azure DNS | |
| GCP |クラウドDNS | |

```text
api.example.com  CNAME  →  myapp-alb-123.us-east-1.elb.amazonaws.com
                           (alias record in Route 53)
```

|ルーティングポリシー |使用 |
|-----|-----|
| **シンプル** |単一のリソース |
| **加重** |カナリアのトラフィック % |
| **フェイルオーバー** |プライマリ + セカンダリのヘルスチェック済み |
| **地理位置情報** | EU ユーザー → EU エンドポイント |

グローバル API ゾーニングについては、ネットワーク DNS ノートを参照してください。

## 5. CDN (エッジ)

**CloudFront**、**Azure CDN**、**Cloudflare** — エッジ PoP [リージョン、AZ、エッジ](iii-regions-azs-and-edge.md) でキャッシュします。

```text
User ──▶ CloudFront edge (cache HIT) → fast
User ──▶ CloudFront edge (MISS) ──▶ origin (ALB or S3)
```

## 6. セキュリティ グループと NACL の比較

| |セキュリティグループ | NACL |
|---|--|------|
| **範囲** |インスタンス / ENI |サブネット |
| **州** |ステートフル (戻りトラフィックは自動許可) |無国籍 |
| **ルール** | | のみを許可します許可 + 拒否、順序付き |
| **デフォルト** |すべての受信を拒否 |すべて許可 (カスタマイズ) |

```text
Security group "web-tier"
  Inbound: 443 from 0.0.0.0/0
  Inbound: 8080 from sg:alb-only
  Outbound: all (or restrict to DB sg)
```

**ベスト プラクティス:** 最小権限の SG。サブネットレベルの拒否リストの NACL (ブロック IP 範囲など)。

## 7. VPC エンドポイント (PrivateLink)

パブリック インターネットや NAT を経由せずに** AWS サービスにアクセスします。

|タイプ |例 |
|-----|----------|
| **ゲートウェイ** | S3、DynamoDB |
| **インターフェース** | Secrets Manager、SQS、その他の API |

NAT コストを削減し、トラフィックを AWS バックボーンに維持します。

## 8. 3 層 VPC の例

```text
┌─────────────────────────────────────────────────┐
│ VPC 10.0.0.0/16                                  │
│  Public:  ALB, NAT GW                            │
│  Private: App tier (ASG across 2 AZs)            │
│  Private: RDS Multi-AZ (no public IP)            │
└─────────────────────────────────────────────────┘
```

## 9. Kubernetes ネットワーキング (概要)

- **クラスター** は VPC サブネット (多くの場合プライベート) に存在します。
- **Ingress** またはクラウド LB は HTTP サービスを公開します。
- **ネットワーク ポリシー**はポッド間のトラフィックを制限します。

**関連:** ネットワーキング TCP/HTTP/DNS/Ingress のメモ、パターン [API ゲートウェイとサービス メッシュ](../patterns-and-design/v-api-gateway-and-service-mesh.md)。
