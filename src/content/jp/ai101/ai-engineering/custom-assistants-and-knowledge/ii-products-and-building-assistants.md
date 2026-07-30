---
label: "II"
subtitle: "製品と建築アシスタント"
group: "AI Applied"
order: 2
---
製品と建築アシスタント

## 1. 製品の同等品

|製品 |特集 |構成内容 |
|----------|----------|--------|
| **チャットGPT** |カスタム GPT、メモリ (オプション) |手順、ファイル、アクション |
| **クロード** |プロジェクト |プロジェクトの知識 + 指示 |
| **ジェミニ** |宝石 |ペルソナ + オプション ファイル |
| **副操縦士** |コパイロット スタジオ / M365 コパイロット |テナント データ、プラグイン |
| **ノートブックLM** |ノート |ソース → 根拠のある Q&A、オーディオの概要 |
| **Cursor** |ルール、ドキュメントのインデックス |リポジトリ +`.cursor/rules`|

考え方はどこでも同じです: **説明書 + 知識 + (オプションの) ツール**。

＃＃２ 「知識」に何を入れるか

|良い情報源 |情報源が悪い |
|--------------|--------------|
|ポリシー PDF、ハンドブック、FAQ |ランダムな古いエクスポート |
|製品仕様、所有する API ドキュメント |アップロードできない機密情報 |
|会議メモ **あなた**が管理 |フィルタリングされていない電子メール アーカイブ全体 |
|スタイルガイド、ブランドボイス |あなたが権利を持たない競合他社のドキュメント |

**リフレッシュ:** 古い知識 → 自信を持って間違った答え。アップロードの日付を記入します。四半期ごとに交換します。

## 3. 便利なカスタム アシスタントの構築

```text
1. One sentence purpose   ("Answers support tier-1 about Billing v2")
2. Audience               (customers vs internal)
3. Tone & format          (short, links, escalate when …)
4. Boundaries             (no legal advice; no discounts)
5. 3–5 example Q&As       (few-shot in instructions)
6. Knowledge files        (indexed docs)
7. Test with edge cases   (unknown product, angry user, non-English)
```

### 指示テンプレート

```text
Purpose: …
Always: cite doc section; say "I don't know" if not in knowledge.
Never: promise refunds; invent SKU prices.
Format: numbered steps for how-to; table for comparisons.
Escalate: billing disputes → human@company.com
```