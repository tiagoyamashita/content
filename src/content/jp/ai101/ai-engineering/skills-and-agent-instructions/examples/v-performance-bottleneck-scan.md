---
label: "V"
subtitle: "パフォーマンスとボトルネック"
group: "Skills examples"
order: 5
---
パフォーマンスとボトルネック

**目標:** **パフォーマンスの問題** (大きなファイル、同期 I/O ヒューリスティック、オプションの HTTP タイミング) をスキャンし、エージェントが要約して修正を提案するために **実行時間と結果** をログに記録する **スキルでトリガーされる** ボット。

## ライブ ファイル (コピー準備完了)

|ファイル |パス |
|------|------|
|スキルの説明 | [`.cursor/skills/perf-scan/SKILL.md`](.cursor/skills/perf-scan/SKILL.md) |
|スクリプト | [`.cursor/skills/perf-scan/scripts/perf_scan.py`](.cursor/skills/perf-scan/scripts/perf_scan.py) |

## フォルダーのレイアウト

```text
.cursor/skills/perf-scan/
  SKILL.md
  scripts/perf_scan.py
  logs/
```

＃＃ 走る

```bash
PERF_URL="${PERF_URL:-}" python3 .cursor/skills/perf-scan/scripts/perf_scan.py "."
```

エージェントのフロー: 範囲を尋ねる → 確認 → 実行 → ログを読み取る → 結果の上位 3 つに優先順位を付けます。

## ループの例と組み合わせる

[スクリプト結果のループ](iii-loop-on-script-results.md) - ベースラインログ、修正、再実行、比較`findings_count`。

＃＃ 関連している

- [パラメータ化されたスクリプト + 明確にする](ii-parameterized-script-clarify.md)
- [例の概要](i-overview.md）
