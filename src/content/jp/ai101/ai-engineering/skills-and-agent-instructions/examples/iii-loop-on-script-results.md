---
label: "III"
subtitle: "スクリプトの結果をループする"
group: "Skills examples"
order: 3
---
スクリプトの結果をループする

**目標:** スクリプトを実行し、**ログ ファイル**を読み取り、同じデータを**反復**します。毎回最初から再フェッチすることなく、修正や分析を改良します。キープする`current_log_file`会話の中で真実の情報源として。

## ライブ ファイル (コピー準備完了)

|ファイル |パス |
|------|------|
|スキルの説明 | [`.cursor/skills/test-flake-hunt/SKILL.md`](.cursor/skills/test-flake-hunt/SKILL.md) |
|スクリプト | [`.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py`](.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py) |

## フォルダーのレイアウト

```text
.cursor/skills/test-flake-hunt/
  SKILL.md
  scripts/run_flaky_tests.py
  logs/
```

## ループパターン (SKILL.md より)

1. **ラウンド 1** — 実行`python3 .cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py "[pattern]"`2.ストア`current_log_file`スクリプト出力から。
3. **ラウンド 2+** — 同じログを読み取ります。修正を提案する。確認のためのみ再実行してください。
4. **停車**`exit_code == 0`、ユーザー停止、または進行なしの 5 回の反復。

## オプション: Cursor`stop`フック

自動「継続」ループの場合は、`stop`フック付き`loop_limit`— [フック — シークレットスキャン](を参照)iv-hook-secrets-env-scan.md）。スキルのみがループインに従うエージェントに依存します。`SKILL.md`。

## タイイン

[ループプロンプト](../../loop-prompting/i-overview.md) — 各ターンの短いデルタ (「反復 3: 最後のログを読み取り、修正する」`auth.test.ts`”）。

＃＃ 次

[フック — 秘密と`.env`スキャン]（iv-hook-secrets-env-scan.md) — ユーザーの要求なしで自動チェックします。
