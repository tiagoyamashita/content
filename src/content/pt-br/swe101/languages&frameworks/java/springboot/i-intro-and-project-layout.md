---
label: "I"
subtitle: "Intro & project layout"
group: "Spring Boot"
groupOrder: 2
order: 1
---
Spring Boot — Part I
What Boot adds on top of Spring, how the entrypoint bootstraps the container, and how to lay out packages so scanning and auto-configuration behave predictably.

**How this section is organized:** finish the **Java** intro track (`intro/`, Parts I–VI) first, then work through these **Spring Boot** pages in order. The **Example (Web MVC)** copy-paste layout lives under **`springboot/`**; **Security basics** follows REST before operations topics.

**JDK / Java language level:** examples in this **Spring Boot** track assume **Java SE 22** — use **`javac --release 22`** or set language level **22** in your build (`pom.xml` / `build.gradle`). The same snippets compile on **JDK 21 LTS** unless a file calls out a newer feature. For services in production, prefer a supported **LTS** JDK unless your organization standardizes on a newer release.

## 1. Problems Boot solves
- **Classpath hell**: starters (e.g. `spring-boot-starter-web`) pin compatible versions of servlet API, Jackson, Tomcat.
- **Embedded server**: run `java -jar app.jar` without installing Tomcat separately.
- **Auto-configuration**: if Hibernate + datasource are on the classpath, JPA set-up appears unless you opt out — driven by **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (Boot 3.x).

## 2. Minimal application entrypoint
`@SpringBootApplication` is shorthand for **`@SpringBootConfiguration`** (specialized `@Configuration`), **`@EnableAutoConfiguration`**, and **`@ComponentScan`** on the declaring class’s package.

```java
// Compile: javac --release 22 …
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
```

- **`SpringApplication.run`** builds the **`ApplicationContext`**, runs **`ApplicationRunner`** / **`CommandLineRunner`** beans, and starts the web server when **`spring-boot-starter-web`** is present.

## 3. Component scanning rules
- Only types under **`com.example.demo`** and **sub-packages** are scanned by default (same package as `@SpringBootApplication`).
- If you put **`@SpringBootApplication`** in **`com.example.demo`** but controllers live in **`com.example.api`**, they **won’t** be beans unless you add **`@ComponentScan("com.example.api")`** or move code under **`demo`**.

```java
// Compile: javac --release 22 …
@SpringBootApplication
@ComponentScan(basePackages = "com.example")
public class DemoApplication { /* ... */ }
```

## 4. Typical Maven coordinates (conceptual)
Your `pom.xml` usually declares **`spring-boot-starter-parent`** (or the BOM via **`spring-boot-dependencies`**) plus starters:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

**Gradle (`build.gradle.kts`):**

```kotlin
plugins {
  id("org.springframework.boot") version "3.4.0"
  id("io.spring.dependency-management") version "1.1.6"
  kotlin("jvm") version "2.0.21" // optional; Java-only projects omit
  java
}

dependencies {
  implementation("org.springframework.boot:spring-boot-starter-web")
  implementation("org.springframework.boot:spring-boot-starter-data-jpa")
}
```

Use the same artifact IDs as Maven; the Spring Boot Gradle plugin applies the BOM for aligned versions.

## 5. Layered packages (recommended shape)
A common layout keeps **web**, **application/service**, and **persistence** concerns apart:

```
com.example.demo
  DemoApplication.java
  config/          ← @Configuration classes, property beans
  web/             ← @RestController, DTOs used at the boundary
  service/         ← @Service, transactions
  domain/          ← entities / domain models (optional)
  persistence/     ← @Repository, JPA adapters
```

Controllers depend on services; services depend on repositories or ports — **avoid** controllers injecting repositories directly when business rules grow.

## 6. Disabling a slice of auto-configuration
When auto-config gets in the way during migration or tests:

```java
// Compile: javac --release 22 …
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class DemoApplication { /* ... */ }
```

Prefer fixing classpath / properties first; **`exclude`** is a deliberate escape hatch.

## 7. Java & Spring Boot versions (Java 8 → today)

This track targets **Spring Boot 3.x** on **Java 21+** (examples often use **Java 22**). Use the tables below when upgrading JDKs, picking a Boot line, or migrating legacy services.

### Spring Boot release → Java range & what changed

| Spring Boot | Min Java | Tested up to | Headline changes for app code |
|-------------|----------|--------------|-------------------------------|
| **2.0** | 8 | 9 | Boot 2 baseline; **`javax.*`** servlet/JPA namespaces; embedded Tomcat 8.5 |
| **2.1 – 2.3** | 8 | 15 | Incremental starters, actuator, test slices mature on **`javax`** stack |
| **2.4 – 2.6** | 8 | 19 | Config import, layered jars; still **`javax`**; Java 11+ recommended for new 2.x work |
| **2.7** | 8 | **21** | **Last 2.x line** — bridge JDK for teams moving 8/11 → 17 before Boot 3 |
| **3.0** | **17** | 21 | **`jakarta.*`** rename (`javax.servlet` → `jakarta.servlet`, JPA, validation); **Spring Framework 6**; **Servlet 6** / Tomcat 10; native-image focus; **no Java 8/11** |
| **3.1** | 17 | 21 | Dev services (Docker Compose), Testcontainers integration; SSL bundle config |
| **3.2** | 17 | 21 | **`spring.threads.virtual.enabled`** (needs **Java 21**); **`RestClient`**; JDBC client auto-config — see [Virtual threads](xi-virtual-threads.md) |
| **3.3** | 17 | 23 | Broader JDK 22/23 support; CDS / AOT tweaks; observability property clean-up |
| **3.4** | 17 | 24 | Structured logging (`logging.structured.format.*`); dependency bumps (Jackson, Tomcat) |
| **3.5+** | 17 | 25+ | Current 3.x maintenance — check [spring.io](https://spring.io/projects/spring-boot) for latest patch and JDK ceiling |

**Big migration jumps:** **2.7 → 3.0** (Java **17** + **Jakarta** package renames + Spring Security 6). **3.0 → 3.2+** is mostly dependency bumps unless you adopt **virtual threads** (Java **21**). Patch upgrades within 3.x are usually days, not weeks.

### Java release → Spring Boot lines & language features

| Java | Spring Boot you can run | Features that matter in Boot apps |
|------|------------------------|-----------------------------------|
| **8** | **2.0 – 2.7** only | Lambdas, streams, `Optional`, `java.time` — typical legacy monolith baseline |
| **11** | **2.1 – 2.7** | LTS; `var` (10+) if you move past 8; still **`javax`** era |
| **17** | **2.7**, **3.0+** | LTS; **records**, sealed classes, pattern matching — **minimum for Boot 3** |
| **21** | **2.7**, **3.0+** | LTS; **virtual threads**, sequenced collections — enable Boot virtual-thread mode on **3.2+** |
| **22** | **3.3+** (3.2 on 21) | Language level used in many examples here (`javac --release 22`) |
| **23 – 25+** | **3.3+** / **3.4+** / **3.5+** | Pick a Boot patch that lists your JDK in [system requirements](https://docs.spring.io/spring-boot/docs/current/reference/html/system-requirements.html) |

### Quick picks (new projects)

| Goal | Sensible default |
|------|------------------|
| Greenfield service in this course | **Boot 3.4+** (or latest 3.x patch) + **Java 21 LTS** |
| Blocking MVC + high concurrency | Same + **`spring.threads.virtual.enabled: true`** on **3.2+** |
| Stuck on Java 8/11 | Stay on **Boot 2.7** until JDK **17** is available — plan Jakarta migration before **3.0** |
| Library still on **`javax.*`** | Upgrade the library or stay **2.7** — Boot 3 will not start with old servlet/JPA APIs on the classpath |

Pin the Boot version in **`spring-boot-starter-parent`** or the Gradle plugin (see §4); let the BOM align Tomcat, Hibernate, and Jackson with that Boot release.
### Complete Spring Boot Annotation Reference (Most Used)

| Annotation | What it’s for / Usage |
|------------|----------------------|
| `@SpringBootApplication` | Main entry point, combines `@Configuration`, `@EnableAutoConfiguration`, and `@ComponentScan`. |
| `@Configuration` | Declares a class as a source of bean definitions (Java-based config). |
| `@ComponentScan` | Controls which packages/classes Spring will scan for beans. |
| `@EnableAutoConfiguration` | Tells Spring Boot to automatically configure beans based on the classpath and other conditions. |
| `@Component` | Generic stereotype for any Spring-managed bean. |
| `@Service` | Stereotype for a service class (business logic). |
| `@Repository` | Stereotype for a repository/DAO component. Adds exception translation for persistence errors. |
| `@Controller` | Declares a servlet controller for web endpoints (MVC, HTML, etc). |
| `@RestController` | Combines `@Controller` and `@ResponseBody`; used for REST APIs (JSON endpoints). |
| `@ControllerAdvice` | Declares a global exception/error handler or advice for controllers. |
| `@RestControllerAdvice` | Combines `@ControllerAdvice` and `@ResponseBody`, for JSON error/advice responses. |
| `@RequestMapping` | Maps an HTTP request (all methods) onto a handler class or method. |
| `@GetMapping`, `@PostMapping`,<br>`@PutMapping`, `@DeleteMapping`, `@PatchMapping` | Shortcut annotations for HTTP verbs. |
| `@ResponseBody` | Directly writes the Java return value to the HTTP response as JSON, etc. |
| `@RequestBody` | Sets up a method param to be bound with the HTTP request body. |
| `@ResponseStatus` | Specifies the HTTP status code for a controller method or exception handler. |
| `@PathVariable` | Binds a URI template variable value to a method parameter. |
| `@RequestParam` | Binds a query string parameter or form field to a method parameter. |
| `@RequestHeader` | Binds a request header value to a method parameter. |
| `@CookieValue` | Binds a cookie value to a method parameter. |
| `@SessionAttribute` | Binds a session attribute to a method parameter. |
| `@ModelAttribute` | Exposes a method parameter or return value to a web view. Also binds form fields to objects. |
| `@InitBinder` | Used in a controller/advice to customize web binding for request parameters. |
| `@ExceptionHandler` | Used with `@ControllerAdvice` or controller class to declare a method as an exception handler. |
| `@CrossOrigin` | Enables CORS (Cross-Origin Resource Sharing) support on a controller/method. |
| `@Valid`, `@Validated` | Triggers validation of a bean or parameter (with JSR-303 or Spring validation annotations). |
| `@Autowired` | Injects dependencies automatically by type (constructor, field, setter, param). |
| `@Qualifier` | Specifies which bean to inject when multiple candidates exist, used with `@Autowired`/`@Inject`. |
| `@Value` | Injects a value from properties or SpEL expression into a field or parameter. |
| `@Bean` | Declares a bean returned from a `@Configuration` class method. Used for manual wiring. |
| `@Primary` | Marks a bean as primary when multiple candidates are eligible for autowiring. |
| `@Order` | Specifies the order of beans/components (for filters, aspects, etc). |
| `@DependsOn` | Declares that a bean depends on specified other beans. |
| `@Scope` | Sets the lifecycle of a bean (singleton, prototype, session, request, etc). |
| `@Lazy` | Creates a bean only when it is first needed, not at startup. |
| `@PostConstruct` | Runs after bean construction; method invoked by Spring for initialization logic. |
| `@PreDestroy` | Runs before bean destruction; cleanup logic hook. |
| `@Transactional` | Declares a method or class as transactional (DB transaction support, commit/rollback). |
| `@EnableTransactionManagement` | Enables annotation-driven transaction management. |
| `@Entity`, `@Table`, `@Column` | JPA: Maps Java classes and fields to DB tables/columns. |
| `@Id`, `@GeneratedValue` | JPA: Specifies primary key and key generation strategy. |
| `@Embeddable`, `@Embedded`, `@MappedSuperclass` | JPA: Used for inheritance, value objects, and composition within entities. |
| `@RepositoryRestResource`, `@RestResource` | Spring Data REST: Expose repositories as REST endpoints. |
| `@EnableJpaRepositories` | Turns on JPA repository support in a configuration class. |
| `@EnableWebMvc` | Forces classic Spring MVC setup (rare in Boot, which auto-configures by default). |
| `@EnableScheduling`, `@Scheduled` | Enables scheduled tasks and marks methods to run on a schedule. |
| `@EnableAsync`, `@Async` | Enables asynchronous method execution and marks methods as async. |
| `@EnableWebSecurity`, `@EnableGlobalMethodSecurity` | Configures Spring Security. Enables web and method-level security respectively. |
| `@Secured`, `@PreAuthorize`, `@PostAuthorize` | Method security: restricts access based on roles or expressions. |
| `@Slf4j` | Lombok: Adds a `private static final Logger` logger to the class. |
| `@Data`, `@Getter`, `@Setter`, `@AllArgsConstructor`, `@NoArgsConstructor`, `@Builder` | Lombok: Reduce boilerplate with auto-generated code. |
| `@JsonIgnore`, `@JsonProperty`, `@JsonInclude`, etc. | Jackson: Customize JSON serialization/deserialization properties. |
| `@Profile` | Specifies which bean should be loaded for a particular active profile/environment. |
| `@ConditionalOnProperty`, `@ConditionalOnClass`, `@ConditionalOnMissingBean`, etc. | Conditional bean registration based on environment or classpath. |
| `@Test`, `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`, etc. | JUnit/JUnit 5 & Spring Boot annotations for structured tests and slices. |
| `@MockBean` | Test: Adds a Mockito mock to the Spring test context, replacing a bean. |
| `@Disabled`, `@Timeout`, etc. | Test lifecycle and control annotations (JUnit 5). |

**Notes:**
- This covers virtually all key annotations found in modern Spring Boot projects for MVC, REST, web, security, data, dependency injection, configuration, testing, and more.
- For edge or integration use cases, see also: `@Import`, `@EnableConfigurationProperties`, `@Conditional`, `@EventListener`, and starter/project-specific annotations.
- Your IDE’s autocomplete and Spring’s [official annotation reference](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.annotations) can help for rare or specialized scenarios.


