---
label: "III"
subtitle: "ルーティングとバージョン"
group: "APIゲートウェイ"
order: 3
---
APIゲートウェイ — ルーティングとバージョン

**パス**、**メソッド**、**ホスト**、**ヘッダー**によるルート - すべてのマイクロサービスのホスト名を公開せずに、パブリック URL を内部サービスおよび API **バージョン**にマッピングします。

## 1. パスベースのルーティング

```text
GET  /api/v1/orders/*     → orders-service:8080
GET  /api/v1/users/*      → users-service:8080
POST /api/v1/webhooks/*   → webhook-handler
```

Kong スタイルの概念的な構成:

```yaml
routes:
  - name: orders-v1
    paths: ["/api/v1/orders"]
    strip_path: false
    service: orders-upstream
  - name: users-v1
    paths: ["/api/v1/users"]
    service: users-upstream
```

|オプション |効果 |
|----------|----------|
| **`strip_path: true`** | `/api/v1/orders/123` → 上流 `/123` |
| **`strip_path: false`** |アップストリームはフルパスを参照 — サービスは `/api/v1/orders` をマウントします。
| **メソッド一致** |同じパス上の `GET` と `POST` → 異なるルート |

## 2. API のバージョン管理戦略

|戦略 |例 |長所/短所 |
|----------|-----------|---------------|
| **URL パス** | `/api/v1/`、`/api/v2/` |明らか;ゲートウェイで簡単 |
| **ヘッダー** | `Accept: application/vnd.app.v2+json` |クリーンな URL;ブラウザでテストするのは難しい |
| **クエリ** | `/api/orders?version=2` |パブリック API としては珍しい |

ゲートウェイは、移行中に **`/api/v1/*`** と **`/api/v2/*`** を異なるアップストリームにルーティングすることがよくあります。

## 3. ホストベースのルーティング

```text
api.example.com      → public REST gateway
partner.example.com  → partner routes + stricter limits
internal.example.com → VPN-only (network policy + gateway)
```

同じゲートウェイ クラスタ、ホスト名ごとに異なる **ルート テーブル**。

## 4. カナリアとトラフィックの分割

トラフィックのわずかな割合を新しいバージョンに送信します。

```text
95% /api/v1/orders → orders-v1
 5% /api/v1/orders → orders-v2-canary
```

以下を介して実装されます:

- ゲートウェイ **加重アップストリーム** (Kong、Envoy、AWS 加重ターゲット)
- **サービス メッシュ** トラフィック分割 (内部)
- アプリ内の **機能フラグ** (ゲートウェイではありません - 別の懸念事項)

Canary でエラー率を監視します — CI を介した自動ロールバック。

## 5. リライトとリダイレクト

|アクション |使用 |
|--------|-----|
| **パスの書き換え** |パブリック `/v1/orders` → 内部 `/orders` |
| **301/302 リダイレクト** |古いホスト名を廃止する |
| **ヘッダー インジェクション** |上流ログの場合は `X-Api-Version: 1` |

デバッグが困難な複雑な書き換えチェーンを避けてください。

## 6. OpenAPI / スキーマ (オプション)

一部のゲートウェイは、**OpenAPI** 仕様をインポートしてルートを定義し、リクエストを検証します (**Cloudflare API Shield**、**Azure APIM**、**Kong リクエスト バリデータ**)。

利点: 不正なリクエストをエッジで拒否します。文書による契約書。

## 7. gRPC と WebSocket

|プロトコル |ゲートウェイのサポート |
|----------|------|
| **HTTP/JSON** |ユニバーサル |
| **gRPC** | Envoy、Kong gRPC、AWS HTTP API (限定) — 多くの場合、gRPC ゲートウェイ変換 |
| **WebSocket** |プロバイダー固有のルート。スティッキーセッションが重要になる可能性があります |

プロトコルに一致するゲートウェイ製品を選択してください。すべてが gRPC をネイティブにサポートしているわけではありません。

＃＃ 次

ゲートウェイでの JWT、API キー、OAuth の [認証](iv-authentication.md) に進みます。
