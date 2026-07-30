---
label: "VII"
subtitle: "Deploy patterns & operations"
group: "CI/CD"
order: 7
---
Deploy patterns & operations
Production deploys need **idempotent playbooks**, clear **staging/prod** separation, and a **CLI path** for hotfixes when Jenkins is down.

## 1. Minimal deploy playbook

```yaml
---
# ansible/playbooks/deploy.yml
- name: Deploy application
  hosts: webservers
  become: true
  serial: 1                    # rolling one host at a time
  vars:
    app_user: myapp
    app_dir: /opt/myapp

  tasks:
    - name: Ensure app directory
      ansible.builtin.file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        mode: '0755'
      tags: [deploy]

    - name: Copy application JAR
      ansible.builtin.copy:
        src: "{{ artifact_path | default('target/myapp-' + app_version + '.jar') }}"
        dest: "{{ app_dir }}/app.jar"
        owner: "{{ app_user }}"
        mode: '0644'
      notify: Restart myapp
      tags: [deploy]

    - name: Ensure systemd unit
      ansible.builtin.template:
        src: ../roles/myapp/templates/myapp.service.j2
        dest: /etc/systemd/system/myapp.service
      notify: Restart myapp
      tags: [config, deploy]

  handlers:
    - name: Restart myapp
      ansible.builtin.systemd:
        name: myapp
        state: restarted
        daemon_reload: true
```

| Setting | Purpose |
|---------|---------|
| `serial: 1` | Rolling deploy — one server at a time |
| `serial: "25%"` | Quarter of fleet per batch |
| `tags: [deploy]` | Jenkins runs `--tags deploy` only |

## 2. Rolling deploy diagram

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" role="img" aria-label="Rolling deploy serial one">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">serial: 1 — update web1, then web2, then web3</text>
  <rect x="12" y="40" width="56" height="36" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="24" y="62" fill="#e4e4e7" font-size="9">web1 ✓</text>
  <rect x="80" y="40" width="56" height="36" rx="3" fill="rgba(251,191,36,0.2)" stroke="#fbbf24"/>
  <text x="92" y="62" fill="#e4e4e7" font-size="9">web2 …</text>
  <rect x="148" y="40" width="56" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="160" y="62" fill="#71717a" font-size="9">web3</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Load balancer keeps serving healthy nodes during rollout</text>
</svg></figure>

## 3. Staging vs production

```text
ansible/
  inventory/
    staging.ini          # 2 small VMs
    production.ini       # full fleet
  group_vars/
    all.yml
    staging/
      webservers.yml     # app_version: latest from CI
    production/
      webservers.yml     # pinned version, stricter jvm_opts
```

Never share production secrets in staging vault files. Use separate **`ansible-vault`** passwords or **`vault_id`** labels.

## 4. Hotfix without Jenkins

Same playbook from laptop (break-glass):

```bash
cd ansible
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault_pass

ansible-playbook \
  -i inventory/production.ini \
  playbooks/deploy.yml \
  -e app_version=1.4.3-hotfix \
  --tags deploy \
  --limit web1.example.com
```

| Step | Action |
|------|--------|
| 1 | Build hotfix JAR locally or pull from CI artifact |
| 2 | `--limit` one canary host first |
| 3 | Verify health / metrics |
| 4 | Remove `--limit` for full fleet |

Document this in runbook — ops shouldn't depend on Jenkins UI during incident.

## 5. Blue/green with Ansible (VM pattern)

Two app directories — switch symlink:

```yaml
- name: Deploy to inactive slot
  ansible.builtin.copy:
    src: "myapp-{{ app_version }}.jar"
    dest: "/opt/myapp/releases/{{ app_version }}/app.jar"

- name: Point current symlink to new release
  ansible.builtin.file:
    src: "/opt/myapp/releases/{{ app_version }}"
    dest: /opt/myapp/current
    state: link
  notify: Restart myapp
```

Rollback = repoint symlink to previous release directory + handler restart.

## 6. Pre-deploy vs deploy tags

| Tag | Runs when | Tasks |
|-----|-----------|-------|
| `packages` | Weekly or new host | JDK, nginx install |
| `config` | Config change PR | templates, systemd units |
| `deploy` | Every release | copy JAR, restart |

```bash
# Full configure (new server)
ansible-playbook site.yml

# Fast path (CI)
ansible-playbook deploy.yml --tags deploy
```

## 7. Integration with release gates

Align with [Release gates & rollbacks](../security-and-best-practices/vii-release-gates-and-rollbacks.md):

- Jenkins **`input`** before production playbook
- Deploy **`app_version=${BUILD_NUMBER}`** or git SHA — immutable reference
- Health check tasks fail playbook → automatic Jenkins stage failure
- Rollback playbook or previous **`app_version`** extra-var

## 8. Operations checklist

- [ ] Inventory in Git matches actual fleet (or dynamic plugin fresh)
- [ ] `--check` on config changes before merge
- [ ] `ansible-lint` in CI
- [ ] Vault secrets rotated on schedule
- [ ] Hotfix runbook tested without Jenkins
- [ ] `serial` set for production rolling updates

## 9. Rehearsal answers

- **Handler** — runs once at end if notified task changed (e.g. restart after config copy).
- **`when { branch 'main' }`** — limits deploy stage to main branch builds.
- **Vault from Jenkins** — `credentials('ansible-vault-pass')` + `--vault-password-file`.
- **postgres role layout** — `tasks/`, `handlers/`, `templates/`, `defaults/`, `vars/`, `meta/`.

**Related:** [Jenkins + Ansible pipelines](vi-jenkins-ansible-pipelines.md), [Inventory & playbooks](iii-inventory-and-playbooks.md).
