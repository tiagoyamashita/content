---
label: "VII"
subtitle: "操作とトラブルシューティング"
group: "CDN"
order: 7
---
CDN — 操作とトラブルシューティング

CDN を運用するには、**ヒット率**、**オリジン ロード**、**エラー率**を監視し、本番環境で何か問題が発生した場合に**パージ**および**ヘッダーをデバッグ**する方法を理解する必要があります。

## 1. 追跡する指標

|メトリック |健全な信号 |
|------|----------------|
| **キャッシュ ヒット率** |静的パスの場合は高 (`/assets/*`) |
| **オリジンリクエスト** | CDN を有効にした後にドロップ |
| **エッジで 4xx/5xx** |低い;スパイク → 設定またはオリジン |
| **最初のバイトまでの時間 (TTFB)** |直接の原点よりもエッジから低い |
| **帯域幅下り** |原点は下り方向に出力されます。 CDN の請求額が上がる可能性がある |

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

**CDN 経由** と **直接オリジン** を比較します (ステージングのみで DNS をオリジン IP にバイパスします):

```bash
curl -sI -H "Host: cdn.example.com" https://origin-internal/assets/main.js
```

## 3. よくある失敗

|症状 |考えられる原因 |修正 |
|----------|--------------|-----|
|デプロイ後にユーザーに古い JS が表示される | `index.html` または SW のキャッシュ時間が長すぎます |シェル上の短い TTL。パージ `index.html` |
| API が間違ったユーザーのデータを返す |プライベート ルート上のパブリック キャッシュ | `no-store`;パスの CDN を無効にする |
| S3 オリジンからの 403 | OAC/OAI ポリシーが間違っています |バケットポリシー + 配布を修正 |
| SSL エラー |証明書が正しいリージョンにない / 間違った SAN | CloudFront 用 ACM us-east-1 |
|ヒット率が低い |クエリ文字列がキャッシュを破壊します |キャッシュキールール。ストリップ追跡パラメータ |
| CORS の失敗 |ヘッダーはオリジンのみ | CORS ヘッダーを CDN またはオリジンに一貫して追加します。
|無限リダイレクト ループ | HTTP/HTTPS の不一致 | SSL モード フル (厳密)。オリジンはHTTPSをリッスンします |

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
2. 影響を受けるパス (および必要に応じてワイルドカード) の **CDN をパージ**します。
3. 応答にトークンが含まれている場合は、シークレットをローテーションします。
4. **キャッシュ キー**を確認します。認証応答がキャッシュ可能でないことを確認します。

## 6. コスト意識

|コストドライバー |注 |
|---------------|------|
| **出口** | CDN 下りは、多くの場合、クラウド オリジン下りよりも安くなります。
| **リクエスト** |一部のレベルでのリクエストごとの価格設定 |
| **無効化** | CloudFront: 月あたりの無料利用枠が制限されている |
| **エッジ コンピューティング** |呼び出しごとの Workers/Lambda@Edge |

不変アセットの長い TTL により、オリジン ** と** 無効化のチャーンが減少します。

## 7. チェックリスト

- [ ] ハッシュ化された静的資産 — `max-age` ≥ 1 年、`immutable`
- [ ] `index.html` — 短い TTL または `must-revalidate`
- [ ] プライベート API — `no-store` または CDN バイパス動作
- [ ] オリジンは公的に書き込み可能ではありません (OAC、署名されたアップロード)
- [ ] TLS フルチェーンが有効です。準備ができたらHSTS
- [ ] ヒット率と5xxの監視
- [ ] セキュリティ展開のための文書化されたパージ ランブック
- [ ] CI はアップロード時に `Cache-Control` を設定します - 手動クリックではありません

＃＃ 次

[CDN と API ゲートウェイを一緒に](viii-cdn-and-api-gateway-together.md) に進み、次に [API ゲートウェイ](../api-gateway/i-overview.md) を追跡します。

## 関連メモ

- [CDN & エッジ キャッシング](../sysdesign/scalable-patterns/vi-cdn-and-edge-caching.md) — デザイン パターン
- [ネットワークのボトルネック](../sysdesign/bottleneck-analysis/v-network.md) — 遅延の話における CDN
- [Redis パフォーマンス](../redis/vii-performance-and-optimizations.md) — アプリ層キャッシュの補完
- [リージョン、AZ、エッジ](../../sre101/cloud-architecture/foundations/iii-regions-azs-and-edge.md) — エッジとリージョン
