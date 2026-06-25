---
label: "II"
subtitle: "Install & mongosh"
group: "MongoDB"
order: 2
---
MongoDB — install & mongosh
Run MongoDB locally or on **Atlas**, connect with a **URI**, and explore data with **`mongosh`**.

## 1. Install options

| Method | When to use |
|--------|-------------|
| **Docker** | Reproducible dev, CI, quick reset |
| **MongoDB Community** | Native install on laptop |
| **MongoDB Atlas** | Free tier, backups, no local daemon |

### Docker

```bash
docker run --name mongo-dev -p 27017:27017 -d mongo:7
docker exec -it mongo-dev mongosh
```

With a persistent volume:

```bash
docker run --name mongo-dev -p 27017:27017 -v mongodata:/data/db -d mongo:7
```

### Atlas (cloud)

1. Create cluster at [mongodb.com/atlas](https://www.mongodb.com/atlas).
2. Add database user + network access (IP allowlist or `0.0.0.0/0` for dev only).
3. Copy connection string from **Connect → Drivers**.

## 2. Connection string

```text
mongodb://USER:PASSWORD@HOST:27017/DATABASE
mongodb+srv://USER:PASSWORD@cluster0.xxxxx.mongodb.net/DATABASE
```

| Part | Notes |
|------|-------|
| **`mongodb+srv://`** | Atlas DNS seed list — TLS by default |
| **DATABASE** | Default auth DB may differ — check Atlas UI |
| **Options** | `?retryWrites=true&w=majority` common on Atlas |

Local example:

```text
mongodb://localhost:27017/myapp_dev
```

## 3. `mongosh` essentials

```javascript
show dbs
use myapp_dev
show collections

db.products.insertOne({
  title: "Keyboard",
  price: 129.99,
  tags: ["hardware"]
})

db.products.find({ tags: "hardware" })
db.products.findOne({ title: "Keyboard" })
```

| Command | Action |
|---------|--------|
| **`use dbname`** | Switch database (creates on first write) |
| **`db.coll.find()`** | Query collection |
| **`db.coll.insertOne()` / `insertMany()`** | Insert |
| **`db.coll.updateOne()` / `deleteOne()`** | Modify |
| **`db.coll.createIndex()`** | Add index |
| **`db.coll.getIndexes()`** | List indexes |
| **`db.coll.stats()`** | Size, count, index stats |

Pretty-print: **`db.products.find().pretty()`**

Run a JS file:

```bash
mongosh "mongodb://localhost:27017/myapp_dev" setup.js
```

## 4. Create user (local dev)

In **`mongosh`** on admin:

```javascript
use admin
db.createUser({
  user: "myapp",
  pwd: "local-only-secret",
  roles: [{ role: "readWrite", db: "myapp_dev" }]
})
```

Connect:

```text
mongodb://myapp:local-only-secret@localhost:27017/myapp_dev
```

Atlas creates users in the UI — prefer **least privilege** (`readWrite` on one DB, not `atlasAdmin`).

## 5. Compass (optional GUI)

**MongoDB Compass** — visual browser, schema inference, index builder, explain plans. Useful alongside **`mongosh`** for exploring unfamiliar collections.

## 6. Smoke test

```javascript
use myapp_dev

db.todos.insertMany([
  { title: "Learn mongosh", done: false, createdAt: new Date() },
  { title: "Model a collection", done: false, createdAt: new Date() }
])

db.todos.find({ done: false }).sort({ createdAt: 1 })
```

## Next

Continue with [Schema & modeling](iii-schema-and-modeling.md) for embed vs reference and validation rules.
