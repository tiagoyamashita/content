---
label: "II"
subtitle: "Ansible の基礎"
group: "CI/CD"
order: 2
---
Ansible の基礎

**Ansible** は、エージェントレス構成管理ツール (Red Hat) です。 **望ましい状態**を YAML で記述します。 Ansible SSH をホストに接続し、状態が一致するまでモジュールを適用します。

## 1. CI/CD で Ansible を使用する理由

|メリット |説明 |
|----------|---------------|
| **エージェントレス** |ターゲットにはデーモンなし - SSH + Python のみ |
| **冪等** | 2 回目の実行では偽の変更は行われません。
| **宣言的** | 「nginx が存在します」は「apt install nginx」ではありません |
| **ポータブル** | Jenkins、ラップトップ、または AWX からの同じ Playbook |

## 2. 基本的な用語

|用語 |意味 |
|-----|----------|
| **制御ノード** | `ansible` / `ansible-playbook` を実行しているマシン (ラップトップ、CI エージェント) |
| **管理対象ノード** |構成中のターゲット ホスト |
| **在庫** |ホストとグループのリスト |
| **モジュール** |作業単位 (`apt`、`copy`、`service`、`template`) |
| **タスク** |引数を使用した 1 つのモジュール呼び出し |
| **プレイ** |ホスト + 順序付けされたタスク (+ ハンドラー) |
| **プレイブック** | 1 つ以上の再生を含む YAML ファイル |

## 3. エージェントレス接続

```bash
# Ad-hoc ping — verifies SSH + Python on targets
ansible webservers -i inventory.ini -m ping
```

| OS |接続 |
|----|-----------|
|リナックス | SSH (デフォルト)、sudo の場合は `become: true` |
|ウィンドウズ | WinRM (`ansible_connection=winrm`) |

管理対象ノードには **Python 3** が必要です (必要に応じて `raw` モジュール ブートストラップを介して新しいホストに最小限インストールします)。

## 4.冪等性

```yaml
- name: Ensure nginx installed
  ansible.builtin.apt:
    name: nginx
    state: present
```

|実行 |結果 |
|-----|----------|
|最初 | nginx をインストール → **変更** |
| 2番目 |すでに存在します → **ok** (変更なし) |

CI/CD では冪等性が重要です。部分的な障害が発生した後にデプロイを再実行するのは安全です。

## 5. モジュールとシェルコマンドの比較

**モジュールを優先します** - 変更/OK/失敗を報告し、エッジケースを処理します。

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

モジュールが適合しない場合は、**`command`/`shell`** を **`creates:`** または **`removes:`** ガードとともに使用してください。

## 6. チェックモード（ドライラン）

```bash
ansible-playbook site.yml --check --diff
```

申請しないと**何が変わる**のかを示します。PR レビューの段階で役立ちます。

## 7. プロジェクトのレイアウト (標準)

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

## 8. ansible.cfg の要点

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

Jenkins では、インベントリ ホストを信頼する場合にのみ `ANSIBLE_HOST_KEY_CHECKING=False` を設定します。 known_hosts または SSH キーを優先します。

**関連:** [インベントリとプレイブック](iii-inventory-and-playbooks.md)、[動的インベントリとモジュール](v-dynamic-inventory-and-modules.md)。
