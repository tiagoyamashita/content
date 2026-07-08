---
label: "VII"
subtitle: "HA と災害復旧"
group: "クラウドアーキテクチャ"
order: 7
---
高可用性と災害復旧

システムに障害が発生します。 **HA** は、リージョン内のダウンタイムを最小限に抑えます。 **DR** は、地域全体または大規模な災害に備えます。戦略を選択する前に、**RTO** と **RPO** を定義してください。

## 1. 主要な指標

|メトリック |定義 |例 |
|----------|-----------|----------|
| **RTO** |復旧 **時間** 目標 — 許容可能な最大 **ダウンタイム** | 4時間 |
| **RPO** |回復 **ポイント** 目標 — 最大許容**データ損失** (時間枠) | 15分 |

```text
Failure at T0 ───────────────────────────▶ Service restored
              │◀──── RTO (downtime) ────▶│

Last good backup ──▶ Failure
              │◀──── RPO (data lost) ───▶│
```

RTO/RPO が低い → コストと複雑さが増加します。

## 2. 障害の範囲

|範囲 |緩和 |
|------|-----------|
|単一インスタンス | Auto Scaling の置き換え、LB ヘルスチェック |
|シングル AZ |マルチ AZ 展開 |
|全域 |マルチリージョン DR |
|オペレーターエラー |バックアップ、IaC、変更レビュー |

## 3. 複数の AZ パターン

### アクティブ/アクティブ (ステートレス層に推奨)

```text
        ┌── AZ-a: app instances ──┐
  ALB ──┤                         ├── all receive traffic
        └── AZ-b: app instances ──┘
```

**常に**、AZ間でトラフィックの負荷が分散されます。

### アクティブ/パッシブ (データベースに共通)

```text
RDS Primary (AZ-a) ──sync──▶ Standby (AZ-b)
         │
    failover on AZ-a failure → promote standby
```

**RTO** がアクティブ/アクティブ アプリ層よりも高い (DB フェールオーバーに ~ 分)。

### オートスケーリンググループ

- Replace unhealthy instances automatically.
- Spread across AZs via launch template.
- Pair with ALB health checks [Networking, VPC & LB](vi-networking-vpc-and-lb.md).

## 4. DR 層 (最安→最低の RTO)

|階層 |説明 | RTO | RPO |コスト |
|------|---------------|-----|-----|------|
| **バックアップと復元** | S3 への定期的なスナップショット。災害時の再建 |時間 – 日 |営業時間 | $ |
| **パイロットライト** |最小限のコア (DB レプリカ、AMI) は常にオン。スケールアップレスト |営業時間 |分–時間 | $$ |
| **ウォーム スタンバイ** |スケールダウンされたフルスタックの実行。フェイルオーバー時のスケール |分–時間 |分 | $$$ |
| **アクティブ-アクティブ マルチリージョン** | 2 つ以上のリージョンでフルキャパシティ |秒–分 |ゼロに近い | $$$$ |

```text
Backup & restore:     [snapshots in S3] ──on DR──▶ rebuild everything

Pilot light:          [DB replica] + [AMIs] ──on DR──▶ launch full fleet

Warm standby:         [small running env in DR region] ──scale up──▶

Active-active:        [Region A: 100%] + [Region B: 100%] via Route 53
```

## 5. バックアップのベスト プラクティス

|リソース |バックアップ方法 |
|----------|--------------|
| RDS |自動バックアップ + 手動スナップショット |
| EBS |スナップショット |
| S3 |バージョニング + リージョン間レプリケーション |
| K8s | Velero、etcd バックアップ (マネージド コントロール プレーン処理) |
| IaC | Git は信頼できる情報源です — Terraform から環境を再構築します |

**テスト復元** — テストされていないバックアップは希望的観測です。

## 6. マルチリージョンに関する考慮事項

|トピック |詳細 |
|------|----------|
| **レプリケーション** |非同期クロスリージョン — ゼロ以外 RPO |
| **DNS フェイルオーバー** | Route 53 ヘルスチェック + フェイルオーバー ルーティング |
| **データ主権** |一部のデータはプライマリ リージョンから出ることができません。
| **スプリット ブレイン** |競合を解決しない二重書き込みを避ける |

## 7. __​​IT0__ ターゲットの例

|ビジネス | RTO | RPO |戦略 |
|----------|-----|-----|----------|
|内部管理ツール | 24時間 | 24時間 |バックアップと復元 |
| B2B SaaS | 4時間 | 1時間 |ウォームスタンバイ |
|支払い API | 15分 | 1分 |マルチ AZ + クロスリージョン レプリカ |
|グローバルソーシャルアプリ | 1分 | ~0 |アクティブ/アクティブ マルチリージョン |

## 8. ランブックの要点

|ステップ |アクション |
|------|----------|
| 1 |検出 (監視、ヘルスチェック) |
| 2 |事件を宣言し、指揮官を任命 |
| 3 |フェイルオーバー DNS / スタンバイを昇格 |
| 4 | SLO を確認し、ステータスを通知します。
| 5 |インシデント後のレビュー、根本原因の修正 |

## 9. HA チェックリスト

- [ ] LB の背後にある **≥ 2 AZ** のアプリ層
- [ ] データベース **Multi-AZ** または同等のもの
- [ ] ヘルスチェック + 自動置換
- [ ] 保持付きバックアップ + **テスト済みの復元**
- [ ] DR 戦略は RTO/RPO で文書化されています
- [ ] ランブックを毎年リハーサル

**Related:** [Regions, AZs & edge](iii-regions-azs-and-edge.md), patterns [Scalability & caching](../patterns-and-design/ii-scalability-and-caching.md), [Well-Architected Framework](viii-well-architected-framework.md).
