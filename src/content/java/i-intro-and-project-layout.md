---
label: "I"
subtitle: "Intro & project layout"
group: "Spring Boot"
groupOrder: 2
order: 1
---
Spring Boot — Part I
What Boot adds on top of Spring, how the entrypoint bootstraps the container, and how to lay out packages so scanning and auto-configuration behave predictably.

**How this section is organized:** finish the **Java** intro track (`intro/`, Parts I–VI) first, then work through these **Spring Boot** pages in order. The **Example (Web MVC)** page is a copy-paste layout; **Security basics** follows REST before operations topics.

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
