---
label: "III"
subtitle: "マイクロサービス vs モノリス"
group: "クラウドアーキテクチャ"
order: 3
---
マイクロサービス vs モノリス

**モノリス** — 1 つの展開可能なユニット。 **マイクロサービス** — ドメインごとの独立したサービス。ほとんどのチームは、より単純な作業から開始し、摩擦によって複雑さが正当化される場合にのみサービスを抽出する必要があります。

## 1. 比較

| |モノリス |マイクロサービス |
|---|----------|---------------|
| **展開** |単一のアーティファクト |サービスごとのパイプライン |
| **スケール** |アプリ全体 |サービスごと |
| **デバッグ** |単一プロセスのスタック トレース |分散トレースが必要 |
| **データ** |共有 DB、ACID トランザクション |サービスごとのデータベース、結果整合性 |
| **チーム** |共有コードベース |チームはエンドツーエンドのサービスを所有します |
| **レイテンシ** |インプロセス呼び出し |ネットワークホップ |

## 2. モノリスの利点

```text
┌─────────────────────────────────┐
│         Monolith (one JAR)       │
│  ┌─────┐ ┌─────┐ ┌──────────┐  │
│  │Auth │ │Orders│ │Inventory │  │
│  └──┬──┘ └──┬──┘ └────┬─────┘  │
│     └───────┴─────────┘         │
│           shared DB              │
└─────────────────────────────────┘
```

- 迅速なローカル開発 - 実行するサービス メッシュが不要
- モジュール間の単純なトランザクション
- 小規模チーム向けの 1 つのデプロイメント アーティファクト

## 3. マイクロサービスの利点

```text
     ┌─────────┐     ┌─────────┐     ┌──────────┐
     │  Auth   │     │ Orders  │     │ Inventory│
     │ service │     │ service │     │ service  │
     └────┬────┘     └────┬────┘     └────┬─────┘
          │    HTTP/gRPC   │               │
          └────────────────┴───────────────┘
                    message bus (optional)
```

- 認証をスケーリングせずにピーク時に **注文** サービスをスケーリングする
- プラットフォーム全体を再デプロイせずにインベントリ修正をデプロイします
- **制限されたコンテキスト**の所有権をクリアします (DDD)

## 4. モジュラーモノリス — 中間パス

コードを 1 つのデプロイ可能な内部に **明確な境界**を持つモジュールとして構造化します。

```text
src/
  auth/       ← package boundary, no direct DB access from orders
  orders/
  inventory/
  shared-kernel/   ← minimal shared types only
```

|ルール |強制する |
|-----|----------|
|クロスモジュール DB テーブルはありません |モジュールはそのスキーマを所有します。
|モジュールごとのパブリック API |内部クラスプライベート |
|継ぎ目での結合テスト |サービスを抽出する前に |

**独立したリリース ペース**、**異なるスケーリング プロファイル**、または **チームの所有権** 境界が安定している場合に、マイクロサービスに抽出します。

## 5. いつ移行するか

|信号 |アクション |
|----------|----------|
|無関係なチームの変更によってデプロイがブロックされる |安定したドメインを抽出 |
| 1 つのモジュールには 10× CPU | が必要です。個別に抽出してスケーリングする |
|さまざまな SLA (支払いとカタログ) |別途サービス + SLO |
|時期尚早の解散は「Netflixのせい」 |モジュラーモノリスを維持 |

**Strangler fig:** route `%` of traffic to new service via gateway; migrate incrementally.

## 6. 分散データの課題

| Monolith | Microservice |
|----------|--------------|
| `BEGIN; UPDATE orders; UPDATE inventory; COMMIT` | Saga or outbox pattern |
| Join across tables | API composition or read model |
| Strong consistency | Eventual consistency + idempotency |

See [Event-driven architecture](iv-event-driven-architecture.md) for sagas.

## 7. 運用コスト

マイクロサービスには次のものが必要です。

- **CI/CD** per service (or monorepo with path filters)
- **Observability** — traces across calls [Observability, SLI & SLO](vi-observability-slo-and-slis.md)
- **Service discovery** — K8s DNS, Consul, cloud LB
- **Versioning** — backward-compatible APIs, consumer-driven contracts

## 8. 意思決定チェックリスト

|質問 |モノリス OK if |
|----------|----------------|
|チームの規模が 10 未満ですか? |多くの場合、そうです |
|シングルリリーストレイン？ |はい |
|ドメインはまだ移行中ですか? |はい — 早期の分割は避けてください |
| 1 つのドメインにスケーリングのボトルネックがあることが判明していますか? |抽出を検討してください |

## 9. 進化の例

|フェーズ |建築 |
|------|--------------|
| MVP |単一の Spring Boot アプリ + Postgres |
|成長 |モジュラーモノリス + Redis + リードレプリカ |
|スケール |支払い (PCI スコープ)、注文 (ピーク負荷) を抽出する |
|成熟した |サービス メッシュ、イベント バス、独立した SLO |

**Related:** [Event-driven architecture](iv-event-driven-architecture.md), [API Gateway & service mesh](v-api-gateway-and-service-mesh.md).
