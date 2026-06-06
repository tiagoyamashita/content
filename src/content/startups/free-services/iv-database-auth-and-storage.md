---
label: "IV"
subtitle: "Database, auth & storage"
group: "Startups"
order: 4
---
Database, auth & storage
Skip installing Postgres on a VM. **Managed free tiers** give you database, authentication, and file storage with backups and TLS.

## 1. Database + backend-as-a-service

| Provider | Free tier (typical) | Includes |
|----------|---------------------|----------|
| **[Supabase](https://supabase.com)** | Project limits | Postgres, auth, storage, realtime |
| **[Firebase](https://firebase.google.com)** | Spark plan | Firestore/Realtime DB, auth, hosting |
| **[Neon](https://neon.tech)** | Serverless Postgres | Branching, scale-to-zero |
| **[PlanetScale](https://planetscale.com)** | Hobby | MySQL-compatible (check current offering) |
| **[MongoDB Atlas](https://www.mongodb.com/atlas)** | M0 cluster | Document DB |

```text
Supabase quick mental model:
  Postgres  ←  SQL migrations, RLS policies
  Auth      ←  email magic link, OAuth (Google, GitHub)
  Storage   ←  S3-like buckets with policies
```

## 2. Authentication

| Option | When |
|--------|------|
| **Supabase / Firebase Auth** | BaaS already chosen |
| **[Clerk](https://clerk.com)** | Polished UI components; free MAU cap |
| **[Auth0](https://auth0.com)** | Free tier for dev; enterprise later |
| **NextAuth / Auth.js** | Self-hosted OAuth in your app |

Use **OAuth** (Sign in with Google/GitHub) to avoid password storage early.

## 3. File & object storage

| Service | Free notes |
|---------|------------|
| **Supabase Storage** | Bundled with project |
| **Cloudflare R2** | Free storage; no egress fee to Cloudflare |
| **AWS S3** | 5 GB free tier (12 months for new accounts) |
| **Firebase Storage** | Spark limits |

Never store uploads on serverless **ephemeral disk** — use object storage with signed URLs.

## 4. Secrets

| Approach | MVP |
|----------|-----|
| Platform env vars | Vercel / Render dashboard |
| **GitHub Secrets** | CI only |
| **Doppler / Infisical** | Free team tiers for sync |

Do not commit `.env` with production keys.

## 5. Example env layout

```bash
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...          # public, RLS protects data
SUPABASE_SERVICE_ROLE_KEY=...     # server only — never expose to browser
RESEND_API_KEY=re_...
```

## 6. When to leave free BaaS

| Signal | Consider |
|--------|----------|
| Connection pool limits | Dedicated Postgres (RDS, Neon paid) |
| Complex queries / RLS pain | Own backend + ORM |
| Vendor lock-in concern | Export data; standard Postgres helps |

**Related:** CS101 **databases** submenu, Supabase skill for RLS/auth depth.
