---
label: "VI"
subtitle: "Jenkins + Ansible pipelines"
group: "CI/CD"
order: 6
---
Jenkins + Ansible pipelines
**Jenkins** builds and tests; a **Deploy** stage invokes **`ansible-playbook`**. General Jenkins CI patterns (Docker agents, Shared Libraries) live in **[Jenkins](../tools-and-platforms/iv-jenkins.md)**.

## 1. Responsibility split

| Layer | Owns |
|-------|------|
| **Jenkins** | Checkout, compile, unit/integration test, artifacts, gates |
| **Ansible** | OS packages, config files, artifact placement, service restart |

## 2. Full Jenkinsfile example

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

| Directive | Effect |
|-------------|--------|
| `when { branch 'main' }` | Deploy stages only on main |
| `input` | Manual approval before prod |
| `--tags deploy` | Skip full site config; deploy tasks only |
| `credentials('ansible-vault-pass')` | Injects secret; masked in logs |

## 3. Ansible Jenkins plugin

Install **Ansible** plugin — cleaner than raw shell:

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

| Parameter | Purpose |
|-----------|---------|
| `credentialsId` | SSH key for `ansible_user` |
| `vaultCredentialsId` | Vault password |
| `extras` | Extra CLI args |

## 4. Artifact handoff

**Option A** — build on Jenkins agent, copy from workspace:

```yaml
# deploy.yml — artifact already in workspace
- ansible.builtin.copy:
    src: "{{ playbook_dir }}/../../target/myapp-{{ app_version }}.jar"
    dest: /opt/myapp/app.jar
```

**Option B** — upload to Nexus/S3 in Jenkins, Ansible fetches:

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

Option B scales when deploy agents differ from build agents.

## 5. Separate deploy agent pool

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

Matches runner segmentation in [Least-privilege runners](../security-and-best-practices/iv-least-privilege-runners.md).

## 6. Multibranch + inventory per env

| Branch | Inventory | Auto-deploy? |
|--------|-----------|--------------|
| `feature/*` | — | Build/test only |
| `main` | `staging.ini` | Yes |
| `release/*` | `production.ini` | Manual approval |

## 7. Troubleshooting

| Symptom | Check |
|---------|-------|
| `Permission denied (publickey)` | SSH credential / `ansible_user` |
| Vault decrypt fail | `vaultCredentialsId` or password file |
| Host unreachable | Security group, VPN, deploy agent network |
| `changed=0` but app old | Wrong `app_version` extra-var |

**Related:** [Jenkins](../tools-and-platforms/iv-jenkins.md), [Deploy patterns & operations](vii-deploy-patterns-and-operations.md).
