---
label: "IV"
subtitle: "役割、変数、Vault"
group: "CI/CD"
order: 4
---
役割、変数、Vault

**ロール** パッケージの再利用可能な自動化。 **変数** 環境ごとのレイヤー構成。 **Ansible Vault** は、Git に保存されているシークレットを暗号化します。

## 1. ロールディレクトリのレイアウト

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

**postgres** ロール `tasks/main.yml`:

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

プレイブックでの使用:

```yaml
- hosts: dbservers
  roles:
    - role: postgres
      vars:
        postgres_version: "16"
```

## 2. 変数の優先順位 (低→高)

|優先順位 |出典 |
|----------|----------|
| 1 |役割 `defaults/main.yml` |
| 2 |在庫 `group_vars` / `host_vars` |
| 3 | `vars:` をプレイ |
| 4 |役割 `vars/main.yml` |
| 5 |タスク `vars:` |
| 6 | CLI の `-e` / `--extra-vars` |

**経験則:** はデフォルトで役割を果たします。 `group_vars/staging/` と `group_vars/production/` の環境オーバーライド。

## 3. group_vars 構造体

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

## 4. Ansible ボールト

リポジトリ内のシークレットを暗号化します。実行時にパスワードまたはキー ファイルを使用して復号化します。

```bash
# Encrypt entire file
ansible-vault encrypt group_vars/production/secrets.yml

# Encrypt single value inline
ansible-vault encrypt_string 'SuperSecretDbPass' --name 'db_password'
```

暗号化されたファイルヘッダー:

```yaml
# group_vars/production/secrets.yml (encrypted)
$ANSIBLE_VAULT;1.1;AES256
663864396538...
```

テンプレートで使用します (実行時に復号化されます):

```yaml
- name: Set DB password in app config
  ansible.builtin.template:
    src: application.yml.j2
    dest: /etc/myapp/application.yml
  vars:
    db_password: "{{ vault_db_password }}"
```

`_vault` プレフィックス規則を使用した `group_vars` からの参照、または暗号化された vars ファイルに含めます。

## 5. CI で Vault を使用して実行する

```bash
# Password file (Jenkins writes from credential)
ansible-playbook site.yml \
  --vault-password-file /tmp/vault_pass \
  -i inventory/production.ini

# Or prompt (interactive only)
ansible-playbook site.yml --ask-vault-pass
```

ボールトのパスワードを決してコミットしないでください。Jenkins **認証情報** [Jenkins + Ansible パイプライン](vi-jenkins-ansible-pipelines.md) に保存します。

## 6. 役割の依存関係

```yaml
# roles/myapp/meta/main.yml
dependencies:
  - role: common
  - role: nginx
    vars:
      nginx_port: 443
```

Ansible は、依存関係を宣言するロールの前に依存関係を実行します。

## 7. ansible-galaxy

コミュニティの役割をインストールします。

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

再現可能なビルドのために CI にバージョンを固定します。

## 8. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
|プレーン `group_vars` の秘密 |ボールトの暗号化 |
| Playbook 間でタスクをコピーアンドペーストする |役割の抽出 |
|すべてに`-e` | inventory/group_vars を使用する |
|巨大な一枚岩の役割 |懸念事項ごとに分割 (nginx、アプリ、ログ) |

**関連:** [インベントリとプレイブック](iii-inventory-and-playbooks.md)、[シークレットと OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)。
