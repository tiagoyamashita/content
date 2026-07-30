---
label: "II"
subtitle: "Install & redis-cli"
group: "Redis"
order: 2
---
Redis — install & redis-cli
Run Redis locally or use a **managed** service (ElastiCache, Redis Cloud, Upstash). Connect with **`redis-cli`** or driver URI.

## 1. Install options

| Method | When to use |
|--------|-------------|
| **Docker** | Dev, CI, quick reset |
| **Native package** | `brew install redis`, Linux packages |
| **Managed** | Production HA without running your own failover |

### Docker

```bash
docker run --name redis-dev -p 6379:6379 -d redis:7
docker exec -it redis-dev redis-cli
```

With persistence volume:

```bash
docker run --name redis-dev -p 6379:6379 -v redisdata:/data -d redis:7 redis-server --appendonly yes
```

## 2. Connection URI

```text
redis://localhost:6379/0
redis://:PASSWORD@host:6379/0
rediss://user:PASSWORD@host:6380/0   # TLS (managed clouds)
```

| Part | Meaning |
|------|---------|
| **`redis://` / `rediss://`** | Plain / TLS |
| **`/0`** | Database number (0–15 by default; cluster uses one logical DB) |
| **Password** | `requirepass` or ACL user |

## 3. `redis-cli` essentials

```bash
redis-cli -h localhost -p 6379
# or
redis-cli -u redis://localhost:6379/0
```

```text
PING                    → PONG
SET greeting "hello"
GET greeting
DEL greeting

SET session:abc "{\"userId\":42}" EX 3600
TTL session:abc

KEYS user:*             # dev only — O(N), blocks on large DBs
SCAN 0 MATCH user:* COUNT 100   # production-safe iteration
```

| Command | Action |
|---------|--------|
| **`SET` / `GET`** | String read/write |
| **`SET key val EX seconds`** | Set with TTL |
| **`INCR` / `DECR`** | Atomic integer |
| **`EXPIRE` / `TTL`** | Manage expiry |
| **`DEL` / `UNLINK`** | Delete (`UNLINK` async free) |
| **`INFO memory`** | Memory stats |
| **`MONITOR`** | Stream all commands — debug only, never prod |
| **`FLUSHDB`** | Delete current DB — dev only |

## 4. ACL user (Redis 6+)

```text
ACL SETUSER myapp on >local-secret ~myapp:* +get +set +del +incr +expire
AUTH myapp local-secret
```

Prefer **least privilege** — app user gets only needed commands and key patterns (`~cache:*`).

## 5. GUI clients (optional)

| Tool | Notes |
|------|-------|
| **Redis Insight** | Official GUI — browser keys, CLI, profiler |
| **Another Redis Desktop Manager** | Cross-platform key browser |

`redis-cli` remains essential for production debugging.

## 6. Smoke test

```text
SET counter 0
INCR counter
INCR counter
GET counter

HSET user:42 name Ada email ada@example.com
HGETALL user:42

EXPIRE user:42 300
TTL user:42
```

## Next

Continue with [Data structures & keys](iii-data-structures-and-keys.md) for types and naming conventions.
