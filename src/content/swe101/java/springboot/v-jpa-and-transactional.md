---
label: "V"
subtitle: "JPA & @Transactional"
group: "Spring Boot"
groupOrder: 2
order: 5
---
Spring Boot — Part V
Map tables with JPA entities, reduce boilerplate via **`JpaRepository`**, and place **`@Transactional`** where business boundaries belong.

## 1. Entity basics (Jakarta Persistence)
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

**`ddl-auto`** (`validate`, `update`, `none`) belongs in YAML — **`none`** + migrations (Flyway/Liquibase) is typical in production.

## 2. Repository interface
Spring Data JPA implements the interface at runtime:

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

Derived query methods (`findBy…`) translate to JPQL — keep them readable; complex reporting queries often belong in **`@Query`** or native SQL.

## 3. Service-layer transactions
Put **`@Transactional`** on **use-case** methods so one call ≡ one business transaction:

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

## 4. Rollback behavior
- **Unchecked** exceptions (`RuntimeException` subclasses) → rollback **by default**.
- **Checked** exceptions → **commit** unless you set **`rollbackFor`**:

```java
// Compile: javac --release 22 …
@Transactional(rollbackFor = Exception.class)
public void importOrders(InputStream csv) throws IOException {
  // IOException now triggers rollback
}
```

## 5. Propagation patterns
| Value | Typical use |
|-------|-------------|
| **`REQUIRED`** (default) | Join caller’s transaction or start a new one |
| **`REQUIRES_NEW`** | Always new tx — audit logging independent of outer rollback |
| **`NOT_SUPPORTED`** | Suspend tx — rare, for integrations that misbehave inside a tx |

```java
// Compile: javac --release 22 …
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void saveAuditEntry(String action) {
  // commits even if outer business tx rolls back (when exceptions handled carefully)
}
```

## 6. Pitfalls
- **`@Transactional`** on **`private`** methods or self-invocations (`this.markPaid`) **does not** start AOP proxies — extract to another bean or call through the injected proxy if you truly need it (better: keep boundaries coarse).
- **`readOnly = true`** hints Hibernate/JDBC drivers for optimizations — pair with **`@Transactional`** on query-heavy service methods.
