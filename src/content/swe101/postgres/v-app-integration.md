---
label: "V"
subtitle: "アプリの統合"
group: "ポストグレ"
order: 5
---
Postgres — アプリの統合

アプリケーションは **ドライバー** (通常は **接続プール**) を介して Postgres と通信します。このノートでは、[Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) トラックに一致する JDBC/Spring パターンについて説明します。

## 1. レイヤー

```text
Controller  →  Service  →  Repository  →  JDBC / JPA  →  Pool  →  Postgres
```

|レイヤー |責任 |
|------|----------------|
| **リポジトリ** | SQL または ORM クエリ。 HTTP の心配はありません |
| **プール** | TCP 接続を再利用します。同時 DB 使用量の上限 |
| **トランザクション** | `@Transactional` 境界 — コミットまたはロールバック |

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

常に **`PreparedStatement`** を使用します。パラメーター バインドにより SQL インジェクションが防止され、プラン キャッシュの再利用が可能になります。

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
| **プールのサイズ** |多くの場合、数百ではなく数十 — Postgres の接続には制限があります。
| **タイムアウト** |スレッドをハングさせるのではなく、プールが使い果たされたときに高速に失敗します。
| **サービスごとに 1 つのプール** |プールせずにリクエストごとに新しい接続を開かないでください。

Postgres **`max_connections`** (デフォルトは ~100) が共有されます - アプリ インスタンスの数 × プール サイズ + 管理オーバーヘッド。

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

トランザクション境界と遅延読み込みの落とし穴については、[JPA とトランザクション](../java/springboot/v-jpa-and-transactional.md) を参照してください。

## 5. Spring Boot での移行

一般的なセットアップ: **Flyway** は JPA が開始する前に実行されます。

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
  jpa:
    hibernate:
      ddl-auto: validate   # never 'update' in production
```

**`ddl-auto: validate`** — Hibernate はエンティティが DB と一致することをチェックします。 Flyway はスキーマ変更を所有します。

## 6. 読み取りと書き込みの分割 (プレビュー)

大規模な場合は、**読み取り専用** クエリをレプリカにルーティングします。

```text
Primary (writes)  ──replication──►  Replica (reads)
```

ORM と接続ルーティングには、単一の JDBC URL から自動的に設定されるものではなく、明示的なリードレプリカ データソース設定が必要です。

## 7. Testcontainers を使用したローカル開発

統合テストは Docker で実際の Postgres を起動します。

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

運用環境と同じ SQL 言語 - Postgres 固有の機能 (`JSONB`、制約) を考慮すると H2 よりも望ましい。

＃＃ 次

役割、ダンプ、およびリカバリの基本については、[操作とバックアップ](vi-operations-and-backups.md) に進みます。
