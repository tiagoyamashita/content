---
label: "VII"
subtitle: "ゲートのリリースとロールバック"
group: "CI/CD"
order: 7
---
ゲートのリリースとロールバック

安全に出荷するということは、誰が何をデプロイできるかを **ゲート**し、**不変のアーティファクト**を使用し、必要になる前に**テスト済みのロールバック**を行うことを意味します。

## 1. ブランチ保護

|ルール |目的 |
|-----|----------|
|マージ前に PR を要求する |ブランチのレビュー + CI |
|ステータスチェックが必要 |ユニット/統合は合格する必要があります |
|署名付きコミットを要求する |著者の身元を確認する |
| `main` にプッシュできる人を制限する |直接コミットはありません |

GitHub: **設定 → ブランチ → ブランチ保護ルール**。

GitLab: **保護されたブランチ** + **マージリクエストの承認** (例: `main` の 2 人の承認者)。

## 2. 環境保護

```yaml
# GitHub — production gate
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: ./deploy.sh ${{ github.sha }}
```

環境設定で **必須レビュー担当者** と **待機タイマー** を構成します。 **保護された環境**を使用した GitLab `environment: production` でも同じパターン。

## 3. 不変のデプロイアーティファクト

**ダイジェスト** または **semver タグ** によってデプロイします。本番環境では `latest` を使用しないでください。

|悪い |良い |
|-----|------|
| `myapp:latest` | `myapp:1.4.2` または `@sha256:abc...` |
|サーバー上で再構築する | CI から事前に構築されたイメージをプルする |
|フローティング ブランチのデプロイ |コミット SHA に `v1.4.2` をタグ付けする |

```yaml
- name: Deploy
  run: |
    kubectl set image deploy/api api=registry.example.com/myapp:${{ github.sha }}
    kubectl rollout status deploy/api --timeout=5m
```

CI は、初期の段階でその正確なイメージを構築し、スキャンしました [CI の Docker](../tools-and-platforms/v-docker-in-ci.md)。

## 4. 段階的な配信

|戦略 |行動 |ロールバック |
|----------|----------|----------|
| **ローリング** |ポッドをバッチで交換する | `kubectl rollout undo` |
| **青/緑** |トラフィックを新しいスタックに切り替える |戻る |
| **カナリア** |トラフィック 5% → 25% → 100% |トラフィックを古いバージョンにルーティングする |

```yaml
# Flagger canary (Kubernetes)
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  progressDeadlineSeconds: 60
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        threshold: 99
```

メトリクスが合格した場合の自動プロモーション。失敗した場合は自動的にロールバックします。

## 5. CI での手動承認

**GitHub アクション:**

```yaml
jobs:
  hold:
    runs-on: ubuntu-latest
    environment: production   # triggers approval
    steps:
      - run: echo "Approved for deploy"

  deploy:
    needs: hold
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy-prod.sh
```

**Gitラボ:**

```yaml
deploy_prod:
  stage: deploy
  when: manual
  environment: production
  script: ./deploy.sh
```

**Jenkins** — `input` ステップ:

```groovy
stage('Approve') {
  when { branch 'main' }
  steps {
    input message: 'Deploy to production?', ok: 'Deploy'
  }
}
```

## 6. ロールバック プレイブック

|ステップ |アクション |
|------|----------|
| 1 |フォワードデプロイを停止/カナリア |
| 2 |最後に正常であった **イメージ タグ** または **git SHA** を特定します。
| 3 |以前のバージョンを再デプロイします (`rollout undo` またはジョブを再デプロイします) |
| 4 |ヘルスチェックと主要な SLO を検証する |
| 5 |インシデント後: 修正を進め、テストを追加 |

```bash
# Kubernetes — one command rollback
kubectl rollout undo deployment/api
kubectl rollout status deployment/api
```

ロールバックは**四半期ごとにテスト**してください。テストされていないロールバックはプレッシャーがかかると失敗します。

## 7. 機能フラグとホットデプロイ

|アプローチ | | の場合に使用します。
|----------|----------|
| **機能フラグ** |不完全なロジックを非表示にします。再デプロイせずに切り替える |
| **ホットフィックス ブランチ** |重大なバグ。普通列車をスキップします |
| **ロールバック** | prod のバイナリ/構成が間違っています |

フラグは、**展開** (安全、頻繁) と **リリース** (ビジネス上の決定) を切り離します。

## 8. 導入のアンチパターン

|アンチパターン |リスク |
|--------------|------|
|金曜日の午後 5 時に展開 |ロールバックする人がいません |
|デプロイ後にヘルスチェックが行われない |サイレント部分障害 |
|共有本番環境/ステージング資格情報 |ステージング違反 → 本番 |
|下位互換性のないデータベースの移行 |ロールバックによりスキーマが破壊される |

**拡張コントラクト移行:** 列の追加 → 二重書き込み → バックフィル → 古い削除 - DB を中断せずにアプリをロールバックできます。

## 9. 最初の本番環境のデプロイ前のチェックリスト

- [ ] 分岐保護 + 必須の CI チェック
- [ ] 運用環境では承認が必要です
- [ ] デプロイでは不変のタグ/ダイジェストを使用します
- [ ] 導入後のヘルスチェック/スモークテスト
- [ ] ロールバック コマンドを文書化してリハーサルしました
- [ ] デプロイ失敗時にオンコールに通知される

**関連:** [テスト戦略](v-testing-strategy.md)、[サプライ チェーンと SLSA](ii-supply-chain-and-slsa.md) (署名されたイメージ)、[秘密と OIDC](iii-secrets-and-oidc.md)。
