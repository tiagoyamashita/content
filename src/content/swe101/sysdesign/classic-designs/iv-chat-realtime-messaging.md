---
label: "IV"
subtitle: "チャットとリアルタイムメッセージング"
group: "システム設計"
order: 4
---
チャットとリアルタイムメッセージング

順序付け、永続性、**プレゼンス**を使用して、メッセージをオンライン受信者に**即座に**配信します。

## 1. 輸送の比較

|方法 |レイテンシ |サーバー負荷 |フィット |
|----------|----------|---------------|-----|
|ショートポーリング |高 (N × 間隔) |無駄 |レガシー |
|ロングポーリング |より良い |接続が保持されています |フォールバック |
| **WebSocket** |低い |永続的な接続 | **チャットのデフォルト** |
| SSE |サーバー → クライアントのみ |よりシンプル |完全なチャットではなく通知 |

## 2. 高レベルのアーキテクチャ

<figure class="notes-diagram"><svg xmlns="6 viewBox="0 0 480 120" role="img" aria-label="Chat architecture WebSocket broker storage presence">
  <rect x="12" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Client</text>
  <path d="M68 60 H108" stroke="#86efac" stroke-width="2"/>
  <rect x="108" y="44" width="72" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="64" fill="#e4e4e7" font-size="9">Chat WS</text>
  <path d="M180 60 H220" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="220" y="44" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="228" y="64" fill="#e4e4e7" font-size="9">Kafka</text>
  <path d="M284 60 H324" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="324" y="44" width="72" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="332" y="64" fill="#e4e4e7" font-size="9">Cassandra</text>
  <rect x="108" y="88" width="72" height="24" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="118" y="104" fill="#e4e4e7" font-size="8">Presence Redis</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Message flow</text>
</svg></figure>

|サービス |役割 |
|-------|------|
| **チャット / 接続** | WebSocket が終了します。受信者のサーバーへのルート |
| **メッセージ ブローカー** |耐久性。複数のチャット ノードへのファンアウト |
| **メッセージストア** |履歴メッセージ |
| **プレゼンス** |オンライン / 最後に見た |
| **プッシュ通知** |受信者がオフラインの場合の APNS/FCM |

## 3. メッセージの保存

**Cassandra** (ワイドカラム) — パーティション キーの設計:

|パーティションキー |クラスタリング |クエリ |
|---------------|-----------|------|
| `conversation_id` | `message_id DESC` |スレッド内の最新 N 個のメッセージ |

**スノーフレーク ID:** タイムスタンプ + マシン ID + シーケンス → 中央 DB シーケンスなしで **ソート可能**。

|プロパティ |メリット |
|----------|----------|
|時間順 | ID による範囲スキャン |
|クラスター全体で一意 |インサートごとに調整なし |

## 4. 存在感

|イベント |アクション |
|------|----------|
|接続 |セット `presence:{user_id}` TTL 30 秒 |
|心拍数は 5 秒ごと |期限切れ更新 |
|切断/タイムアウト |キーの有効期限が切れた → オフライン |

**Redis** に保存します。購読者はパブ/サブまたはブローカー経由で友人に通知します。

## 5. 配送保証

- **少なくとも 1 回** ブローカー経由 - クライアントは `message_id` によって **重複排除**します。
- オフライン ユーザー: 次回の同期時に永続 + **プッシュ通知**。
- マルチデバイス: `user_id` のすべてのアクティブなセッションにファンアウトします。

## 6. スケールノート

- WebSocket アフィニティの **スティッキー セッション** または **ユーザー → サーバー** ルーティング テーブル。
- `conversation_id`までに会話をシャード化します。
- メディア: オブジェクト ストア + CDN;メッセージには URL のみが含まれます。

**関連:** ネットワーキング パート I (WebSocket/TCP)、スケーラブルなパターン メッセージング。
