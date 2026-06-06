---
label: "I"
subtitle: "概要"
group: "クラウドアーキテクチャ"
order: 1
---
基礎 — 概要

パターンとスケールの前に、**クラウド プロバイダーが提供するもの**: サービス モデル、リージョン、コンピューティング、ストレージ、ネットワーキング、**障害と復旧**に備えた設計方法を理解してください。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [サービスモデル](ii-service-models.md) | IaaS、PaaS、SaaS、共同責任 |
| [リージョン、AZ、エッジ](iii-regions-azs-and-edge.md) |リージョン、AZ、CDN エッジ、データ常駐 |
| [計算オプション](iv-compute-options.md) | VM、コンテナ/K8、サーバーレス、コールド スタート |
| [ストレージとデータベース](v-storage-and-databases.md) |オブジェクト、ブロック、ファイルストレージ。 SQL と NoSQL |
| [ネットワーキング、VPC、LB](vi-networking-vpc-and-lb.md) | VPC、サブネット、ロードバランサー、DNS、ファイアウォール |
| [HA および災害復旧](vii-ha-and-disaster-recovery.md) | RTO/RPO、マルチ AZ、DR 層 |
| [適切に設計されたフレームワーク](viii-well-architected-framework.md) | 6 つの柱とクラウドの例 |

**次へ:** **パターンとデザイン** サブメニュー - スケーラビリティ、マイクロサービス、イベント、可観測性、コスト。

## クラウドスタックの概要

<figure class="notes-diagram"><svg xmlns="0 viewBox="0 0 440 100" role="img" aria-label="Cloud foundation layers compute storage network">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Build blocks every architecture uses</text>
  <rect x="12" y="40" width="80" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="28" y="60" fill="#e4e4e7" font-size="9">Compute</text>
  <rect x="108" y="40" width="80" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="124" y="60" fill="#e4e4e7" font-size="9">Storage</text>
  <rect x="204" y="40" width="80" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="220" y="60" fill="#e4e4e7" font-size="9">Network</text>
  <rect x="300" y="40" width="80" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="60" fill="#e4e4e7" font-size="9">Security</text>
  <text x="12" y="88" fill="#71717a" font-size="9">All run inside regions · spread across AZs for HA</text>
</svg></figure>

## リハーサル

- IaaS 対 PaaS 対 SaaS — それぞれ 1 つの例?
- **≥ 2 AZ** に展開する理由は何ですか?
- オブジェクト ストレージとブロック ストレージ — それぞれをいつ使用するか?
- RTO と RPO — ダウンタイムとデータ損失はどちらですか?
