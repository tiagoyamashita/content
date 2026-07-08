---
label: "VIII"
subtitle: "Distributed cache"
group: "Spring Boot"
groupOrder: 2
order: 10
---
Spring Boot — Part VIII: Distributed cache
A **distributed cache** stores entries on **shared infrastructure** (usually **Redis**) so **every instance** of your app sees the same data. A **local** cache (**Caffeine** in one JVM) is faster per read but **not** shared across pods or servers.

**Java baseline:** **Java SE 22** (`javac --release 22`); examples target **Spring Boot 3.x**.

## 1. When you need which

| Approach | Shared across instances? | Typical use |
|----------|-------------------------|-------------|
| **No cache** | — | Source of truth only in DB |
| **Local** (`Caffeine`, `ConcurrentHashMap`) | No | Per-node hot reads, config flags |
| **Distributed** (Redis, Hazelcast) | Yes | Session-like data, rate limits, shared lookup tables, reducing DB load cluster-wide |

**Cache-aside (lazy loading):** app reads cache → on miss, load from DB → write cache → return. You own **invalidation** when data changes (`@CacheEvict`, TTL, or message-driven eviction).

## 2. Stack for Spring Boot + Redis

Add dependencies (Maven coordinates — use your BOM versions):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

- **`spring-boot-starter-cache`** — **`@Cacheable`**, **`CacheManager`**, AOP around your beans.
- **`spring-boot-starter-data-redis`** — **`RedisConnectionFactory`**, **`RedisTemplate`**, Lettuce client (default).

Enable caching on the application class:

```java
// Compile: javac --release 22 …
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
```

## 3. Configuration (`application.yml`)

Point every instance at the **same** Redis (or cluster). Use env vars in prod (see **Part II** — [YAML & external config](ii-yaml-and-external-config.md)).

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
      ssl:
        enabled: ${REDIS_SSL:false}
      timeout: 2s

  cache:
    type: redis
    redis:
      time-to-live: 10m
      cache-null-values: false
      key-prefix: "billing::"
```

| Property | Role |
|----------|------|
| **`spring.cache.type=redis`** | Use Redis-backed **`CacheManager`** (not in-memory only) |
| **`time-to-live`** | Default entry expiry — avoids stale data forever |
| **`key-prefix`** | Namespace keys when several apps share one Redis |
| **`cache-null-values: false`** | Optional: do not cache “not found” unless you intend to |

**Cluster / Sentinel:** use **`spring.data.redis.cluster.nodes`** or **`spring.data.redis.sentinel`** — same Spring Cache layer; connection factory changes only.

Run Redis locally for dev:

```text
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

## 4. Declarative cache on services

Put **`@Cacheable`** on **service** methods (not controllers). Cache key defaults to method params; customize with **`key`** SpEL.

```java
// Compile: javac --release 22 …
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class ProductService {

  private final ProductRepository products;

  public ProductService(ProductRepository products) {
    this.products = products;
  }

  @Cacheable(cacheNames = "products", key = "#id")
  public ProductDto getById(long id) {
    return products.findById(id)
        .map(ProductDto::from)
        .orElseThrow(() -> new ProductNotFoundException(id));
  }

  @CacheEvict(cacheNames = "products", key = "#id")
  public ProductDto update(long id, UpdateProductDto body) {
    Product saved = products.save(/* map from body */);
    return ProductDto.from(saved);
  }

  @CacheEvict(cacheNames = "products", allEntries = true)
  public void rebuildCatalog() {
    // bulk refresh — clear whole cache name
  }
}
```

**`unless = "#result == null"`** can skip caching misses if you did not disable null caching in YAML.

## 5. Explicit `RedisTemplate` (non-annotation use)

For counters, locks, pub/sub, or custom key shapes, inject **`RedisTemplate<String, String>`** (or typed values with serializers):

```java
// Compile: javac --release 22 …
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class RateLimiter {

  private final StringRedisTemplate redis;

  public RateLimiter(StringRedisTemplate redis) {
    this.redis = redis;
  }

  public boolean allow(String userId) {
    String key = "rate:" + userId;
    Long count = redis.opsForValue().increment(key);
    if (count != null && count == 1L) {
      redis.expire(key, java.time.Duration.ofMinutes(1));
    }
    return count != null && count <= 100;
  }
}
```

Spring Cache and **`RedisTemplate`** can coexist — use annotations for **entity-shaped** reads; template for **operational** keys.

## 6. Serialization

Redis stores **bytes**. Spring Cache with Redis typically serializes values as **JSON** (configure **`RedisCacheConfiguration`** with **`GenericJackson2JsonRedisSerializer`**) or JDK serialization (avoid JDK for security/versioning reasons in new code).

Custom **`@Bean`** when you need JSON and typed keys:

```java
// Compile: javac --release 22 …
import java.time.Duration;
import org.springframework.boot.autoconfigure.cache.RedisCacheManagerBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;

@Configuration
public class CacheConfig {

  @Bean
  public RedisCacheManagerBuilderCustomizer redisCacheManagerBuilderCustomizer() {
  return builder -> builder
      .cacheDefaults(
          RedisCacheConfiguration.defaultCacheConfig()
              .entryTtl(Duration.ofMinutes(10))
              .disableCachingNullValues());
  }
}
```

## 7. Conditional enablement (dev without Redis)

Gate cache beans so local dev can run without Redis when desired (see **Part III** — `@ConditionalOnProperty`):

```yaml
app:
  cache:
    enabled: true
```

```java
// Compile: javac --release 22 …
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")
public class DistributedCacheConfig {
}
```

For **`app.cache.enabled=false`**, use **`spring.cache.type=none`** or a **`NoOpCacheManager`** profile so **`@Cacheable`** becomes a no-op.

## 8. Operations checklist

1. **TTL** on every cache name — bounded staleness beats mystery bugs.
2. **Invalidate** on writes (`@CacheEvict`) or accept short inconsistency by design.
3. **Monitor** Redis memory, evictions, hit rate; alert on connection errors.
4. **Do not** treat cache as source of truth — DB (or event log) remains authoritative.
5. **Thundering herd:** many misses on one hot key — consider single-flight locking or short local overlay (advanced).
6. **Security:** password, TLS in prod; never expose Redis to the public internet.

## 9. Alternatives (names only)

| Product | Notes |
|---------|--------|
| **Redis** | De facto with Spring; strings, hashes, TTL, cluster |
| **Hazelcast** | JVM grid; embedded or client/server; Spring integration available |
| **Memcached** | Simple KV; less feature-rich than Redis |
| **Caffeine** | Local only — pair with Redis (L1 + L2) in high-scale setups |

## 10. Related notes

- **YAML & config** — Part II [YAML & external config](ii-yaml-and-external-config.md)
- **Beans & profiles** — Part III [Beans & dependency injection](iii-beans-and-dependency-injection.md)
- **JPA & transactions** — Part V [JPA & @Transactional](v-jpa-and-transactional.md) — cache sits **outside** the DB transaction; evict **after** successful commit when consistency matters
- **Security** — [Basics & filter chain](security-basics-and-filter-chain.md) (Redis passwords, TLS, network exposure)
- **Distributed transactions** — Part IX [Distributed transactions & microservices](ix-distributed-transactions-and-microservices.md) — cache invalidation vs cross-service consistency
