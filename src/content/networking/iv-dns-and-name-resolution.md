---
label: "IV"
subtitle: "DNS and name resolution"
group: "Networking"
order: 4
---
Networking — Part IV: DNS and name resolution

**DNS** maps **human-readable names** (`api.example.com`) to **records** used at connection time: mostly **A/AAAA** (addresses), **CNAME** (alias), **MX** (mail), **TXT** (verification, SPF, etc.).

## 1. Why DNS matters before TCP and TLS

To open **TCP** to `api.example.com:443`, the resolver must obtain an **IP address**. The TLS **ClientHello** often includes **SNI** with the same hostname so the server can pick the right certificate.

## 2. Recursive vs authoritative

- **Stub resolver** (your laptop, container) asks a **recursive resolver** (ISP, `8.8.8.8`, corporate DNS, CoreDNS in Kubernetes).
- The recursive resolver walks the tree from **root** → **TLD** (`.com`) → **authoritative** nameservers for `example.com` until it gets the final answer, then **caches** it according to **TTL**.

## 3. Record types (practical subset)

| Type | Role | Name | Value |
|------|------|------|-------|
| **A** | IPv4 address | `api` | `203.0.113.50` |
| **AAAA** | IPv6 address | `api` | `2001:db8::1` |
| **CNAME** | Canonical name — alias to another hostname | `api` | `k8s-lb.eu-west-1.elb.amazonaws.com` |
| **TXT** | Arbitrary text | `_acme-challenge.api` | `xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cB2aE` |
| **TXT** | Arbitrary text | `@` | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Delegates zone to authoritative servers | `@` | `ns1.cloudflare.com` |
| **NS** | Delegates zone to authoritative servers | `@` | `ns2.cloudflare.com` |

### Hostinger hPanel — DNS zone list (zone `myrestapp.com`)

Same records as they appear under **Websites → myrestapp.com → DNS / DNS records** (columns **Type**, **Name**, **Points to**, **TTL**):

| Type | Name | Points to | TTL |
|------|------|-----------|-----|
| A | @ | 185.248.155.42 | 14400 |
| A | ftp | 185.248.155.42 | 14400 |
| CNAME | www | myrestapp.com | 14400 |
| CNAME | api | lb-1847293021.eu-west-1.elb.amazonaws.com | 300 |
| AAAA | api | 2001:db8:5ca8:1::42 | 300 |
| TXT | _acme-challenge.api | xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cB2aE | 300 |
| TXT | @ | v=spf1 include:_spf.google.com ~all | 14400 |
| NS | @ | ns1.dns-parking.com | 14400 |
| NS | @ | ns2.dns-parking.com | 14400 |

## 4. TTL and caching

**TTL** (time to live) on each answer tells resolvers how long they may cache. **Low TTL** speeds failover and migrations; **high TTL** reduces load and can improve resilience to resolver issues but slows cutover.

## 5. Kubernetes and ingress

Inside a cluster, **CoreDNS** serves **cluster.local** names for **Services**. **External** names still use upstream resolvers. **Ingress** resources rely on DNS in the real world pointing **A/AAAA/CNAME** to your **load balancer** or **anycast** edge so clients reach the right IP before HTTP/TLS applies.

## 6. Operational footguns

- **Stale cache** after IP changes.
- **Split-horizon DNS** — different answers inside corp vs internet (debugging surprises).
- **DNSSEC** — authenticity chain for DNS itself (adoption varies).

Next: **Ingress** and edge routing (HTTP routing on top of names and IPs).
