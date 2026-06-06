---
label: "V"
subtitle: "APIゲートウェイとサービスメッシュ"
group: "クラウドアーキテクチャ"
order: 5
---
APIゲートウェイとサービスメッシュ

**南北**トラフィック (クライアント → クラスタ) と **東西** トラフィック (サービス ↔ サービス) には、異なるコントロール プレーンが必要です。 **サーキット ブレーカー** は、障害の連鎖を阻止します。

## 1. 交通案内

<figure class="notes-diagram"><svg xmlns="4 viewBox="0 0 400 110" role="img" aria-label="North south API gateway east west service mesh">
  <text x="12" y="18" fill="#d4d4d8" font-size="11" font-weight="600">North-south vs east-west</text>
  <rect x="160" y="28" width="80" height="24" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="172" y="44" fill="#e4e4e7" font-size="9">API Gateway</text>
  <rect x="12" y="72" width="56" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="88" fill="#e4e4e7" font-size="8">Client</text>
  <path d="M68 84 H160 44" stroke="#60a5fa" stroke-width="1.5" fill="none"/>
  <rect x="100" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="108" y="88" fill="#e4e4e7" font-size="8">Svc A</text>
  <rect x="200" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="88" fill="#e4e4e7" font-size="8">Svc B</text>
  <rect x="300" y="72" width="56" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="308" y="88" fill="#e4e4e7" font-size="8">Svc C</text>
  <path d="M156 84 H200 84" stroke="#fbbf24" stroke-width="1.5"/>
  <path d="M256 84 H300 84" stroke="#fbbf24" stroke-width="1.5"/>
  <text x="220" y="68" fill="#71717a" font-size="8">east-west (mesh)</text>
</svg></figure>

## 2. API ゲートウェイ (南北)

クライアント用の単一のパブリック エントリ ポイント。

|能力 |例 |
|-----------|-----------|
| **ルーティング** | `/api/orders` → 注文サービス |
| **TLS 終端** |エッジでの HTTPS |
| **認証** | JWT 検証、API キー |
| **レート制限** |クライアントあたり 1000 リクエスト/分 |
| **変換のリクエスト** |ヘッダー挿入、パス書き換え |
| **WAF の統合** |ブロック SQLi パターン |

|製品 |クラウド |
|----------|----------|
| **AWS API ゲートウェイ** | REST / HTTP API |
| **Azure API 管理** |アズール |
| **Google Apigee / ゲートウェイ** | GCP |
| **コング、NGINX** |セルフホスト / K8s Ingress |

```yaml
# Conceptual route (Kong-style)
routes:
  - name: orders
    paths: ["/api/v1/orders"]
    service: orders-upstream
    plugins:
      - name: rate-limiting
        config: { minute: 500 }
      - name: jwt
```

## 3. サービス メッシュ (東西)

各ポッドの隣にある **サイドカー プロキシ** (Envoy) は、サービス間のトラフィックを処理します。

```text
Pod: [ app container ] [ Envoy sidecar ]
         │                    │
         └──── localhost ─────┘
                    │
              mTLS to peer Envoy
```

|特集 |メッシュなし |メッシュあり (Istio、Linkerd) |
|----------|--------------|----------------------------|
|再試行/タイムアウト |ライブラリごと | YAML のポリシー |
| mTLS |アプリコードまたは手動証明書 |自動 |
|トラフィック分割 |カスタム LB ルール |構成内の 90/10 カナリア |
|メトリクス |アプリごとのインストルメンテーション |均一なサイドカー メトリクス |

|製品 |メモ |
|----------|----------|
| **Istio** |機能が豊富で複雑 |
| **リンカード** |軽量 |
| **AWS アプリメッシュ** | AWS ネイティブの Envoy |

**いつ採用するか:** 多くのマイクロサービスでは、統一された mTLS とトラフィック ポリシーが必要です。3 サービス システムには必要ありません。

## 4. サーキットブレーカー

障害を下流の依存関係まで追跡します。異常な場合は **すぐに失敗します**。

|状態 |行動 |
|------|----------|
| **閉店** |通常の通話 |
| **開く** |すぐに失敗します - タイムアウトを待たないでください |
| **ハーフオープン** |制限された呼び出しでプローブする - 回復または再オープン |

```text
Svc A ──▶ [ breaker CLOSED ] ──▶ Svc B (healthy)

Svc B down → failures exceed threshold
Svc A ──▶ [ breaker OPEN ] ──✕ fast fail (fallback or cached response)

After cooldown → HALF-OPEN → test call → CLOSED if OK
```

**Resilience4j** (Java)、**Envoy 外れ値検出**、**Istio 宛先ルール**。

|ブレーカーなし |ブレーカー付き |
|-----------------|--------------|
|タイムアウトでブロックされたスレッド |ミリ秒以内に失敗します |
|再試行の嵐により停止が拡大 |シェッドロード |
|カスケード: A は B を待機し、C は待機します。 A は正常に劣化します。

## 5. ゲートウェイとメッシュの結合

|レイヤー |ハンドル |
|------|-----------|
| **ゲートウェイ** |外部認証、パブリック API バージョニング、WAF |
| **メッシュ** |内部 mTLS、サービス間での再試行 |
| **両方** |ゲートウェイでの相関 ID の挿入、メッシュによって伝播 |

## 6. Ingress と API ゲートウェイ (Kubernetes)

| | Ingress (NGINX、ALB) | APIゲートウェイ |
|---|---------------------|---------------|
|範囲 |クラスターへの L7 ルーティング |完全な API 管理 |
|認証 |基本、アノテーションによる OAuth |組み込みポリシー |
|使用 |内部 + 単純なパブリック |パブリック API 製品 |

多くの場合: Web の **CloudFront → ALB Ingress → サービス**。パートナー API 用の **API ゲートウェイ**。

## 7. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
|初日のメッシュ |痛みが現れるまで K8s DNS を直接指定する |
|ゲートウェイはビジネス ロジックを実行します。シン ゲートウェイ — サービス内のロジック |
| HTTP クライアントでタイムアウトなし |接続 + 読み取りタイムアウト + ブレーカーを設定 |
|ジッターなしで 20 回再試行 |制限された再試行 + 指数バックオフ |

**関連:** ネットワーキングイングレスノート、[可観測性、SLI および SLO](vi-observability-slo-and-slis.md)、[イベント駆動型アーキテクチャ](iv-event-driven-architecture.md)。
