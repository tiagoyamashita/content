---
label: "I"
subtitle: "概要"
group: "Skills examples"
order: 1
---
スキルの例 - 概要

スキル、スクリプト、フックの 4 つの **コピー＆ペースト パターン**。すべての例には次のものが含まれます。

-A **`scripts/`** Python ファイル (実際のコード - 内部にはありません)`SKILL.md`)
- **構造化されたランタイム ログ** (タイムスタンプ、期間、終了コード、結果) (stdlib 経由)`json`モジュール
- **ログ出力の処理方法**に関するエージェントへの指示

スクリプトはマークダウンに埋め込まれません**。[スクリプトが存在する場所](を参照)../i-overview.md#where-scripts-live-not-inside-the-md）。

実行可能なファイルは **[ の下にあります`.cursor/`](.cursor/README.md)** — そのフォルダーをプロジェクトのルートにコピーします ([プロジェクトにコピー](を参照)#copy-to-your-project））。

## プロジェクトにコピーする

```bash
cd src/content/en/ai101/ai-engineering/skills-and-agent-instructions/examples
chmod +x scripts/copy-to-project.sh
./scripts/copy-to-project.sh /path/to/your-project
```

または手動でコピーします。`examples/.cursor/skills/`、`examples/.cursor/hooks/`、 そして`examples/.cursor/hooks.json`→ あなたのレポ`.cursor/`。パスの編集は必要ありません —`SKILL.md`ファイルはすでに使用されています`.cursor/...`。

煙テスト:

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

## なぜ Python (bash ではない) なのか

| | **Python** | **バッシュ** |
|---|-----------|----------|
| JSON ログ |`json.dump`- いいえ`jq`|ヒアドキュメント + バグのエスケープ |
|引数 |`argparse`|マニュアル`case`/`getopts`|
|差分の解析、AST、perf |`re`、`pathlib`、`ast`|壊れやすい`grep`/`awk`|
|フック | stdin JSON を読み取り、dict を返します。同じですが、間違いやすいです |
|デプス |これらの例では **stdlib のみ**頻繁に必要となる`jq`、`curl`|

**Python 3.10+** を使用してください。以下の例では pip パッケージは必要ありません。

## 例のマップ

|例 |パターン |トリガー |
|----------|----------|----------|
| [パラメータ化されたスクリプト + 明確にする](ii-parameterized-script-clarify.md) |引数を渡します。行方不明かどうかを尋ねます。意図を確認する |スキル (ユーザーがツールの実行を要求) |
| [スクリプト結果のループ](iii-loop-on-script-results.md) |同じログ データを再利用します。反復全体で絞り込む |スキル + エージェント ループ |
| [フック — 秘密と`.env`スキャン]（iv-hook-secrets-env-scan.md) |コミット/シェルの前にブロックまたは警告 | Cursor フック |
| [パフォーマンスとボトルネック](v-performance-bottleneck-scan.md) |プロファイル/スキャン;ログの調査結果 |スキル |

## 共有ログヘルパー

[で実装されました。`.cursor/skills/deploy-check/scripts/lib/run_log.py`](.cursor/skills/deploy-check/scripts/lib/run_log.py) (各スキルにコピーされます)`scripts/lib/`）。同じモジュール`test-flake-hunt`そして`perf-scan`。

## 共有ログ形状

```text
.cursor/skills/<skill-name>/logs/
  run-20260710T120301Z.json
.cursor/hooks/logs/
  secrets-scan-20260710T120405Z.json
```

```json
{
  "script": "deploy_check.py",
  "started_at": "2026-07-10T12:03:01Z",
  "finished_at": "2026-07-10T12:03:04Z",
  "duration_ms": 3120,
  "exit_code": 0,
  "parameters": { "environment": "staging", "dry_run": true },
  "results": { "checks_failed": 0 },
  "messages": ["Health OK"],
  "log_file": ".cursor/skills/deploy-check/logs/run-20260710T120301Z.json"
}
```

追加`logs/`に`.gitignore`実行がローカルのみの場合。一時的なログ ファイルではなく、**script** と **SKILL.md** をコミットします。

## スキルとフック (どちらの例をコピーするか)

|必要 |コピー |
|------|------|
|ユーザーがワークフローを呼び出します。パラメータが必要な場合があります | [パラメータ化されたスクリプト + 明確にする](ii-parameterized-script-clarify.md) |
|十分な結果が得られるまで、同じスクリプト出力を繰り返します。 [スクリプト結果のループ](iii-loop-on-script-results.md) |
|コミット/git/シェルの自動チェック | [フック — 秘密のスキャン](iv-hook-secrets-env-scan.md) |
|オンデマンドのパフォーマンス レビュー | [パフォーマンススキャン](v-performance-bottleneck-scan.md) |

## 勉強の順番

[パラメータ化されたスクリプト + 明確にする](ii-parameterized-script-clarify.md) 最初に (パラメータ + ログ)、次に [スクリプト結果のループ](iii-loop-on-script-results.md）。 [フック — シークレット スキャン](iv-hook-secrets-env-scan.md) **自動**ゲートが必要な場合。

＃＃ 関連している

- [スキル、エージェント、フックの使用](../using-skills-agents-and-hooks/i-overview.md) — 各レイヤーを個別に使用する場合
- [修正スクリプトのリンク](../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script)
- [ループプロンプト](../../loop-prompting/i-overview.md)
- [MCP の仕組み](../../how-mcp-works/i-overview.md) — ライブデータと静的スクリプト
