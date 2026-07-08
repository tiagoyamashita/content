---
label: "II"
subtitle: "ゲートウェイの仕組み"
group: "API Gateway"
order: 2
---
API ゲートウェイ — ゲートウェイの仕組み

**南北**のトラフィックは、**クライアント** (インターネット、モバイル、パートナー) からゲートウェイを介して**システムに流れます。ゲートウェイはクライアント接続を終了し、ポリシーを適用して、上流サービスへの**新しい**接続を開きます。

## 1. リクエストの流れ

```text
1. Client TLS handshake with gateway (api.example.com)
2. Gateway matches route (path, method, host)
3. Plugins/policies run (auth, rate limit, WAF)
4. Gateway forwards to upstream (HTTP/gRPC/Lambda)
5. Upstream responds
6. Gateway may transform response → client
```

|ステップ |故障モード |
|------|--------------|
| **ルートミス** |ゲートウェイからの 404 — アップストリーム ヒットなし |
| **認証失敗** | 401/403 — アップストリームが呼び出されません |
| **レート制限** | 429 — 上流を保護する |
| **アップストリームのタイムアウト** | 504 — ゲートウェイとサービスのタイムアウトを調整する |

## 2. 南北と東西

|方向 |パス |ツーリング |
|----------|------|----------|
| **南北** |クライアント → ゲートウェイ → サービス | **API ゲートウェイ**、CDN |
| **東西** |サービス ↔ サービス | K8s DNS、**サービス メッシュ** (Istio、Linkerd) |

ゲートウェイは **外部** 信頼境界を処理します。内部サービス呼び出しでは、多くの場合、パブリック ゲートウェイをスキップします。メッシュまたはダイレクト クラスター DNS と mTLS を使用します。

See [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## 3. ゲートウェイとロードバランサー

| | **ロード バランサ (ALB/NLB)** | **API ゲートウェイ** |
|---|----------------------------|---------------|
| **レイヤー** | L4/L7 ディストリビューション | L7 API セマンティクス |
| **ルーティング** |ホスト/パス → ターゲットグループ |バージョン管理されたルート、プラグイン |
| **認証** |最小限 | JWT、API キー、OAuth |
| **レート制限** |オプションの低速 |ファーストクラス |
| **典型的なスタック** |ゲートウェイ **→** ALB **→** ポッド |両層共通 |

ALB は負荷を分散します。ゲートウェイは **API 製品** 機能を追加します。

## 4. CDN を前に置く

```text
GET /assets/app.js     → CDN → S3 (gateway not involved)
POST /api/v1/orders    → CDN bypass → Gateway → orders-service
```

CDN may share hostname — **path-based behaviors** send API traffic to gateway origin. Details: [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

## 5. 同期統合と非同期統合

|上流タイプ |パターン |
|--------------|----------|
| **HTTP サービス** |プロキシパススルー |
| **AWS ラムダ** | API Gateway イベントの呼び出し |
| **キュー** |ゲートウェイ HTTP → サービス エンキュー (ゲートウェイはクライアントとの同期を維持します) |
| **WebSocket** |ゲートウェイのアップグレード + ルート (プロバイダー固有) |

非同期パターン (202 + ポーリング/Webhook) を公開しない限り、クライアントは通常、**1** の同期応答を待ちます。

## 6. ヘッダーとコンテキスト

ゲートウェイはアップストリームにコンテキストを挿入します。

```http
X-Request-Id: 7f3a9c2e-...
X-Forwarded-For: 203.0.113.10
X-Authenticated-User: user_42
Authorization: (stripped or forwarded per policy)
```

内部ネットワーク (mTLS またはプライベート サブネット) がクライアントのスプーフィングを防止する場合にのみ、サービスは **ゲートウェイ検証済み** ID ヘッダーを信頼します。

## 7. コールド パスとホット パス

| |ゲートウェイ |上流サービス |
|---|--------|----|
| **ステートレスを維持** |はい — 水平スケール | DB のビジネス状態 |
| **構成の変更** |ルート、プラグイン — 慎重にデプロイ |アプリのリリース |
| **レイテンシ バジェット** | 1 桁のミリ秒オーバーヘッド目標 |ほとんどの作業はここで行われます |

＃＃ 次

Continue with [Routing & versions](iii-routing-and-versions.md) for paths, staging, and canaries.
