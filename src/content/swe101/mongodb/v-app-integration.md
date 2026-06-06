---
label: "V"
subtitle: "アプリの統合"
group: "MongoDB"
order: 5
---
MongoDB — アプリの統合


Connect from applications via **official drivers** or ODMs. Examples align with the [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) and [Python](../python/i-basics-and-syntax.md) tracks.

## 1. レイヤー

```text
Controller  →  Service  →  Repository  →  Driver / ODM  →  MongoDB
```

|レイヤー |責任 |
|------|----------------|
| **リポジトリ** |クエリ、インデックスが想定されます。いいえ HTTP |
| **サービス** |ビジネス ルール、コレクションにまたがるトランザクション |
| **DTO / ドキュメント** | BSON ↔ アプリの種類をマップする |

## 2. Spring Boot + Spring データ MongoDB

**依存関係** (概念):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

**構成：**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/myapp_dev
      # or mongodb+srv://... for Atlas
```

**ドキュメントエンティティ:**

```java
@Document(collection = "products")
public class Product {
  @Id
  private String id;
  private String title;
  private double price;
  private List<String> tags;
  private Instant createdAt;
  // getters/setters
}
```

**リポジトリ:**

```java
public interface ProductRepository extends MongoRepository<Product, String> {
  List<Product> findByTagsContainingAndPriceLessThan(String tag, double maxPrice);
}
```

Custom queries with **`@Query`**:

```java
@Query("{ 'tags': ?0, 'price': { $lt: ?1 } }")
List<Product> cheapByTag(String tag, double maxPrice);
```

**トランザクション** (レプリカ セットが必要):

```java
@Transactional
public void transfer(String fromId, String toId, double amount) {
  // multiple repository calls in one transaction
}
```

Enable with **`@EnableMongoRepositories`** and **`MongoTransactionManager`** bean.

## 3. Python (PyMongo)

```python
from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017")
db = client["myapp_dev"]

result = db.products.insert_one({
    "title": "Keyboard",
    "price": 129.99,
    "tags": ["hardware"],
    "created_at": datetime.now(timezone.utc),
})

cursor = db.products.find(
    {"tags": "hardware", "price": {"$lt": 150}},
    {"title": 1, "price": 1},
).sort("price", -1).limit(20)

for doc in cursor:
    print(doc["title"], doc["price"])
```

非同期 FastAPI アプリには **Motor** を使用します。

## 4. 接続プーリング

ドライバーはデフォルトで接続をプールします。多くのアプリ インスタンスが Atlas に接続するときに調整します。

| Knob | Guidance |
|------|----------|
| **`maxPoolSize`** | Often 50–100 per process — avoid thousands of connections |
| **`serverSelectionTimeoutMS`** | Fail fast if cluster unreachable |
| **`retryWrites`** | Default true on Atlas — safe retries for idempotent writes |

One **`MongoClient`** (or Spring singleton) per process — not per request.

## 5. ODM と raw ドライバーの比較

| | **生のドライバー** | **Spring データ / Mongoose (ノード)** |
|---|----------------|-------------------------------------|
| **コントロール** |完全な BSON コントロール |従来の定型文を削減 |
| **クエリ** |明示的な JSON |メソッド名/スキーマ |
| **移行** |あなたのスクリプト |あなたのスクリプト |

Avoid N+1: fetch related data with **`$lookup`** in aggregation, **`@DocumentReference`**, or embed when modeled that way — same class of bug as SQL ORMs.

## 6. テスト

| Approach | Notes |
|----------|-------|
| **Testcontainers** (`mongodb` module) | Real server in Docker for integration tests |
| **Flapdoodle embedded** | In-process — version match carefully |
| **In-memory mock** | Unit tests only — misses index/query behavior |

```java
@Container
static MongoDBContainer mongo = new MongoDBContainer("mongo:7");

@DynamicPropertySource
static void mongoProps(DynamicPropertyRegistry registry) {
  registry.add("spring.data.mongodb.uri", mongo::getReplicaSetUrl);
}
```

**トランザクション**をテストする場合は、レプリカセット URL を使用します。

## 7. セキュリティの基本

- Never commit Atlas credentials — use env vars / secrets manager.
- App user: **`readWrite`** on one DB only.
- Enable **TLS** (`mongodb+srv` on Atlas).
- Field-level encryption or app-layer crypto for highly sensitive PII if required.

＃＃ 次

Continue with [Operations & backups](vi-operations-and-backups.md) for replica sets and restore drills.
