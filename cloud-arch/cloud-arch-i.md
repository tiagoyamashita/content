---
label: "I"
subtitle: "Foundations"
group: "Cloud architecture"
order: 1
---
Cloud Architecture — Part I: Foundations
Service models, global infrastructure, compute, storage, networking, HA.

## 1. Cloud service models
Three layers of abstraction over physical hardware:

- IaaS (Infrastructure as a Service):
You manage: OS, runtime, app, data.
Provider manages: hypervisor, networking hardware, data-center.
Examples: EC2, Azure VMs, GCE.

- PaaS (Platform as a Service):
You manage: app code & data.
Provider manages: OS, runtime, scaling.
Examples: Heroku, Google App Engine, AWS Elastic Beanstalk.

- SaaS (Software as a Service):
You manage: configuration & data.
Provider manages: everything else.
Examples: Gmail, Salesforce, GitHub.

Rule of thumb: higher up the stack → less ops burden, less flexibility.


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


## 2. Global infrastructure
- Region: independent geographic area (e.g. us-east-1, eu-west-1).
– Chosen for latency, compliance (data residency), and service availability.
– Resources in one region do not automatically replicate to another.

- Availability Zone (AZ): one or more physically separate data centers
within a region, connected by low-latency private links.
– Deploy across ≥ 2 AZs to survive a single data-center failure.

- Edge / PoP (Point of Presence): CDN cache nodes close to end users.
– AWS CloudFront, Azure CDN, Cloudflare — serve static assets & cache.

Mental model:
Region → [AZ-a, AZ-b, AZ-c]  (typically 3 AZs per region)
each AZ → one or more physical data centers
Edge PoPs → globally distributed (100s of locations)

## 3. Compute options
Three main patterns, ordered by abstraction:

a) Virtual Machines (IaaS):
- Full OS, persistent, always-on billing.
- Best for: lift-and-shift workloads, stateful services, custom OS config.
- AWS EC2, Azure VMs, GCE.

b) Containers / orchestration (IaaS ↔ PaaS boundary):
- Docker image + container runtime; Kubernetes for scheduling.
- Managed K8s: EKS, AKS, GKE — provider handles the control plane.
- Best for: microservices, portable workloads, predictable density.

c) Serverless / FaaS:
- Upload a function; provider handles runtime, scaling, patching.
- Billing per invocation + duration (millisecond granularity).
- Cold start: first invocation after idle has extra latency (~100 ms–1 s).
- Best for: event-driven work, sporadic traffic, glue code.
- AWS Lambda, Azure Functions, Google Cloud Functions.

## 4. Storage & databases
Object storage (blob):
- Flat namespace, HTTP PUT/GET, cheap at scale.
- AWS S3, Azure Blob, GCS — the default for static assets, backups, data lakes.
- Durability: 11 nines (S3 standard) — achieved via erasure coding across AZs.

Block storage:
- Attached to a VM like a hard drive; low latency random I/O.
- AWS EBS, Azure Managed Disks — use for database volumes.

File storage (NFS):
- Shared file system mountable by many VMs simultaneously.
- AWS EFS, Azure Files.

Relational (RDS / Cloud SQL / Azure SQL):
- Managed PostgreSQL / MySQL / SQL Server.
- Multi-AZ for HA; read replicas for read scale-out.

NoSQL:
- Key-value: DynamoDB, Redis (ElastiCache) — single-digit ms reads.
- Document: MongoDB Atlas, Firestore.
- Wide-column: Cassandra, Bigtable — time-series / IoT at scale.

## 5. Networking fundamentals
VPC (Virtual Private Cloud):
- Logically isolated network you define (CIDR range, subnets, route tables).
- Public subnet: has route to Internet Gateway → instances can get public IPs.
- Private subnet: no direct internet route → reach internet via NAT Gateway.

Load balancers:
- L4 (TCP/UDP): fast, low overhead — AWS NLB.
- L7 (HTTP/HTTPS): path-based routing, SSL termination, WAF — AWS ALB.
- Distribute traffic across targets in multiple AZs for fault tolerance.

DNS & CDN:
- Route 53 / Azure DNS — authoritative DNS with health checks & failover.
- CloudFront / Akamai / Cloudflare — cache at edge, reduce origin load.

Security groups & NACLs:
- Security group: stateful, per-instance firewall (allow rules only).
- NACL: stateless, per-subnet — explicit allow + deny, evaluated in order.

## 6. High availability & disaster recovery
Key metrics:
- RTO (Recovery Time Objective): max acceptable downtime after failure.
- RPO (Recovery Point Objective): max acceptable data loss (time window).

HA patterns:
- Multi-AZ active-active: traffic load-balanced across AZs at all times.
- Multi-AZ active-passive: standby promoted on failure (higher RTO).
- Auto Scaling Group: replace unhealthy instances automatically.

DR tiers (cheapest → fastest recovery):
- Backup & restore: periodic snapshots to object storage. High RTO/RPO.
- Pilot light: minimal running infrastructure; scale up on disaster.
- Warm standby: reduced-capacity replica always running; scale on failover.
- Active-active multi-region: lowest RTO/RPO; highest cost.

## 7. Well-Architected pillars
AWS Well-Architected Framework — six pillars (also applies to Azure/GCP):

1. Operational Excellence:
Run and monitor systems; refine processes.
→ IaC, small reversible changes, runbooks, observability.

2. Security:
Protect data and systems.
→ Least privilege IAM, encryption at rest & in transit, audit logs.

3. Reliability:
Recover from failures, meet demand.
→ Multi-AZ, auto scaling, health checks, circuit breakers.

4. Performance Efficiency:
Use resources efficiently; adapt to change.
→ Right-size instances, use managed services, benchmark regularly.

5. Cost Optimization:
Avoid unnecessary spend.
→ Reserved/Spot instances, auto scaling, delete idle resources.

6. Sustainability:
Minimize environmental impact.
→ Maximize utilization, prefer managed services, right-size aggressively.

## 8. Remember & rehearse
- What is the difference between IaaS, PaaS, and SaaS? Give one example each.
- What is an Availability Zone and why should you deploy across multiple AZs?
- Compare object storage vs block storage — when would you use each?
- What is a VPC? Explain public vs private subnet.
- Define RTO and RPO. What DR strategy gives you the lowest RTO?
- Name the six Well-Architected pillars.
- What is a cold start in serverless and why does it happen?
