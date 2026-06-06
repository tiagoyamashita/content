---
label: "II"
subtitle: "Service models"
group: "Cloud architecture"
order: 2
---
Service models — IaaS, PaaS, SaaS
Cloud providers abstract hardware in **layers**. Higher layers mean **less ops burden** and **less low-level control**.

## 1. Three models

| Model | You manage | Provider manages | Examples |
|-------|------------|------------------|----------|
| **IaaS** | OS, runtime, app, data | Hypervisor, hardware, DC | EC2, Azure VMs, GCE |
| **PaaS** | App code & data | OS, runtime, scaling | App Engine, Elastic Beanstalk, Heroku |
| **SaaS** | Config & your data | Everything else | Gmail, Salesforce, GitHub |

```text
Responsibility stack (bottom = always provider):

  SaaS     │████████████████│  you: config only
  PaaS     │████████░░░░░░░░│  you: app + data
  IaaS     │████░░░░░░░░░░░░│  you: OS through app
           └────────────────┘
           Hardware / virtualization
```

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 140" role="img" aria-label="IaaS PaaS SaaS responsibility stack">
  <rect x="20" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="80" y="27" fill="#86efac" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">IaaS</text>
  <rect x="160" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="220" y="27" fill="#fbbf24" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">PaaS</text>
  <rect x="300" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="360" y="27" fill="#60a5fa" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">SaaS</text>
  <text x="220" y="68" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">← more control          less ops burden →</text>
  <rect x="20" y="82" width="400" height="18" rx="3" fill="#18181b"/>
  <text x="220" y="95" fill="#52525b" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Physical hardware / data center (always provider-managed)</text>
  <rect x="20" y="106" width="400" height="18" rx="3" fill="#1c1c1f"/>
  <text x="220" y="119" fill="#52525b" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Hypervisor / virtualization</text>
</svg></figure>

## 2. Shared responsibility model

Security and compliance are **always shared** — even in SaaS you configure access and protect credentials.

| Area | IaaS | PaaS | SaaS |
|------|------|------|------|
| Physical security | Provider | Provider | Provider |
| Network patching | Provider | Provider | Provider |
| OS patching | **You** | Provider | Provider |
| App vulnerabilities | **You** | **You** | Shared |
| Identity & access | **You** | **You** | **You** |
| Data encryption | **You** | **You** | Often shared |

## 3. Choosing a model

| Situation | Lean toward |
|-----------|-------------|
| Lift-and-shift legacy app | IaaS (EC2) |
| Standard web app, minimal ops | PaaS (Cloud Run, Elastic Beanstalk) |
| Email, CRM, source control | SaaS |
| Need custom kernel modules | IaaS |
| Spiky event processing | Serverless/FaaS (PaaS family) |

## 4. FaaS as PaaS extreme

**Functions as a Service** (Lambda, Cloud Functions) — you upload code; provider runs and scales it. See [Compute options](iv-compute-options.md).

## 5. Hybrid and multi-cloud

| Term | Meaning |
|------|---------|
| **Hybrid** | On-prem + cloud (VPN/Direct Connect) |
| **Multi-cloud** | AWS + Azure for redundancy or vendor mix |
| **Cloud-native** | Designed for cloud APIs from the start |

IaaS flexibility helps hybrid; SaaS reduces integration burden.

## 6. Cost implication

| Model | Typical billing |
|-------|-----------------|
| IaaS | Per hour/second VM, attached disks |
| PaaS | App instance hours or request units |
| SaaS | Per seat / per feature tier |

Higher abstraction often improves **utilization** — you pay for what you use, not idle OS patching time.

## 7. Examples mapped

| Workload | Model | Service |
|----------|-------|---------|
| Custom Java on Linux | IaaS | EC2 + EBS |
| Spring Boot container | IaaS/PaaS boundary | EKS, Cloud Run |
| Static site + API | PaaS | S3 + API Gateway + Lambda |
| Company email | SaaS | Google Workspace |

**Related:** [Compute options](iv-compute-options.md), [Well-Architected Framework](viii-well-architected-framework.md).
