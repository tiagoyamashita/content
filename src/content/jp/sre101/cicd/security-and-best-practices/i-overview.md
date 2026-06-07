---
label: "I"
subtitle: "概要"
group: "CI/CD"
order: 1
---
セキュリティとベスト プラクティス — 概要

安全な CI/CD は、**ソース**、**ビルド**、**アーティファクト**、**デプロイ ターゲット**を保護します。パイプラインを単なるアプリコードではなく、**攻撃対象領域**の一部として扱います。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [サプライチェーンとSLSA](ii-supply-chain-and-slsa.md) | SLSA、SBOM、署名、依存関係の固定 |
| [秘密と OIDC](iii-secrets-and-oidc.md) |ボールト、ローテーション、クラウドへの OIDC |
| [最も権限のないランナー](iv-least-privilege-runners.md) |トークン スコープ、セルフホスト ランナー、フォーク PR |
| [テスト戦略](v-testing-strategy.md) |テスト ピラミッド、ゲート、シャーディング、不安定なテスト |
| [パイプラインの可観測性と DORA](vi-pipeline-observability-and-dora.md) | DORA メトリクス、アラート、パイプライン トレース |
| [ゲートの解放とロールバック](vii-release-gates-and-rollbacks.md) |承認、不変のデプロイ、ロールバック |

**関連:** パート I の基礎、**ツールとプラットフォーム** サブメニュー、**Terraform** サブメニュー → [Terraform in CI/CD](../terraform/vii-terraform-in-cicd.md) (適用ジョブの OIDC)。

##安全なパイプライン層

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="CI/CD security layers from source to deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Defense in depth across the pipeline</text>
  <rect x="12" y="36" width="88" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="20" y="54" fill="#e4e4e7" font-size="8">Source &amp; deps</text>
  <path d="M100 50 H120" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="120" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="128" y="54" fill="#e4e4e7" font-size="8">Build &amp; scan</text>
  <path d="M208 50 H228" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="228" y="36" width="88" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="236" y="54" fill="#e4e4e7" font-size="8">Secrets &amp; IAM</text>
  <path d="M316 50 H336" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="336" y="36" width="88" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="344" y="54" fill="#e4e4e7" font-size="8">Deploy gates</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Pin actions · SBOM · least privilege · OIDC · signed images · prod approval</text>
</svg></figure>

## 簡単なチェックリスト

|レイヤー |こうする |
|------|-----------|
|依存関係 |ファイルのロック、改修/依存ボット、CVE のスキャン |
|アクション / プラグイン | **コミット SHA** に固定し、フローティングではない`@v4`タグ |
|資格情報 | OIDC または有効期間の短いトークン。リポジトリ内でキーを決して使用しない |
|ランナー |一時的な VM。 PR ジョブから本番ネットワークがありません |
|アーティファクト |画像に署名 (Cosign);デプロイ前に検証する |
|制作 |環境保護、手動承認、ロールバック パス |

## リハーサル

- SLSA L2 と L3 とは何ですか?
- GitHub アクションを SHA に固定する理由は何ですか?
- 4 つの DORA メトリクスに名前を付けます。
- シークレットを使用して自己ホスト ランナーでフォーク PR を実行してみてはいかがでしょうか?
