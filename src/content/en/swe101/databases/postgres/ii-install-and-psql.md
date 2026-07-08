---
label: "II"
subtitle: "Install & psql"
group: "Postgres"
order: 2
---
Postgres — install & psql
Run Postgres locally, connect with **`psql`**, and inspect databases before wiring an application.

## 1. Install options

| Method | When to use |
|--------|-------------|
| **Docker** | Reproducible version, easy reset, matches CI |
| **Native package** | macOS (`brew`), Linux (`apt`/`dnf`), Windows installer |
| **Managed cloud** | Neon, Supabase, RDS — no local daemon |

### Docker (recommended for learning)

```bash
docker run --name pg-dev -e POSTGRES_PASSWORD=dev -p 5432:5432 -d postgres:16
docker exec -it pg-dev psql -U postgres
```

Data persists in the container until removed. For a named volume:

```bash
docker run --name pg-dev -e POSTGRES_PASSWORD=dev -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data -d postgres:16
```

## 2. Connection string

```text
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

Example for local Docker:

```text
postgresql://postgres:dev@localhost:5432/postgres
```

| Part | Typical local value |
|------|---------------------|
| **USER** | `postgres` |
| **PASSWORD** | value from `POSTGRES_PASSWORD` |
| **HOST** | `localhost` |
| **PORT** | `5432` |
| **DATABASE** | `postgres` (default DB) or one you create |

## 3. `psql` essentials

Connect:

```bash
psql "postgresql://postgres:dev@localhost:5432/postgres"
# or
psql -h localhost -U postgres -d postgres
```

| Command | Action |
|---------|--------|
| `\l` | List databases |
| `\c mydb` | Connect to database `mydb` |
| `\dt` | List tables in current schema |
| `\d users` | Describe table `users` |
| `\du` | List roles |
| `\timing` | Show query execution time |
| `\q` | Quit |

Run SQL from a file:

```bash
psql -U postgres -d myapp -f schema.sql
```

## 4. Create a dev database and role

```sql
CREATE DATABASE myapp_dev;
CREATE USER myapp WITH PASSWORD 'local-only-secret';
GRANT ALL PRIVILEGES ON DATABASE myapp_dev TO myapp;

\c myapp_dev
GRANT ALL ON SCHEMA public TO myapp;
```

**Principle of least privilege in production:** app role gets `SELECT/INSERT/UPDATE/DELETE` on needed tables — not `SUPERUSER`.

## 5. First table (smoke test)

```sql
CREATE TABLE todos (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  done       BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO todos (title) VALUES ('Learn psql'), ('Read migrations note');
SELECT * FROM todos WHERE NOT done;
```

## 6. Configuration files (know they exist)

| File | Purpose |
|------|---------|
| **`postgresql.conf`** | Memory, connections, logging |
| **`pg_hba.conf`** | Who can connect from which host (auth rules) |

In Docker, config is inside the container unless you mount overrides. For local tuning you rarely need to change defaults until you load-test.

## 7. GUI clients (optional)

| Tool | Notes |
|------|-------|
| **pgAdmin** | Full-featured, ships with many installers |
| **DBeaver** | Cross-DB, good ER diagrams |
| **TablePlus / DataGrip** | Paid, polished UX |

`psql` stays worth learning — scripts, CI, and production debugging often happen in the shell.

## Next

Continue with [Schema & migrations](iii-schema-and-migrations.md) for versioned DDL and safe schema evolution.
