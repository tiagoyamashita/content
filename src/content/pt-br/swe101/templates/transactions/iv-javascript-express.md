---
label: "IV"
subtitle: "JavaScript — Express"
group: "Transactions"
order: 4
---
Transaction template — JavaScript (Express)
Express has **no built-in transaction API**. Transactions live in your **database client** (`pg`, `mysql2`, Prisma `$transaction`, Knex, etc.). Wrap multi-step writes in the service layer; routes stay thin.

Service context: [Services](../services/iv-javascript-express.md).

## Template

```javascript
const { Pool } = require("pg");
const { randomUUID } = require("crypto");

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

/**
 * Run fn inside a SQL transaction. Rolls back on throw.
 * @template T
 * @param {(client: import("pg").PoolClient) => Promise<T>} fn
 * @returns {Promise<T>}
 */
async function withTransaction(fn) {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const result = await fn(client);
    await client.query("COMMIT");
    return result;
  } catch (err) {
    await client.query("ROLLBACK");
    throw err;
  } finally {
    client.release();
  }
}

const itemService = {
  async create({ name }) {
    return withTransaction(async (client) => {
      const id = randomUUID();
      const { rows } = await client.query(
        "INSERT INTO items (id, name) VALUES ($1, $2) RETURNING id, name",
        [id, name.trim()]
      );
      // await client.query("INSERT INTO item_audit ...", [id]); // same TX
      return rows[0];
    });
  },

  async get(id) {
    const { rows } = await pool.query(
      "SELECT id, name FROM items WHERE id = $1",
      [id]
    );
    return rows[0] ?? null;
  },
};

module.exports = { withTransaction, itemService };
```

Route handler — no transaction logic here:

```javascript
const express = require("express");
const { itemService } = require("./itemService");

const router = express.Router();

router.post("/", async (req, res, next) => {
  try {
    const name = req.body?.name;
    if (typeof name !== "string" || name.trim() === "") {
      return res.status(400).json({ error: "name is required" });
    }
    const item = await itemService.create({ name });
    return res.status(201).json(item);
  } catch (err) {
    return next(err);
  }
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **Client owns TX** | `BEGIN` / `COMMIT` / `ROLLBACK` via driver — not Express middleware |
| **Service boundary** | `withTransaction` wraps use-case methods, not every route |
| **ORM helpers** | Prisma `prisma.$transaction([...])`, Knex `trx` — same rule: scope in service |
| **Read-only** | Simple queries can use pool directly — no TX needed |
| **Connection pool** | Always `release()` client in `finally`; don't leak connections on error |

## Next

[Go — net/http](v-go-nethttp.md) · [Transactions overview](i-overview.md).
