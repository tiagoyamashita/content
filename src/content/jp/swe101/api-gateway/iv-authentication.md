---
label: "IV"
subtitle: "認証"
group: "API Gateway"
order: 4
---
API ゲートウェイ — 認証

トラフィックがサービスに到達する前に、**誰** が電話をかけているかを検証します (**JWT**、**API キー**、**OAuth**、または **mTLS**)。ゲートウェイは不正な認証情報を早期に拒否し (401/403)、信頼されたコンテキストを上流に転送します。

## 1. 認証が実行される場所

```text
Client ──Authorization: Bearer …──► Gateway validates
                                         │
                                         ├── invalid → 401
                                         └── valid → upstream (+ optional identity headers)
```

|レイヤー |責任 |
|------|----------------|
| **ゲートウェイ** |トークンの形式、署名、有効期限、API キーの検索 |
| **サービス** |認可 (このユーザーはこのアクションを実行できますか?) |

ゲートウェイ **認証**;サービス **承認** (RBAC、所有権チェック)。

## 2. JWT (ベアラートークン)

SPA とモバイルに共通:

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

ゲートウェイのチェック:

- Signature (JWKS from IdP)
- `exp`, `iss`, `aud`
- Optional claims (`scope`, `roles`)

```yaml
# Conceptual plugin config
plugins:
  - name: jwt
    config:
      claims_to_verify: [exp]
      key_claim_name: kid
```

アップストリームはヘッダーでデコードされたクレームを受信するか (構成されている場合)、JWT を再検証します — **二重作業を回避します**。信頼境界を 1 つ選択します。

## 3. API キー

パートナーと脚本:

```http
X-Api-Key: sk_live_abc123
# or
?api_key=...   (avoid in URLs — logs leak)
```

ゲートウェイは、キー → **コンシューマ** → レート制限層をマップします。ダッシュボードでキーを回転します。 git には決してコミットしないでください。

## 4. OAuth 2.0 / OpenID Connect

ブラウザのログイン フローは **認証サービス** で終了します。 API 呼び出しでは **アクセス トークン**を使用します。

```text
User → Login (OAuth) → Auth server → access token
Client → API Gateway (Bearer access token) → services
```

ゲートウェイは、認証サーバーからのアクセス トークン イントロスペクションまたは JWT を検証します。

## 5. mTLS (相互 TLS)

クライアントが証明書を提示します — **B2B** API に共通:

```text
Partner client cert → Gateway verifies CA → route to upstream
```

強いアイデンティティ。運用の負担が大きくなります (証明書のローテーション、パートナーのオンボーディング)。

## 6. CDN でキャッシュすべきでないもの

認証された応答では以下を使用する必要があります。

```http
Cache-Control: private, no-store
```

Or route `api.example.com` **without CDN cache** — see [CDN APIs & dynamic content](../cdn/vi-apis-and-dynamic-content.md).

## 7. セキュリティチェックリスト

- [ ] HTTPS only; HSTS at CDN/gateway
- [ ] Validate JWT `aud` for your API — not just signature
- [ ] API keys in headers, not query strings
- [ ] Rate limit per key/user ([Rate limiting & resilience](v-rate-limiting-and-resilience.md))
- [ ] Do not trust `X-User-Id` from internet — only from gateway on private link
- [ ] Log auth failures — detect credential stuffing

＃＃ 次

Continue with [Rate limiting & resilience](v-rate-limiting-and-resilience.md) for throttling and failure handling.
