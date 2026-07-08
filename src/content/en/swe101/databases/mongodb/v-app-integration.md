---
label: "V"
subtitle: "App integration"
group: "MongoDB"
order: 5
---
MongoDB — app integration
Connect from applications via **official drivers** or ODMs. Examples align with the [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) and [Python](../python/i-basics-and-syntax.md) tracks.

## 1. Layers

```text
Controller  →  Service  →  Repository  →  Driver / ODM  →  MongoDB
```

| Layer | Responsibility |
|-------|----------------|
| **Repository** | Queries, indexes assumed; no HTTP |
| **Service** | Business rules, transactions spanning collections |
| **DTO / document** | Map BSON ↔ app types |

## 2. Spring Boot + Spring Data MongoDB

**Dependency** (conceptual):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

**Configuration:**

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/myapp_dev
      # or mongodb+srv://... for Atlas
```

**Document entity:**

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

**Repository:**

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

**Transactions** (replica set required):

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

Use **Motor** for async FastAPI apps.

## 4. Connection pooling

Drivers pool connections by default. Tune when many app instances connect to Atlas:

| Knob | Guidance |
|------|----------|
| **`maxPoolSize`** | Often 50–100 per process — avoid thousands of connections |
| **`serverSelectionTimeoutMS`** | Fail fast if cluster unreachable |
| **`retryWrites`** | Default true on Atlas — safe retries for idempotent writes |

One **`MongoClient`** (or Spring singleton) per process — not per request.

## 5. ODM vs raw driver

| | **Raw driver** | **Spring Data / Mongoose (Node)** |
|---|----------------|-----------------------------------|
| **Control** | Full BSON control | Convention, less boilerplate |
| **Queries** | Explicit JSON | Method names / schemas |
| **Migrations** | Your scripts | Your scripts |

Avoid N+1: fetch related data with **`$lookup`** in aggregation, **`@DocumentReference`**, or embed when modeled that way — same class of bug as SQL ORMs.

## 6. Testing

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

Use replica-set URL when testing **transactions**.

## 7. Security basics

- Never commit Atlas credentials — use env vars / secrets manager.
- App user: **`readWrite`** on one DB only.
- Enable **TLS** (`mongodb+srv` on Atlas).
- Field-level encryption or app-layer crypto for highly sensitive PII if required.

## Next

Continue with [Operations & backups](vi-operations-and-backups.md) for replica sets and restore drills.
