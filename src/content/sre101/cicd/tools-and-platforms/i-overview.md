---
label: "I"
subtitle: "概要"
group: "CI/CD"
order: 1
---
ツールとプラットフォーム — 概要

**CI/CD プラットフォーム** は、**ランナー** (エージェント) でパイプラインを実行します: コードのチェックアウト、ビルド、テスト、スキャン、デプロイ。 **コードが存在する場所**、**ホスティング**、**チームのスキル**に基づいて選択してください。

## このサブメニューのマップ

|注 |プラットフォーム |設定ファイル |
|------|----------|---------------|
| [GitHub アクション](ii-github-actions.md) | GitHub アクション |`.github/workflows/*.yml`|
| [Gitラボ CI](iii-gitlab-ci.md) | Gitラボ CI/CD |`.gitlab-ci.yml`|
| [Jenkins](iv-jenkins.md) | Jenkins |`Jenkinsfile`|
| [CI の Docker](v-docker-in-ci.md) | Docker (すべてのプラットフォーム) |`Dockerfile`、ビルド引数 |
| [CircleCI](vi-circleci.md) |サークルCI |`.circleci/config.yml`|
| [テクトン](vii-tekton.md) |テクトン (Kubernetes) |`Pipeline`、`Task`CRD |
| [プラットフォームの選択](viii-choosing-a-platform.md) |意思決定ガイド | — |

**関連:** パート I の基礎、**セキュリティとベスト プラクティス** サブメニュー、**Ansible および Jenkins** サブメニュー、**Terraform** サブメニュー。

## あらゆるプラットフォーム上の一般的なパイプライン

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="CI pipeline stages checkout build test publish deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Same stages, different YAML syntax</text>
  <rect x="12" y="36" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="54" fill="#e4e4e7" font-size="8">checkout</text>
  <path d="M68 50 H88" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="88" y="36" width="48" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="54" fill="#e4e4e7" font-size="8">build</text>
  <path d="M136 50 H156" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="156" y="36" width="48" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="164" y="54" fill="#e4e4e7" font-size="8">test</text>
  <path d="M204 50 H224" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="224" y="36" width="56" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="232" y="54" fill="#e4e4e7" font-size="8">publish</text>
  <path d="M280 50 H300" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="300" y="36" width="56" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="308" y="54" fill="#e4e4e7" font-size="8">deploy</text>
</svg></figure>

## リハーサル

- 最小限の GitHub アクション: チェックアウト → インストール → テスト?
- Gitラボ`needs:`対ステージ？
- CI で Docker を複数段階にするのはなぜですか?
