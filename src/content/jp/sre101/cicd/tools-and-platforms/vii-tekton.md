---
label: "VII"
subtitle: "テクトン"
group: "CI/CD"
order: 7
---
テクトン

**Kubernetes ネイティブ** CI/CD — **CRD** としてのパイプライン (`Pipeline`、`PipelineRun`、`Task`)。コンポーザブルで GitOps フレンドリー。組み込みの UI はありません (OpenShift Pipelines、Argo、またはカスタム ダッシュボードを使用します)。

## 1. コアリソース

|リソース |役割 |
|----------|------|
| **タスク** |作業単位 (ビルド、テスト、デプロイ) |
| **パイプライン** |タスクの順序付き/並列グラフ |
| **パイプライン実行** | 1 つの実行インスタンス |
| **ワークスペース** |タスク間の共有ボリューム |
| **トリガー** | EventListener + バインディング — Webhook → PipelineRun |

## 2. 単純なタスク (テストの実行)

```yaml
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: npm-test
spec:
  params:
    - name: package
      type: string
      default: .
  workspaces:
    - name: source
  steps:
    - name: install-and-test
      image: node:22-bookworm
      workingDir: $(workspaces.source.path)/$(params.package)
      script: |
        #!/bin/sh
        npm ci
        npm test
```

## 3. パイプラインチェーンタスク

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: build-and-deploy
spec:
  workspaces:
    - name: shared-data
  params:
    - name: image
      type: string
  tasks:
    - name: fetch
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: shared-data

    - name: test
      runAfter: [fetch]
      taskRef:
        name: npm-test
      workspaces:
        - name: source
          workspace: shared-data

    - name: build-push
      runAfter: [test]
      taskRef:
        name: kaniko
      params:
        - name: IMAGE
          value: $(params.image)
      workspaces:
        - name: source
          workspace: shared-data
```

## 4. PipelineRun (手動トリガー)

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  generateName: build-and-deploy-run-
spec:
  pipelineRef:
    name: build-and-deploy
  params:
    - name: image
      value: registry.example.com/myapp:abc123
  workspaces:
    - name: shared-data
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 1Gi
```

```bash
kubectl create -f pipelinerun.yaml
tkn pipelinerun logs -f
```

## 5. トリガー (GitHub Webhook)

```yaml
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: pr-build
spec:
  params:
    - name: gitrevision
    - name: gitrepositoryurl
  resourcetemplates:
    - apiVersion: tekton.dev/v1
      kind: PipelineRun
      metadata:
        generateName: pr-run-
      spec:
        pipelineRef:
          name: build-and-deploy
        # bind params from webhook body...
```

**EventListener** + Ingress を `POST /hook` にインストールします。

## 6. Tekton 対 SaaS CI

| |テクトン | GitHub アクション |
|---|--------|----------------|
|実行日 | K8s クラスター |管理ランナー |
|構成 | YAML クラスター内の CRD |リポジトリ内のワークフロー |
| UI |自分のものを持参してください |内蔵 |
|マルチテナント |名前空間の分離 |組織/リポジトリのスコープ |

## 7. テクトンを選択する場合

|長所 |短所 |
|------|------|
|アプリと同じクラスター - アウトバウンド ランナー フリートなし |より急峻なセットアップ |
| GitOps: リポジトリからパイプライン YAML を適用する |デバッグには `tkn` / kubectl | が必要です。
|再利用可能な **カタログ** タスク |電池を含むレジストリはありません |

|良いフィット感 |あまり理想的ではない |
|----------|-----------|
| Kubernetes のプラットフォーム チーム |小規模チーム、GitHub のみ |
| OpenShift Pipelines はすでにライセンスを取得済み |組織に K8 がありません |

**関連:** **Terraform** サブメニュー → [CI/CD の Terraform](../terraform/vii-terraform-in-cicd.md) (クラスター インフラ)、[CI の Docker](v-docker-in-ci.md) (Kaniko ビルド)。
