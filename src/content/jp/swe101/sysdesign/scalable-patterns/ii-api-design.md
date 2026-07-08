---
label: "II"
subtitle: "API デザイン"
group: "システム設計"
order: 2
---
API 設計 — REST、gRPC、GraphQL

クライアントとサービスが大規模にデータを交換する方法: **リソース指向 HTTP**、**バイナリ RPC**、**柔軟なクエリ**。

## 1. REST (表現状態の転送)

**REST** はリソースを URL としてモデル化します。 HTTP 動詞は意図を表現します。サーバーは **ステートレス**のままです。セッション状態は、接続ごとのサーバー メモリではなく、トークンまたはクライアント ストレージ内に存在します。

| Method | Path | Semantics | Idempotent? |
|--------|------|-----------|-------------|
| **GET** | `/users/{id}` | Read resource | Yes |
| **POST** | `/users` | Create (server assigns id) | No |
| **PUT** | `/users/{id}` | Full replace | Yes |
| **PATCH** | `/users/{id}` | Partial update | No* |
| **DELETE** | `/users/{id}` | Remove | Yes |

\*PATCH 冪等性はパッチ ドキュメントの設計によって異なります。

**ステータス コード (サブセット)**

|コード |意味 |いつ |
|------|------|------|
| 200 | OK | GET/PUT/PATCH 本体で成功 |
| 201 |作成された | POST がリソースを作成しました |
| 204 |コンテンツなし | DELETE 成功 |
| 400 |間違ったリクエスト |検証に失敗しました |
| 401 / 403 |認証/禁止 |資格情報が欠落しているか不十分です |
| 404 |見つかりません |不明なリソース ID |
| 409 |紛争 |重複作成、バージョンの衝突 |
| 429 |リクエストが多すぎます |レート制限 |
| 500 |サーバーエラー |処理できない障害 |

### バージョン管理

| Strategy | Example | Trade-off |
|----------|---------|-----------|
| URL path | `/v1/users` | Explicit; easy routing at gateway |
| Header | `Accept-Version: 1` | Clean URLs; harder to cache |
| Query | `/users?api-version=1` | Rare in public APIs |

**ルール:** バージョン上の既存のクライアントを決して壊さないでください。フィールドを追加し、非推奨にし、その後廃止します。

### ページネーション

| Style | Query | Pros | Cons |
|-------|-------|------|------|
| **Offset** | `?offset=100&limit=20` | Simple SQL `OFFSET` | Skips/dupes if rows inserted/deleted while paging |
| **Cursor** | `?cursor=eyJpZCI6…}&limit=20` | Stable under live feeds | Opaque cursor; harder “jump to page 50” |

Cursor pattern: `WHERE (created_at, id) > (:last_ts, :last_id) ORDER BY created_at, id LIMIT 20`.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="Offset pagination vs cursor pagination under concurrent inserts">
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

**gRPC** は、**HTTP/2** 上で **プロトコル バッファ** を使用します: バイナリ、型指定されたコントラクト、ストリーミング。

| Feature | REST/JSON | gRPC |
|---------|-----------|------|
| Payload | Text JSON | Binary protobuf |
| Contract | OpenAPI (optional) | `.proto` required |
| Streaming | Uncommon | Native (server/client/bidi) |
| Browser | Native | Needs grpc-web proxy |
| Best for | Public HTTP APIs | Internal service mesh |

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
|フィールドのオーバーフェッチはありません | **N+1** リゾルバーがナイーブかどうかをクエリします。
|関連データ1往復 | REST URL よりもキャッシュが難しい |
|スキーマによる強力な型指定 |複雑さの制限、深層攻撃 |

**N+1 fix:** **DataLoader** batches `userIds` → one `SELECT WHERE id IN (…)`.

## 4. API スタイルの選択

|シナリオ |優先する |
|----------|----------|
|パブリックモバイル/Web REST エコシステム | **REST** + オープンAPI |
|内部マイクロサービス、低遅延 | **gRPC** |
|複数のクライアント、さまざまな分野のニーズ | **GraphQL** |
|ファイルのアップロード、簡単な CRUD | **REST** |

## 5. 横断的な API の懸念事項

- POST (支払い) の **Idempotency-Key** ヘッダー - 安全な再試行。
- **Correlation-Id** / トレース ヘッダー — サービス全体での可観測性。
- **HATEOAS** — オプション。発見可能性への応答におけるハイパーメディア リンク。

**Related:** [Rate limiting](iv-rate-limiting.md) (429), [Distributed transactions](vii-distributed-transactions.md) (idempotency).
