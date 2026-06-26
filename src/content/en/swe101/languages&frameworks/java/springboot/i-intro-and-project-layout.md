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
