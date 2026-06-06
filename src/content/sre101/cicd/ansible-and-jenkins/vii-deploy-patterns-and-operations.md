---
label: "VII"
subtitle: "パターンとオペレーションをデプロイする"
group: "CI/CD"
order: 7
---
パターンとオペレーションをデプロイする

運用環境のデプロイには、*冪等のプレイブック**、明確な**ステージング/本番**の分離、および Jenkins がダウンしている場合のホットフィックス用の **CLI パス**が必要です。

## 1. 最小限のデプロイ プレイブック

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

|設定 |目的 |
|----------|----------|
| `serial: 1` |ローリング デプロイ - 一度に 1 台のサーバー |
| `serial: "25%"` |バッチあたりのフリートの 4 分の 1 |
| `tags: [deploy]` | Jenkins は `--tags deploy` のみを実行します。

## 2. ローリング デプロイ図

<figure class="notes-diagram"><svg xmlns="31 viewBox="0 0 400 100" role="img" aria-label="Rolling deploy serial one">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">serial: 1 — update web1, then web2, then web3</text>
  <rect x="12" y="40" width="56" height="36" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="24" y="62" fill="#e4e4e7" font-size="9">web1 ✓</text>
  <rect x="80" y="40" width="56" height="36" rx="3" fill="rgba(251,191,36,0.2)" stroke="#fbbf24"/>
  <text x="92" y="62" fill="#e4e4e7" font-size="9">web2 …</text>
  <rect x="148" y="40" width="56" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="160" y="62" fill="#71717a" font-size="9">web3</text>
  <text x="12" y="92" fill="#71717a" font-size="9">Load balancer keeps serving healthy nodes during rollout</text>
</svg></figure>

## 3. ステージングと本番環境

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

ステージング ボールト ファイルでは本番環境の秘密を決して共有しないでください。個別の **`ansible-vault`** パスワードまたは **`vault_id`** ラベルを使用してください。

## 4. Jenkins を使用しないホットフィックス

ラップトップからの同じプレイブック (ブレークグラス):

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

|ステップ |アクション |
|------|----------|
| 1 |ホットフィックス JAR をローカルでビルドするか、CI アーティファクトからプルする |
| 2 | `--limit` 最初に 1 つのカナリア ホスト |
| 3 |健全性/メトリクスを確認する |
| 4 |フルフリートの場合は `--limit` を削除 |

これをランブックに文書化します。インシデント発生中、運用は Jenkins UI に依存すべきではありません。

## 5. Ansible を使用したブルー/グリーン (VM パターン)

2 つのアプリ ディレクトリ — シンボリックリンクを切り替えます。

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

ロールバック = シンボリックリンクを以前のリリースのディレクトリに再ポイントし、ハンドラーを再起動します。

## 6. 事前デプロイタグとデプロイタグ

|タグ | | の場合に実行されます。タスク |
|-----|-----------|------|
| `packages` |毎週または新しいホスト | JDK、nginxのインストール |
| `config` |構成変更 PR |テンプレート、systemd ユニット |
| `deploy` |リリースごと | JAR をコピーし、再起動します。

```bash
# Full configure (new server)
ansible-playbook site.yml

# Fast path (CI)
ansible-playbook deploy.yml --tags deploy
```

## 7. リリースゲートとの統合

[ゲートとロールバックのリリース](../security-and-best-practices/vii-release-gates-and-rollbacks.md) と調整します。

- 本番プレイブック前のジェンキンス **`input`**
- **`app_version=${BUILD_NUMBER}`** または git SHA のデプロイ — 不変参照
- ヘルスチェックタスクがプレイブックに失敗する → 自動 Jenkins ステージが失敗する
- Playbook または以前の **`app_version`** 追加変数をロールバックします

## 8. 操作チェックリスト

- [ ] Git のインベントリは実際のフリート (または新しい動的プラグイン) と一致します
- マージ前の設定変更に関する [ ] `--check`
- [ ] `ansible-lint` (CI)
- [ ] Vault シークレットがスケジュールに従ってローテーションされました
- [ ] Hotfix Runbook は Jenkins を使用せずにテストされました
- [ ] `serial` は本番環境のローリング アップデートに設定されています

## 9. リハーサルの答え

- **ハンドラー** — 通知されたタスクが変更された場合、最後に 1 回実行されます (例: 構成コピー後の再起動)。
- **`when { branch 'main' }`** — デプロイ ステージをメイン ブランチ ビルドに制限します。
- **Jenkins からの Vault** — `credentials('ansible-vault-pass')` + `--vault-password-file`。
- **postgres ロール レイアウト** — `tasks/`、`handlers/`、`templates/`、`defaults/`、`vars/`、`meta/`。

**関連:** [Jenkins + Ansible パイプライン](vi-jenkins-ansible-pipelines.md)、[インベントリとプレイブック](iii-inventory-and-playbooks.md)。
