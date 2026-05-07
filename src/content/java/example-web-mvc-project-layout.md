---
label: "Example"
subtitle: "Web MVC project layout"
group: "Spring Boot"
groupOrder: 2
order: 7
---
Example project — Spring Web MVC
Browse the **Explorer** on the left: open folders and click a file to view its source. The layout matches a typical **`spring-boot-starter-web`** + **Thymeleaf** app: entrypoint, **`@Controller`** + **`@GetMapping`**, a small **`@Service`**, and a view under **`templates/`**.

**Run locally:** from the project root, `./mvnw spring-boot:run` (or your IDE’s Run on `DemoApplication`), then open `http://localhost:8080/hello?name=Ada`.

## 1. Package layout (typical)

```text
src/main/java/com/example/demo/
  DemoApplication.java
  web/
    HelloController.java
  app/
    GreetingService.java
src/main/resources/
  templates/
    hello.html
  application.properties   (optional)
pom.xml
```

## 2. Code examples

### `pom.xml` — Web + Thymeleaf starters

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
  </dependency>
</dependencies>
```

Use **`spring-boot-starter-parent`** (or the BOM) so versions stay aligned.

### `DemoApplication.java` — entrypoint

```java
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

### `GreetingService.java` — injected bean

```java
package com.example.demo.app;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {

  public String buildMessage(String name) {
    return "Hello, " + name + "!";
  }
}
```

### `HelloController.java` — MVC mapping + model

```java
package com.example.demo.web;

import com.example.demo.app.GreetingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HelloController {

  private final GreetingService greetingService;

  public HelloController(GreetingService greetingService) {
    this.greetingService = greetingService;
  }

  @GetMapping("/hello")
  public String hello(
      @RequestParam(name = "name", required = false, defaultValue = "world") String name,
      Model model) {
    model.addAttribute("message", greetingService.buildMessage(name));
    return "hello"; // → templates/hello.html
  }
}
```

### `templates/hello.html` — Thymeleaf view

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
  <meta charset="UTF-8"/>
  <title>Hello</title>
</head>
<body>
  <p th:text="${message}">Rendered greeting appears here.</p>
</body>
</html>
```

### Optional `application.properties`

```properties
spring.application.name=demo
```

Try **`http://localhost:8080/hello?name=Ada`** — the **`message`** attribute comes from **`GreetingService`** and is bound by **`th:text`**.

## 3. Annotations to notice
- **`@SpringBootApplication`** — component scanning + auto-configuration for this package and below.
- **`@Controller`** / **`@GetMapping`** — MVC mapping; return value is a **view name** (`"hello"` → `templates/hello.html`).
- **`@Service`** — stereotype bean; constructor injection into the controller.
- **`Model`** — server-side attributes passed into the Thymeleaf view (`th:text`).

## 4. Compared to REST
For JSON APIs you would use **`@RestController`** and return DTOs or **`ResponseEntity`** instead of view names; the package and **`pom.xml`** layout stay the same.
