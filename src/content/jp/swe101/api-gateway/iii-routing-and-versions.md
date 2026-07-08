---
label: "III"
subtitle: "ルーティングとバージョン"
group: "API Gateway"
order: 3
---
API ゲートウェイ — ルーティングとバージョン

**パス**、**メソッド**、**ホスト**、**ヘッダー**によるルート - すべてのマイクロサービスのホスト名を公開せずに、パブリック URL を内部サービスおよび API **バージョン**にマップします。

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

| Option | Effect |
|--------|--------|
| **`strip_path: true`** | `/api/v1/orders/123` → upstream `/123` |
| **`strip_path: false`** | Upstream sees full path — service mounts `/api/v1/orders` |
| **Method match** | `GET` vs `POST` on same path → different routes |

## 2. API バージョン管理戦略

| Strategy | Example | Pros / cons |
|----------|---------|-------------|
| **URL path** | `/api/v1/`, `/api/v2/` | Obvious; easy at gateway |
| **Header** | `Accept: application/vnd.app.v2+json` | Clean URLs; harder to test in browser |
| **Query** | `/api/orders?version=2` | Rare for public APIs |

Gateway often routes **`/api/v1/*`** and **`/api/v2/*`** to different upstreams during migration.

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

- ゲートウェイ **重み付けされたアップストリーム** (Kong、Envoy、AWS 重み付けされたターゲット)
- **サービス メッシュ** トラフィック分割 (内部)
- アプリ内の **機能フラグ** (ゲートウェイではありません - 別の懸念事項)

Canary のエラー率を監視します — CI による自動ロールバック。

## 5. リライトとリダイレクト

| Action | Use |
|--------|-----|
| **Path rewrite** | Public `/v1/orders` → internal `/orders` |
| **301/302 redirect** | Deprecate old hostname |
| **Header injection** | `X-Api-Version: 1` for upstream logging |

デバッグが困難な複雑な書き換えチェーンを避けてください。

## 6. OpenAPI / スキーマ (オプション)

一部のゲートウェイは、**OpenAPI** 仕様をインポートしてルートを定義し、リクエストを検証します (**Cloudflare API Shield**、**Azure APIM**、**Kong request validator**)。

利点: 不正なリクエストをエッジで拒否します。文書による契約書。

## 7. gRPC と WebSocket

|プロトコル |ゲートウェイのサポート |
|----------|------|
| **HTTP/JSON** |ユニバーサル |
| **gRPC** | Envoy、Kong gRPC、AWS HTTP API (限定) — 多くの場合、gRPC ゲートウェイ変換 |
| **WebSocket** |プロバイダー固有のルート。スティッキーセッションが重要になる可能性があります |

プロトコルに一致するゲートウェイ製品を選択してください。すべてが gRPC をネイティブにサポートしているわけではありません。

＃＃ 次

Continue with [Authentication](iv-authentication.md) for JWT, API keys, and OAuth at the gateway.
