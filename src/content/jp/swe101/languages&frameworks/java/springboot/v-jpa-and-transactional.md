---
label: "V"
subtitle: "JPA と @Transactional"
group: "Spring Boot"
groupOrder: 2
order: 5
---
Spring Boot — パート V






テーブルを JPA エンティティにマップし、** を介して定型文を削減します`JpaRepository`**と**を配置します`@Transactional`** ビジネスの境界が属する場所。

## 1. エンティティの基本 (Jakarta Persistence)```java
// Compile: javac --release 22 …
package com.example.demo.domain;

import jakarta.persistence.*;
import java.util.UUID;

@Entity
@Table(name = "orders")
public class OrderEntity {

  @Id
  @GeneratedValue
  private UUID id;

  @Column(nullable = false, length = 120)
  private String customerEmail;

  @Enumerated(EnumType.STRING)
  @Column(nullable = false, length = 32)
  private OrderStatus status;

  protected OrderEntity() {} // JPA

  public OrderEntity(String customerEmail, OrderStatus status) {
    this.customerEmail = customerEmail;
    this.status = status;
  }

  public UUID getId() {
    return id;
  }

  public OrderStatus getStatus() {
    return status;
  }

  public void markPaid() {
    this.status = OrderStatus.PAID;
  }
}

enum OrderStatus {
  NEW,
  PAID,
  CANCELLED
}
```

**`ddl-auto`** (`validate`、`update`、`none`) YAML に属します — **`none`** + 移行 (Flyway/Liquibase) は実稼働環境では一般的です。

## 2. リポジトリインターフェース
Spring Data JPA は実行時にインターフェイスを実装します。

```java
// Compile: javac --release 22 …
package com.example.demo.persistence;

import com.example.demo.domain.OrderEntity;
import com.example.demo.domain.OrderStatus;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<OrderEntity, UUID> {

  List<OrderEntity> findByStatus(OrderStatus status);
}
```

派生クエリメソッド (`findBy…`) JPQL に変換します — 読み取り可能な状態に保ちます。複雑なレポート クエリは、** に属することがよくあります。`@Query`** またはネイティブ SQL。

## 3. サービス層トランザクション
**を入れてください`@Transactional`** **ユースケース** メソッドの場合、1 回の呼び出し ≡ 1 つのビジネス トランザクション:

```java
// Compile: javac --release 22 …
package com.example.demo.service;

import com.example.demo.domain.OrderEntity;
import com.example.demo.domain.OrderStatus;
import com.example.demo.persistence.OrderRepository;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {

  private final OrderRepository orders;

  public OrderService(OrderRepository orders) {
    this.orders = orders;
  }

  @Transactional(readOnly = true)
  public OrderEntity get(UUID id) {
    return orders.findById(id).orElseThrow(() -> new IllegalArgumentException("unknown order"));
  }

  @Transactional
  public OrderEntity placeOrder(String email) {
    OrderEntity o = new OrderEntity(email, OrderStatus.NEW);
    return orders.save(o);
  }

  @Transactional
  public void markPaid(UUID id) {
    OrderEntity o = get(id);
    o.markPaid(); // dirty checking persists at flush/commit
  }
}
```

## 4. ロールバック動作
- **チェックされていない**例外 (`RuntimeException`サブクラス) → **デフォルトで**ロールバックします。
- **チェック済み**例外 → **設定しない限り**コミット**`rollbackFor`**:

```java
// Compile: javac --release 22 …
@Transactional(rollbackFor = Exception.class)
public void importOrders(InputStream csv) throws IOException {
  // IOException now triggers rollback
}
```

## 5. 伝播パターン
|値 |一般的な使用法 |
|------|-----------|
| **`REQUIRED`** (デフォルト) |呼び出し元のトランザクションに参加するか、新しいトランザクションを開始します |
| **`REQUIRES_NEW`** |常に新しい tx — 外部ロールバックに依存しない監査ログ |
| **`NOT_SUPPORTED`** | tx を一時停止する — まれに、tx 内で誤動作する統合の場合 |

```java
// Compile: javac --release 22 …
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void saveAuditEntry(String action) {
  // commits even if outer business tx rolls back (when exceptions handled carefully)
}
```

## 6. 落とし穴
- **`@Transactional`** の上 **`private`** メソッドまたは自己呼び出し (`this.markPaid`) **AOP プロキシを開始しません** — 本当に必要な場合は、別の Bean に抽出するか、挿入されたプロキシを介して呼び出します (より良い: 境界を粗く保つ)。
- **`readOnly = true`** 最適化のための Hibernate/JDBC ドライバーのヒント — ** と組み合わせます`@Transactional`** クエリの多いサービス メソッドについて。
