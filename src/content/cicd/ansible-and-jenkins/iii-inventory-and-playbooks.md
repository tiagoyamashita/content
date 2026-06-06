---
label: "III"
subtitle: "Inventory & playbooks"
group: "CI/CD"
order: 3
---
Inventory & playbooks
**Inventory** defines **which hosts** Ansible manages. **Playbooks** define **what** to configure on them.

## 1. Static inventory (INI)

```ini
# inventory/staging.ini
[webservers]
web1.staging.example.com ansible_host=10.0.1.10
web2.staging.example.com ansible_host=10.0.1.11

[dbservers]
db1.staging.example.com

[webservers:vars]
ansible_user=deploy
http_port=8080

[staging:children]
webservers
dbservers
```

| Pattern | Use |
|---------|-----|
| `[group]` | Logical tier (web, db, cache) |
| `[group:vars]` | Variables for all hosts in group |
| `[parent:children]` | Nest groups (`staging` includes web + db) |
| `ansible_host` | DNS alias vs actual IP |

## 2. YAML inventory (alternative)

```yaml
# inventory/staging.yml
all:
  children:
    webservers:
      hosts:
        web1.staging.example.com:
          ansible_host: 10.0.1.10
      vars:
        http_port: 8080
    dbservers:
      hosts:
        db1.staging.example.com:
```

## 3. Full playbook example

```yaml
---
# playbooks/site.yml
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    app_name: myapp

  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy nginx site config
      ansible.builtin.template:
        src: ../roles/nginx/templates/default.conf.j2
        dest: /etc/nginx/sites-enabled/default
        mode: '0644'
      notify: Restart nginx

    - name: Ensure nginx running
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
ansible-playbook -i inventory/staging.ini playbooks/site.yml
```

Limit to one host during debugging:

```bash
ansible-playbook -i inventory/staging.ini playbooks/site.yml --limit web1.staging.example.com
```

## 4. Handlers

Handlers run **once at end of play**, only if a task **notifies** them and reported **changed**:

```yaml
tasks:
  - name: Update app config
    ansible.builtin.template:
      src: app.yml.j2
      dest: /etc/myapp/config.yml
    notify: Restart myapp

handlers:
  - name: Restart myapp
    ansible.builtin.systemd:
      name: myapp
      state: restarted
```

| Concept | Behavior |
|---------|----------|
| **notify** | Queue handler if task changed |
| **listen** | Multiple notifies can trigger one handler name |
| **flush_handlers** | Meta task to run handlers mid-play |

## 5. Jinja2 templates

```jinja2
{# roles/nginx/templates/default.conf.j2 #}
server {
    listen {{ http_port }};
    server_name {{ ansible_fhostname }};

    location / {
        proxy_pass http://127.0.0.1:{{ app_port | default(8080) }};
    }
}
```

Built-in facts like **`ansible_hostname`**, **`ansible_default_ipv4`** come from setup module.

## 6. Conditionals and loops

```yaml
- name: Install packages on Debian
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - curl
    - jq
  when: ansible_os_family == "Debian"

- name: Create app users
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
  loop: "{{ app_users }}"
```

## 7. Tags — run subset of tasks

```yaml
- name: Copy application JAR
  ansible.builtin.copy:
    src: "artifacts/{{ artifact }}"
    dest: /opt/myapp/app.jar
  tags: [deploy, app]

- name: Install OS packages
  ansible.builtin.apt:
    name: openjdk-22-jre
    state: present
  tags: [packages]
```

```bash
# Deploy only — skip full config
ansible-playbook playbooks/site.yml --tags deploy
```

Jenkins uses `--tags deploy` for fast redeploys (`vi-jenkins-ansible-pipelines.md`).

## 8. Ad-hoc commands

```bash
# Restart service on all webservers
ansible webservers -i inventory/staging.ini -b -m service -a "name=nginx state=restarted"

# Gather facts
ansible webservers -i inventory/staging.ini -m setup
```

**Related:** `iv-roles-variables-and-vault.md`, `vii-deploy-patterns-and-operations.md`.
