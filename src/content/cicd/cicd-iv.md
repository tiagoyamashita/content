---
label: "IV"
subtitle: "Ansible & Jenkins"
group: "CI/CD"
order: 4
---
CI/CD — Part IV: Ansible & Jenkins
Configuration management meets pipeline orchestration.

## 1. Ansible overview
Ansible: agentless configuration management tool by Red Hat.
- Written in Python; communicates over SSH (Linux) or WinRM (Windows).
- Agentless — no daemon to install on target hosts.
- Idempotent — running the same playbook twice leaves the system unchanged.
- Declarative YAML syntax — describe desired state, not commands.

Core terms:
- Control node: the machine that runs Ansible (your laptop, CI runner).
- Managed node: the target host being configured.
- Module: a single unit of work (apt, copy, service, template, …).
- Task: one call to a module with arguments.
- Play: a mapping of hosts → list of tasks.
- Playbook: one or more plays in a YAML file.

## 2. Inventory & playbooks
inventory.ini — defines target hosts and groups:

```ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
```

Dynamic inventory: script or plugin that queries AWS, GCP, etc.
site.yml — minimal playbook example:

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    http_port: 80
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Copy site config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-enabled/default
      notify: Restart nginx

    - name: Ensure nginx is running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

Run:

```bash
ansible-playbook -i inventory.ini site.yml
```


## 3. Roles & variables
Role: a reusable, structured unit of automation.
Directory layout of a role named 'nginx':

```
roles/nginx/
  tasks/main.yml       ← task list
  handlers/main.yml    ← handlers
  templates/           ← Jinja2 templates (.j2)
  files/               ← static files to copy
  defaults/main.yml    ← default variable values (lowest priority)
  vars/main.yml        ← role vars (higher priority than defaults)
  meta/main.yml        ← role metadata and dependencies
```

Variable precedence (low → high):
- role defaults < inventory vars < playbook vars < extra-vars (-e flag)
Vault: encrypt secrets at rest.

```bash
ansible-vault encrypt_string 'mypassword' --name 'db_pass'
# Decrypted automatically at runtime when --ask-vault-pass is passed.
```


## 4. Jenkins overview
Jenkins: open-source automation server; self-hosted; plugin ecosystem (1800+).
- Master (controller): schedules builds, serves UI, holds config.
- Agent (node): executes the actual build steps.
- Executor: a slot on an agent — one build per executor at a time.

Two pipeline syntaxes:
- Scripted Pipeline  — Groovy DSL, maximum flexibility.
- Declarative Pipeline — structured YAML-like Groovy; preferred.

Jenkinsfile lives in the repo root → Pipeline as Code.

## 5. Declarative pipeline walkthrough
Jenkinsfile example — build, test, deploy with Ansible:

```groovy
pipeline {
  agent { label 'linux' }

  environment {
    ANSIBLE_HOST_KEY_CHECKING = 'False'
    VAULT_PASS = credentials('ansible-vault-pass')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps { sh 'mvn clean package -DskipTests' }
    }
    stage('Test') {
      steps { sh 'mvn test' }
      post {
        always { junit 'target/surefire-reports/**/*.xml' }
      }
    }
    stage('Deploy to Staging') {
      when { branch 'main' }
      steps {
        sh '''
          ansible-playbook \
            -i inventory/staging.ini \
            --vault-password-file <(echo $VAULT_PASS) \
            playbooks/deploy.yml \
            -e app_version=${BUILD_NUMBER}
        '''
      }
    }
  }
  post {
    failure {
      mail to: 'team@example.com',
           subject: "Build ${BUILD_NUMBER} failed",
           body: "Check ${BUILD_URL}"
    }
  }
}
```


## 6. Ansible + Jenkins together
Common pattern:
1. Jenkins builds & tests the application artifact.
2. Jenkins calls ansible-playbook to push that artifact to servers.
3. Ansible handles idempotent server configuration and service restart.

Benefits of the split:
- Jenkins owns the CI pipeline (build, test, gate).
- Ansible owns infrastructure state (install deps, configure, deploy).
- Reuse the same Ansible playbook from the CLI for hotfixes — no Jenkins needed.

Tips:
- Store inventory files in the same repo as the Jenkinsfile.
- Use ansible-lint in a Jenkins stage before the deploy stage.
- Tag Ansible tasks (--tags deploy) so Jenkins can run only deploy tasks
without re-running the full configuration pass.
- Use the Ansible plugin for Jenkins — provides an 'ansiblePlaybook' step
with built-in credential binding and colorised output.

Minimal Ansible deploy playbook (playbooks/deploy.yml):

```yaml
---
- name: Deploy application
  hosts: webservers
  become: true
  vars:
    artifact: "myapp-{{ app_version }}.jar"
  tasks:
    - name: Copy JAR
      ansible.builtin.copy:
        src: "target/{{ artifact }}"
        dest: "/opt/myapp/app.jar"

    - name: Restart app service
      ansible.builtin.service:
        name: myapp
        state: restarted
```


## 7. Remember & rehearse
- What does 'agentless' mean in Ansible? How does it connect to hosts?
- Explain idempotency — why is it important for configuration management?
- What is a handler and when does it fire?
- Sketch the Ansible directory layout for a role named 'postgres'.
- In a Jenkinsfile, what does the when { branch 'main' } directive do?
- How do you pass an Ansible Vault password securely from Jenkins?
