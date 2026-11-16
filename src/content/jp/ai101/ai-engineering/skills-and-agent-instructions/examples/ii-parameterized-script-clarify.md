---
label: "II"
subtitle: "パラメータ化されたスクリプト + 明確化"
group: "Skills examples"
order: 2
---
パラメータ化されたスクリプト + 明確化

**目標:** **パラメータ**を使用してスクリプトを実行します(`environment`、`dry_run`、など）。ユーザーが十分な情報を提供しなかった場合、エージェントは実行前に欠落値を**確認し、**意図を確認**します。スクリプトは実行時間と結果を JSON に **ログ**します。

## ライブ ファイル (コピー準備完了)

|ファイル |パス |
|------|------|
|スキルの説明 | [`.cursor/skills/deploy-check/SKILL.md`](.cursor/skills/deploy-check/SKILL.md) |
|スクリプト | [`.cursor/skills/deploy-check/scripts/deploy_check.py`](.cursor/skills/deploy-check/scripts/deploy_check.py) |
|ロギングヘルパー | [`.cursor/skills/deploy-check/scripts/lib/run_log.py`](.cursor/skills/deploy-check/scripts/lib/run_log.py) |

[ をすべてコピーします`.cursor/`](.cursor/README.md) をプロジェクトへ — パスはすでに使用されています`.cursor/skills/...`。

## フォルダーのレイアウト

```text
.cursor/skills/deploy-check/
  SKILL.md
  scripts/
    lib/run_log.py
    deploy_check.py
  logs/                    ← gitignore; created at runtime
```

## スキルがエージェントに教えること

から [`SKILL.md`](.cursor/skills/deploy-check/SKILL.md):

1. **質問**`environment`がありません (`staging`|`production`）。
2. 実行前に**確認**してください (特に運用環境の場合)。
3. **実行**`python3 .cursor/skills/deploy-check/scripts/deploy_check.py …`4. 以下の JSON ログを **読んでください**`logs/`そして要約します`duration_ms`、`exit_code`、`messages`。

## エージェントの流れ

```text
User: "check if we're ready to deploy"
  → Skill loads
  → Agent: missing environment → asks user
  → Agent: restates command → user confirms
  → Agent runs script via Shell
  → Script writes logs/run-….json
  → Agent reads log → reports results
```

＃＃ テスト

プロジェクトにコピーした後、次のようにします。

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

新しいエージェント チャット: *「デプロイ チェックの実行」* — エージェントは実行前に環境を尋ねる必要があります。

＃＃ 次

[スクリプト結果のループ](iii-loop-on-script-results.md) - 繰り返しにわたってログ データを再利用します。
