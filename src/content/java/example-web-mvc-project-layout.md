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

## 1. Annotations to notice
- **`@SpringBootApplication`** — component scanning + auto-configuration for this package and below.
- **`@Controller`** / **`@GetMapping`** — MVC mapping; return value is a **view name** (`"hello"` → `templates/hello.html`).
- **`@Service`** — stereotype bean; constructor injection into the controller.
- **`Model`** — server-side attributes passed into the Thymeleaf view (`th:text`).

## 2. Compared to REST
For JSON APIs you would use **`@RestController`** and return DTOs or **`ResponseEntity`** instead of view names; the package and **`pom.xml`** layout stay the same.
