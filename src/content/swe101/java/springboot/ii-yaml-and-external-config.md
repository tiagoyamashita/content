---
label: "II"
subtitle: "YAML & external config"
group: "Spring Boot"
groupOrder: 2
order: 2
---
Spring Boot — Part II
Bind typed configuration from **`application.yml`** / **`application.properties`**, switch behavior with **profiles**, and keep secrets out of source control.

## 1. Resolution order (mental model)
Later sources **override** earlier ones for the same property key. Typical precedence includes (simplified):

1. Command-line arguments (`--server.port=9090`)
2. **`SPRING_APPLICATION_JSON`** inline JSON env var
3. **`Java System` properties**
4. **`OS environment variables`** (relaxed binding: `SPRING_DATASOURCE_URL` → `spring.datasource.url`)
5. Profile-specific files: **`application-{profile}.yml`**
6. **`application.yml`** at the root of the classpath

Exact ordering is documented per Boot version — rely on **one obvious source per environment** (env vars / secrets manager in prod).

## 2. Nested YAML mapped to property keys
YAML nests become dot-separated keys Spring already understands:

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

## 3. Profiles for environment-shaped defaults
**`application-dev.yml`** loads when **`dev`** is active:

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

The **`---`** document separator can split multiple logical documents inside one YAML file; separate files per profile are usually clearer.

Activate via **`spring.profiles.active=prod`**, **`SPRING_PROFILES_ACTIVE`**, or **`@ActiveProfiles("test")`** in tests.

## 4. `@Value` for individual keys
Good for a handful of scalars; defaults avoid crashes when a key is missing:

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

**Limitation**: many unrelated **`@Value`** fields on one class become hard to test and document — prefer grouped **`@ConfigurationProperties`**.

## 5. `@ConfigurationProperties` (typed groups)
Declare an immutable record (Boot 3+) and bind the **`app.notification`** subtree:

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

Register the bean:

```java
// Compile: javac --release 22 …
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(NotificationProperties.class)
public class NotificationConfig {}
```

Or place **`@ConfigurationPropertiesScan`** next to **`@SpringBootApplication`** so Boot discovers **`@ConfigurationProperties`** types in scanned packages.

Inject like any bean:

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

## 6. Relaxed binding reminders
`from-address` in YAML binds to **`fromAddress`** in Java; env vars use **`APP_NOTIFICATION_FROMADDRESS`** style upper snake case for prefix **`app.notification`**.

## 7. Type-safe config summary
| Approach | Best for |
|----------|----------|
| **`@Value`** | One-off flags / legacy integration |
| **`@ConfigurationProperties`** | Structured settings with validation |
| **`Environment` / `@Environment`** | Dynamic lookups or framework code |
