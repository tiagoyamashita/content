---
label: "Example"
subtitle: "Web MVC プロジェクトのレイアウト"
group: "スプリングブーツ"
groupOrder: 2
order: 1
---
サンプルプロジェクト — Spring Web MVC

以下のレイアウトとスニペットを新しいプロジェクト (または IDE の Spring Initializr 出力) にコピーします。このページはバンドルされたリポジトリ サンプルではありません**。典型的な **`spring-boot-starter-web`** + **Thymeleaf** アプリ: エントリポイント、**`@Controller`** + **`@GetMapping`**、小さな **`@Service`**、**`templates/`** の下のビューが文書化されています。

**ローカルで実行:** プロジェクト ルート `./mvnw spring-boot:run` (または **`gradle bootRun`**) から `http://localhost:8080/hello?name=Ada` を開きます。

## 1. パッケージレイアウト (代表例)

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

## 2. コード例

### `pom.xml` — Web + Thymeleaf スターター

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

**`spring-boot-starter-parent`** (または BOM) を使用して、バージョンを揃えてください。

**Gradle と同等:**

```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-web")
  implementation("org.springframework.boot:spring-boot-starter-thymeleaf")
}
```

### `DemoApplication.java` — エントリポイント

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

### `GreetingService.java` — 注入された Bean

```java
// Compile: javac --release 22 …
package com.example.demo.app;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {

  public String buildMessage(String name) {
    return "Hello, " + name + "!";
  }
}
```

### `HelloController.java` — MVC マッピング + モデル

```java
// Compile: javac --release 22 …
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

### `templates/hello.html` — Thymeleaf ビュー

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

### オプション `application.properties`

```properties
spring.application.name=demo
```

**`http://localhost:8080/hello?name=Ada`** を試してください。**`message`** 属性は **`GreetingService`** から来ており、**`th:text`** によってバインドされています。

## 3. 注意すべき注釈
- **`@SpringBootApplication`** — このパッケージ以下のコンポーネント スキャン + 自動構成。
- **`@Controller`** / **`@GetMapping`** — MVC マッピング。戻り値は **ビュー名** (`"hello"` → `templates/hello.html`) です。
- **`@Service`** — ステレオタイプ Bean。コントローラーへのコンストラクターの注入。
- **`Model`** — Thymeleaf ビュー (`th:text`) に渡されるサーバー側属性。

## 4. RESTとの比較
JSON API の場合は、**`@RestController`** を使用し、ビュー名の代わりに DTO または **`ResponseEntity`** を返します。パッケージと**`pom.xml`**のレイアウトは変わりません。親 **`java/`** フォルダーの **REST コントローラー** を参照してください (パート IV)。
