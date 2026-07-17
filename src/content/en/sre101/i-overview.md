---
label: "I Overview"
group: "SRE101"
order: 1
---
SRE101 — overview
**Site reliability / platform engineering** notes: how software gets built, shipped, and kept alive in production — CI/CD, cloud architecture, and observability tooling.

Assumes you can write an app; this track is about **delivery and operations**.

## Map of SRE101

| Submenu | Focus |
|---------|--------|
| [**CI/CD**](cicd/i-fundamentals.md) | Pipelines, Terraform, Ansible/Jenkins, security gates |
| [**Cloud architecture**](cloud-architecture/foundations/i-overview.md) | Cloud foundations, patterns & design |
| [**Tooling**](tooling/prometheus/i-intro-and-architecture.md) | Prometheus, Grafana, Alertmanager, Loki, Kubernetes, Terraform |

## CI/CD

| Area | Focus |
|------|--------|
| [Fundamentals](cicd/i-fundamentals.md) | What CI/CD is and why it matters |
| [Tools & platforms](cicd/tools-and-platforms/i-overview.md) | GitHub Actions, GitLab CI, Jenkins, and friends |
| [Terraform](cicd/terraform/i-overview.md) | Infra as code in the pipeline |
| [Ansible & Jenkins](cicd/ansible-and-jenkins/i-overview.md) | Config management and classic CI |
| [Security & best practices](cicd/security-and-best-practices/i-overview.md) | Supply chain, secrets, OIDC, gates |

## Cloud architecture

| Area | Focus |
|------|--------|
| [Foundations](cloud-architecture/foundations/i-overview.md) | Regions, compute, storage, networking |
| [Patterns & design](cloud-architecture/patterns-and-design/i-overview.md) | Scalability, microservices, observability, cost |

## Tooling

| Area | Focus |
|------|--------|
| [Prometheus](tooling/prometheus/i-intro-and-architecture.md) | Metrics and PromQL |
| [Grafana](tooling/grafana/i-intro.md) | Dashboards |
| [Alertmanager](tooling/alertmanager/i-intro.md) | Routing alerts |
| [Loki](tooling/iv-loki.md) | Log aggregation |
| [Kubernetes](tooling/kubernetes/i-intro-and-architecture.md) | Workloads and ops |
| [Terraform](tooling/terraform/i-intro-and-architecture.md) | CLI workflow and state |

## Suggested order

```text
CI/CD fundamentals → Tools & platforms
  → Cloud foundations → Patterns & design
  → Prometheus / Grafana (observe what you ship)
  → Kubernetes when you run containers at scale
```

## How this relates to other tracks

| Track | Overlap |
|-------|---------|
| [SWE101](../swe101/i-overview.md) | Apps and APIs you deploy |
| [CS101 networking](../cs101/networking/i-tcp-udp-and-transport-basics.md) | L4/L7, DNS, TLS under the cloud LB |
| [Cybersecurity](../cybersecurity/i-overview.md) | Identity, secrets, incident response |
