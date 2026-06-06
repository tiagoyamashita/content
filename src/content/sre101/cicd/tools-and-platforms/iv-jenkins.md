---
label: "IV"
subtitle: "Jenkins"
group: "CI/CD"
order: 4
---
Jenkins

**1800 以上のプラグイン**を備えた **セルフホスト** オートメーション サーバー。 **`Jenkinsfile`** のコードとしてのパイプライン (宣言的またはスクリプト化された Groovy)。

**こちらもご覧ください:** **Ansible と Jenkins** サブメニュー — プレイブック、Vault、デプロイ パターン [概要](../ansible-and-jenkins/i-overview.md)。

## 1. パイプラインの種類

|タイプ |構文 |使用 |
|------|----------|-----|
| **宣言的** |構造化された `pipeline { }` |新しいプロジェクト — 優先 |
| **スクリプト付き** |完全な Groovy DSL |従来の複雑なフロー制御 |
| **フリースタイル** | UIのみ |新しい仕事の場合は避ける |

## 2. 宣言的なスケルトン

```groovy
// Jenkinsfile
pipeline {
  agent any

  options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        sh 'mvn -B package -DskipTests'
      }
    }
    stage('Test') {
      steps {
        sh 'mvn -B test'
      }
      post {
        always {
          junit '**/target/surefire-reports/*.xml'
        }
      }
    }
  }
}
```

## 3. ステージごとの Docker エージェント

```groovy
pipeline {
  agent none

  stages {
    stage('Test') {
      agent {
        docker { image 'eclipse-temurin:22-jdk' }
      }
      steps {
        sh './mvnw test'
      }
    }
    stage('Publish') {
      agent { label 'docker-build' }
      steps {
        sh 'docker build -t myapp:$BUILD_NUMBER .'
      }
    }
  }
}
```

## 4. 認証情報と環境

```groovy
pipeline {
  agent any
  environment {
    REGISTRY = 'registry.example.com'
  }
  stages {
    stage('Push') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'registry-creds',
          usernameVariable: 'USER',
          passwordVariable: 'PASS'
        )]) {
          sh '''
            echo "$PASS" | docker login $REGISTRY -u "$USER" --password-stdin
            docker push $REGISTRY/myapp:$BUILD_NUMBER
          '''
        }
      }
    }
  }
}
```

## 5. マルチブランチ パイプライン

Jenkins は各ブランチ/PR で **`Jenkinsfile`** を検出します。

- **ブランチソース** → GitHub/GitLab Webhook
- PR ビルドはステータス チェックを取得します
- リポジトリ内の `Jenkinsfile` が信頼できる情報源です

## 6. 共有ライブラリ

別のリポジトリで再利用可能な Groovy:

```groovy
@Library('my-company-lib@v2') _

pipeline {
  agent any
  stages {
    stage('Deploy') {
      steps {
        deployToK8s(env: 'staging', image: "myapp:${env.BUILD_NUMBER}")
      }
    }
  }
}
```

ライブラリ リポジトリの **`vars/deployToK8s.groovy`** は、kubectl/helm ロジックをカプセル化します。

## 7. __​​IT1__ から Ansible をトリガーする

```groovy
stage('Configure servers') {
  steps {
    ansiblePlaybook(
      playbook: 'deploy/site.yml',
      inventory: 'inventory/production',
      credentialsId: 'ssh-deploy-key',
      extras: '-e app_version=$BUILD_NUMBER'
    )
  }
}
```

**Ansible** プラグインが必要です。

## 8. Jenkins を選択する場合

|長所 |短所 |
|------|------|
|オンプレミスでフルコントロール | HA、アップグレード、プラグインを操作する |
|大規模なプラグイン エコシステム |素晴らしい学習曲線 |
|エアギャップ / コンプライアンスに優しい | UI と SaaS CI は時代遅れに感じることがあります。

| | の場合は Jenkins を選択してください。次の場合には SaaS を選択してください |
|---------------------|------|
|厳しいオンプレミス要件 | GitHub/GitLab ネイティブ CI で十分 |
|既存の Jenkins 投資 |コントローラーのメンテナンスをゼロにしたい |

**関連:** [Jenkins + Ansible パイプライン](../ansible-and-jenkins/vi-jenkins-ansible-pipelines.md)、[プラットフォームの選択](viii-choosing-a-platform.md)。
