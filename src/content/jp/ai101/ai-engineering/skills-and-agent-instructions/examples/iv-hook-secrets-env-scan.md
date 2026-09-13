---
label: "IV"
subtitle: "フック — シークレットと環境スキャン"
group: "Skills examples"
order: 4
---
フック — 秘密と`.env`スキャン

**目標:** シェルが実行される前に **フック** で実行される **ボット**`git commit`— そして暴露された秘密をスキャンします。`.env`ファイルはステージングされ、API キーは diff にあります。 **ログ**を書き込みます。次の場合にアクションを**ブロック**できます`failClosed`が設定されています。

フックは **自動的に** 実行されます。ユーザーが要求するとスキルが実行されます。 [修正されたスクリプトのリンク](../../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script）。

## ライブ ファイル (コピー準備完了)

|ファイル |パス |
|------|------|
|フック構成 | [`.cursor/hooks.json`](.cursor/hooks.json) |
|フックスクリプト | [`.cursor/hooks/secrets_scan.py`](.cursor/hooks/secrets_scan.py) |
|スキャンロジック | [`.cursor/hooks/lib/scan_staged_secrets.py`](.cursor/hooks/lib/scan_staged_secrets.py) |
| CLI | 事前コミット[`.cursor/hooks/lib/scan_staged_secrets_cli.py`](.cursor/hooks/lib/scan_staged_secrets_cli.py) |
|ヘルプスキル | [`.cursor/skills/secrets-scan-help/SKILL.md`](.cursor/skills/secrets-scan-help/SKILL.md) |

[ をすべてコピーします`.cursor/`](.cursor/README.md) をプロジェクトのルートに追加します。

## フォルダーのレイアウト

```text
.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
    logs/
```

## フック構成

見る [`.cursor/hooks.json`](.cursor/hooks.json) —`beforeShellExecution`の上`git\s+commit`、`failClosed: true`。

手動でテストします。

```bash
echo '{"command":"git commit -m test"}' | python3 .cursor/hooks/secrets_scan.py
```

## オプション: git 事前コミット

```bash
chmod +x .cursor/hooks/lib/scan_staged_secrets_cli.py
# .git/hooks/pre-commit → exec python3 .cursor/hooks/lib/scan_staged_secrets_cli.py
```

## エージェント/ユーザー フロー

```text
User or agent: git commit -m "…"
  → beforeShellExecution fires
  → secrets_scan.py runs → writes log
  → exit 2 → commit blocked (if failClosed)
  → secrets-scan-help skill → read log → suggest fixes
```

＃＃ 次

[パフォーマンスとボトルネック](v-performance-bottleneck-scan.md) — オンデマンド プロファイリング スキル。
