---
label: "I"
subtitle: "概要"
group: "クラウドアーキテクチャ"
order: 1
---
パターンとデザイン — 概要

**基礎** サブメニューでは、**クラウドが提供するもの** (コンピューティング、ストレージ、VPC) をカバーします。このサブメニューでは、アプリケーションおよびプラットフォーム レベルでの規模、復元力、可観測性、コストを**設計する方法**について説明します。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [スケーラビリティとキャッシュ](ii-scalability-and-caching.md) |スケールアップ/アウト、ステートレス アプリ、自動スケーリング、キャッシュ層 |
| [マイクロサービス vs モノリス](iii-microservices-vs-monolith.md) |モノリス、モジュラーモノリス、マイクロサービスのトレードオフ |
| [イベント駆動型アーキテクチャ](iv-event-driven-architecture.md) |キュー、パブ/サブスク、ストリーミング、物語 |
| [APIゲートウェイとサービスメッシュ](v-api-gateway-and-service-mesh.md) |南北対東西、サーキットブレーカー |
| [可観測性、SLI および SLO](vi-observability-slo-and-slis.md) |ログ、メトリック、トレース、SLI/SLO/SLA |
| [コストとガバナンス](vii-cost-and-governance.md) |価格モデル、FinOps、IAM、ガードレール |

**関連:** **Foundations** サブメニュー (Well-Architected の柱)、システム設計 **スケーラブル パターン**、ネットワーキング Ingress/CDN のメモ。

## アーキテクチャ層 (メンタルモデル)

<figure class="notes-diagram"><svg xmlns="0 viewBox="0 0 440 120" role="img" aria-label="Cloud architecture layers client gateway services data">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Request path — patterns apply at each hop</text>
  <rect x="12" y="40" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="58" fill="#e4e4e7" font-size="8">Client</text>
  <path d="M68 54 H88" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="88" y="40" width="64" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="58" fill="#e4e4e7" font-size="8">CDN / GW</text>
  <path d="M152 54 H172" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="172" y="40" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="180" y="58" fill="#e4e4e7" font-size="8">Services</text>
  <path d="M244 54 H264" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="264" y="40" width="56" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="272" y="58" fill="#e4e4e7" font-size="8">Cache</text>
  <path d="M320 54 H340" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="340" y="40" width="56" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="348" y="58" fill="#e4e4e7" font-size="8">Data</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Scale services horizontally · cache reads · async where possible · observe everything</text>
</svg></figure>

## 適切に設計された接続

|柱 |このサブメニューのパターン |
|----------|--------------------------|
| **信頼性** |オートスケーリング、サーキットブレーカー、マルチ AZ (基盤) |
| **パフォーマンス** |キャッシュ、CDN、適切なサイジング |
| **セキュリティ** |ゲートウェイ認証、IAM 最小権限、ガバナンス |
| **コスト** |スポット、予約済み、FinOps タグ付け |
| **優れた運用能力** |可観測性、SLO |

## リハーサル

- ステートレスとステートフル — 自動スケーリングへの影響?
- キューとパブ/サブスクライブ — 1 人のコンシューマーか、それとも複数のコンシューマーか?
- SLI、SLO、SLA — どちらが契約上のものですか?
