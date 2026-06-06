---
label: "Guide"
subtitle: "トピックとフォルダー"
group: "はじめに"
order: 10
---
このメモ リポジトリの使用

フォルダーとメタデータがどのように組み合わされるか、および新しいトピックを追加する方法。

## 1. レイアウト

すべてのメモは **`src/content/`** の下に保存されます。

- **`src/content/_meta.json`** — ライブラリ全体のルート メタデータ (Cursor Notes などの GitHub ベースのビューアで必要)。
- **`src/content/<topic-folder>/`** — サイドバー セクションごとに 1 つのフォルダー (例: `python`、`sysdesign`)。
- **`src/content/<topic-folder>/_meta.json`** — セクションのタイトルとセクション間の並べ替え順序を定義します。
- **`src/content/<topic-folder>/*.md`** — 個別のメモ (Markdown と YAML フロントマター)。
- **`src/content/<topic-folder>/<subfolder>/`** — そのトピックの下の**折りたたみ可能なサブメニュー**のオプションのネストされたフォルダー (各サブフォルダーは独自の **`_meta.json`** および独自の **`.md`** ファイルを取得します)。

フォルダー名は短く、小文字で、ハイフンを付けてください (`Machine Learning` ではなく `machine-learning`)。

### このリポジトリの例

**`getting-started/`** の下の **`intro/`** サブフォルダーは、**インストール** と **セットアップ** を個別のファイルとしてグループ化します。**`getting-started/intro/_meta.json`** と **`i-installation.md`** および **`ii-setup.md`** を参照してください。サブメニューが必要な場所には同じパターンを使用します (`advanced/`、`labs/` など)。

## 2. セクションメタデータ (`_meta.json`)

各 **トピック** フォルダーには、メモの隣 (およびサブフォルダーの隣) に **`_meta.json`** が必要です。

```json
{
  "label": "Human-readable section title",
  "order": 3
}
```

各 **ネストされたサブフォルダ** (サブメニュー) には、同じ形状の独自の **`_meta.json`** もあり、折りたたみ可能なグループをサポートするクライアントでは、**`label`** がサブメニュー タイトルになります。

**`order`** は、兄弟間の配置 (コンテンツ ルートのセクション、または 1 つのトピック内のメモ/サブフォルダー) を制御します。小さい数字が早く表示されます。

## 3. 前付に注意してください

すべての **`.md`** ファイルは **`---`** 行間の YAML で始まります。

```yaml
---
label: "I"
subtitle: "Basics & syntax"
group: "Python"
order: 1
---
```

|フィールド |目的 |
|--------|--------|
| **`label`** |注文または番号付けのための短いマーカー (ローマ数字、「ガイド」など)。ファイル名の先頭で使用されます (下記を参照)。 |
| **`subtitle`** |セクション内のピースを区別します。ファイル名の一部になります。メモが単一の特別なページである場合にのみ省略します (メモリ推定の例を参照)。 |
| **`group`** |グループ化/カリキュラム名を表示します。通常、トピックのテーマと一致します (そのトピック内のノート間で同じ文字列が問題ありません)。 |
| **`order`** |このメモの **フォルダー内** (または、ビューアーの並べ替え方法に応じてそのグループ内) の並べ替え順序。 |

オプションのキー (すでに他の場所で使用している場合のみ): 例: **`groupOrder`**。

最後の **`---`** の後に、通常どおり Markdown でタイトル行と本文を記述します。

## 4. ファイルの命名

ファイル名は次のとおりです。

**ケバブケース**の**`{label}-{subtitle-slug}.md`** (小文字、スペースと句読点 → ハイフン、**`&`** → **`and`**)。

例:

- ラベル **`I`**、サブタイトル **`ML Foundations`** → **`i-ml-foundations.md`**
- ラベル **`III`**、サブタイトル **`Beans & dependency injection`** → **`iii-beans-and-dependency-injection.md`**

**`subtitle` がない**場合は、**`{label-slug}.md`** のみを使用してください (例: **`memory-estimator.md`**)。

ブックマークや外部リンクが GitHub パスを指している場合は、ファイル名を不用意に変更しないでください。名前を変更する場合は **`git mv`** を優先してください。

## 5. 新しいトピック (チェックリスト) の追加

1. **`src/content/<your-topic>/`** を作成します。
2. **`src/content/<your-topic>/_meta.json`** と **`label`** および **`order`** を追加します。
3. フロントマター **`label`**、**`subtitle`** (単一ラベルの例外が適用される場合を除く)、**`group`**、**`order`**、および上記のルールから作成されたファイル名を含む 1 つ以上の **`.md`** ファイルを追加します。
4. オプション: **`src/content/<your-topic>/<subfolder>/`** と独自の **`_meta.json`** を追加し、関連する **`.md`** ファイルをそのサブフォルダー内に配置します (同じフロントマターと命名規則)。
5. **`main`** をコミットしてプッシュします (このリポジトリは **`master`** ではなく **`main`** を使用します)。

## 6. カーソルメモ / GitHub 設定

これらのメモをカーソルの GitHub からロードするには:

1. Notes UI (メニュー) から **GitHub** 設定を開きます。
2. **所有者/リポジトリ** を GitHub リポジトリに設定します。
3. **ブランチ** を **`main`** (またはプッシュ先のブランチ) に設定します。
4. **コンテンツ パス**を **`src/content`** に設定し、ルート **`_meta.json`** とすべてのトピック フォルダーが正しく解決されるようにします。
5. リポジトリがプライベートの場合は、リポジトリへのアクセス権を持つトークンを使用します。

フォルダー名またはファイル名を変更した後、クライアントがツリーを再取得できるように更新または同期します。

## 7. クイック テンプレート (トピック + ネストされたイントロ サブメニュー)

新しいトピック **`_meta.json`** **`robotics`**:

```json
{
  "label": "Robotics",
  "order": 10
}
```

**`src/content/robotics/i-overview.md`**:

```yaml
---
label: "I"
subtitle: "Overview"
group: "Robotics"
order: 1
---
Robotics — Part I: Overview

Your intro paragraph and sections follow here.
```

ロボット工学の下の **ネストされたサブメニュー**:

```text
src/content/robotics/intro/_meta.json
src/content/robotics/intro/i-installation.md
src/content/robotics/intro/ii-setup.md
```

**`intro/_meta.json`**:

```json
{
  "label": "Intro",
  "order": 1
}
```

これは、このリポジトリ内での **`getting-started/intro/`** のレイアウトと一致します。

## 8. ノート間の相互リンク

読者にこのリポジトリ内の別のメモを参照させる場合は、**相対パス** (裸のバックティック ファイル名ではなく) を含む **マークダウン リンク**を使用してください。

|する |しないでください |
|----|--------|
| `[Networking, VPC & LB](../foundations/vi-networking-vpc-and-lb.md)` | `` `vi-networking-vpc-and-lb.md` `` |
| `[Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)` | `` `../security-and-best-practices/iii-secrets-and-oidc.md` `` |

**リンク テキスト:** フロントマターのターゲット ノートの **`subtitle`** を使用します (例: 「ネットワーク、VPC & LB」)。サブタイトルがない場合は、ファイル名から人の短いタイトルを使用します。

**同じサブメニュー** — ファイル名のみで問題ありません。

```markdown
**Related:** [HA & disaster recovery](vii-ha-and-disaster-recovery.md)
```

**別のサブメニューまたはトピック** — パスを含めます。

```markdown
See [Docker in CI](../../cicd/tools-and-platforms/v-docker-in-ci.md).
```

**散文のサブメニュー名** — サイドバーのラベルは太字のままにします。概要または特定のメモへのリンク:

```markdown
**Patterns & design** submenu — start at [Overview](../patterns-and-design/i-overview.md).
```

**外部 URL** — 通常のマークダウン リンク (`[Rust Book](https://doc.rust-lang.org/book/)`)。

**このガイドのメタ例 (命名規則として示されているファイル名)、外部リポジトリの `README.md`、またはまだ存在しないメモにはリンクしないでください。

一括編集後にリンクを再適用するには、次を実行します。

```text
python scripts/linkify-content-refs.py
```
