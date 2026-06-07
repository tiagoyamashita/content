---
label: "VI"
subtitle: "Jenkins + Ansible パイプライン"
group: "CI/CD"
order: 6
---
Jenkins + Ansible パイプライン

**Jenkins** はビルドとテストを行います。 **Deploy** ステージは **`ansible-playbook`** を呼び出します。一般的な Jenkins CI パターン (Docker エージェント、共有ライブラリ) は **[Jenkins](../tools-and-platforms/iv-jenkins.md)** に存在します。

## 1. 責任の分担

|レイヤー |所有 |
|------|------|
| **Jenkins** |チェックアウト、コンパイル、単体/統合テスト、アーティファクト、ゲート |
| **Ansible** | OS パッケージ、構成ファイル、アーティファクトの配置、サービスの再起動 |

## 2. 完全な Jenkins ファイルの例

```groovy
// Jenkinsfile
pipeline {
  agent { label 'linux' }

  environment {
    ANSIBLE_HOST_KEY_CHECKING = 'False'
    ANSIBLE_FORCE_COLOR = 'true'
    VAULT_PASS = credentials('ansible-vault-pass')
  }

  options {
    timestamps()
    timeout(time: 45, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build') {
      steps {
        sh './mvnw -B package -DskipTests'
      }
    }

    stage('Test') {
      steps {
        sh './mvnw -B test'
      }
      post {
        always {
          junit 'target/surefire-reports/**/*.xml'
        }
      }
    }

    stage('Ansible Lint') {
      steps {
        sh 'ansible-lint ansible/playbooks ansible/roles'
      }
    }

    stage('Deploy Staging') {
      when { branch 'main' }
      steps {
        sh '''
          ansible-playbook \
            -i ansible/inventory/staging.ini \
            --vault-password-file <(echo "$VAULT_PASS") \
            ansible/playbooks/deploy.yml \
            -e app_version=${BUILD_NUMBER} \
            --tags deploy
        '''
      }
    }

    stage('Deploy Production') {
      when { branch 'main' }
      steps {
        input message: 'Deploy to production?', ok: 'Deploy'
        sh '''
          ansible-playbook \
            -i ansible/inventory/production.ini \
            --vault-password-file <(echo "$VAULT_PASS") \
            ansible/playbooks/deploy.yml \
            -e app_version=${BUILD_NUMBER} \
            --tags deploy
        '''
      }
    }
  }

  post {
    failure {
      mail to: 'team@example.com',
           subject: "Build ${env.BUILD_NUMBER} failed — ${env.JOB_NAME}",
           body: "See ${env.BUILD_URL}"
    }
  }
}
```

|ディレクティブ |効果 |
|---------------|----------|
| `when { branch 'main' }` |ステージをメインにのみデプロイ |
| `input` |本番前の手動承認 |
| `--tags deploy` |完全なサイト構成をスキップします。デプロイタスクのみ |
| `credentials('ansible-vault-pass')` |シークレットを注入します。ログ内でマスクされる |

## 3. Ansible Jenkins プラグイン

**Ansible** プラグインをインストールします — 生のシェルよりもクリーンです:

```groovy
stage('Deploy') {
  when { branch 'main' }
  steps {
    ansiblePlaybook(
      playbook: 'ansible/playbooks/deploy.yml',
      inventory: 'ansible/inventory/staging.ini',
      credentialsId: 'ssh-deploy-key',
      vaultCredentialsId: 'ansible-vault-pass',
      colorized: true,
      extras: "-e app_version=${env.BUILD_NUMBER} --tags deploy",
      disableHostKeyChecking: false
    )
  }
}
```

|パラメータ |目的 |
|----------|----------|
| `credentialsId` | `ansible_user` の SSH キー |
| `vaultCredentialsId` |ボールトのパスワード |
| `extras` |追加の CLI 引数 |

## 4. アーティファクトの引き継ぎ

**オプション A** — Jenkins エージェント上に構築し、ワークスペースからコピーします。

```yaml
# deploy.yml — artifact already in workspace
- ansible.builtin.copy:
    src: "{{ playbook_dir }}/../../target/myapp-{{ app_version }}.jar"
    dest: /opt/myapp/app.jar
```

**オプション B** — Jenkins で Nexus/S3 にアップロードすると、Ansible が取得されます。

```groovy
stage('Publish') {
  steps {
    sh './mvnw deploy -DskipTests'
  }
}
```

```yaml
- ansible.builtin.get_url:
    url: "https://nexus.example.com/repository/releases/myapp-{{ app_version }}.jar"
    dest: /opt/myapp/app.jar
    mode: '0644'
```

オプション B は、デプロイ エージェントがビルド エージェントと異なる場合に拡張されます。

## 5. 個別のデプロイ エージェント プール

```groovy
pipeline {
  agent none
  stages {
    stage('Build & Test') {
      agent { label 'linux-build' }
      steps { /* mvn ... */ }
    }
    stage('Deploy') {
      agent { label 'linux-deploy' }   // prod network access
      steps {
        ansiblePlaybook(/* ... */)
      }
    }
  }
}
```

[最小権限ランナー](../security-and-best-practices/iv-least-privilege-runners.md) のランナー セグメンテーションと一致します。

## 6. マルチブランチ + 環境ごとのインベントリ

|支店 |在庫 |自動展開しますか? |
|------|-----------|--------------|
| `feature/*` | — |ビルド/テストのみ |
| `main` | `staging.ini` |はい |
| `release/*` | `production.ini` |手動承認 |

## 7. トラブルシューティング

|症状 |チェック |
|----------|----------|
| `Permission denied (publickey)` | SSH 認証情報 / `ansible_user` |
|ボールトの復号化に失敗しました | `vaultCredentialsId` またはパスワード ファイル |
|ホストに到達できません |セキュリティ グループ、VPN、エージェント ネットワークの展開 |
| `changed=0` ですがアプリは古い |間違った `app_version` 追加変数 |

**関連:** [Jenkins](../tools-and-platforms/iv-jenkins.md)、[パターンと操作のデプロイ](vii-deploy-patterns-and-operations.md)。
