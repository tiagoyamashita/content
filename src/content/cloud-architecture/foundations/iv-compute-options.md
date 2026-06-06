---
label: "IV"
subtitle: "Compute options"
group: "Cloud architecture"
order: 4
---
Compute options
Cloud **compute** ranges from full **VMs** to **functions**. Pick based on control, portability, traffic pattern, and ops capacity.

## 1. Spectrum of abstraction

```text
More control                                                          Less ops
    │                                                                      │
    VM ──▶ Container (K8s) ──▶ PaaS (managed runtime) ──▶ FaaS (Lambda)
```

| Option | Billing | Best for |
|--------|---------|----------|
| **VM (IaaS)** | Per second/hour while running | Lift-and-shift, stateful, custom OS |
| **Containers** | Cluster + nodes | Microservices, portable workloads |
| **Serverless** | Per invocation + duration | Event-driven, sporadic traffic |

## 2. Virtual machines

Full OS instance — persistent, always-on (unless stopped).

| Cloud | Service |
|-------|---------|
| AWS | EC2 |
| Azure | Virtual Machines |
| GCP | Compute Engine |

```text
EC2 instance
  ├── instance type: t3.micro, m6i.xlarge (CPU/RAM profile)
  ├── AMI: Amazon Linux, Ubuntu, Windows
  ├── EBS volume: root + data disks
  └── security group + subnet
```

| Strength | Weakness |
|----------|----------|
| Full control | You patch OS, size instances |
| Any software stack | Slower scale-out than containers/serverless |
| Predictable for steady load | Pay while idle |

**Use when:** legacy apps, licensed software, GPU workloads, strong isolation needs.

## 3. Containers and Kubernetes

**Docker** packages app + dependencies; **Kubernetes** schedules containers across nodes.

| Managed K8s | Provider runs control plane |
|-------------|----------------------------|
| **EKS** | AWS |
| **AKS** | Azure |
| **GKE** | GCP |

```yaml
# Simplified Deployment — 3 replicas across AZs
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: registry.example.com/api:1.2.3
          resources:
            requests: { cpu: "250m", memory: "512Mi" }
            limits:   { cpu: "500m", memory: "1Gi" }
```

| Strength | Weakness |
|----------|----------|
| Portable images | K8s learning curve |
| Dense packing on nodes | You manage manifests/Helm |
| Fast scale pods | Cluster ops (even managed) |

**Use when:** microservices, need portable deploy across envs, team has K8s skills.

**Lighter alternatives:** ECS Fargate, Cloud Run, Azure Container Apps — less YAML, more opinionated.

## 4. Serverless / FaaS

Upload a **function**; provider handles runtime, scaling, patching.

| Cloud | Service |
|-------|---------|
| AWS | Lambda |
| Azure | Functions |
| GCP | Cloud Functions / Cloud Run (container-based) |

```python
# AWS Lambda handler (conceptual)
def handler(event, context):
    order_id = event["orderId"]
    process_order(order_id)
    return {"statusCode": 200}
```

**Billing:** per invocation + GB-seconds of memory × duration.

## 5. Cold start

First invocation after idle incurs extra latency — provider must:

1. Allocate sandbox
2. Download deployment package / start container
3. Initialize runtime (JVM especially slow)

| Runtime | Typical cold start |
|---------|-------------------|
| Node.js / Python | ~100–300 ms |
| Java / .NET | ~500 ms–2 s |
| VPC-attached Lambda | + ENI setup (historically slower) |

| Mitigation | How |
|------------|-----|
| **Provisioned concurrency** | Keep N warm instances |
| **Smaller package** | Trim dependencies |
| **SnapStart** (Java on Lambda) | Snapshot init phase |
| **Avoid VPC** unless needed | Or use newer hyperplane ENI |

**Use serverless when:** event triggers (S3 upload, queue message, API sporadic traffic), glue/ETL, webhooks.

**Avoid when:** strict sub-10 ms latency always, long-running compute, heavy state in memory.

## 6. Comparison table

| | VM | K8s pod | Lambda |
|---|-----|---------|--------|
| Scale speed | Minutes (ASG) | Seconds | Milliseconds |
| Max duration | Unlimited | Unlimited | 15 min (Lambda) |
| State | Local disk | Ephemeral | Ephemeral |
| Cost at zero traffic | Still paying | Node baseline | ~$0 |

## 7. Decision flow

```text
Need custom OS/kernel?     → VM
Team on K8s, many services? → EKS/GKE/AKS
HTTP API with variable traffic? → Lambda or Cloud Run
Batch nightly job?          → Spot VM or Lambda
```

## 8. Example architecture mix

| Component | Compute choice |
|-----------|----------------|
| Public REST API | Lambda + API Gateway OR K8s + ALB |
| Background workers | K8s Deployment or Lambda from SQS |
| PostgreSQL | RDS (managed VM) — not Lambda |
| Redis cache | ElastiCache (managed) |

**Related:** `ii-service-models.md`, patterns `ii-scalability-and-caching.md`.
