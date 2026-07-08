---
label: "VII"
subtitle: "分散トランザクション"
group: "システム設計"
order: 7
---
分散トランザクション

When one business action touches **multiple services** or **databases**, you cannot rely on a single local `COMMIT` — you need **coordination patterns**.

## 1. 問題

```text
Order service (DB A)     Payment service (DB B)
        │                         │
        └──── both must succeed or neither ────┘
```

ネットワークの分断と独立した障害により、単純な「A を呼び出してから B を呼び出す」フローが破壊されます。

## 2. 2 フェーズコミット (2PC)

|フェーズ |アクション |
|------|----------|
| **準備** |コーディネーターは参加者に「コミットできますか?」と尋ねます。 |
| **コミット** |すべてはい → すべてコミットします。任意 いいえ → すべて中止 |

|長所 |短所 |
|------|------|
|クラスター内の強力な原子性 | **コーディネーターが死亡した場合はブロック** |
| RDBMS でよくわかりました | **マイクロサービス間の適合性が低い** |
| |レイテンシ + 可用性コスト |

1 つのデータベース クラスターまたは密結合ストアの **内部** を使用します。10 個のマイクロサービス全体でデフォルトとして**使用することはできません**。

##3.サーガパターン

**サガ** = **ローカル トランザクション**のシーケンス;各ステップで成功が公開されます。失敗した場合は、**補償**の手順を逆に実行します。

例: **注文の作成 → 支払いの請求 → 在庫の予約**

|ステップ |進む |補償 |
|-----|--------|--------------|
| 1 |注文の作成 (保留中) |注文をキャンセル |
| 2 |チャージカード |払い戻し |
| 3 |在庫を予約 |在庫をリリース |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 120" role="img" aria-label="Saga forward steps and compensating rollback">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Orchestration saga</text>
  <rect x="12" y="36" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="8">1. Order OK</text>
  <path d="M84 50 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="36" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="54" fill="#e4e4e7" font-size="8">2. Pay OK</text>
  <path d="M180 50 H204" stroke="#f87171" stroke-width="1.5"/>
  <rect x="204" y="36" width="72" height="28" rx="3" fill="rgba(248,113,113,0.15)" stroke="#f87171"/>
  <text x="214" y="54" fill="#e4e4e7" font-size="8">3. Stock FAIL</text>
  <text x="12" y="82" fill="#fbbf24" font-size="9">Compensate: refund (2) → cancel order (1)</text>
  <path d="M180 90 H108" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 2"/>
  <path d="M108 90 H36" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 2"/>
</svg></figure>

### 振り付けとオーケストレーション

| |振付 |オーケストレーション |
|---|--------------|--------------|
|コントロール |各サービスは **イベント** に反応します。 **中央オーケストレーター** がコマンドを送信します |
|長所 |単一のコーディネーターがいない SPOF |ステート マシンをクリアし、デバッグを容易にする |
|短所 |グローバルな状態が見えにくい |オーケストレーターの可用性は重要です |
|フィット |少ないステップで成熟したイベント文化 |複雑なフロー、可視性が必要 |

## 4. 冪等性キー

Clients send **`Idempotency-Key: uuid`** on POST; service stores key → response mapping.

|再試行 |行動 |
|------|----------|
|同じキー、進行中 |待つか同じ結果を返す |
|同じキー、完了 |キャッシュされた応答を返す |
|新しいキー |新しい操作 |

**少なくとも 1 回** メッセージングを有効にし、二重料金なしで HTTP を再試行します。

## 5. パターンの選択

|状況 |パターン |
|----------|----------|
|単一の Postgres トランザクション |ローカル ACID |
|同じ DB、複数のテーブル |ローカル ACID |
|マイクロサービス、長期実行 | **佐賀** + 送信ボックス |
| 1 つの DB で強力なクロスシャード | 2PC / XA (アプリ層では稀) |
|モデルを読む |結果整合性 + CDC |

**Related:** [Message queues & async](iii-message-queues-and-async.md) (outbox, events), [API design](ii-api-design.md) (Idempotency-Key).
