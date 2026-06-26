---
label: "VI"
subtitle: "Lambdas & modern Java"
group: "Java"
groupOrder: 1
order: 6
---
Java — Part VI
Functional interfaces, lambdas, switch expressions, sealed types, and virtual threads.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Lambdas and method references

A **lambda** implements a **functional interface** — an interface with exactly one abstract method (`Comparator`, `Runnable`, `Predicate`, …).

```java
// Compile: javac --release 22 …
import java.util.Comparator;
import java.util.List;

List<String> names = List.of("Ada", "Grace", "Linus");
names.sort(Comparator.comparing(String::length)); // method reference
names.sort((a, b) -> a.compareToIgnoreCase(b)); // lambda
```

**Method reference** forms: **`Type::staticMethod`**, **`instance::method`**, **`Type::new`**.

## 2. Switch expressions

Modern **`switch`** can return a value and use **`->`** without fall-through:

```java
// Compile: javac --release 22 …
enum Role { ADMIN, USER, GUEST }

static String label(Role role) {
  return switch (role) {
    case ADMIN -> "Administrator";
    case USER -> "User";
    case GUEST -> "Guest";
  };
}
```

With **sealed** hierarchies the compiler can verify exhaustiveness (see below).

## 3. Sealed classes and pattern matching

**Sealed** types restrict who may extend them — useful for domain models and exhaustive **`switch`**:

```java
// Compile: javac --release 22 …
sealed interface Shape permits Circle, Rectangle {}

record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}

static double area(Shape shape) {
  return switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
  };
}
```

## 4. Virtual threads (Java 21+)

**Virtual threads** are lightweight — ideal for I/O-bound work (HTTP, DB) without one platform thread per request:

```java
// Compile: javac --release 22 …
import java.util.concurrent.Executors;

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
  executor.submit(() -> fetchFromService("orders"));
  executor.submit(() -> fetchFromService("inventory"));
} // waits for tasks when executor closes
```

Use **`ExecutorService`** with a bounded platform pool for CPU-bound work; measure before mixing models.

In **Spring Boot 3.2+**, enable the same model for Tomcat with **`spring.threads.virtual.enabled=true`** — see [Virtual threads](../springboot/xi-virtual-threads.md).

## 5. Where to go next

- **Collections & streams in depth** — Part III; **CS101 → Algorithms → Solving with the JDK** for production **`HashMap`**, **`PriorityQueue`**, sorts.
- **Build & tests** — Part IV, then the **Spring Boot** track (same **`src/content/java/`** folder, **`groupOrder: 2`**) when you are ready for web services.
