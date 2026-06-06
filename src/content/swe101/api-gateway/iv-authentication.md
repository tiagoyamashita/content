---
label: "IV"
subtitle: "Authentication"
group: "API Gateway"
order: 4
---
API gateway — authentication
Validate **who** is calling before traffic hits your services — **JWT**, **API keys**, **OAuth**, or **mTLS**. Gateway rejects bad credentials early (401/403) and forwards trusted context to upstream.

## 1. Where auth runs

```text
Client ──Authorization: Bearer …──► Gateway validates
                                         │
                                         ├── invalid → 401
                                         └── valid → upstream (+ optional identity headers)
```

| Layer | Responsibility |
|-------|----------------|
| **Gateway** | Token format, signature, expiry, API key lookup |
| **Service** | Authorization (can this user do this action?) |

Gateway **authentication**; service **authorization** (RBAC, ownership checks).

## 2. JWT (Bearer token)

Common for SPA and mobile:

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

Gateway checks:

- Signature (JWKS from IdP)
- `exp`, `iss`, `aud`
- Optional claims (`scope`, `roles`)

```yaml
# Conceptual plugin config
plugins:
  - name: jwt
    config:
      claims_to_verify: [exp]
      key_claim_name: kid
```

Upstream receives decoded claims in header (if configured) or re-validates JWT — **avoid double work**; pick one trust boundary.

## 3. API keys

Partners and scripts:

```http
X-Api-Key: sk_live_abc123
# or
?api_key=...   (avoid in URLs — logs leak)
```

Gateway maps key → **consumer** → rate limit tier. Rotate keys in dashboard; never commit to git.

## 4. OAuth 2.0 / OpenID Connect

Browser login flows terminate at **auth service**; API calls use **access token**:

```text
User → Login (OAuth) → Auth server → access token
Client → API Gateway (Bearer access token) → services
```

Gateway validates access token introspection or JWT from auth server.

## 5. mTLS (mutual TLS)

Client presents certificate — common for **B2B** APIs:

```text
Partner client cert → Gateway verifies CA → route to upstream
```

Strong identity; higher ops burden (cert rotation, partner onboarding).

## 6. What not to cache at CDN

Authenticated responses must use:

```http
Cache-Control: private, no-store
```

Or route `api.example.com` **without CDN cache** — see [CDN APIs & dynamic content](../cdn/vi-apis-and-dynamic-content.md).

## 7. Security checklist

- [ ] HTTPS only; HSTS at CDN/gateway
- [ ] Validate JWT `aud` for your API — not just signature
- [ ] API keys in headers, not query strings
- [ ] Rate limit per key/user ([Rate limiting & resilience](v-rate-limiting-and-resilience.md))
- [ ] Do not trust `X-User-Id` from internet — only from gateway on private link
- [ ] Log auth failures — detect credential stuffing

## Next

Continue with [Rate limiting & resilience](v-rate-limiting-and-resilience.md) for throttling and failure handling.
