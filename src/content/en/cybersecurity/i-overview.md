---
label: "I"
subtitle: "Overview"
group: "Cybersecurity"
order: 1
---
Cybersecurity — overview
**Cybersecurity** is protecting **systems, data, and people** from unauthorized access, abuse, and loss — while keeping services **available** to legitimate users.

This track is practical: threat thinking, identity, application and network controls, and what to do when something goes wrong.

## Map of Cybersecurity

| Note | Focus |
|------|--------|
| [Threat modeling & risk](ii-threat-modeling-and-risk.md) | Assets, attackers, STRIDE, prioritization |
| [Identity, access & secrets](iii-identity-access-and-secrets.md) | AuthN, AuthZ, MFA, least privilege, credentials |
| [Application & network security](iv-application-and-network-security.md) | OWASP, TLS, segmentation, zero trust basics |
| [Incident response & operations](v-incident-response-and-operations.md) | Detection, IR phases, logging, tabletop drills |

**Related in this repo:** [CI/CD security](../sre101/cicd/security-and-best-practices/i-overview.md), [Networking](../cs101/networking/i-overview.md), [Trust & verify (AI)](../ai101/using-ai/vii-trust-privacy-and-verify.md).

## 1. The CIA triad

| Pillar | Meaning | Example failure |
|--------|---------|-----------------|
| **Confidentiality** | Only authorized parties see data | Leaked customer database |
| **Integrity** | Data and systems are not tampered with | Attacker changes prices in admin panel |
| **Availability** | Service works when needed | DDoS takes checkout offline |

Modern security adds:

| Extension | Why |
|-----------|-----|
| **Authentication** | Prove *who* is calling |
| **Authorization** | Decide *what* they may do |
| **Non-repudiation** | Strong audit trail (who did what, when) |
| **Privacy** | Collect and use data lawfully (GDPR, etc.) |

## 2. Defense in depth

No single control stops every attack. Layer controls so one failure does not mean total compromise.

```text
User → WAF / CDN → TLS → auth → app validation → DB permissions → encryption at rest → backups → monitoring
```

| Layer | Examples |
|-------|----------|
| **Perimeter** | Firewall, DDoS protection, geo blocks |
| **Identity** | SSO, MFA, service accounts with scoped roles |
| **Application** | Input validation, parameterized queries, CSRF tokens |
| **Data** | Encryption, tokenization, row-level security |
| **Operations** | Patching, logging, alerts, incident runbooks |

## 3. Who you are protecting against

| Actor | Motivation | Typical technique |
|-------|------------|-------------------|
| **Opportunistic** | Easy money (ransomware, card fraud) | Phishing, exposed S3 buckets |
| **Insider** | Revenge, profit, negligence | Over-broad access, data exfil |
| **Organized crime** | Scale fraud | Credential stuffing, malware |
| **Nation-state** | Espionage, disruption | Supply chain, zero-days |
| **Script kiddie** | Curiosity | Scanning for default passwords |

You cannot defend equally against all of them on every system — **risk prioritization** (next note) picks where effort goes.

## 4. Security vs convenience

| Too loose | Too tight |
|-----------|-----------|
| Shared admin password | MFA on every internal wiki click |
| No logging | 6-month access approval for dev read-only |

Aim for **proportionate** controls: protect crown jewels hardest; automate safe defaults (TLS everywhere, secret scanners in CI).

## 5. Where this fits in a software career

```text
Build feature     →  secure coding (validation, secrets, dependencies)
Ship to prod      →  IAM, network policy, CI/CD signing (SRE track)
Run in production →  monitoring, IR, patching (this track + SRE)
```

Developers own **bugs that become vulnerabilities**. SRE and security teams own **platform guardrails** — but everyone shares **incident response**.

## 6. Quick checklist (any new service)

| Question | If “no”, fix before prod |
|----------|--------------------------|
| Who can authenticate and how? | Define authN + MFA policy |
| What can each role do? | Least-privilege RBAC |
| Where are secrets stored? | Vault / env — not git |
| Is traffic encrypted in transit? | TLS 1.2+ |
| Are dependencies scanned? | CI CVE gate |
| Are logs centralized and retained? | SIEM or log platform |
| Is there a rollback and IR contact? | Runbook + on-call |

## 7. Rehearsal questions

- Define confidentiality, integrity, and availability with one example each.
- What does “defense in depth” mean in one sentence?
- Name two layers between the internet and your database.
- Why can’t you secure everything equally?

**Next:** [Threat modeling & risk](ii-threat-modeling-and-risk.md).
