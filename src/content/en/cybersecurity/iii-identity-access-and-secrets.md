---
label: "III"
subtitle: "Identity, access & secrets"
group: "Cybersecurity"
order: 3
---
Identity, access & secrets
Most breaches involve **stolen or misused credentials**. Strong **identity**, **least-privilege access**, and **secret hygiene** block a large share of real-world attacks.

## 1. Authentication vs authorization

| Term | Question | Mechanism |
|------|----------|-----------|
| **Authentication (AuthN)** | Who are you? | Password, passkey, SSO, API key |
| **Authorization (AuthZ)** | What may you do? | RBAC, ABAC, policy engine |

```text
Login (AuthN) → session/JWT issued → each request checked against roles/policies (AuthZ)
```

Never confuse them: a valid login does **not** mean access to every resource.

## 2. Identity patterns

| Pattern | Fit | Watch out |
|---------|-----|-----------|
| **Local username/password** | Small apps, dev | Weak passwords, no MFA |
| **SSO (SAML/OIDC)** | Companies, B2B | Misconfigured redirect URIs |
| **Social login** | Consumer apps | Account linking bugs |
| **Service accounts** | Machine-to-machine | Long-lived keys in repos |
| **Workload identity** | K8s, cloud VMs | Over-broad IAM roles |

**Prefer:** central IdP (Okta, Entra ID, Google Workspace) + **MFA** for humans; **short-lived tokens** for machines.

## 3. MFA and passkeys

| Factor | Example |
|--------|---------|
| Something you **know** | Password |
| Something you **have** | TOTP app, hardware key, push approve |
| Something you **are** | Biometric (device-bound) |

| Policy | Recommendation |
|--------|----------------|
| Admin / prod access | **MFA required** |
| Customer accounts | MFA optional → encouraged for high-value actions |
| API automation | No password — use scoped tokens + rotation |

**Passkeys (WebAuthn)** reduce phishing: credential is bound to your site origin; no reusable password to steal.

## 4. Authorization models

| Model | Idea | Example |
|-------|------|---------|
| **RBAC** | Roles → permissions | `billing_admin` can refund |
| **ABAC** | Attributes on user + resource | `department=finance` AND `amount<1000` |
| **ReBAC** | Relationships (graph) | Google Zanzibar-style “editor of doc X” |

Principles:

| Principle | Practice |
|-----------|----------|
| **Least privilege** | Default deny; grant minimum needed |
| **Separation of duties** | Deployer ≠ approver for prod |
| **Break-glass** | Emergency admin with extra logging |
| **Regular access reviews** | Quarterly: who still needs this role? |

## 5. Session and token hygiene

| Issue | Mitigation |
|-------|------------|
| Stolen session cookie | `HttpOnly`, `Secure`, `SameSite`, short TTL |
| JWT in localStorage | Prefer httpOnly cookie or memory + refresh rotation |
| Over-scoped JWT claims | Small audience; short expiry; validate `iss`/`aud` |
| Refresh token reuse | Detect reuse → revoke family |

```text
Access token:  short (minutes)
Refresh token: longer, rotatable, stored carefully
API key:       scoped, auditable, revocable
```

## 6. Secrets — never in git

| Secret type | Store | Anti-pattern |
|-------------|-------|--------------|
| DB password | Vault, cloud secret manager, CI secret | `config.yml` in repo |
| API key | Env at runtime, OIDC where possible | Slack webhook in README |
| TLS private key | KMS, cert manager | Committed `.pem` |
| Encryption key | HSM / KMS | Hard-coded in source |

**CI/CD:** use platform secrets + **OIDC to cloud** instead of static AWS keys ([Secrets & OIDC](../sre101/cicd/security-and-best-practices/iii-secrets-and-oidc.md)).

| Detection | Tooling |
|-----------|---------|
| Pre-commit | `gitleaks`, `trufflehog` |
| CI | Secret scan on every PR |
| Response | Rotate immediately if leaked |

## 7. Machine identity in cloud

| Workload | Pattern |
|----------|---------|
| Lambda / Cloud Run | Execution role with minimal IAM |
| Kubernetes pod | IRSA / workload identity — no node-wide creds |
| GitHub Actions → AWS | OIDC `role-to-assume` per repo/environment |

```text
Bad:  one shared "prod-admin" key on every service
Good: service A role can only read queue X; service B only write table Y
```

## 8. Access checklist (production)

| Check | Pass criteria |
|-------|---------------|
| Human admin | SSO + MFA, no shared accounts |
| Prod data access | Role-based, logged, time-bound if possible |
| Service accounts | Named per service; no user passwords for bots |
| Secrets | Central store; rotation calendar |
| Offboarding | IdP disable removes access same day |

## 9. Rehearsal questions

- AuthN vs AuthZ — one sentence each?
- Why are long-lived API keys in git dangerous even in private repos?
- What does least privilege mean for a CI job deploying to staging?
- Name two session cookie flags that reduce theft risk.

**Related:** [Threat modeling](ii-threat-modeling-and-risk.md), [Application security](iv-application-and-network-security.md), [CI/CD least-privilege runners](../sre101/cicd/security-and-best-practices/iv-least-privilege-runners.md).
