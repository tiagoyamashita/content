---
label: "V"
subtitle: "私のセットアップ"
group: "AI Applied"
order: 5
---
私のセットアップ — マルチエージェント Cursor ワークフロー
**Cursor エージェント**を毎日どのように実行しているか: 1 つのチャットが **グローバル ルール**を所有し、他のチャットが **リポジトリ作業**を行い、複数のエージェントが同じコードベースに触れるときの **並行作業**を安全に保ちます。

これは個人の運用モデルであり、製品要件ではありません。関連: [監督エージェント](iii-directing-agents.md)、[Cursor スキル、ルール & AGENTS.md](../skills-and-agent-instructions/iv-cursor-skills-rules-agents-md.md)、[エージェント オーケストレーション](../skills-and-agent-instructions/using-skills-agents-and-hooks/vi-agent-orchestration.md）。

## 1. 役割の概要

|エージェントチャット |所有 |所有していない |
|-----------|------|--------------|
| **ルールエージェント** |ユーザー ルール、グローバルな習慣、リポジトリ間の規則 |製品リポジトリの機能 PR |
| **レポエージェント** |それぞれ 1 つ (またはいくつか) の git リモート/ワークツリー |グローバル ルール セットを「作業中に」編集する |
| **私** |決定をマージします。チャットが書き込みを許可される |すべてのツール呼び出しを盲目的に信頼する |

```mermaid
flowchart TB
  Me[You]
  Rules[Rules agent chat]
  A[Agent — repo A]
  B[Agent — repo B]
  C[Agent — repo C]

  Me -->|change global / user rules| Rules
  Me -->|feature / fix / PR| A
  Me -->|feature / fix / PR| B
  Me -->|feature / fix / PR| C

  Rules -->|writes| GR[User rules / global skills]
  A -->|writes| RA[Repo A worktree]
  B -->|writes| RB[Repo B worktree]
  C -->|writes| RC[Repo C worktree]

  GR -.->|loaded by| A
  GR -.->|loaded by| B
  GR -.->|loaded by| C
```

**ルール:** ルール エージェントは **すべてのエージェントの動作**を変更します。リポジトリ エージェントが **コード**を変更します。 1 つのチャットにこれらのジョブを混在させると、予期せぬ差分や中途半端なルール編集が発生します。

## 2. ルールエージェント (グローバル)

唯一の役割が指示領域である **専用チャット** (多くの場合、スクラッチ ワークスペースやメモ ワークスペース) を使用します。

|レイヤー |典型的な場所 |範囲 |
|------|------|------|
| **ユーザールール** | Cursor ユーザー ルール (アカウント/設定) |すべてのプロジェクト |
| **ユーザースキル** |`~/.cursor/skills/`|すべてのプロジェクト |
| **ユーザーフック** |ユーザーレベルのフック (使用する場合) |すべてのプロジェクト |
| **チームルール** |そのリポジトリを明示的に開いた場合のみ |そのリモコン |

Rules エージェントのプロンプト パターン:

```text
You only edit global / user-level Cursor rules and skills.
Do not change application code in product repos.
Propose the rule text, show before/after, wait for my OK, then apply.
```

```mermaid
sequenceDiagram
  actor You
  participant Rules as Rules agent
  participant Cursor as Cursor settings / ~/.cursor
  participant Repo as Any repo agent later

  You->>Rules: "Always use HEREDOC for commit messages"
  Rules->>You: Draft rule + impact
  You->>Rules: Approve
  Rules->>Cursor: Update user rule / skill
  Note over Repo: Next sessions load the new rule
  You->>Repo: "Ship feature X"
  Repo->>Repo: Follows updated global rule
```

ルール チャット (または個人的なメモ) に短い **変更ログ** を記録してください: 日付、変更内容、理由 - これにより、不適切なグローバル指示をロールバックできます。

## 3. リポジトリエージェント (異なるリモート)

**アクティブなリポジトリごとに 1 つのエージェント チャット** (またはエピックごと) をスピンします。編集を要求する前に、ワークスペースのルートがそのクローンを指すようにしてください。

```mermaid
flowchart LR
  subgraph Session1[Chat 1]
    W1[Workspace: ~/Git/content]
  end
  subgraph Session2[Chat 2]
    W2[Workspace: ~/Git/notes-app]
  end
  subgraph Session3[Chat 3]
    W3[Workspace: ~/Git/infra]
  end

  Session1 --> R1[(origin content)]
  Session2 --> R2[(origin notes-app)]
  Session3 --> R3[(origin infra)]
```

|練習 |なぜ |
|----------|-----|
| **チャットにリポジトリ/チケットの名前を付けます** |文脈のにじみが少なくなる |
| **可能な場合、エージェントごとに 1 つのブランチ** |よりクリーンな PR |
| **ルートを移動できる場合は、エージェントにリポジトリ パスを伝えます** |間違ったツリーを編集しないようにする |
| **チャット B に「グローバル ルールも修正してください」と依頼しないでください** |それがルールエージェントの仕事です |

## 4. 同じリポジトリ、同じ時間

同じファイルをめぐって競合しない限り、**1 つのリモート**上に複数のエージェントが存在しても問題ありません。 **git worktree** (または個別のクローン) を使用して、各チャットが独自のチェックアウトとブランチを持つようにします。

```mermaid
flowchart TB
  Remote[(remote: org/app)]
  Main["main clone — Chat A — feat/auth"]
  WT["worktree — Chat B — feat/billing"]

  Remote --> Main
  Remote --> WT

  Main -->|"PR 1"| Remote
  WT -->|"PR 2"| Remote
```

### 調整チェックリスト

|リスク |緩和 |
|------|-----------|
| 2 人のエージェントが同じファイルを編集する |ディレクトリ/所有権ごとに分割。またはシリアル化する |
|両方とも 1 つのブランチにコミットします。 **エージェントごとに 1 つのブランチ**;あなた経由でリベース/マージ |
|プル後のコンテキストが古い |各チャットにいつかを伝えます`main`移動しました |
|フック/ロックファイルの戦い | 2 つのツリーで長いインストーラーを必要なしに同時に実行しないでください。
|飛行中にルールが変更される |リポジトリエージェントを一時停止します。ルールエージェントを更新します。履歴書 |

```mermaid
sequenceDiagram
  actor You
  participant A as Agent A worktree
  participant B as Agent B worktree
  participant GH as GitHub

  You->>A: Implement auth on feat/auth
  You->>B: Implement billing on feat/billing
  par Auth path
    A->>A: Edit auth files only
  and Billing path
    B->>B: Edit billing files only
  end
  A->>GH: Push and open PR
  B->>GH: Push and open PR
  You->>GH: Review and merge order
  Note over You,GH: If conflict, merge one first then rebase the other
```

### 並列化を「しない」場合

- ツリー全体に影響を与える大規模な名前変更/移動  
- 生成された共有ロック (`package-lock.json`) 計画なし  
- 「すべてをリファクタリング」+「ホットフィックスを配布」を同じ時間内に行う

次に: **1 つのエージェント**、または最初にホットフィックス、次にリファクタリングを行います。

## 5. エンドツーエンドの一日の形

```mermaid
flowchart TD
  Start[Start of day] --> RulesCheck{Global rules OK?}
  RulesCheck -->|No| RulesAgent[Rules agent chat]
  RulesAgent --> RulesCheck
  RulesCheck -->|Yes| Pick[Pick repos / tickets]
  Pick --> Spawn[Open one agent per repo or worktree]
  Spawn --> Work[Agents implement on their branches]
  Work --> Gate{Ready to merge?}
  Gate -->|No| Work
  Gate -->|Yes| YouMerge[You review, commit policy, PR, merge]
  YouMerge --> Done[Done / next ticket]
```

## 6. 再利用するプロンプト スニペット

**ルールエージェント**

```text
Scope: user-level Cursor rules only.
Output: proposed rule text, files touched, rollback note.
Do not modify any git repo application source.
```

**レポエージェント**

```text
Repo: <path or name>. Branch: feat/<ticket>.
Do not change user/global Cursor rules.
If a standing rule should change, say so — I will run the Rules agent.
```

**同じリポジトリの並列**

```text
You own paths: <dirs>. Other agent owns: <dirs>.
Do not edit outside your paths. Worktree: <path>. Branch: <name>.
```

## 7. 関連メモ

|トピック |注 |
|------|------|
|エージェントを操作する方法 | [監督エージェント](iii-directing-agents.md) |
|ルール/スキルが存在する場所 | [Cursor スキル、ルール、AGENTS.md](../skills-and-agent-instructions/iv-cursor-skills-rules-agents-md.md) |
|人間の承認ループ | [製品と関係者](iv-products-and-human-in-the-loop.md) |

＃＃ 次

[エージェントとエージェント ワークフローの概要] に戻る(i-overview.md）。
