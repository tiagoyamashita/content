---
label: "V"
subtitle: "JPA と @Transactional"
group: "スプリングブーツ"
groupOrder: 2
order: 5
---
スプリング ブーツ — パート V

テーブルを JPA エンティティにマップし、**`JpaRepository`** によってボイラープレートを削減し、ビジネス境界が属する場所に **`@Transactional`** を配置します。

## 1. エンティティの基本 (Jakarta Persistence)
```java
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

**`ddl-auto`** (`validate`、`update`、`none`) は YAML に属します — **`none`** + 移行 (Flyway/Liquibase) は運用環境では一般的です。

## 2. リポジトリインターフェース
Spring Data JPA は実行時にインターフェースを実装します。

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

派生クエリ メソッド (`findBy…`) は JPQL に変換されます。読み取り可能な状態を保ちます。複雑なレポート クエリは、**`@Query`** またはネイティブ SQL に属することがよくあります。

## 3. サービス層トランザクション
**ユースケース** メソッドに **`@Transactional`** を設定して、1 つの呼び出し≡ 1 つのビジネス トランザクションを実行します。

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
- **チェックされていない**例外(`RuntimeException`サブクラス) → **デフォルトで**ロールバック。
- **チェック済み**の例外 → **`rollbackFor`** を設定しない限り **コミット**:

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
- **`private`** メソッドまたは自己呼び出し (`this.markPaid`) の **`@Transactional`** は AOP プロキシを **開始しません** - 本当に必要な場合は、別の Bean に抽出するか、挿入されたプロキシを介して呼び出します (より良い: 境界を粗く保つ)。
- **`readOnly = true`** は、最適化のための Hibernate/JDBC ドライバーをヒントします。クエリの多いサービス メソッドでは **`@Transactional`** と組み合わせます。
