---
label: "IV"
subtitle: "ツール、リソース、プロンプト"
group: "How to create your custom MCP"
order: 4
---
ツール、リソース、プロンプト

## 1. ツール設計ルール

|ルール |なぜ |
|------|-----|
| **動詞と名** |`create_ticket`、`list_deployments`— LLM の明確な意図 |
| **豊富な説明** |ホストはツールを選択するときに名前と説明を表示します - 「次の場合に使用する」を含める |
| **小さな入力** |好む`id`+`limit`巨大な入れ子になった BLOB 上 |
| **制限された出力** |リスト (上位 10 ～ 50) を切り詰めます。大きなペイロードを要約する |
| **明示的な読み取り/書き込み** |説明: 「読み取り専用」または「レコードを作成します - UI でのユーザー確認が必要です」 |

### 入力の検証

**Zod** (TypeScript) またはタイプ ヒント (FastMCP) を使用して、API 呼び出しの **前** に不正な引数が失敗するようにします。

```typescript
{
  issue_id: z.string().uuid(),
  comment: z.string().max(4000),
  dry_run: z.boolean().optional().default(false),
}
```

検証エラーをツールの結果として返します。`isError: true`そのため、モデルは再試行できます。

## 2. ツール結果の形状

MCP ツールは **content** ブロックを返します (通常はテキスト:)

```typescript
return {
  content: [
    { type: "text", text: "Found 3 open incidents:\n1. ..." },
  ],
};
```

|コンテンツタイプ |使用 |
|--------------|-----|
|`text`|書式設定された文字列としての JSON、人による要約、ログ |
|`image`| Base64 または URL (ホストがサポートしている場合) |
|`resource`|リソースへの参照 URI |

構造化データの場合、**JSON.stringify** をテキストに変換しても問題ありません。モデルは次のターンにそれを解析します。

### モデルで修正できるエラー

```typescript
return {
  content: [{ type: "text", text: "Error: Project 'foo' not found. Use list_projects first." }],
  isError: true,
};
```

運用環境ではスタック トレースを回避します。サーバー側でログを記録し、短いメッセージを返します。

## 3. リソース (オプション)

リソースは、**読み取り可能な** コンテンツを URI によって公開します。これは、Runbook、構成スニペット、キャッシュされたエクスポートに適しています。

TypeScript (概念的):

```typescript
server.resource(
  "runbook://checkout-failures",
  "Runbook for checkout payment failures",
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/markdown",
        text: await loadRunbook("checkout-failures"),
      },
    ],
  }),
);
```

|ツール |リソース |
|------|-----------|
|モデルはパラメータを指定して**呼び出し**します。モデルまたはユーザー **IT0__ による **読み取り** |
|検索、作成、変更 |静的またはゆっくりと変化するドキュメント |

## 4. プロンプト (オプション)

プロンプトは、スラッシュ コマンドなどの引数を備えた **名前付きテンプレート**です。

```typescript
server.prompt(
  "incident-summary",
  { incident_id: z.string() },
  async ({ incident_id }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Summarize incident ${incident_id} using get_incident and list_timeline events.`,
        },
      },
    ],
  }),
);
```

ほとんどのカスタム サーバーは、ツールが安定するまでプロンプトをスキップします。

## 5. 複数の関連ツール — サンプル セット

|ツール |タイプ |説明の抜粋 |
|------|------|----------|
|`list_projects`|読む |ユーザーがアクセスできるプロジェクトのリスト。他のプロジェクト ツールの前に呼び出します。 |
|`get_issue`|読む | ID で 1 つの課題を取得します。 |
|`search_issues`|読む |クエリ文字列で検索します。最大 20 件の結果。 |
|`add_comment`|書く |問題にコメントを追加します — 破壊的です。 |

説明内の順序のヒント (`Call list_projects first`) 複数ステップのエージェントの実行を改善します。

## 6. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
|任意の SQL | を実行する 1 つのツールパラメータ化されたクエリまたは固定レポート ID |
|`run_shell`フルバッシュで |決して、またはサンドボックス内で厳密に許可リストに登録されたコマンドを使用しない |
| 10 MB JSON を返します |ページネーション、サーバー側の要約 |
|大文字と小文字のみが異なるツール名 |ヘビケースにこだわる |

[セキュリティと配布](vi-security-and-distribution.md) および [MCP 対コネクタとセキュリティ](../iv-mcp-vs-connectors-and-security.md）。

＃＃ 次

[テストして Cursor に接続](v-test-and-wire-cursor.md) - IDE でサーバーを実行します。
