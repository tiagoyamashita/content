---
label: "V"
subtitle: "App integration"
group: "Postgres"
order: 5
---
Postgres — app integration
Applications talk to Postgres through a **driver**, usually via a **connection pool**. This note covers JDBC/Spring patterns that match the [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) track.

## 1. Layers

```text
Controller  →  Service  →  Repository  →  JDBC / JPA  →  Pool  →  Postgres
```

| Layer | Responsibility |
|-------|----------------|
| **Repository** | SQL or ORM queries; no HTTP concerns |
| **Pool** | Reuse TCP connections; cap concurrent DB usage |
| **Transaction** | `@Transactional` boundary — commit or rollback |

## 2. JDBC (minimal example)

```java
// Java SE 22 — try-with-resources
var url = "jdbc:postgresql://localhost:5432/myapp_dev";
try (var conn = DriverManager.getConnection(url, "myapp", "secret");
     var ps = conn.prepareStatement(
         "SELECT id, title FROM todos WHERE done = ? ORDER BY id")) {
  ps.setBoolean(1, false);
  try (var rs = ps.executeQuery()) {
    while (rs.next()) {
      System.out.printf("%d %s%n", rs.getLong("id"), rs.getString("title"));
    }
  }
}
```

Always use **`PreparedStatement`** — parameter binding prevents SQL injection and enables plan cache reuse.

## 3. Connection pooling (HikariCP)

Spring Boot defaults to **HikariCP**. Configure pool size from **expected concurrent requests**, not “as high as possible”:

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/myapp_dev
    username: myapp
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
      connection-timeout: 5000
```

| Guideline | Rule of thumb |
|-----------|---------------|
| **Pool size** | Often tens, not hundreds — Postgres has limited connections |
| **Timeout** | Fail fast when pool exhausted instead of hanging threads |
| **One pool per service** | Do not open a new connection per request without pooling |

Postgres **`max_connections`** (default ~100) is shared — count app instances × pool size + admin overhead.

## 4. Spring Data JPA entity sketch

```java
@Entity
@Table(name = "todos")
public class Todo {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String title;

  @Column(nullable = false)
  private boolean done;

  @Column(name = "created_at", nullable = false, updatable = false)
  private Instant createdAt;

  @PrePersist
  void onCreate() {
    createdAt = Instant.now();
  }
}
```

```java
public interface TodoRepository extends JpaRepository<Todo, Long> {
  List<Todo> findByDoneFalseOrderByIdAsc();
}
```

See [JPA & transactional](../java/springboot/v-jpa-and-transactional.md) for transaction boundaries and lazy-loading pitfalls.

## 5. Migrations in Spring Boot

Typical setup: **Flyway** runs before JPA starts:

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
  jpa:
    hibernate:
      ddl-auto: validate   # never 'update' in production
```

**`ddl-auto: validate`** — Hibernate checks entities match DB; Flyway owns schema changes.

## 6. Read vs write splitting (preview)

At scale, route **read-only** queries to replicas:

```text
Primary (writes)  ──replication──►  Replica (reads)
```

ORM and connection routing need explicit read-replica datasource config — not automatic from a single JDBC URL.

## 7. Local dev with Testcontainers

Integration tests spin up real Postgres in Docker:

```java
@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

@DynamicPropertySource
static void dbProps(DynamicPropertyRegistry registry) {
  registry.add("spring.datasource.url", postgres::getJdbcUrl);
  registry.add("spring.datasource.username", postgres::getUsername);
  registry.add("spring.datasource.password", postgres::getPassword);
}
```

Same SQL dialect as production — preferable to H2 for Postgres-specific features (`JSONB`, constraints).

## Next

Continue with [Operations & backups](vi-operations-and-backups.md) for roles, dumps, and recovery basics.
