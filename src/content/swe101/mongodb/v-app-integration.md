---
label: "V"
subtitle: "アプリの統合"
group: "モンゴDB"
order: 5
---
MongoDB — アプリの統合

**公式ドライバー**または ODM を介してアプリケーションから接続します。例は、[Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) および [Python](../python/i-basics-and-syntax.md) トラックに沿っています。

## 1. レイヤー

```text
Controller  →  Service  →  Repository  →  Driver / ODM  →  MongoDB
```

|レイヤー |責任 |
|------|----------------|
| **リポジトリ** |クエリ、インデックスが想定されます。 HTTPなし |
| **サービス** |ビジネス ルール、コレクションにまたがるトランザクション |
| **DTO / ドキュメント** | BSON ↔ アプリの種類をマップ |

## 2. Spring Boot + Spring Data MongoDB

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

**`@Query`** を使用したカスタム クエリ:

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

**`@EnableMongoRepositories`** および **`MongoTransactionManager`** Bean で有効にします。

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

|ノブ |ガイダンス |
|------|----------|
| **`maxPoolSize`** |多くの場合、プロセスごとに 50 ～ 100 — 数千の接続を避ける |
| **`serverSelectionTimeoutMS`** |クラスターに到達できない場合はフェイルファスト |
| **`retryWrites`** | Atlas のデフォルトは true — 冪等書き込みの安全な再試行 |

リクエストごとではなく、プロセスごとに 1 つの **`MongoClient`** (または Spring シングルトン)。

## 5. ODM と生のドライバーの比較

| | **生のドライバー** | **Spring データ / Mongoose (ノード)** |
|---|----------------|-------------------------------------|
| **コントロール** |完全な BSON コントロール |従来の定型文を削減 |
| **クエリ** |明示的な JSON |メソッド名/スキーマ |
| **移行** |あなたのスクリプト |あなたのスクリプト |

N+1 を回避します。**`$lookup`** を集約して関連データをフェッチするか、**`@DocumentReference`** でモデル化する場合は埋め込みます。これは SQL ORM と同じクラスのバグです。

## 6. テスト

|アプローチ |メモ |
|----------|----------|
| **テストコンテナ** (`mongodb` モジュール) |統合テスト用の Docker の実サーバー |
| **Flapdoodle が埋め込まれています** |インプロセス — バージョンは慎重に一致します |
| **インメモリモック** |単体テストのみ - インデックス/クエリ動作が欠落します。

```java
@Container
static MongoDBContainer mongo = new MongoDBContainer("mongo:7");

@DynamicPropertySource
static void mongoProps(DynamicPropertyRegistry registry) {
  registry.add("spring.data.mongodb.uri", mongo::getReplicaSetUrl);
}
```

**トランザクション**をテストする場合は、レプリカ セット URL を使用します。

## 7. セキュリティの基本

- Atlas 認証情報を決してコミットしないでください。環境変数 / シークレット マネージャーを使用してください。
- アプリユーザー: **`readWrite`** 1 つの DB のみ。
- **TLS** を有効にします (Atlas では `mongodb+srv`)。
- 必要に応じて、機密性の高い PII に対するフィールド レベルの暗号化またはアプリ層の暗号化。

＃＃ 次

レプリカセットとリストアの訓練については、[操作とバックアップ](vi-operations-and-backups.md) に進みます。
