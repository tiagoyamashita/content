---
label: "IV"
subtitle: "Jenkins"
group: "CI/CD"
order: 4
---
Jenkins
**Self-hosted** automation server with **1800+ plugins**. Pipelines as code in a **`Jenkinsfile`** (Declarative or Scripted Groovy).

**Also see:** **Ansible & Jenkins** submenu — playbooks, Vault, deploy patterns (`../ansible-and-jenkins/i-overview.md`).

## 1. Pipeline types

| Type | Syntax | Use |
|------|--------|-----|
| **Declarative** | Structured `pipeline { }` | New projects — preferred |
| **Scripted** | Full Groovy DSL | Legacy, complex flow control |
| **Freestyle** | UI-only | Avoid for new work |

## 2. Declarative skeleton

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

## 3. Docker agent per stage

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

## 4. Credentials and environment

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

## 5. Multibranch pipeline

Jenkins discovers **`Jenkinsfile`** on each branch/PR:

- **Branch Source** → GitHub/GitLab webhook
- PR builds get status checks
- `Jenkinsfile` in repo is source of truth

## 6. Shared Libraries

Reusable Groovy in a separate repo:

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

**`vars/deployToK8s.groovy`** in library repo encapsulates kubectl/helm logic.

## 7. Trigger Ansible from Jenkins

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

Requires **Ansible** plugin.

## 8. When to choose Jenkins

| Pros | Cons |
|------|------|
| Full control on-prem | You operate HA, upgrades, plugins |
| Massive plugin ecosystem | Groovy learning curve |
| Air-gapped / compliance friendly | UI can feel dated vs SaaS CI |

| Choose Jenkins when | Choose SaaS when |
|---------------------|------------------|
| Strict on-prem requirement | GitHub/GitLab native CI enough |
| Existing Jenkins investment | Want zero controller maintenance |

**Related:** `../ansible-and-jenkins/vi-jenkins-ansible-pipelines.md`, `viii-choosing-a-platform.md`.
