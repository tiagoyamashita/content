---
label: "IV"
subtitle: "Application & network security"
group: "Cybersecurity"
order: 4
---
Application & network security
**Application security** stops bugs from becoming exploits. **Network security** limits who can reach what. Together they shrink blast radius when something fails.

## 1. OWASP Top 10 (mindset)

The [OWASP Top 10](https://owasp.org/www-project-top-ten/) changes over time; the **themes** stay constant:

| Theme | What goes wrong | Dev habit |
|-------|-----------------|-----------|
| **Broken access control** | User A reads user B’s order (IDOR) | Check ownership on every object access |
| **Injection** | SQL/shell built from user input | Parameterized queries; no string concat |
| **Cryptographic failures** | Weak TLS, passwords in logs | Modern ciphers; never log secrets |
| **Insecure design** | Missing rate limits on login | Threat model at design time |
| **Security misconfiguration** | Default admin password, open S3 | Hardening guides, IaC review |
| **Vulnerable components** | Log4Shell-style CVEs | Lockfiles, Dependabot, CI scan |
| **Auth failures** | Weak session, no MFA on admin | Central IdP, secure cookies |
| **Integrity failures** | Unsigned updates, tampered CI | Sign artifacts, verify deploy |
| **Logging gaps** | No audit trail after fraud | Structured security logs |
| **SSRF** | Server fetches internal URLs | Allowlist outbound, no raw user URLs |

One **secure coding** rule covers many rows: **never trust client input** — validate, encode, authorize server-side.

## 2. Input validation and output encoding

| Layer | Rule |
|-------|------|
| **API** | Schema validation (types, lengths, enums) |
| **SQL** | Prepared statements / ORM parameter binding |
| **HTML** | Context-aware encoding (avoid XSS) |
| **Shell** | Never pass user strings to `exec` |
| **File upload** | Type/size limits; store outside web root |

```text
Client sends:  { "role": "admin" }  on signup
Server must:  ignore role field OR reject — don't trust hidden form fields
```

## 3. TLS and transport

| Practice | Detail |
|----------|--------|
| **HTTPS everywhere** | Redirect HTTP → HTTPS; HSTS on public sites |
| **TLS version** | 1.2 minimum; prefer 1.3 |
| **Certificate management** | Let’s Encrypt / ACM / cert-manager — automate renewal |
| **mTLS** | Service-to-service: both sides present certs |

TLS protects **on the wire**; it does **not** fix application auth bugs or compromised servers.

## 4. Network segmentation

```text
Internet
  → DMZ (load balancer, WAF)
  → App tier (no direct DB port to internet)
  → Data tier (private subnet only)
  → Admin / bastion (jump host, VPN, or SSO portal)
```

| Control | Purpose |
|---------|---------|
| **Security groups / NSGs** | Allow only required ports between tiers |
| **Private subnets** | DB and internal APIs not routable from public net |
| **Egress filtering** | Limit what compromised app can call outbound |
| **WAF** | Block common HTTP attacks at edge |

Deeper networking concepts: [CS101 networking](../cs101/networking/i-tcp-udp-and-transport-basics.md).

## 5. Zero trust (practical version)

**“Never trust, always verify”** — being on the corporate network is **not** enough.

| Old model | Zero trust |
|-----------|------------|
| VPN = inside = trusted | Every request authenticated + authorized |
| Flat internal network | Micro-segmentation |
| Long-lived VPN session | Short-lived device + user context |

| Step | Action |
|------|--------|
| 1 | Strong identity (SSO + MFA) |
| 2 | Device posture where possible (managed laptop, patch level) |
| 3 | Policy per app/resource (not “all employees see prod DB”) |
| 4 | Log and alert on anomalies |

You do not need a vendor “zero trust platform” on day one — **identity per request + least network access** is the core shift.

## 6. API and B2B security

| Risk | Mitigation |
|------|------------|
| Broken object level auth | Resource IDs scoped to tenant/user |
| Excessive data exposure | DTOs — don’t return full internal models |
| Mass assignment | Allowlist updatable fields |
| Rate limiting | Per IP, per API key, per user |
| Webhooks | Verify HMAC signature; replay protection |

Public APIs: version, document auth, monitor abuse patterns.

## 7. Dependency and build security

| Stage | Control |
|-------|---------|
| **Source** | Branch protection, required review |
| **Dependencies** | Lock files, CVE gates in CI |
| **Build** | Reproducible builds, pinned base images |
| **Deploy** | Signed containers, policy before prod |

Full pipeline detail: [Supply chain & SLSA](../sre101/cicd/security-and-best-practices/ii-supply-chain-and-slsa.md).

## 8. Security headers (web apps)

| Header | Effect |
|--------|--------|
| `Content-Security-Policy` | Restrict script sources — mitigates XSS |
| `X-Frame-Options` / `frame-ancestors` | Clickjacking protection |
| `Strict-Transport-Security` | Force HTTPS |
| `Referrer-Policy` | Limit leaked URLs in Referer |

Use framework middleware or reverse proxy defaults; tune CSP without breaking legit scripts.

## 9. Rehearsal questions

**Practice questions:**

- What is IDOR and how do you prevent it?
- Why doesn’t TLS alone stop SQL injection?
- Draw three network tiers from internet to database.
- Name two differences between “VPN trust” and zero trust.
- What is the purpose of a content security policy (CSP) header?
- Why are short-lived credentials preferred over long-lived ones?
- How can you mitigate mass assignment vulnerabilities in APIs?
- What is the risk of excessive data exposure in APIs, and how can it be avoided?
- What’s the role of mutual TLS (mTLS) in microservice communication?
- What does “least privilege” mean in application/network security design?

**Sample answers:**

- **What is IDOR and how do you prevent it?**  
  IDOR (Insecure Direct Object Reference) occurs when access to data objects (like user IDs or document IDs) isn't properly restricted, allowing unauthorized users to access data by guessing or manipulating IDs.  
  *Prevention*: Always perform authorization checks on every object access, ensuring users can only access their permitted resources. Scope object IDs to users/tenants so IDs cannot be guessed.

- **Why doesn’t TLS alone stop SQL injection?**  
  TLS encrypts data in transit between client and server, preventing eavesdropping. However, SQL injection exploits flaws in how the application processes user input at the database—TLS offers no protection once the data arrives at your backend.

- **Draw three network tiers from internet to database.**  
  1. **Internet** (user/browser)  
  2. **Web/Application Server** (handles business logic)  
  3. **Database Server** (stores data; not directly exposed to internet)

- **Name two differences between “VPN trust” and zero trust.**  
  1. VPN trust treats being “on the VPN” as sufficient trust for access; zero trust re-authenticates and re-authorizes every request.  
  2. VPN sessions are often long-lived; zero trust grants ephemeral access tied to short-lived device and user context.

- **What is the purpose of a content security policy (CSP) header?**  
  The CSP header controls which sources of content (scripts, styles, etc.) are allowed to load in the browser, helping to prevent XSS and other script injection attacks.

- **Why are short-lived credentials preferred over long-lived ones?**  
  Short-lived credentials limit the impact window if credentials are leaked. Attackers have less time to use them, reducing exposure and making compromise detection and recovery easier.

- **How can you mitigate mass assignment vulnerabilities in APIs? Give an example.**  
  By allowlisting fields that are allowed to be updated, rather than accepting all user-supplied fields.

  *Example:*  
  ```python
  # BAD: Accepts all fields in incoming request—dangerous!
  user.update(request.json)
  
  # GOOD: Only updates explicitly allowed fields
  allowed_fields = ['email', 'display_name']
  data = {k: v for k, v in request.json.items() if k in allowed_fields}
  user.update(data)
  ```

- **What is the risk of excessive data exposure in APIs, and how can it be avoided?**  
  Exposing entire internal models may reveal sensitive or unintended data (e.g., passwords, internal notes).  
  *Prevention*: Use Data Transfer Objects (DTOs) or serializers to return only required/expected fields.

- **What’s the role of mutual TLS (mTLS) in microservice communication?**  
  mTLS provides authentication between both parties in a connection (not just the server), ensuring only authorized clients and services can communicate with each other—this is especially useful for service-to-service trust within internal networks.

- **What does “least privilege” mean in application/network security design?**  
  Every user, device, process, or service should be granted the minimum set of permissions required to perform its job, and no more. This limits the potential blast radius if an account is compromised.

**Related:** [Identity & secrets](iii-identity-access-and-secrets.md), [Incident response](v-incident-response-and-operations.md), [Threat modeling](ii-threat-modeling-and-risk.md).
