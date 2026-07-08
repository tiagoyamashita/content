---
label: "III"
subtitle: "メッセージキューと非同期"
group: "システム設計"
order: 3
---
メッセージキューと非同期フロー

**非同期メッセージング** は、時間と規模の面でプロデューサーとコンシューマーを切り離します。これは、ピーク トラフィックが同期容量を超える場合に重要です。

## 1. 同期と非同期

| |同期 HTTP/RPC |非同期キュー |
|---|---------------------|---------------|
|カップリング |発信者は待機します。呼び出し先は起きている必要があります |プロデューサーがエンキューして続行します。
|発信者までの待ち時間 |完全な処理を含む |ブローカーのみに永続化後の確認応答 |
|スパイク処理 |タイムアウト カスケード |キューがバックログを吸収 |
|デバッグ |単一トレース |ホップ間の相関 ID が必要 |
|一貫性 |即時読み取り書き込み |最終的には;遅延を考慮した設計 |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 140" role="img" aria-label="Sync call vs async queue decoupling">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Sync vs async</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="9">Sync: API ──wait──▶ Worker (both must scale together)</text>
  <rect x="12" y="48" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="66" fill="#e4e4e7" font-size="9">API</text>
  <path d="M68 62 H140" stroke="#f87171" stroke-width="2"/>
  <rect x="140" y="48" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="148" y="66" fill="#e4e4e7" font-size="9">Worker</text>
  <text x="12" y="92" fill="#a1a1aa" font-size="9">Async: API ──▶ Queue ──▶ Worker (scale consumers independently)</text>
  <rect x="12" y="102" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="120" fill="#e4e4e7" font-size="9">API</text>
  <rect x="88" y="102" width="56" height="28" rx="3" fill="rgba(59,130,246,0.15)" stroke="#60a5fa"/>
  <text x="100" y="120" fill="#e4e4e7" font-size="9">Queue</text>
  <path d="M144 116 H200" stroke="#86efac" stroke-width="1.5"/>
  <rect x="200" y="102" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="208" y="120" fill="#e4e4e7" font-size="9">Worker</text>
</svg></figure>

## 2. メッセージングのパターン

|パターン |トポロジ |製品例 |
|----------|----------|---------------------|
| **タスクキュー** | 1 人のプロデューサー → N 人の競合するコンシューマー | SQS、RabbitMQ ワークキュー、Celery |
| **パブ/サブ** | 1 つのイベント → 多くの登録者 | SNS、Kafka トピック、Google Pub/Sub |
| **ログ/ストリーム** |順序付けされたパーティションのログ。リプレイ |カフカ、キネシス、パルサー |
| **配信不能キュー (DLQ)** | N 回の再試行後に失敗したメッセージ | SQS DLQ、RabbitMQ DLX |

## 3. 配送保証

|保証 |意味 |あなたの責任 |
|----------|-----------|----------|
| **最大 1 回** |メッセージが失われる可能性があります |重要な仕事には珍しい |
| **少なくとも 1 回** |重複する可能性があります | **冪等** コンシューマ |
| **1 回だけ** |ハードエンドツーエンド |トランザクション送信ボックス + 冪等シンク、または EOS によるストリーム処理 |

ほとんどの実稼働システム: **少なくとも 1 回** + **冪等キー**。

## 4. トランザクション送信ボックス

**問題:** DB コミットは成功するが、メッセージのパブリッシュが失敗 (またはその逆) → 一貫性のない状態。

**解決策:** ビジネス行 ** と** 送信トレイ行を **1 つの DB トランザクション**で書き込みます。別の **リレー** がブローカーに公開し、送信トレイに送信済みのマークを付けます。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Transactional outbox pattern">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Transactional outbox</text>
  <rect x="12" y="36" width="100" height="80" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="54" fill="#86efac" font-size="9" font-weight="600">Single DB txn</text>
  <text x="24" y="72" fill="#a1a1aa" font-size="8">INSERT order</text>
  <text x="24" y="86" fill="#a1a1aa" font-size="8">INSERT outbox_event</text>
  <path d="M112 76 H160" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="160" y="56" width="80" height="40" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="172" y="80" fill="#e4e4e7" font-size="9">Relay poller</text>
  <path d="M240 76 H288" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="288" y="56" width="72" height="40" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="300" y="80" fill="#e4e4e7" font-size="9">Kafka/SQS</text>
  <text x="12" y="128" fill="#71717a" font-size="9">Event published iff business transaction committed.</text>
</svg></figure>

| Step | Action |
|------|--------|
| 1 | `BEGIN; INSERT orders …; INSERT outbox (payload); COMMIT;` |
| 2 | Relay reads `outbox WHERE sent = false` |
| 3 | Publish to broker; mark row sent (or delete) |

## 5. 順序付けと分割

- **Kafka:** order guaranteed **per partition** — choose partition key (e.g. `user_id`) for related events.
- **Global order:** single partition — limits throughput.
- **Poison message:** after max retries → DLQ + alert; don’t block whole queue.

## 6. 非同期を使用する場合

|非同期を使用する |同期を保つ |
|----------|----------|
|電子メール、通知、検索インデックス作成 |即時結果を待っているユーザー |
|画像・動画処理 |同じリクエストに対する強力な読み取り書き込み |
|多くの加入者へのファンアウト |低遅延のシンプルな CRUD SLA |

**Related:** [Distributed transactions](vii-distributed-transactions.md) (saga events), [Search systems](v-search-systems.md) (CDC to index).
