---
label: "III"
subtitle: "インベントリとプレイブック"
group: "CI/CD"
order: 3
---
インベントリとプレイブック

**インベントリ**は、Ansible が管理する**ホスト**を定義します。 **プレイブック**は、**何を**構成するかを定義します。

## 1. 静的インベントリ (INI)

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

|パターン |使用 |
|----------|-----|
| `[group]` |論理層 (Web、DB、キャッシュ) |
| `[group:vars]` |グループ内のすべてのホストの変数 |
| `[parent:children]` |ネストグループ (`staging` には Web + データベースが含まれます) |
| `ansible_host` | DNS エイリアスと実際の IP |

## 2. YAML インベントリー (代替)

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

## 3. 完全なプレイブックの例

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

走る：

```bash
ansible-playbook -i inventory/staging.ini playbooks/site.yml
```

デバッグ中は 1 つのホストに制限します。

```bash
ansible-playbook -i inventory/staging.ini playbooks/site.yml --limit web1.staging.example.com
```

## 4. ハンドラー

ハンドラーは、タスクが **通知**し、**変更が報告された**場合にのみ、**プレイ終了時に 1 回**実行されます。

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

|コンセプト |行動 |
|----------|----------|
| **通知** |タスクが変更された場合のキュー ハンドラー |
| **聞いてください** |複数の通知で 1 つのハンドラー名をトリガーできます。
| **flush_handlers** |プレイ中にハンドラーを実行するメタタスク |

## 5. Jinja2 テンプレート

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

**`ansible_hostname`**、**`ansible_default_ipv4`** などの組み込みファクトは、セットアップ モジュールから取得されます。

## 6. 条件文とループ

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

## 7. タグ — タスクのサブセットを実行する

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

Jenkins は高速再デプロイに `--tags deploy` を使用します [Jenkins + Ansible パイプライン](vi-jenkins-ansible-pipelines.md)。

## 8. アドホックコマンド

```bash
# Restart service on all webservers
ansible webservers -i inventory/staging.ini -b -m service -a "name=nginx state=restarted"

# Gather facts
ansible webservers -i inventory/staging.ini -m setup
```

**関連:** [ロール、変数、および Vault](iv-roles-variables-and-vault.md)、[デプロイ パターンと操作](vii-deploy-patterns-and-operations.md)。
