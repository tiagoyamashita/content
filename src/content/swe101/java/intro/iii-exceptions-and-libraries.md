---
label: "III"
subtitle: "Exceptions & libraries"
group: "Java"
groupOrder: 1
order: 3
---
Java — Part III
Exceptions, generics, collections, streams, and practical APIs.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Exceptions
- **Checked** exceptions (`extends Exception`): callers must handle or declare — use sparingly for recoverable failures.
- **Unchecked** (`extends RuntimeException`): no mandatory handling — programming bugs or unlikely faults.
- **`try-with-resources`** auto-closes `AutoCloseable` instances — prefer over manual `finally`.
- Never swallow exceptions silently; at minimum log with context; preserve cause via `initCause` / constructor chaining.

```java
// Compile: javac --release 22 …
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

static String readFirstLine(Path path) throws IOException {
  try (BufferedReader reader = Files.newBufferedReader(path)) {
    return reader.readLine();
  }
}

static int parsePort(String raw) {
  try {
    int port = Integer.parseInt(raw);
    if (port < 1 || port > 65535) {
      throw new IllegalArgumentException("port out of range: " + port);
    }
    return port;
  } catch (NumberFormatException e) {
    throw new IllegalArgumentException("invalid port: " + raw, e);
  }
}
```


## 2. Generics
- Type parameters (`List<String>`) enforce element types at compile time via erasure — runtime sees raw types + casts.
- Wildcards: `? extends T` (read producer), `? super T` (write consumer) — **PECS**: producer-extends, consumer-super.
- Avoid raw types (`List` without `<>`); unchecked warnings flag weaker guarantees.

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

static double sum(List<? extends Number> values) {
  double total = 0;
  for (Number n : values) {
    total += n.doubleValue();
  }
  return total;
}

static void addIntegers(List<? super Integer> sink) {
  sink.add(42);
}

static List<String> names() {
  return new ArrayList<>();
}
```


## 3. Collections framework
- **`List`**: ordered, indexed (`ArrayList`, `LinkedList`).
- **`Set`**: no duplicates (`HashSet`, `LinkedHashSet`, `TreeSet` sorted).
- **`Map`**: key → value (`HashMap`, `LinkedHashMap`, `TreeMap`).
- Choose by access pattern: hash tables average O(1) lookups; trees give sorted order at O(log n).

Hand-rolled structures (linked list, BST, heap) live under **CS101 → Data structures**. In production code, prefer **`java.util`** implementations — see **CS101 → Algorithms → Solving with the JDK**.

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.Map;
import java.util.TreeSet;

static void countWords(String[] words) {
  Map<String, Integer> freq = new HashMap<>();
  for (String w : words) {
    freq.merge(w, 1, Integer::sum);
  }

  TreeSet<String> sortedKeys = new TreeSet<>(freq.keySet());
  sortedKeys.forEach(k -> System.out.println(k + " → " + freq.get(k)));
}
```


## 4. Streams API (basics)
- `stream()` for declarative pipelines: `filter`, `map`, `reduce`, `collect`.
- Intermediate ops lazy; terminal ops (`toList`, `count`, `findFirst`) drive execution.
- Parallel streams help only when workload is large and splittable — measure before defaulting to parallel.

```java
// Compile: javac --release 22 …
import java.util.List;

static List<String> activeEmails(List<User> users) {
  return users.stream()
      .filter(User::active)
      .map(User::email)
      .sorted()
      .toList();
}

record User(String email, boolean active) {}
```


## 5. Dates, optional, and records (recap)
- **`java.time`** (`Instant`, `ZonedDateTime`, `LocalDate`) replaces legacy `Date`/`Calendar`.
- **`Optional<T>`** signals absent values without null — avoid using as fields or constructor params; use as return types thoughtfully.
- **`enum`** types are full classes — can carry methods and implement interfaces.

```java
// Compile: javac --release 22 …
import java.time.Instant;
import java.util.Optional;

enum OrderStatus {
  NEW, PAID, SHIPPED;

  boolean canShip() {
    return this == PAID;
  }
}

static Optional<Instant> parseInstant(String raw) {
  if (raw == null || raw.isBlank()) {
    return Optional.empty();
  }
  return Optional.of(Instant.parse(raw));
}
```


## 6. Concurrency note
- **`ExecutorService`** + tasks beats raw `Thread` per job for pooling and lifecycle.
- Shared mutable state needs synchronization (`synchronized`, locks, concurrent collections) or confinement/immutability.
- **Virtual threads** (Java 21+) suit I/O-heavy code — see **Part VI (Lambdas & modern Java)**.

```java
// Compile: javac --release 22 …
import java.util.concurrent.Executors;

static void runBatch(Runnable... tasks) throws InterruptedException {
  try (var pool = Executors.newFixedThreadPool(4)) {
    for (Runnable task : tasks) {
      pool.submit(task);
    }
  }
}
```
