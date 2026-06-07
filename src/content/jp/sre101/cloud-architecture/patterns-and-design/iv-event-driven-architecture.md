---
label: "IV"
subtitle: "イベント駆動型アーキテクチャ"
group: "クラウドアーキテクチャ"
order: 4
---
イベント駆動型アーキテクチャ

サービスは、同期チェーンではなく、**メッセージ ブローカー**上の**イベント**を介して通信します。プロデューサーを消費者から切り離し、トラフィックの急増を吸収します。

## 1. 同期と非同期

|同期 (HTTP) |非同期 (イベント) |
|----||---------|
|発信者が待つ |プロデューサーは解雇して忘れる |
|密結合 |時間内の疎結合 |
|簡単なデバッグ |冪等性が必要です、DLQ |
|カスケード遅延 |負荷時のバッファリング |

```text
Sync:  Order Svc ──HTTP──▶ Inventory Svc ──HTTP──▶ Payment Svc
       (failure in payment blocks whole chain)

Async: Order Svc ──▶ queue ──▶ Inventory worker
                    └──▶ Payment worker (parallel)
```

## 2. メッセージキュー (ポイントツーポイント)

**1 つのコンシューマ** が各メッセージを処理します (競合するコンシューマ)。

```text
Producer ──▶ [ Queue ] ──▶ Consumer A
                    └──▶ Consumer B  (only one gets each message)
```

|クラウドサービス |モデル |
|---------------|------|
| **AWS SQS** |標準または FIFO キュー |
| **Azure サービス バス** |キュー |
| **Google Cloud タスク** |タスクキュー |

**次の場合に使用します:** ジョブ処理、作業分散、バックプレッシャー (プロデューサーがコンシューマーよりも速い)。

```json
{
  "eventType": "OrderPlaced",
  "orderId": "ord-9281",
  "items": [{"sku": "WIDGET-1", "qty": 2}],
  "timestamp": "2026-05-19T14:22:00Z"
}
```

## 3. パブリッシュ/サブスクライブ (ファンアウト)

**各購読者**はメッセージのコピーを受信します。

```text
Publisher ──▶ [ Topic ] ──▶ Subscriber A (email)
                    ├──▶ Subscriber B (analytics)
                    └──▶ Subscriber C (inventory)
```

|クラウドサービス |パターン |
|--------------|----------|
| **AWS SNS** + SQS | SNS は複数の SQS キューにファンアウトします。
| **Google Pub/Sub** |ネイティブパブ/サブ |
| **Azure Event Grid** |イベントルーティング |

**Use when:** notify multiple systems of same fact (`UserRegistered` → welcome email + CRM + audit).

## 4. キューとパブ/サブスクライブの比較

| |キュー |パブ/サブ |
|---|------|----------|
|配送 |メッセージごとに 1 人のコンシューマ |すべての購読者はコピーを取得します |
|注文 | FIFO キューはオプション |トピックの順序は異なります |
|例 |支払い処理ジョブ |ブロードキャスト設定の変更 |
|背圧 |キューの深さのメトリック |遅いサブスクライバには独自のキューが必要です。

## 5. イベントストリーミング

**順序付けされた再生可能なログ** — 消費者はオフセットを追跡します。

```text
Producer ──▶ [ Kafka topic: orders ] ──▶ Consumer group A (analytics)
                                   └──▶ Consumer group B (fraud)
```

|プラットフォーム |特徴 |
|----------|------|
| **Apache Kafka** |パーティション、保持、再生 |
| **AWS キネシス** |シャード、ストリーム処理 |
| **Azure イベント ハブ** | Kafka 互換エンドポイント |

**次の場合に使用します:**

- **監査証跡** — 再生履歴
- **イベント ソーシング** — イベント ログから派生した状態
- **複数の独立したコンシューマー**が異なる速度で使用可能
- **ストリーム処理** — Flink、ksqlDB、Lambda

##6.サーガパターン

サービス間での分散トランザクション — **単一の DB トランザクションはありません**。

### 振付（イベントのみ）

```text
OrderCreated ──▶ ReserveInventory ──▶ PaymentCaptured ──▶ OrderConfirmed
                      │ fail
                      └──▶ ReleaseInventory (compensating)
```

各サービスはリッスンして、次のステップまたは補償を公開します。

### オーケストレーション (中央コーディネーター)

```text
Saga orchestrator
  1. call inventory.reserve()
  2. call payment.charge()
  3. on failure → payment.refund(), inventory.release()
```

| |振付 |オーケストレーション |
|---|--------------|--------------|
|カップリング |ルース | Orchestrator はすべての手順を知っています |
|可視性 |追跡が困難 |中央ステートマシン |
|ツーリング |イベントバス |時間関数、ステップ関数 |

## 7. 信頼性パターン

| Pattern | Purpose |
|---------|---------|
| **Dead-letter queue (DLQ)** | Poison messages after N retries |
| **Idempotent consumer** | Same `orderId` processed once |
| **Outbox pattern** | DB commit + event publish atomically |
| **Visibility timeout** | SQS redelivery if worker crashes |

```java
// Idempotent consumer — Java 22
void handle(OrderPlaced event) {
  if (processedEvents.exists(event.id())) return;
  process(event);
  processedEvents.mark(event.id());
}
```

## 8. イベントを使用しない場合

|状況 |優先する |
|----------|----------|
|即時応答を待っているユーザー | HTTP/gRPC を同期する |
|強い一貫性が必要 |単一の DB トランザクション |
| 2 つのサービスのスタートアップ |複雑になるまで直接呼び出し |

**Related:** [Microservices vs monolith](iii-microservices-vs-monolith.md), [API Gateway & service mesh](v-api-gateway-and-service-mesh.md).
