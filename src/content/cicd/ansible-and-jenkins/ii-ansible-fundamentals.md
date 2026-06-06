---
label: "II"
subtitle: "Ansible fundamentals"
group: "CI/CD"
order: 2
---
Ansible fundamentals
**Ansible** is an agentless configuration management tool (Red Hat). You describe **desired state** in YAML; Ansible SSHs to hosts and applies modules until state matches.

## 1. Why Ansible in CI/CD

| Benefit | Explanation |
|---------|-------------|
| **Agentless** | No daemon on targets — only SSH + Python |
| **Idempotent** | Second run makes no spurious changes |
| **Declarative** | "nginx present" not "apt install nginx" |
| **Portable** | Same playbook from Jenkins, laptop, or AWX |

## 2. Core terms

| Term | Meaning |
|------|---------|
| **Control node** | Machine running `ansible` / `ansible-playbook` (laptop, CI agent) |
| **Managed node** | Target host being configured |
| **Inventory** | List of hosts and groups |
| **Module** | Unit of work (`apt`, `copy`, `service`, `template`) |
| **Task** | One module invocation with arguments |
| **Play** | Hosts + ordered tasks (+ handlers) |
| **Playbook** | YAML file with one or more plays |

## 3. Agentless connection

```bash
# Ad-hoc ping — verifies SSH + Python on targets
ansible webservers -i inventory.ini -m ping
```

| OS | Connection |
|----|------------|
| Linux | SSH (default), `become: true` for sudo |
| Windows | WinRM (`ansible_connection=winrm`) |

Managed nodes need **Python 3** (minimal install on fresh hosts via `raw` module bootstrap if needed).

## 4. Idempotency

```yaml
- name: Ensure nginx installed
  ansible.builtin.apt:
    name: nginx
    state: present
```

| Run | Result |
|-----|--------|
| First | Installs nginx → **changed** |
| Second | Already present → **ok** (no change) |

Idempotency matters for CI/CD: re-running deploy after a partial failure is safe.

## 5. Modules vs shell commands

**Prefer modules** — they report changed/ok/failed and handle edge cases:

```yaml
# Good — idempotent
- ansible.builtin.file:
    path: /opt/myapp
    state: directory
    owner: myapp
    mode: '0755'

# Avoid unless necessary — always shows changed
- ansible.builtin.shell: mkdir -p /opt/myapp && chown myapp /opt/myapp
```

Use **`command`/`shell`** with **`creates:`** or **`removes:`** guards when no module fits.

## 6. Check mode (dry run)

```bash
ansible-playbook site.yml --check --diff
```

Shows what **would** change without applying — useful in PR review stages.

## 7. Project layout (typical)

```text
ansible/
  inventory/
    staging.ini
    production.ini
  group_vars/
    webservers.yml
  host_vars/
    web1.example.com.yml
  roles/
    nginx/
    myapp/
  playbooks/
    site.yml
    deploy.yml
  ansible.cfg
```

## 8. ansible.cfg essentials

```ini
[defaults]
inventory = inventory/staging.ini
roles_path = roles
host_key_checking = False
retry_files_enabled = False

[privilege_escalation]
become = True
become_method = sudo
```

In Jenkins set `ANSIBLE_HOST_KEY_CHECKING=False` only when you trust inventory hosts; prefer known_hosts or SSH keys.

**Related:** `iii-inventory-and-playbooks.md`, `v-dynamic-inventory-and-modules.md`.
