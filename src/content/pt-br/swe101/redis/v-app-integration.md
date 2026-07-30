---
label: "V"
subtitle: "App integration"
group: "Redis"
order: 5
---
Redis — app integration
Use **connection pooling**, **timeouts**, and **key conventions** from day one. Examples align with [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) and [Python](../python/i-basics-and-syntax.md).

## 1. Java — Lettuce (recommended)

Lettuce is async-capable and default in Spring Boot 2+:

```java
// Conceptual — io.lettuce:lettuce-core
RedisClient client = RedisClient.create("redis://localhost:6379/0");
StatefulRedisConnection<String, String> conn = client.connect();
RedisCommands<String, String> cmd = conn.sync();

cmd.set("greeting", "hello");
String val = cmd.get("greeting");

cmd.setex("session:abc", 3600, "{\"userId\":42}");
cmd.incr("counter:views");
```

Use **`try-with-resources`** or Spring-managed beans — one client per app, not per request.

## 2. Spring Boot + Spring Data Redis

**Dependency:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

**Configuration:**

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      # password: ${REDIS_PASSWORD}
      timeout: 2s
```

**`RedisTemplate` / `StringRedisTemplate`:**

```java
@Service
public class ProductCache {
  private final StringRedisTemplate redis;

  public ProductCache(StringRedisTemplate redis) {
    this.redis = redis;
  }

  public Optional<String> getProductJson(String id) {
    return Optional.ofNullable(redis.opsForValue().get("cache:product:" + id));
  }

  public void putProductJson(String id, String json, Duration ttl) {
    redis.opsForValue().set("cache:product:" + id, json, ttl);
  }

  public void invalidateProduct(String id) {
    redis.delete("cache:product:" + id);
  }
}
```

**Cache abstraction:**

```java
@Cacheable(value = "products", key = "#id")
public Product findById(String id) {
  return productRepository.findById(id).orElseThrow();
}

@CacheEvict(value = "products", key = "#product.id")
public void update(Product product) {
  productRepository.save(product);
}
```

Enable with **`@EnableCaching`** and Redis cache manager bean.

**Spring Session** (shared across Spring apps — see [Shared sessions across apps](viii-shared-sessions-across-apps.md)):

```xml
<dependency>
  <groupId>org.springframework.session</groupId>
  <artifactId>spring-session-data-redis</artifactId>
</dependency>
```

```yaml
spring:
  session:
    store-type: redis
```

## 3. Python — redis-py

```python
import json
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

r.set("greeting", "hello", ex=300)
r.get("greeting")

r.hset("user:42", mapping={"name": "Ada", "email": "ada@example.com"})
r.hget("user:42", "email")

r.set("cache:product:8812", json.dumps({"title": "Keyboard", "price": 129.99}), ex=600)
```

Use **connection pool**:

```python
pool = redis.ConnectionPool(host="localhost", port=6379, max_connections=20)
r = redis.Redis(connection_pool=pool)
```

**redis.asyncio** for FastAPI/async workers.

## 4. Pipelines and transactions

Batch commands — one round trip:

```java
// Lettuce async pipeline
RedisAsyncCommands<String, String> async = conn.async();
async.set("k1", "v1");
async.set("k2", "v2");
async.incr("counter");
async.flushCommands();
```

```python
pipe = r.pipeline()
pipe.set("k1", "v1")
pipe.incr("counter")
pipe.execute()
```

**`MULTI`/`EXEC`** — atomic group (not same as SQL transaction across keys with rollback on failure — know Redis semantics).

## 5. Error handling

| Error | Action |
|-------|--------|
| **Connection refused** | Fail fast; circuit breaker to DB if cache optional |
| **OOM / maxmemory** | Alert; review eviction policy and key sizes |
| **Timeout** | Retry idempotent reads; avoid unbounded retries on writes |

**Cache optional pattern:** on Redis failure, fall back to database — slower but available.

## 6. Testing

| Approach | Notes |
|----------|-------|
| **Testcontainers** (`redis:7`) | Integration tests with real server |
| **Embedded Redis mock** | Unit tests only — behavior differs |

```java
@Container
static GenericContainer<?> redis = new GenericContainer<>("redis:7").withExposedPorts(6379);

@DynamicPropertySource
static void redisProps(DynamicPropertyRegistry registry) {
  registry.add("spring.data.redis.host", redis::getHost);
  registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
}
```

## Next

Continue with [Operations & persistence](vi-operations-and-persistence.md) for RDB, AOF, and replication.
