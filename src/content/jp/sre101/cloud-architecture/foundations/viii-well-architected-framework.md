---
label: "VIII"
subtitle: "適切に設計されたフレームワーク"
group: "クラウドアーキテクチャ"
order: 8
---
適切に設計されたフレームワーク

AWS **Well-Architected フレームワーク** (概念的には Azure/GCP にも適用されます) は、ワークロードをレビューするための **6 つの柱**を定義します。設計レビューや事件後の回顧に使用してください。

## 1. 柱の概要

| # |柱 |質問に答える |
|---|--------|----------|
| 1 | **オペレーショナルエクセレンス** |システムを実行して改善することはできるでしょうか? |
| 2 | **セキュリティ** |データとインフラストラクチャは保護されていますか? |
| 3 | **信頼性** |障害から回復して需要に応えられるか? |
| 4 | **パフォーマンス効率** |私たちは資源をうまく活用できていますか? |
| 5 | **コストの最適化** |私たちは無駄を避けていますか？ |
| 6 | **持続可能性** |私たちは環境への影響を最小限に抑えていますか? |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 100" role="img" aria-label="Six Well-Architected pillars">
  <text x="12" y="18" fill="#d4d4d8" font-size="11" font-weight="600">Six pillars — no single pillar wins alone</text>
  <rect x="12" y="32" width="52" height="22" rx="2" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="16" y="47" fill="#e4e4e7" font-size="7">Ops</text>
  <rect x="70" y="32" width="52" height="22" rx="2" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="74" y="47" fill="#e4e4e7" font-size="7">Security</text>
  <rect x="128" y="32" width="52" height="22" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="132" y="47" fill="#e4e4e7" font-size="7">Reliable</text>
  <rect x="186" y="32" width="52" height="22" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="190" y="47" fill="#e4e4e7" font-size="7">Perf</text>
  <rect x="244" y="32" width="52" height="22" rx="2" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="248" y="47" fill="#e4e4e7" font-size="7">Cost</text>
  <rect x="302" y="32" width="52" height="22" rx="2" fill="rgba(45,212,191,0.12)" stroke="#2dd4bf"/>
  <text x="306" y="47" fill="#e4e4e7" font-size="7">Sustain</text>
  <text x="12" y="78" fill="#71717a" font-size="9">Trade-offs: stricter security may add latency; higher availability adds cost</text>
</svg></figure>

## 2. 優れた運用性

システムを実行および監視します。継続的に改善します。

|練習 |クラウドの例 |
|----------|--------------|
| **コードとしてのインフラストラクチャ** | Terraform、クラウドフォーメーション |
| **可逆的な小さな変化** |機能フラグ、青/緑の展開 |
| **ランブック** | DR フェイルオーバー手順を文書化 |
| **可観測性** |ログ、メトリクス、トレース、アラーム |

```text
Change → CI/CD → automated test → staged deploy → monitor → rollback if SLO burn
```

**アンチパターン:** 監査証跡を伴わない手動のコンソール変更。

## 3. セキュリティ

情報、システム、資産を保護します。

|練習 |クラウドの例 |
|----------|--------------|
| **最低特権 IAM** |ワークロードごとのロール、ワイルドカードなし |
| **暗号化** | TLS は転送中、KMS は静止中 |
| **監査** | CloudTrail、構成、GuardDuty |
| **ネットワーク分離** |プライベートサブネット、セキュリティグループ |

See patterns [Cost & governance](../patterns-and-design/vii-cost-and-governance.md) for IAM/SCP detail.

## 4. 信頼性

障害から回復し、需要に応えます。

|練習 |クラウドの例 |
|----------|--------------|
| **マルチ AZ** | AZ 全体の ASG + ALB |
| **自動スケーリング** | CPU/RPS でのターゲット追跡 |
| **健康診断** | LB + ルート 53 |
| **グレースフルデグラデーション** |サーキット ブレーカー、キャッシュされたフォールバック |

Foundations: [HA & disaster recovery](vii-ha-and-disaster-recovery.md). Patterns: event-driven, circuit breakers.

## 5. パフォーマンス効率

需要の変化に応じてコンピューティング リソースを効率的に使用します。

|練習 |クラウドの例 |
|----------|--------------|
| **適切なサイジング** | Compute Optimizer の推奨事項 |
| **マネージド サービス** | RDS と EC2 上の自己管理型 Postgres の比較 |
| **キャッシング** | CloudFront、Redis |
| **ベンチマーク** |起動前の負荷テスト |

|レビュー |質問 |
|----------|----------|
|間違ったインスタンス ファミリ | CPU はメモリ最適化に依存していますか? |
| CDN が見つかりません |静的アセットがオリジンにヒットしますか? |
|非同期が適した場所で同期 |キューの分離 |

## 6. コストの最適化

要件を満たしながら不必要な支出を回避します。

|練習 |クラウドの例 |
|----------|--------------|
| **予約/節約プラン** |安定したベースライン容量 |
| **スポット** |バッチ、フォールト トレラント ワーカー |
| **自動スケールイン** |アイドル容量を削除 |
| **タグ付けと予算** |チームごとのコスト配分 |

Full detail: patterns [Cost & governance](../patterns-and-design/vii-cost-and-governance.md).

## 7. 持続可能性

クラウド ワークロードによる環境への影響を最小限に抑えます。

|練習 |効果 |
|----------|----------|
| **適切なサイズ** |無駄な CPU サイクルが減少 |
| **使用率の向上** |全体的な物理サーバーの数が少ない |
| **マネージド サービス** |プロバイダーはハードウェア効率を最適化します |
| **Graviton / ARM インスタンス** |互換性のあるアプリのパフォーマンス/ワットの向上 |
| **アイドル状態のリソースを削除します** |ゴースト EC2 または接続されていない EBS はありません。

多くの場合、**コスト** の最適化と連携します。効率的であるということは、通常、より環境に優しいということを意味します。

## 8. 適切に設計されたレビュー (WAR)

柱ごとに構造化されたアンケート — 実行:

- メジャーリリース前
- 重大な事件の後
- 重要なワークロードについては毎年

出力: **HRI** (高リスクの問題) を優先して修復します。

## 9. 柱のトレードオフ

|テンション |バランス |
|----------|----------|
|セキュリティとパフォーマンス | mTLS はレイテンシを追加します - 東西を問わず価値があります |
|信頼性とコスト |マルチリージョンのインフラが 2 倍になる — ビジネスケースが必要 |
|スピードと運用の卓越性 |締め切りのプレッシャー下でも自動化 |
|コストと信頼性 |バッチにはスポット、クリティカル パスにはオンデマンド |

## 10. 柱をこのトラックにマップします

| Pillar | Foundations note | Patterns note |
|--------|------------------|---------------|
| Ops | [HA & disaster recovery](vii-ha-and-disaster-recovery.md) | observability, CI/CD |
| Security | [Networking, VPC & LB](vi-networking-vpc-and-lb.md) | governance |
| Reliability | multi-AZ, DR | scaling, circuit breakers |
| Performance | compute, storage | caching |
| Cost | — | FinOps |
| Sustainability | right-size compute | utilization |

## 11. リハーサルの答え

- **6 つの柱** — 運用、セキュリティ、信頼性、パフォーマンス、コスト、持続可能性。
- **信頼性と HA** — 信頼性が柱です。 HA は複数の AZ テクニックです。
- **IaC** — Ops + Security (レビュー可能な変更) をサポートします。

**Related:** [Overview](i-overview.md), **Patterns & design** submenu, CI/CD Terraform submenu.
