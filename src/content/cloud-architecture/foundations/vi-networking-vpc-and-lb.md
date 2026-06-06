---
label: "VI"
subtitle: "Networking, VPC & LB"
group: "Cloud architecture"
order: 6
---
Networking, VPC & load balancing
A **VPC** is your private network in the cloud. **Subnets**, **load balancers**, and **firewalls** control where traffic flows and who can reach what.

## 1. VPC basics

**Virtual Private Cloud** — logically isolated network you define.

| Cloud | Name |
|-------|------|
| AWS | VPC |
| Azure | Virtual Network (VNet) |
| GCP | VPC Network |

```text
VPC CIDR: 10.0.0.0/16
  ├── public subnet  10.0.1.0/24  (AZ-a)  → route to Internet Gateway
  ├── public subnet  10.0.2.0/24  (AZ-b)
  ├── private subnet 10.0.11.0/24 (AZ-a)  → NAT Gateway for outbound
  └── private subnet 10.0.12.0/24 (AZ-b)  → app + DB tiers
```

## 2. Public vs private subnet

| | Public subnet | Private subnet |
|---|---------------|----------------|
| **Route to internet** | Via Internet Gateway (IGW) | No direct inbound from internet |
| **Typical resources** | ALB, bastion (if used) | App servers, databases |
| **Inbound from web** | Through LB in public tier | LB forwards to private targets |

```text
Internet ──▶ IGW ──▶ ALB (public subnet)
                         │
                         └──▶ EC2 targets (private subnet)

Private EC2 outbound: private subnet ──▶ NAT GW (public subnet) ──▶ IGW
```

**NAT Gateway** cost note: hourly + data processing — use **VPC endpoints** for S3/DynamoDB to avoid NAT for AWS API traffic.

## 3. Load balancers

Distribute traffic across targets in **multiple AZs**.

| Layer | Name | Routes on | AWS example |
|-------|------|-----------|-------------|
| **L4** | Transport | IP + port (TCP/UDP) | NLB |
| **L7** | Application | HTTP path, host header | ALB |

```text
Client HTTPS ──▶ ALB (SSL termination)
                    ├── /api/*  → target group A (API pods)
                    └── /*      → target group B (static S3 via IP targets)
```

| Feature | ALB (L7) | NLB (L4) |
|---------|----------|----------|
| Path routing | Yes | No |
| WebSockets / HTTP/2 | Yes | TCP pass-through |
| Static IP | Via NLB | Yes |
| Latency | Slightly higher | Ultra-low |

**Health checks** — LB removes unhealthy targets; pairs with Auto Scaling.

## 4. DNS

| Cloud | Service | Features |
|-------|---------|----------|
| AWS | Route 53 | Health checks, failover, geo routing |
| Azure | Azure DNS | |
| GCP | Cloud DNS | |

```text
api.example.com  CNAME  →  myapp-alb-123.us-east-1.elb.amazonaws.com
                           (alias record in Route 53)
```

| Routing policy | Use |
|----------------|-----|
| **Simple** | Single resource |
| **Weighted** | Canary % traffic |
| **Failover** | Primary + secondary health-checked |
| **Geolocation** | EU users → EU endpoint |

See networking DNS notes for global API zoning.

## 5. CDN (edge)

**CloudFront**, **Azure CDN**, **Cloudflare** — cache at edge PoPs (`iii-regions-azs-and-edge.md`).

```text
User ──▶ CloudFront edge (cache HIT) → fast
User ──▶ CloudFront edge (MISS) ──▶ origin (ALB or S3)
```

## 6. Security groups vs NACLs

| | Security group | NACL |
|---|----------------|------|
| **Scope** | Instance / ENI | Subnet |
| **State** | Stateful (return traffic auto-allowed) | Stateless |
| **Rules** | Allow only | Allow + deny, ordered |
| **Default** | Deny all inbound | Allow all (customize) |

```text
Security group "web-tier"
  Inbound: 443 from 0.0.0.0/0
  Inbound: 8080 from sg:alb-only
  Outbound: all (or restrict to DB sg)
```

**Best practice:** least privilege SGs; NACLs for subnet-level deny lists (e.g. block IP range).

## 7. VPC endpoints (PrivateLink)

Access AWS services **without** traversing public internet or NAT:

| Type | Example |
|------|---------|
| **Gateway** | S3, DynamoDB |
| **Interface** | Secrets Manager, SQS, other APIs |

Reduces NAT cost and keeps traffic on AWS backbone.

## 8. Example three-tier VPC

```text
┌─────────────────────────────────────────────────┐
│ VPC 10.0.0.0/16                                  │
│  Public:  ALB, NAT GW                            │
│  Private: App tier (ASG across 2 AZs)            │
│  Private: RDS Multi-AZ (no public IP)            │
└─────────────────────────────────────────────────┘
```

## 9. Kubernetes networking (brief)

- **Cluster** lives in VPC subnets (often private).
- **Ingress** or cloud LB exposes HTTP services.
- **Network policies** restrict pod-to-pod traffic.

**Related:** networking TCP/HTTP/DNS/Ingress notes, patterns `v-api-gateway-and-service-mesh.md`.
