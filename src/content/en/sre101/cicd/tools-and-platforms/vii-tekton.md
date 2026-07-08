---
label: "VII"
subtitle: "Tekton"
group: "CI/CD"
order: 7
---
Tekton
**Kubernetes-native** CI/CD — pipelines as **CRDs** (`Pipeline`, `PipelineRun`, `Task`). Composable, GitOps-friendly; no built-in UI (use OpenShift Pipelines, Argo, or custom dashboards).

## 1. Core resources

| Resource | Role |
|----------|------|
| **Task** | Unit of work (build, test, deploy) |
| **Pipeline** | Ordered / parallel graph of Tasks |
| **PipelineRun** | One execution instance |
| **Workspace** | Shared volume between Tasks |
| **Trigger** | EventListener + Binding — webhook → PipelineRun |

## 2. Simple Task (run tests)

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

## 3. Pipeline chaining Tasks

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

## 4. PipelineRun (manual trigger)

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

## 5. Triggers (GitHub webhook)

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

Install **EventListener** + Ingress for `POST /hook`.

## 6. Tekton vs SaaS CI

| | Tekton | GitHub Actions |
|---|--------|----------------|
| Runs on | Your K8s cluster | Managed runners |
| Config | YAML CRDs in cluster | Workflow in repo |
| UI | Bring your own | Built-in |
| Multi-tenant | Namespace isolation | Org/repo scoped |

## 7. When to choose Tekton

| Pros | Cons |
|------|------|
| Same cluster as apps — no outbound runner fleet | Steeper setup |
| GitOps: apply Pipeline YAML from repo | Debugging requires `tkn` / kubectl |
| Reusable **Catalog** Tasks | No batteries-included registry |

| Good fit | Less ideal |
|----------|------------|
| Platform team on Kubernetes | Small team, GitHub-only |
| OpenShift Pipelines already licensed | No K8s in org |

**Related:** **Terraform** submenu → [Terraform in CI/CD](../terraform/vii-terraform-in-cicd.md) (cluster infra), [Docker in CI](v-docker-in-ci.md) (Kaniko builds).
