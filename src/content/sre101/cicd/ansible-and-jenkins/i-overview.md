---
label: "I"
subtitle: "概要"
group: "CI/CD"
order: 1
---
Ansible と Jenkins — 概要

**Jenkins** は CI パイプライン (ビルド、テスト、ゲート) を実行します。 **Ansible** はサーバーに **望ましい状態** を適用します (パッケージ、構成、デプロイ、再起動)。責任を分割することで、デプロイ ロジックを Jenkins の外部で再利用できるようになります。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [Ansible の基礎](ii-ansible-fundamentals.md) |エージェントレス モデル、冪等性、中心用語 |
| [インベントリとプレイブック](iii-inventory-and-playbooks.md) |ホスト、グループ、タスク、ハンドラー |
| [ロール、変数、およびボールト](iv-roles-variables-and-vault.md) |ロールのレイアウト、var の優先順位、シークレット |
| [動的インベントリとモジュール](v-dynamic-inventory-and-modules.md) |クラウド インベントリ、共通モジュール、ansible-lint |
| [Jenkins + Ansible パイプライン](vi-jenkins-ansible-pipelines.md) | Jenkinsfile、Vault 認証、Ansible プラグイン |
| [パターンと操作のデプロイ](vii-deploy-patterns-and-operations.md) |プレイブック、タグ、ホットフィックス、ステージング/本番環境をデプロイする |

**関連:** **ツールとプラットフォーム** → [Jenkins](../tools-and-platforms/iv-jenkins.md) (CI 中心の Jenkins)、パート I の基礎、**Terraform** サブメニュー。

## CI ビルド → Ansible デプロイの流れ

<figure class="notes-diagram"><svg xmlns="0 viewBox="0 0 480 110" role="img" aria-label="Jenkins CI then Ansible deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Jenkins owns CI · Ansible owns server state</text>
  <rect x="12" y="36" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="8">Jenkins</text>
  <text x="20" y="68" fill="#71717a" font-size="7">build test</text>
  <path d="M84 52 H104" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="104" y="36" width="72" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="116" y="56" fill="#e4e4e7" font-size="8">artifact</text>
  <path d="M176 52 H196" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="196" y="36" width="88" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="56" fill="#e4e4e7" font-size="8">ansible-playbook</text>
  <path d="M284 52 H304" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="304" y="36" width="88" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="56" fill="#e4e4e7" font-size="8">webservers</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Same playbook from Jenkins or laptop for hotfixes</text>
</svg></figure>

## このパターンが当てはまる場合

|良いフィット感 |代替案を検討する |
|----------|--------------------------|
| VM またはベアメタル フリート |純粋な Kubernetes → Helm/GitOps |
|混合 Linux 構成 + デプロイ |サーバーレス → CI をクラウド API にデプロイ |
|すでに Jenkins を使用したオンプレミス |グリーンフィールド SaaS → GitHub アクション + Terraform |

## リハーサル

- **エージェントレス** は Ansible にとって何を意味しますか?
- この分割では、**ビルド**と**サーバー構成**の所有者はどちらですか?
- なぜ Jenkinsfile と同じリポジトリにインベントリを保持するのでしょうか?
