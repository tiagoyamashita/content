---
label: "VI"
subtitle: "セキュリティと配布"
group: "How to create your custom MCP"
order: 6
---
セキュリティと配布

カスタム MCP サーバーは、入力した資格情報に関係なく **ユーザーのマシン**上で実行されます`env`。生産衛生を備えた小規模なサービスのようにそれらを扱います。

## 1. セキュリティチェックリスト

|リスク |緩和 |
|------|-----------|
| **漏洩したAPIキー**`mcp.json`| OS シークレット ストアの env を使用します。`.gitignore`ローカルオーバーライド。コミットされた構成内でのみドキュメントのプレースホルダー |
| **圧倒的なトークン** |スコープ付き API キー (読み取り専用 CRM、単一 GitHub リポジトリ) |
| **即時注入 → ツールの乱用** |狭いツール。任意のコードが実行されることはありません。 UI への書き込みを確認します ([信頼して検証](../../trust-privacy-and-verify/i-overview.md)) |
| **パストラバーサル** |ファイルを読み取る場合は、パスを正規化し、ホワイトリストに登録されたルートにジェイルします。
| **SSRF** |ユーザーの URL をサーバー側に直接渡さないでください`fetch`ホワイトリストなし |
| **シークレットのロギング** | stderr ログ内のトークンを編集する |

MCP は権限を追加しません。API トークンは依然として、アップストリームの API が許可することのみを実行します。

## 2. 最小権限のツール

|パターン |例 |
|----------|----------|
|個別の読み取りツールと書き込みツール |`get_order`対`cancel_order`— 信頼性の低いコンテキストで書き込みサーバーを無効にする |
|許可リストに登録されたアクション |`rerun_job`ジョブ ID が一致する場合のみ`^ci-\d+$`|
|レート制限 |スロットルコストの高い API 呼び出しがサーバー側 |

## 3. リポジトリの README テンプレート

```markdown
# my-mcp-server

MCP server for [system]. Exposes tools: `list_x`, `get_x`, `create_x`.

## Env vars

| Variable | Required | Description |
|----------|----------|-------------|
| CRM_API_KEY | yes | Read-only CRM token |

## Cursor

Add to `.cursor/mcp.json` (see docs).

## Development

npm run build && npx @modelcontextprotocol/inspector node dist/index.js
```

## 4. 配布オプション

|方法 |観客 |
|----------|----------|
| **Git リポジトリ +`mcp.json`スニペット** |社内チーム |
| **npm**`npx -y @yourorg/my-mcp-server`| TS サーバー — 公式 MCP パッケージと同じパターン |
| **ピップ** +`uvx`| Python FastMCP パッケージ |
| **単一バイナリ** (Go/Rust) |エアギャップがあるか、ホスト上にノード/Python がありません |

で公開されたパッケージの例`mcp.json`:

```json
{
  "mcpServers": {
    "crm": {
      "command": "npx",
      "args": ["-y", "@yourorg/crm-mcp-server"],
      "env": { "CRM_API_KEY": "..." }
    }
  }
}
```

## 5. バージョン管理と重大な変更

|変更 |練習 |
|----------|----------|
|名前変更ツール |メジャーバージョンのバンプ。ドキュメントの移行 |
|オプションのフィールドを追加 |マイナー - 下位互換性 |
|ツールを削除 |選考科目;サーバー起動ログで警告 |

## 6. MCP とスキル — いつどちらを追加するか

|レイヤー |ホールド |
|------|------|
| **MCP サーバー** |ライブ データ、認証された API、突然変異 |
| **スキル** |チームがエージェントにこれらのツール ([スキル]() をどのように使用してもらいたいか../../skills-and-agent-instructions/i-overview.md)) |

例: MCP が公開する`search_logs`;スキルには「常にフィルターする」というものがあります。`env=prod`ユーザーが別途指定しない限り、最後の 1 時間。」

## 7. 運用監視

|信号 |アクション |
|----------|----------|
|ツールの遅延 |標準エラー出力へのログ期間。 p95 の警告 |
| API 401/403 |エラー テキストをクリア — 「CRM_API_KEY を回転」 |
|起動時にクラッシュする | CI モック環境に対してヘッドレスで Inspector を実行するジョブ |

＃＃ 関連している

- [MCP の仕組み](../i-overview.md)
- [JSON-RPC & トランスポート](../ii-json-rpc-and-transports.md)
- [MCP 対コネクタとセキュリティ](../iv-mcp-vs-connectors-and-security.md)
- [エージェントと MCP の配線](../../agents-and-agentic-workflows/ii-chat-assistant-agent.md)
