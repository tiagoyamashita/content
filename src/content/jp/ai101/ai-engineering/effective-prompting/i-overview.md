---
label: "I"
subtitle: "概要"
group: "AI Applied"
order: 1
---
効果的なプロンプト — 概要
**効果的なプロンプト**について詳しく説明します。以下で焦点を絞ったメモに分割します。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [最低限のプロンプトとテクニック](ii-minimum-prompt-and-techniques.md) |効果的なプロンプトトラックの一部 |
| [イテレーションとテンプレート](iii-iteration-and-templates.md) |効果的なプロンプトトラックの一部 |
| [システムの指示と間違い](iv-system-instructions-and-mistakes.md) |効果的なプロンプトトラックの一部 |

効果的なプロンプト
**プロンプト** は、ChatGPT、Claude、Gemini、および同様のツールを操作する方法です。モデルを「プログラミング」しているわけではありません。**タスクを指定している**ので、5 回の再試行ではなく、1 回だけ役立つ十分なコンテキストがモデルに与えられます。

API レベルの詳細 (ロール、JSON モード) については、[LLM プロンプト エンジニアリング](../../llms/iv-prompt-engineering.md）。このメモは**日常使用**用です。

```mermaid
flowchart LR
  Role[Role] --> Task --> Constraints --> Format[Output format]
  Format --> Model[Model reply]
```

プロンプトが繰り返し動作したら、それを永続的な命令にプロモートします。[ループ プロンプト]( を参照)../loop-prompting/i-overview.md）。

## 勉強の順番

[最低限のプロンプトとテクニック](ii-minimum-prompt-and-techniques.md) → [反復とテンプレート](iii-iteration-and-templates.md) → [システムの指示と間違い](iv-system-instructions-and-mistakes.md) → [ループプロンプト](../loop-prompting/i-overview.md)
