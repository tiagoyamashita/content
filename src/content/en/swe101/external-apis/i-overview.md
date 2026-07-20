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
| [GitHub OAuth](iii-github-oauth.md) | OAuth App, scopes, code flow, API calls, device flow |
| [GitLab OAuth](iv-gitlab-oauth.md) | OAuth application on GitLab.com or self-managed, tokens + refresh |

## Mental model

```text
Your app  →  OAuth / API credentials  →  Vendor API (Drive, GitHub, GitLab, …)
                ↑
         refresh / rotate secrets
```

| Credential type | Who acts | Typical use |
|-----------------|----------|-------------|
| **OAuth user consent** | End user | Access *their* Drive / repos |
| **Service account / GitHub App** | Your backend | Server-to-server; install on orgs |
| **PAT / API key** | User or bot | Scripts and CI — rotate and scope tightly |
| **API key (public)** | Anonymous / limited | Public APIs only — **not** for private Drive/repos |

## Next

Start with [Google OAuth & Drive](ii-google-oauth-and-drive.md), or jump to [GitHub OAuth](iii-github-oauth.md) / [GitLab OAuth](iv-gitlab-oauth.md).
