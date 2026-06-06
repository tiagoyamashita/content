---
label: "V"
subtitle: "動的なインベントリとモジュール"
group: "CI/CD"
order: 5
---
動的なインベントリとモジュール

静的 INI ファイルは、固定フリートで機能します。 **動的インベントリ**は、**AWS、Azure、GCP**、またはカスタム スクリプトからライブ ホスト リストを取得します。

## 1. AWS EC2 動的インベントリ

コレクションをインストールします。

```bash
ansible-galaxy collection install amazon.aws
```

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: staging
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: aws_region
hostnames:
  - tag:Name
compose:
  ansible_host: private_ip_address
```

走る：

```bash
ansible-playbook -i inventory/aws_ec2.yml playbooks/site.yml
```

|メリット |詳細 |
|----------|----------|
|自動検出 | `Role=web` タグが付いた新しい EC2 インスタンスがグループに参加します |
|手動編集なし |終了したインスタンスがインベントリから削除される |
| CI フレンドリー | IAM ロールを持つ Jenkins エージェントが AWS API をクエリする |

## 2. Azure / GCP プラグイン (スケッチ)

```yaml
# Azure — azure.azcollection.azure_rm
plugin: azure.azcollection.azure_rm
include_vm_resource_groups:
  - myapp-staging-rg
```

```yaml
# GCP — google.cloud.gcp_compute
plugin: google.cloud.gcp_compute
projects:
  - my-project-id
filters:
  - status = RUNNING
  - labels.env = staging
```

制御ノードで **サービス アカウント** または **OIDC** 資格情報を使用します。これは、CI [シークレットと OIDC](../security-and-best-practices/iii-secrets-and-oidc.md) と同じ最小特権の考え方です。

## 3. 共通モジュールのリファレンス

|モジュール |目的 |例 |
|----------|-----------|----------|
| `apt` / `yum` |パッケージ | `name: nginx state: present` |
| `copy` |制御ノードからファイルをプッシュ | JAR アーティファクトをサーバーへ |
| `template` | Jinja2 レンダリング → ファイル | nginx.conf |
| `service` / `systemd` |サービス状態 | `state: restarted` |
| `user` / `group` |アカウント |アプリサービスユーザー |
| `file` |ディレクトリ、シンボリックリンク、権限 | `/opt/myapp` |
| `get_url` |リモート ファイルをダウンロード |リリース tarball を取得する |
| `uri` | HTTP チェック |導入後の健全性プローブ |
| `wait_for` |ポートが開くのを待ちます | 8080 でリッスンするアプリ |

## 4. ヘルスチェックの例をデプロイする

```yaml
- name: Restart application
  ansible.builtin.systemd:
    name: myapp
    state: restarted

- name: Wait for app port
  ansible.builtin.wait_for:
    port: 8080
    host: 127.0.0.1
    delay: 2
    timeout: 60

- name: HTTP health check
  ansible.builtin.uri:
    url: http://127.0.0.1:8080/actuator/health
    status_code: 200
  register: health
  retries: 5
  delay: 10
  until: health.status == 200
```

健全性が決して通過しない場合、プレイブックは失敗します。Jenkins ステージは失敗し、サイレント不良デプロイは発生しません。

## 5. CI の ansible-lint

デプロイ前にスタイルエラーと危険なパターンをキャッチします。

```bash
pip install ansible-lint
ansible-lint playbooks/
```

```yaml
# .ansible-lint
profile: production
skip_list:
  - yaml[line-length]
```

ジェンキンスのステージ:

```groovy
stage('Ansible Lint') {
  steps {
    sh 'ansible-lint playbooks/ roles/'
  }
}
```

|ルールクラス |キャッチ |
|-----------|-----------|
| `risky-shell-pipe` |安全でないシェル |
| `no-changed-when` |誤解を招く変更レポート |
| `command-instead-of-module` |非冪等コマンド |

## 6. 分子 (オプションの役割テスト)

実サーバーを使用せずに Docker でロールをテストします。

```bash
cd roles/myapp
molecule test
```

作成→収束→検証→破棄を実行します。ロール作成者には適していますが、単純なデプロイ リポジトリには重くなります。

## 7. パフォーマンスのヒント

|ヒント |なぜ |
|-----|-----|
| `strategy: free` |大規模なフリートで高速化 (順序なし) |
| `--forks 20` |パラレル SSH (デフォルト 5) |
| ansible.cfg の `pipelining = True` | SSH 往復の削減 |
|ファクトキャッシュ |繰り返しスキップ `setup` |

**関連:** [Ansible の基礎](ii-ansible-fundamentals.md)、[Jenkins + Ansible パイプライン](vi-jenkins-ansible-pipelines.md)。
