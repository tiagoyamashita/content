---
label: "V"
subtitle: "アプリの統合"
group: "Postgres"
order: 5
---
Postgres — アプリの統合


Applications talk to Postgres through a **driver**, usually via a **connection pool**. This note covers JDBC/Spring patterns that match the [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) track.

## 1. レイヤー

```text
Controller  →  Service  →  Repository  →  JDBC / JPA  →  Pool  →  Postgres
```

| Layer | Responsibility |
|-------|----------------|
| **Repository** | SQL or ORM queries; no HTTP concerns |
| **Pool** | Reuse TCP connections; cap concurrent DB usage |
| **Transaction** | `@Transactional` boundary — commit or rollback |

## 2. JDBC (最小限の例)

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

## 3. コネクションプーリング(HikariCP)

Spring Boot のデフォルトは **HikariCP** です。 「可能な限り大きく」ではなく、**予想される同時リクエスト**に基づいてプール サイズを構成します。

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

|ガイドライン |経験則 |
|----------|------|
| **プールのサイズ** |多くの場合、数百ではなく数十 — Postgres の接続は限られています。
| **タイムアウト** |スレッドをハングさせるのではなく、プールが使い果たされたときに高速に失敗します。
| **サービスごとに 1 つのプール** |プールせずにリクエストごとに新しい接続を開かないでください。

Postgres **`max_connections`** (default ~100) is shared — count app instances × pool size + admin overhead.

## 4. Spring Data JPA エンティティのスケッチ

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

## 5. Spring Boot での移行

一般的なセットアップ: **Flyway** は JPA が開始される前に実行されます。

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

## 6. 読み取りと書き込みの分割 (プレビュー)

大規模な場合は、**読み取り専用** クエリをレプリカにルーティングします。

```text
Primary (writes)  ──replication──►  Replica (reads)
```

ORM と接続ルーティングには、明示的なリードレプリカ データソース構成が必要です。単一の JDBC URL から自動的には構成されません。

## 7. Testcontainers を使用したローカル開発

統合テストは、実際の Postgres を Docker でスピンアップします。

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

＃＃ 次

Continue with [Operations & backups](vi-operations-and-backups.md) for roles, dumps, and recovery basics.
