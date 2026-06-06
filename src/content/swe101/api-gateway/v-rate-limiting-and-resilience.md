---
label: "V"
subtitle: "レート制限と回​​復力"
group: "API Gateway"
order: 5
---
API ゲートウェイ — レート制限と復元力

ゲートウェイでの **レート制限** により、アップストリームを悪用や不当な使用から保護します。回復力を高めるために、**タイムアウト**、**再試行** (慎重に)、および **サーキット ブレーカー** と組み合わせてください。

Deep dive on algorithms: [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md). App-layer limiter: [Redis patterns](../redis/iv-patterns-and-use-cases.md).

## 1. ゲートウェイで制限する理由

|目標 |例 |
|-----|----------|
| **虐待** |ブロックスクレイピング、クレデンシャルスタッフィング |
| **公平性** |無料利用枠 100 リクエスト/分。 10,000 を支払った |
| **コスト** | LLM/GPU エンドポイント |
| **安定性** | 1 つのテナントが接続プールを使い果たすことはできません。

Reject with **429 Too Many Requests** + **`Retry-After`** header when possible.

## 2. 寸法の制限

| Key | Use |
|-----|-----|
| **API key / client id** | Partner quotas |
| **User id** (from JWT) | Per-account fairness |
| **IP address** | Anonymous endpoints — noisy neighbor |
| **Route** | Stricter on `/search` vs `/health` |

```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 500
      policy: local   # or redis for cluster-wide
      limit_by: consumer
```

複数のゲートウェイ インスタンスがカウンターを共有する必要がある場合は、**Redis-backed** リミッターを使用します。

## 3. トークンバケット (通常)

- バケット サイズ **B** ではバーストが可能
- 補充率 **R** の上限が維持されます QPS

ゲートウェイ プラグインは多くの場合、「1 分あたりのリクエスト」を公開し、内部でバケット/ウィンドウにマップします。

## 4. タイムアウトとペイロード制限

|設定 |目的 |
|----------|----------|
| **接続タイムアウト** |上流が停止している場合は高速に失敗する |
| **読み取りタイムアウト** |応答本文の最大待ち時間 |
| **最大ボディサイズ** |エッジで巨大なアップロードを拒否 |

Gateway timeout should be **≤ CDN timeout** and **≥ upstream p99** — align all three layers ([CDN & gateway together](../cdn/viii-cdn-and-api-gateway-together.md)).

## 5. サーキットブレーカー

アップストリームのエラー率が急上昇した場合、スレッドをキューに入れる代わりに**フェイルファスト**します。

|状態 |行動 |
|------|----------|
| **閉店** |通常のプロキシ |
| **開く** |クライアントへの即時 503/504 |
| **ハーフオープン** |プローブリクエスト — 回復するか開いたままにする |

**Resilience4j** (Java)、**Envoy 外れ値検出**、**Istio 宛先ルール** - ゲートウェイまたはメッシュ。

ブレーカーなし: 再試行の嵐により停止が拡大します。

## 6. ゲートウェイでの再試行

|安全に再試行できます |安全ではありません |
|---------------|----------|
| **GET** べき等 | **POST** 支払い |
| **503** 冪等 ID |冪等でない書き込み |

ゲートウェイが再試行する場合は、**制限付き再試行 + ジッター** を使用します。書き込みにはアプリ内の冪等キーを優先します。

## 7. __​​IT0__ とボット保護

多くのスタックは以下を組み合わせています。

```text
CDN/WAF (SQLi, XSS patterns) → Gateway (auth, rate limit) → service
```

Cloudflare、ALB/API Gateway 上の AWS WAF — アプリコードの前に明らかな攻撃をブロックします。

＃＃ 次

Continue with [Setup & providers](vi-setup-and-providers.md) for AWS API Gateway, Kong, and NGINX patterns.
