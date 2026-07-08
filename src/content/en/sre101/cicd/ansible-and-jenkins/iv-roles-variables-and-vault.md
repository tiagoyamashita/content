---
label: "IV"
subtitle: "Roles, variables & Vault"
group: "CI/CD"
order: 4
---
Roles, variables & Vault
**Roles** package reusable automation. **Variables** layer config per env. **Ansible Vault** encrypts secrets at rest in Git.

## 1. Role directory layout

```text
roles/postgres/
  tasks/main.yml       ← task list (entry point)
  handlers/main.yml    ← restart handlers
  templates/           ← Jinja2 (.j2)
  files/               ← static files to copy
  defaults/main.yml    ← lowest-priority defaults
  vars/main.yml        ← role-internal vars (higher than defaults)
  meta/main.yml        ← dependencies, min Ansible version
  molecule/            ← optional test scenarios
```

**postgres** role `tasks/main.yml`:

```yaml
---
- name: Install PostgreSQL
  ansible.builtin.apt:
    name: postgresql-{{ postgres_version }}
    state: present

- name: Configure pg_hba
  ansible.builtin.template:
    src: pg_hba.conf.j2
    dest: /etc/postgresql/{{ postgres_version }}/main/pg_hba.conf
  notify: Restart postgres
```

Use in playbook:

```yaml
- hosts: dbservers
  roles:
    - role: postgres
      vars:
        postgres_version: "16"
```

## 2. Variable precedence (low → high)

| Priority | Source |
|----------|--------|
| 1 | Role `defaults/main.yml` |
| 2 | Inventory `group_vars` / `host_vars` |
| 3 | Play `vars:` |
| 4 | Role `vars/main.yml` |
| 5 | Task `vars:` |
| 6 | `-e` / `--extra-vars` on CLI |

**Rule of thumb:** defaults in role; environment overrides in `group_vars/staging/` vs `group_vars/production/`.

## 3. group_vars structure

```text
inventory/
  group_vars/
    all.yml              # every host
    webservers.yml
    staging/
      webservers.yml     # when using inventory dir layout
    production/
      webservers.yml
```

```yaml
# group_vars/staging/webservers.yml
app_version: "latest-staging"
db_host: db1.staging.internal
jvm_opts: "-Xms512m -Xmx512m"
```

```yaml
# group_vars/production/webservers.yml
app_version: "1.4.2"
db_host: db.prod.internal
jvm_opts: "-Xms2g -Xmx2g"
```

## 4. Ansible Vault

Encrypt secrets in repo — decrypt at runtime with password or key file.

```bash
# Encrypt entire file
ansible-vault encrypt group_vars/production/secrets.yml

# Encrypt single value inline
ansible-vault encrypt_string 'SuperSecretDbPass' --name 'db_password'
```

Encrypted file header:

```yaml
# group_vars/production/secrets.yml (encrypted)
$ANSIBLE_VAULT;1.1;AES256
663864396538...
```

Use in template (decrypted at runtime):

```yaml
- name: Set DB password in app config
  ansible.builtin.template:
    src: application.yml.j2
    dest: /etc/myapp/application.yml
  vars:
    db_password: "{{ vault_db_password }}"
```

Reference from `group_vars` with `_vault` prefix convention or include in encrypted vars file.

## 5. Running with Vault in CI

```bash
# Password file (Jenkins writes from credential)
ansible-playbook site.yml \
  --vault-password-file /tmp/vault_pass \
  -i inventory/production.ini

# Or prompt (interactive only)
ansible-playbook site.yml --ask-vault-pass
```

Never commit vault password — store in Jenkins **Credentials** [Jenkins + Ansible pipelines](vi-jenkins-ansible-pipelines.md).

## 6. Role dependencies

```yaml
# roles/myapp/meta/main.yml
dependencies:
  - role: common
  - role: nginx
    vars:
      nginx_port: 443
```

Ansible runs dependencies before the role that declares them.

## 7. ansible-galaxy

Install community roles:

```bash
ansible-galaxy install geerlingguy.java --roles-path roles
```

```yaml
# requirements.yml
roles:
  - name: geerlingguy.java
    version: "2.3.0"
```

```bash
ansible-galaxy install -r requirements.yml
```

Pin versions in CI for reproducible builds.

## 8. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Secrets in plain `group_vars` | Vault encrypt |
| Copy-paste tasks across playbooks | Extract role |
| `-e` for everything | Use inventory/group_vars |
| Huge monolithic role | Split by concern (nginx, app, log) |

**Related:** [Inventory & playbooks](iii-inventory-and-playbooks.md), [Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md).
