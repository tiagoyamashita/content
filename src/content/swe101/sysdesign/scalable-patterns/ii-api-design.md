---
label: "II"
subtitle: "API設計"
group: "システム設計"
order: 2
---
API 設計 — REST、gRPC、GraphQL

クライアントとサービスが大規模にデータを交換する方法: **リソース指向 HTTP**、**バイナリ RPC**、**柔軟なクエリ**。

## 1. REST (表現状態転送)

**REST** はリソースを URL としてモデル化します。 HTTP 動詞は意図を表現します。サーバーは **ステートレス**のままです。セッション状態は、接続ごとのサーバー メモリではなく、トークンまたはクライアント ストレージ内に存在します。

|方法 |パス |セマンティクス |べき等ですか？ |
|----------|------|-----------|---------------|
| **入手** | `/users/{id}` |リソースを読む |はい |
| **投稿** | `/users` |作成 (サーバーが ID を割り当てます) |いいえ |
| **置く** | `/users/{id}` |完全に置き換える |はい |
| **パッチ** | `/users/{id}` |部分更新 |いいえ* |
| **削除** | `/users/{id}` |削除 |はい |

\*PATCH の冪等性はパッチ ドキュメントの設計によって異なります。

**ステータス コード (サブセット)**

|コード |意味 |いつ |
|------|------|------|
| 200 | OK |本文での GET/PUT/PATCH の成功 |
| 201 |作成された |作成したリソースを POST |
| 204 |コンテンツなし |削除成功 |
| 400 |間違ったリクエスト |検証に失敗しました |
| 401 / 403 |認証/禁止 |資格情報が欠落しているか不十分です |
| 404 |見つかりません |不明なリソース ID |
| 409 |紛争 |重複作成、バージョンの衝突 |
| 429 |リクエストが多すぎます |レート制限 |
| 500 |サーバーエラー |処理できない障害 |

### バージョン管理

|戦略 |例 |トレードオフ |
|----------|-----------|----------|
| URL パス | `/v1/users` |明示的;ゲートウェイでの簡単なルーティング |
|ヘッダー | `Accept-Version: 1` |クリーンな URL;キャッシュするのが難しい |
|クエリ | `/users?api-version=1` |パブリック API では珍しい |

**ルール:** バージョン上の既存のクライアントを決して壊さないでください。フィールドを追加し、非推奨にし、その後廃止します。

### ページネーション

|スタイル |クエリ |長所 |短所 |
|------|-------|------|------|
| **オフセット** | `?offset=100&limit=20` |単純な SQL `OFFSET` |ページング中に行が挿入/削除された場合はスキップ/重複します。
| **カーソル** | `?cursor=eyJpZCI6…}&limit=20` |ライブフィードでも安定 |不透明なカーソル。難しい「50ページにジャンプ」 |

カーソルパターン: `WHERE (created_at, id) > (:last_ts, :last_id) ORDER BY created_at, id LIMIT 20`。

<figure class="notes-diagram"><svg xmlns="16 viewBox="0 0 440 120" role="img" aria-label="Offset pagination vs cursor pagination under concurrent inserts">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Offset vs cursor (live feed)</text>
  <text x="12" y="38" fill="#f87171" font-size="9">Offset page 2: row inserted at top → duplicate or skip</text>
  <text x="12" y="54" fill="#86efac" font-size="9">Cursor after id=105 → always next rows by sort key</text>
  <rect x="12" y="64" width="48" height="20" rx="2" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="22" y="78" fill="#e4e4e7" font-size="8">new</text>
  <rect x="64" y="64" width="48" height="20" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="78" y="78" fill="#e4e4e7" font-size="8">101</text>
  <rect x="116" y="64" width="48" height="20" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="130" y="78" fill="#e4e4e7" font-size="8">102</text>
  <text x="180" y="78" fill="#fbbf24" font-size="9">← cursor "after 102"</text>
</svg></figure>

## 2.gRPC

**gRPC** は、**HTTP/2** 上で **プロトコル バッファ** を使用します: バイナリ、型付きコントラクト、ストリーミング。

|特集 | REST/JSON | gRPC |
|----------|-----------|------|
|ペイロード |テキスト JSON |バイナリ プロトバッファ |
|契約 | OpenAPI (オプション) | `.proto` 必須 |
|ストリーミング |珍しい |ネイティブ (サーバー/クライアント/BIDI) |
|ブラウザ |ネイティブ | grpc-web プロキシが必要 |
|こんな方に最適 |パブリック HTTP API |内部サービスメッシュ |

**ストリーミング モード**

|モード |使用例 |
|------|----------|
|単項 |単一のリクエスト → 単一の応答 |
|サーバーストリーミング |大量のダウンロード、ライブアップデート |
|クライアントストリーミング |バッチをアップロード |
|双方向 |チャット、共同編集 |

```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);
}
```

## 3. GraphQL

クライアントは、正確な応答形状を記述する 1 つの **クエリ**を送信します。

|長所 |短所 |
|------|------|
|フィールドのオーバーフェッチはありません |リゾルバーがナイーブな場合は **N+1** クエリ |
|関連データ1往復 | REST URL よりもキャッシュが難しい |
|スキーマによる強力な型指定 |複雑さの制限、深層攻撃 |

**N+1 修正:** **DataLoader** バッチ `userIds` → 1 つ `SELECT WHERE id IN (…)`。

## 4. API スタイルの選択

|シナリオ |優先する |
|----------|----------|
|パブリックモバイル/Web REST エコシステム | **REST** + OpenAPI |
|内部マイクロサービス、低遅延 | **gRPC** |
|複数のクライアント、さまざまな分野のニーズ | **グラフQL** |
|ファイルのアップロード、単純な CRUD | **休憩** |

## 5. 横断的な API に関する懸念

- POST (支払い) の **Idempotency-Key** ヘッダー - 安全な再試行。
- **Correlation-Id** / トレース ヘッダー — サービス全体での可観測性。
- **HATEOAS** — オプション。発見可能性への応答におけるハイパーメディア リンク。

**関連:** [レート制限](iv-rate-limiting.md) (429)、[分散トランザクション](vii-distributed-transactions.md) (冪等性)。
