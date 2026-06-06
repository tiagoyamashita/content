---
label: "II"
subtitle: "サプライチェーンとSLSA"
group: "CI/CD"
order: 2
---
サプライチェーンとSLSA

**サプライ チェーン攻撃**は、アプリケーション コードだけでなく、依存関係、ビルド ツール、レジストリもターゲットにします。 **SLSA** (ソフトウェア アーティファクトのサプライ チェーン レベル) は、信頼できるビルドの成熟度レベルを定義します。

## 1. 一般的なリスク

|リスク |例 |
|-----|----------|
| **タイポスクワッティング** | PyPI では `requests` の代わりに `reqeusts`
| **依存関係の混乱** |プライベートパッケージ名が公開される |
| **侵害されたアクション/プラグイン** | CI アクションへの悪意のある更新 |
| **レジストリの乗っ取り** |レジストリ内の署名のないイメージが置き換えられました。
| **ビルド スクリプト インジェクション** |信頼できない PR がワークフロー YAML を変更する |

## 2. SLSA レベル

|レベル |要件 |典型的な CI 機能 |
|----------|---------------|--------------------------|
| **L1** |ビルドプロセスを文書化して記録 |履歴のある任意の CI |
| **L2** |ホストされたビルド サービス + 署名された来歴 | GitHub/GitLab 証明書 |
| **L3** |強化され、分離された、再現可能なビルド |専用ビルドクラスター、ハーメチックdeps |
| **L4** | 2 人によるレビュー + 密閉性、再現性 |最高の保証 (実際にはまれです) |

ほとんどのチームは、署名された来歴と固定された依存関係を持つ **L2** をターゲットとしています。 **L3** セキュリティが重要なリリースの場合。

## 3. ピンのアクションと依存関係

**悪い** — タグは移動する可能性があります:

```yaml
- uses: actions/checkout@v4
```

**より良い** — 不変コミット SHA:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb625be47e5b2ead783297 # v4.1.1
```

**Renovate** または **Dependabot** を使用して、SHA/タグが更新されたときに PR を開きます。マージ前に確認します。

**Maven / npm** — ロック ファイル (`package-lock.json`、BOM 付き `pom.xml`) をコミットします。

```xml
<!-- pom.xml — pin dependency versions explicitly -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
  <version>3.4.0</version>
</dependency>
```

## 4. SBOM の生成

**SBOM** (ソフトウェア部品表) には、ビルド内のすべてのコンポーネントがリストされます。

```yaml
# GitHub Actions — Syft SBOM
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: .
    format: spdx-json

- name: Upload SBOM artifact
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom.spdx.json
```

|ツール |出力 |使用 |
|------|----------|-----|
| **シフト** | SPDX、サイクロンDX |一般的なSBOM |
| **トリビー** | CVE + SBOM |スキャン + インベントリ |
| **Gradle SBOM プラグイン** |サイクロンDX | JVM ビルド |

監査およびインシデント対応のために、リリース アーティファクトを含む SBOM を保存します。

## 5. アーティファクトに署名して検証する

**Cosign** (sigstore) コンテナ イメージに署名します。

```bash
# Sign after push
cosign sign --yes registry.example.com/myapp:1.2.3

# Verify before deploy (in cluster or deploy script)
cosign verify registry.example.com/myapp:1.2.3 \
  --certificate-identity=... \
  --certificate-oidc-issuer=...
```

GitHub **アーティファクト証明** はビルドをコミットとワークフローに結び付けます。消費者はプロモーションの前に来歴を検証します。

## 6. CI でのスキャン

```yaml
# Trivy — filesystem + image
- name: Scan repo
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    severity: CRITICAL,HIGH
    exit-code: 1

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
```

|スキャンの種類 |キャッチ |
|----------|----------|
| **依存関係 (SCA)** |ライブラリ内の既知の CVE |
| **SAST** |コードパターン (Semgrep、CodeQL) |
| **コンテナ** |イメージ レイヤーの OS パッケージ |
| **IaC** | Terraform/K8s マニフェストの構成ミス |

**CRITICAL/HIGH** でゲートがマージします。バックログで MEDIUM を追跡します。

## 7. 改修/依存ボットの例

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "pinDigests": true
    },
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

## 8. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
|チェックサムなしの Dockerfile の `curl \| bash` |ピンのバージョン + ハッシュの検証 |
|イメージ レイヤーのプライベート レジストリ認証 | BuildKit の秘密、マルチステージ |
|スキャン失敗を無視する | HIGH+ の `exit-code: 1` |
|リポジトリにロック ファイルがありません |ロックファイルをコミットします。同期していない場合は CI が失敗します |

**関連:** [CI の Docker](../tools-and-platforms/v-docker-in-ci.md)、[秘密と OIDC](iii-secrets-and-oidc.md)。
