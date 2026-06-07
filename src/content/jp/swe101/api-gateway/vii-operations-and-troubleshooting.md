---
label: "VII"
subtitle: "操作とトラブルシューティング"
group: "API Gateway"
order: 7
---
API ゲートウェイ — 操作とトラブルシューティング

**アクセス ログ**、**アップストリームの健全性**を使用してゲートウェイを操作し、CDN、ゲートウェイ、サービス全体にわたる**タイムアウト**の調整をクリアします。

## 1. 注目すべき指標

|メトリック |信号 |
|----------|----------|
| **4xx レート** |認証の設定ミス、不正なクライアント |
| **5xx レート** |アップストリームまたはゲートウェイの過負荷 |
| **レイテンシ p50/p99** |ゲートウェイのオーバーヘッドとサービスの遅さ |
| **429 レート** |レート制限の機能 - しきい値の調整 |
| **統合エラー** | Lambda/ALB に到達できません |

**ルート**と**APIバージョン**ごとにダッシュボードを分割します。

## 2. 失敗したリクエストをデバッグする

```text
1. Reproduce with curl -v (include Authorization if needed)
2. Check gateway access log — was upstream called?
3. If 401/403 → auth plugin / JWT claims
4. If 429 → rate limit key / Redis counter
5. If 502/504 → upstream health, timeout, security group
6. Compare direct-to-upstream (VPN) vs via gateway
```

```bash
curl -v https://api.example.com/api/v1/health \
  -H "Authorization: Bearer $TOKEN"
```

## 3. よくある失敗

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| **502 Bad Gateway** | Upstream down, wrong port, VPC link broken | Health check target group |
| **504 Gateway Timeout** | Service slow; gateway timeout too low | Increase timeout or fix service |
| **401 on valid user** | Wrong JWKS, clock skew, `aud` mismatch | Sync NTP; fix issuer config |
| **CORS error in browser** | Gateway missing `Access-Control-*` | Add CORS plugin at gateway |
| **Double slash / 404** | `strip_path` mismatch | Align gateway rewrite with service mount |
| **Works in Postman, fails in prod** | Different host, missing WAF rule | Compare headers and path |

## 4. CDN + ゲートウェイ インシデント

| Symptom | Check |
|---------|-------|
| API cached for wrong user | CDN cache on `/api/*` — bypass or `no-store` |
| Intermittent 504 | CDN timeout &lt; gateway &lt; service — align |
| SSL errors | Cert on CDN vs gateway hostname mismatch |

Full topology: [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

## 5. デプロイメントとロールバック

- **青/緑のアップストリーム** — スイッチ ゲートウェイ ターゲットの重み
- **CI のルート構成** — lint OpenAPI、ドライラン適用
- サービスの **機能フラグ** — ゲートウェイ ルートは安定しています。重みを介したカナリア

Keep **backward-compatible** `/api/v1` during `/api/v2` rollout.

## 6. セキュリティ運用

- API キーをスケジュールに従ってローテーションします。未使用のコンシューマを監査する
- WAF ブロックを確認する — 誤検知と実際の攻撃
- アプリサーバーだけでなく、パブリックゲートウェイ表面の侵入テスト

## 7. チェックリスト

- [ ] Routes match OpenAPI / contract tests
- [ ] Auth enforced on all non-public paths
- [ ] Rate limits per tier documented
- [ ] Timeouts aligned CDN → gateway → service
- [ ] Access logs shipped to SIEM or log aggregator
- [ ] Trace ID from gateway through services
- [ ] `/health` and `/ready` excluded from heavy plugins
- [ ] CDN bypass or `no-store` on authenticated API

## 関連メモ

- [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md) — combined edge architecture
- [CDN operations](../cdn/vii-operations-and-troubleshooting.md) — cache-side debug
- [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md) — algorithms
- [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md) — mesh vs gateway
