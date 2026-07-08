---
label: "VIII"
subtitle: "分散キャッシュ"
group: "Spring Boot"
groupOrder: 2
order: 10
---
Spring Boot — パート VIII: 分散キャッシュ

**分散キャッシュ**は**共有インフラストラクチャ** (通常は**Redis**) にエントリを保存するため、アプリの**すべてのインスタンス**は同じデータを参照できます。 **ローカル** キャッシュ (1 つの JVM 内の **Caffeine**) は読み取りごとに高速ですが、ポッドまたはサーバー間で共有されません**。

**Java ベースライン:** **Java SE 22** (`javac --release 22`);例は **Spring Boot 3.x** をターゲットとしています。

## 1.必要な場合

|アプローチ |インスタンス間で共有されますか? |一般的な使用法 |
|----------|--------------------------|---------------|
| **キャッシュなし** | — |真実の情報源は DB のみ |
| **地元** （`Caffeine`、`ConcurrentHashMap`) |いいえ |ノードごとのホット読み取り、構成フラグ |
| **分散** (Redis、Hazelcast) |はい |セッションのようなデータ、レート制限、共有ルックアップ テーブル、クラスター全体の DB 負荷の削減 |

**キャッシュアサイド (遅延読み込み):** アプリはキャッシュを読み取ります → ミスの場合、DB からロードします → キャッシュを書き込みます → 戻ります。データが変更されると、**無効化**が発生します (`@CacheEvict`、TTL、またはメッセージ駆動型のエビクション）。

## 2. Spring Boot + Redis のスタック

依存関係を追加します (Maven 座標 — BOM バージョンを使用します)。

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

- **`spring-boot-starter-cache`** — **`@Cacheable`**、**`CacheManager`**、Bean の周りの AOP。
- **`spring-boot-starter-data-redis`** — **`RedisConnectionFactory`**、**`RedisTemplate`**、レタスクライアント (デフォルト)。

アプリケーションクラスでキャッシュが有効になります。

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

## 3. 設定 (`application.yml`)

すべてのインスタンスが **同じ** Redis (またはクラスター) を指すようにします。 prod で環境変数を使用します (**パート II** を参照 — [YAML & 外部構成](ii-yaml-and-external-config.md））。

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

|プロパティ |役割 |
|----------|------|
| **`spring.cache.type=redis`** | Redis が支援する ** を使用する`CacheManager`** (メモリ内のみではない) |
| **`time-to-live`** |デフォルトのエントリの有効期限 — 古いデータを永久に回避します。
| **`key-prefix`** |複数のアプリが 1 つの Redis | を共有する場合の名前空間キー
| **`cache-null-values: false`** |オプション: 意図しない限り、「見つかりません」をキャッシュしないでください。

**クラスター/センチネル:** 使用 **`spring.data.redis.cluster.nodes`** または **`spring.data.redis.sentinel`** — 同じ Spring Cache 層。接続ファクトリーの変更のみ。

開発用にローカルで Redis を実行します。

```text
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

## 4. サービスの宣言型キャッシュ

置く **`@Cacheable`** サービス** メソッド (コントローラーではない) 上。キャッシュキーのデフォルトはメソッドパラメータです。 ** でカスタマイズする`key`** 特別。

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

**`unless = "#result == null"`** YAML で null キャッシュを無効にしなかった場合、キャッシュ ミスをスキップできます。

## 5.明示的`RedisTemplate`(アノテーション以外の使用)

カウンター、ロック、パブリッシュ/サブスクライブ、またはカスタム キー形状の場合は、** を注入します。`RedisTemplate<String, String>`** (またはシリアライザーを使用して型指定された値):

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

Spring キャッシュと **`RedisTemplate`** 共存可能 — **エンティティ形状**の読み取りにはアノテーションを使用します。 **操作**キーのテンプレート。

## 6.シリアル化

Redis は **バイト** を保存します。 Redis を使用した Spring Cache は通常、値を **JSON** としてシリアル化します (** を構成します)`RedisCacheConfiguration`** と **`GenericJackson2JsonRedisSerializer`**) または JDK シリアル化 (新しいコードではセキュリティ/バージョン管理上の理由から JDK を避けてください)。

カスタム **`@Bean`** JSON と入力されたキーが必要な場合:

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

## 7. 条件付き有効化 (Redis を使用しない開発)

ゲート キャッシュ Bean により、必要に応じてローカル開発が Redis なしで実行できるようになります (**パート III** を参照)`@ConditionalOnProperty`):

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

のために **`app.cache.enabled=false`**、 使用 **`spring.cache.type=none`** または **`NoOpCacheManager`**プロフィールです**`@Cacheable`** は noop になります。

## 8. 動作チェックリスト

1. すべてのキャッシュ名に **TTL** — 境界のある古さは謎のバグを克服します。
2. 書き込みを **無効にする** (`@CacheEvict`）または設計上の短い不一致を受け入れます。
3. **監視** Redis メモリ、エビクション、ヒット率。接続エラーに関するアラート。
4. **キャッシュを真実の情報源として扱わないでください** — DB (またはイベント ログ) が引き続き権威を持ちます。
5. **サンダーリングの群れ:** 1 つのホット キーで多くのミスが発生します。シングルフライト ロックまたは短いローカル オーバーレイ (上級) を検討してください。
6. **セキュリティ:** パスワード、本番環境の TLS。 Redis を公共のインターネットに公開しないでください。

## 9. 代替案 (名前のみ)

|製品 |メモ |
|----------|----------|
| **Redis** | Spring では事実上、文字列、ハッシュ、TTL、クラスター |
| **ヘーゼルキャスト** | JVM グリッド;組み込みまたはクライアント/サーバー。 Spring 統合が利用可能 |
| **Memcached** |単純な KV; Redis よりも機能が豊富ではありません。
| **カフェイン** |ローカルのみ — 大規模セットアップでは Redis (L1 + L2) と組み合わせます。

## 10. 関連メモ

- **YAML & 構成** — パート II [YAML & 外部構成](ii-yaml-and-external-config.md)
- **Bean とプロファイル** — パート III [Bean と依存関係の注入](iii-beans-and-dependency-injection.md)
- **JPA とトランザクション** — パート V [JPA と @Transactional](v-jpa-and-transactional.md) — キャッシュは DB トランザクションの**外側**にあります。一貫性が重要な場合は、**成功したコミット後に**削除します
- **セキュリティ** — [基本とフィルター チェーン](security-basics-and-filter-chain.md) (Redis パスワード、TLS、ネットワーク露出)
