---
label: "II"
subtitle: "スタックと足場を選択してください"
group: "How to create your custom MCP"
order: 2
---
スタックと足場を選択してください

**TypeScript** または **Python** を選択します。どちらにも公式の MCP SDK があります。すでに Node を使用しているほとんどの IDE チームの場合、**TypeScript** は Cursor の例と一致します。 **Python** は、ロジックが既に Python スクリプトまたはデータ ライブラリに含まれている場合に最も高速です。

## 1. スタックの比較

| | **TypeScript** | **Python (高速MCP)** |
|---|--|-----------|
| **パッケージ** |`@modelcontextprotocol/sdk`|`mcp`(`FastMCP`) |
| **ランタイム** |ノード 18+ | Python 3.10+ |
| **スキーマ** |ゾッド |タイプヒント / Pydantic |
| **最適な時期** | JS/TS モノリポジトリ、npm パブリッシュ |データ/ML スクリプト、FastAPI チーム |
| **Cursor スポーン** |`node dist/index.js`|`python server.py`または`uv run`|

**stdio** トランスポートから開始します。サブプロセスは 1 つで、開いているポートはありません。リモートのチームがホストするサーバーが必要な場合にのみ、後で HTTP を追加します。

## 2. TypeScript スキャフォールド

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --outDir dist --rootDir src
```

**`package.json`** — Cursor の bin エントリを追加します。

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**レイアウト:**

```text
my-mcp-server/
├── src/
│   ├── index.ts       # server entry + transport
│   └── tools/         # one file per domain (issues.ts, users.ts)
├── package.json
└── tsconfig.json
```

## 3. Python 足場

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install mcp
```

**レイアウト:**

```text
my-mcp-server/
├── server.py          # FastMCP entry
├── tools/
│   └── tickets.py     # optional split
├── pyproject.toml     # optional — uv/poetry
└── .venv/
```

**uv** を使用する場合 (再現可能なスポーンに推奨):

```bash
uv init my-mcp-server
uv add mcp
```

## 4. 命名とバージョン管理

|フィールド |ガイダンス |
|------|----------|
| **サーバ`name`** |短いスネークケース ID:`acme-tickets`、 ない`My Cool Server`|
| **バージョン** |サーバー メタデータの Semver — Cursor が起動したビルドのデバッグに役立ちます。
| **ツール名** |動詞+名詞:`search_tickets`、`create_ticket`— リリース間で安定 |

ホストはモデルにツール名を表示します。名前を変更してエージェントの習慣を打ち破ります。ツール名を小さなパブリック API のように扱います。

## 5. 環境と秘密

トークンをハードコーディングしないでください。ホストが渡す環境変数から読み取る`mcp.json`:

```json
"env": {
  "ACME_API_TOKEN": "…",
  "ACME_BASE_URL": "https://api.internal.example"
}
```

コード内:`process.env.ACME_API_TOKEN`(TS) または`os.environ["ACME_API_TOKEN"]`(Python)。必要な変数が欠落している場合、起動時に失敗します。

＃＃ 次

[ツールとリソースを定義する](iii-define-tools-and-resources.md) — ハンドラーを作成する前に、エージェントが呼び出せるものを設計します。
