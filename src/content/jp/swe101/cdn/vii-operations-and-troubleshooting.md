---
label: "VII"
subtitle: "操作とトラブルシューティング"
group: "CDN"
order: 7
---
CDN — 操作とトラブルシューティング

**ヒット率**、**オリジン ロード**、**エラー率**を監視し、本番環境で何か問題が発生した場合に**パージ**および**ヘッダーをデバッグ**する方法を理解して、CDNを操作します。

## 1. 追跡する指標

| Metric | Healthy signal |
|--------|----------------|
| **Cache hit ratio** | High for static paths (`/assets/*`) |
| **Origin requests** | Drop after CDN enabled |
| **4xx/5xx at edge** | Low; spike → config or origin |
| **Time to first byte (TTFB)** | Lower from edge than direct origin |
| **Bandwidth egress** | Origin egress down; CDN bill may rise |

プロバイダー ダッシュボード: CloudFront **モニタリング**、Cloudflare **分析**、Fastly **リアルタイム統計**。

## 2.カールによるデバッグ

```bash
# Response headers
curl -sI https://cdn.example.com/assets/main.js

# Look for:
# Cache-Control, Age, ETag
# CloudFront: X-Cache: Hit from cloudfront
# Cloudflare: CF-Cache-Status: HIT | MISS | BYPASS
```

**CDN** 経由と **直接オリジン** を比較します (ステージングのみで DNS をオリジン IP にバイパスします):

```bash
curl -sI -H "Host: cdn.example.com" https://origin-internal/assets/main.js
```

## 3. よくある失敗

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Users see old JS after deploy | `index.html` or SW cached too long | Short TTL on shell; purge `index.html` |
| API returns wrong user’s data | Public cache on private route | `no-store`; disable CDN for path |
| 403 from S3 origin | OAC/OAI policy wrong | Fix bucket policy + distribution |
| SSL error | Cert not in right region / wrong SAN | ACM us-east-1 for CloudFront |
| Low hit rate | Query string busts cache | Cache key rules; strip tracking params |
| CORS failures | Headers only on origin | Add CORS headers at CDN or origin consistently |
| Infinite redirect loop | HTTP/HTTPS mismatch | SSL mode Full (strict); origin listens HTTPS |

## 4. 古いコンテンツのプレイブック

```text
1. Confirm symptom (one region vs global)
2. curl -sI URL — Hit or Miss? Age?
3. Check recent deploy — index.html vs assets
4. Purge specific path(s) if needed
5. Verify Cache-Control at origin
6. Post-incident: version URLs or shorter TTL
```

習慣的な **すべてパージ** を避けてください。ハッシュベースのデプロイ規則が欠落していることをマスクします。

## 5. セキュリティインシデント

悪意のあるファイルまたは漏洩したファイルがキャッシュされていた場合:

1. **原点から削除**してください。
2. **影響を受けるパス (および必要に応じてワイルドカード) の CDN** を削除します。
3. 応答にトークンが含まれている場合は、シークレットをローテーションします。
4. **キャッシュ キー**を確認します。認証応答がキャッシュ可能でないことを確認します。

## 6. コスト意識

|コストドライバー |注 |
|---------------|------|
| **出口** | CDN エグレスは、多くの場合、クラウド オリジンのエグレスよりも安価です。
| **リクエスト** |一部のレベルでのリクエストごとの価格設定 |
| **無効化** | CloudFront: 月あたりの無料利用枠が制限されている |
| **エッジ コンピューティング** |呼び出しごとの Workers/Lambda@Edge |

不変アセットに対する長い TTL により、オリジン ** と ** 無効化のチャーンが減少します。

## 7. チェックリスト

- [ ] Hashed static assets — `max-age` ≥ 1 year, `immutable`
- [ ] `index.html` — short TTL or `must-revalidate`
- [ ] Private API — `no-store` or CDN bypass behavior
- [ ] Origin not publicly writable (OAC, signed uploads)
- [ ] TLS full chain valid; HSTS when ready
- [ ] Monitoring on hit ratio and 5xx
- [ ] Documented purge runbook for security deploys
- [ ] CI sets `Cache-Control` on upload — not manual clicks

＃＃ 次

Continue with [CDN & API gateway together](viii-cdn-and-api-gateway-together.md), then the [API gateway](../api-gateway/i-overview.md) track.

## 関連メモ

- [CDN & edge caching](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md) — design patterns
- [Network bottlenecks](../sysdesign/bottleneck-analysis/v-network.md) — CDN in latency story
- [Redis performance](../redis/vii-performance-and-optimizations.md) — app-layer cache complement
- [Regions, AZs & edge](../../sre101/cloud-architecture/foundations/iii-regions-azs-and-edge.md) — edge vs region
