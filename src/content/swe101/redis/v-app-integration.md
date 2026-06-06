---
label: "V"
subtitle: "アプリの統合"
group: "レディス"
order: 5
---
Redis — アプリの統合

**接続プーリング**、**タイムアウト**、**重要な規則**を初日から使用してください。例は [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) および [Python](../python/i-basics-and-syntax.md) に準拠しています。

## 1. Java — レタス (推奨)

Lettuce は非同期対応であり、Spring Boot 2+ ではデフォルトです。

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

**`try-with-resources`** または Spring マネージド Bean を使用します。リクエストごとではなく、アプリごとに 1 つのクライアントを使用します。

## 2. Spring Boot + Spring Data Redis

**依存：**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

**構成：**

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

**キャッシュの抽象化:**

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

**`@EnableCaching`** および Redis キャッシュ マネージャー Bean で有効にします。

**春のセッション:**

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

**接続プール**を使用します:

```python
pool = redis.ConnectionPool(host="localhost", port=6379, max_connections=20)
r = redis.Redis(connection_pool=pool)
```

FastAPI/非同期ワーカーの場合は **redis.asyncio**。

## 4. パイプラインとトランザクション

バッチ コマンド - 1 往復:

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

**`MULTI`/`EXEC`** — アトミック グループ (失敗時のロールバックを伴うキー間の SQL トランザクションとは異なります。Redis セマンティクスを理解しています)。

## 5. エラー処理

|エラー |アクション |
|------|----------|
| **接続が拒否されました** |早く失敗してください。キャッシュがオプションの場合は DB へのサーキット ブレーカー |
| **OOM / 最大メモリ** |警告;エビクションポリシーとキーサイズを確認する |
| **タイムアウト** |べき等読み取りを再試行します。書き込み時の無制限の再試行を回避します。

**キャッシュのオプション パターン:** Redis 障害が発生した場合、データベースにフォールバックします。速度は遅くなりますが、利用可能です。

## 6. テスト

|アプローチ |メモ |
|----------|----------|
| **テストコンテナ** (`redis:7`) |実サーバーとの統合テスト |
| **埋め込み Redis モック** |単体テストのみ - 動作が異なります。

```java
@Container
static GenericContainer<?> redis = new GenericContainer<>("redis:7").withExposedPorts(6379);

@DynamicPropertySource
static void redisProps(DynamicPropertyRegistry registry) {
  registry.add("spring.data.redis.host", redis::getHost);
  registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
}
```

＃＃ 次

RDB、AOF、およびレプリケーションの[操作と永続性](vi-operations-and-persistence.md)に進みます。
