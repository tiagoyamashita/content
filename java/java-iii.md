---
label: "III"
subtitle: "Exceptions & libraries"
group: "Java"
groupOrder: 1
order: 3
---
Java — Part III
Exceptions, generics, collections, streams, and practical APIs.

## 1. Exceptions
- **Checked** exceptions (`extends Exception`): callers must handle or declare — use sparingly for recoverable failures.
- **Unchecked** (`extends RuntimeException`): no mandatory handling — programming bugs or unlikely faults.
- **`try-with-resources`** auto-closes `AutoCloseable` instances — prefer over manual `finally`.
- Never swallow exceptions silently; at minimum log with context; preserve cause via `initCause` / constructor chaining.


## 2. Generics
- Type parameters (`List<String>`) enforce element types at compile time via erasure — runtime sees raw types + casts.
- Wildcards: `? extends T` (read producer), `? super T` (write consumer) — **PECS**: producer-extends, consumer-super.
- Avoid raw types (`List` without `<>`); unchecked warnings flag weaker guarantees.


## 3. Collections framework
- **`List`**: ordered, indexed (`ArrayList`, `LinkedList`).
- **`Set`**: no duplicates (`HashSet`, `LinkedHashSet`, `TreeSet` sorted).
- **`Map`**: key → value (`HashMap`, `LinkedHashMap`, `TreeMap`).
- Choose by access pattern: hash tables average O(1) lookups; trees give sorted order at O(log n).


## 4. Streams API (basics)
- `stream()` for declarative pipelines: `filter`, `map`, `reduce`, `collect`.
- Intermediate ops lazy; terminal ops (`toList`, `count`, `findFirst`) drive execution.
- Parallel streams help only when workload is large and splittable — measure before defaulting to parallel.


## 5. Dates, optional, and records (recap)
- **`java.time`** (`Instant`, `ZonedDateTime`, `LocalDate`) replaces legacy `Date`/`Calendar`.
- **`Optional<T>`** signals absent values without null — avoid using as fields or constructor params; use as return types thoughtfully.
- **`enum`** types are full classes — can carry methods and implement interfaces.


## 6. Concurrency note
- **`ExecutorService`** + tasks beats raw `Thread` per job for pooling and lifecycle.
- Shared mutable state needs synchronization (`synchronized`, locks, concurrent collections) or confinement/immutability — detailed concurrency is a separate deep dive.
