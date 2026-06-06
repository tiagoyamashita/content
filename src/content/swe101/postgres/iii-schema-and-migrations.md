---
label: "III"
subtitle: "Schema & migrations"
group: "Postgres"
order: 3
---
Postgres — schema & migrations
Define tables with **DDL**, enforce rules with **constraints**, and evolve schema through **versioned migrations** — never hand-edit production without a tracked script.

## 1. DDL building blocks

```sql
CREATE TABLE accounts (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email         TEXT NOT NULL,
  display_name  TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'suspended', 'closed')),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT accounts_email_unique UNIQUE (email)
);

CREATE TABLE posts (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  account_id  BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  body        TEXT NOT NULL,
  published   BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX posts_account_id_idx ON posts (account_id);
```

| Constraint | Prevents |
|------------|----------|
| **`PRIMARY KEY`** | Duplicate ids |
| **`NOT NULL`** | Missing required fields |
| **`UNIQUE`** | Duplicate emails, slugs |
| **`CHECK`** | Invalid enum-like values |
| **`REFERENCES`** | Orphan foreign keys |

## 2. Migrations workflow

```text
V1__create_accounts.sql   →  applied once, recorded in history table
V2__add_posts.sql         →  runs on next deploy
V3__index_posts.sql       →  additive, backward-compatible when possible
```

| Rule | Why |
|------|-----|
| **One direction per file** | Up migration is the contract; down is optional |
| **Idempotent where tools allow** | `IF NOT EXISTS` for indexes in some flows |
| **Expand → deploy → contract** | Add column nullable → backfill → set NOT NULL → drop old |
| **Never rewrite applied history** | Fix forward with a new migration |

Popular tools: **Flyway**, **Liquibase**, **Alembic** (Python), **Rails migrations**, **Prisma migrate**, **golang-migrate**.

### Flyway example

```sql
-- V1__create_accounts.sql
CREATE TABLE accounts (
  id    BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE
);
```

```bash
flyway -url=jdbc:postgresql://localhost:5432/myapp_dev \
  -user=myapp -password=secret migrate
```

Flyway creates **`flyway_schema_history`** and applies only new versions.

## 3. Safe column changes

| Change | Safer pattern |
|--------|---------------|
| **Add column** | `ADD COLUMN col TYPE DEFAULT value` — avoids full table rewrite on recent Postgres for nullable + default |
| **Rename column** | Migration + app deploy that reads both names, or deploy in lockstep |
| **Drop column** | Stop writing → deploy → stop reading → migration drops |
| **Change type** | New column `col_new`, backfill, swap names in two releases |

**Avoid** long **`ACCESS EXCLUSIVE`** locks on hot tables during peak traffic. Use **`CONCURRENTLY`** for index creation (see [Indexes & EXPLAIN](iv-indexes-and-explain.md)).

## 4. `JSONB` when the shape is flexible

```sql
ALTER TABLE products ADD COLUMN metadata JSONB NOT NULL DEFAULT '{}';
CREATE INDEX products_metadata_gin ON products USING GIN (metadata);

SELECT id, title FROM products
WHERE metadata @> '{"category": "electronics"}';
```

Use **`JSONB`** (binary, indexable) not **`JSON`** (text parse per read) for queryable document fields inside a relational model.

## 5. Triggers for `updated_at` (common pattern)

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER accounts_updated_at
  BEFORE UPDATE ON accounts
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

Many teams prefer setting `updated_at` in application code instead — fewer surprises in the DB layer.

## 6. Seeds vs migrations

| | Migrations | Seeds |
|---|------------|-------|
| **Purpose** | Schema structure | Dev/demo data |
| **Runs in prod** | Yes | Usually no |
| **Example** | `CREATE TABLE` | `INSERT INTO roles …` |

Keep production data out of migration files.

## Next

Continue with [Indexes & EXPLAIN](iv-indexes-and-explain.md) to make queries fast and readable in production.
