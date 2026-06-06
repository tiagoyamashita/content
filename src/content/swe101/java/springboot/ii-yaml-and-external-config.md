---
label: "II"
subtitle: "YAML と外部構成"
group: "スプリングブーツ"
groupOrder: 2
order: 2
---
Spring Boot — パート II

**`application.yml`** / **`application.properties`** から型指定された構成をバインドし、**プロファイル**で動作を切り替え、秘密をソース管理外に保ちます。

## 1. 解決順序 (メンタルモデル)
後のソースは、同じプロパティ キーの以前のソースを**オーバーライド**します。一般的な優先順位には次のものが含まれます (簡略化)。

1. コマンドライン引数 (`--server.port=9090`)
2. **`SPRING_APPLICATION_JSON`** インライン JSON 環境変数
3. **`Java System` プロパティ**
4. **`OS environment variables`** (リラックスバインディング: `SPRING_DATASOURCE_URL` → `spring.datasource.url`)
5. プロファイル固有のファイル: **`application-{profile}.yml`**
6. クラスパスのルートにある **`application.yml`**

正確な順序はブート バージョンごとに文書化されています。**環境ごとに 1 つの明らかなソース** (本番環境の環境変数 / シークレット マネージャー) に依存します。

## 2. プロパティ キーにマップされたネストされた YAML
YAML ネストはドット区切りのキーになります Spring はすでに以下を理解しています。

```yaml
server:
  port: 8080

spring:
  application:
    name: billing-service
  datasource:
    url: jdbc:postgresql://localhost:5432/billing
    username: billing
    password: ${DB_PASSWORD}   # never hard-code real secrets in repo

logging:
  level:
    root: INFO
    org.hibernate.SQL: DEBUG
```

`spring.datasource.password` resolves **`${DB_PASSWORD}`** from the process environment at runtime.

## 3. 環境に合わせたデフォルトのプロファイル
**`dev`** がアクティブな場合、**`application-dev.yml`** がロードされます。

```yaml
# application.yml — shared defaults
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

---
# application-dev.yml
spring:
  jpa:
    hibernate:
      ddl-auto: update
logging:
  level:
    com.example: DEBUG
```

**`---`** ドキュメント セパレーターを使用すると、1 つの YAML ファイル内の複数の論理ドキュメントを分割できます。通常、プロファイルごとに個別のファイルを作成すると、より明確になります。

テストでは **`spring.profiles.active=prod`**、**`SPRING_PROFILES_ACTIVE`**、または **`@ActiveProfiles("test")`** を通じてアクティブ化します。

## 4. 個々のキーの場合は `@Value`
少数のスカラーには適しています。デフォルトでは、キーが欠落している場合のクラッシュを回避します。

```java
// Compile: javac --release 22 …
@Component
public class FeatureToggle {

  @Value("${app.features.beta:false}")
  private boolean betaUi;

  @Value("${app.rate-limit.max:100}")
  private int maxRequestsPerMinute;

  public boolean isBetaUi() {
    return betaUi;
  }
}
```

**制限事項**: 1 つのクラス上の無関係な **`@Value`** フィールドが多数あると、テストと文書化が難しくなります。グループ化された **`@ConfigurationProperties`** をお勧めします。

## 5. `@ConfigurationProperties` (型付きグループ)
不変レコード (ブート 3+) を宣言し、**`app.notification`** サブツリーをバインドします。

```yaml
# application.yml
app:
  notification:
    from-address: no-reply@example.com
    retry-attempts: 3
    timeout-ms: 5000
```

```java
// Compile: javac --release 22 …
package com.example.demo.config;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@ConfigurationProperties(prefix = "app.notification")
@Validated
public record NotificationProperties(
    @NotBlank @Email String fromAddress,
    @Min(0) @Max(10) int retryAttempts,
    @Min(100) long timeoutMs
) {}
```

Bean を登録します。

```java
// Compile: javac --release 22 …
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(NotificationProperties.class)
public class NotificationConfig {}
```

または、**`@ConfigurationPropertiesScan`** を **`@SpringBootApplication`** の隣に配置して、ブートがスキャンされたパッケージ内の **`@ConfigurationProperties`** タイプを検出できるようにします。

他の Bean と同様に注入します。

```java
// Compile: javac --release 22 …
@Service
public class MailNotificationService {

  private final NotificationProperties props;

  public MailNotificationService(NotificationProperties props) {
    this.props = props;
  }

  public void sendWelcome(String to) {
    // use props.fromAddress(), props.retryAttempts(), …
  }
}
```

## 6. 緩和された拘束力のリマインダー
YAML の `from-address` は Java の **`fromAddress`** にバインドされます。環境変数は、接頭辞 **`app.notification`** に **`APP_NOTIFICATION_FROMADDRESS`** スタイルの大文字スネークケースを使用します。

## 7. タイプセーフな構成の概要
|アプローチ |こんな方に最適 |
|----------|----------|
| **`@Value`** |一回限りのフラグ / 従来の統合 |
| **`@ConfigurationProperties`** |検証を伴う構造化された設定 |
| **`Environment` / `@Environment`** |動的検索またはフレームワーク コード |
