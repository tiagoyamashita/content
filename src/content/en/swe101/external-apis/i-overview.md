---
label: "I"
subtitle: "Overview"
group: "External APIs"
order: 1
---
External APIs — overview
**External APIs** are third-party HTTP services your app calls — Google, Stripe, Slack, GitHub — usually with **OAuth 2.0**, **API keys**, or **service accounts**. This track covers how to **register apps**, obtain **tokens**, store secrets safely, and call vendor APIs from your code.

Related: [API gateway authentication](../api-gateway/iv-authentication.md) (validating tokens *you* issue), [Identity & secrets](../../cybersecurity/iii-identity-access-and-secrets.md).

## Map of this track

| Note | Focus |
|------|--------|
| [Google OAuth & Drive](ii-google-oauth-and-drive.md) | Cloud project, consent, tokens, Drive API so you can list/upload/manage files |

## Mental model

```text
Your app  →  OAuth / API credentials  →  Vendor API (Drive, Gmail, …)
                ↑
         refresh / rotate secrets
```

| Credential type | Who acts | Typical use |
|-----------------|----------|-------------|
| **OAuth user consent** | End user | Access *their* Drive / Gmail |
| **Service account** | Your backend | Server-to-server; Workspace domain-wide or shared drives |
| **API key** | Anonymous / limited | Public APIs only — **not** for private Drive files |

## Next

Start with [Google OAuth & Drive](ii-google-oauth-and-drive.md).
