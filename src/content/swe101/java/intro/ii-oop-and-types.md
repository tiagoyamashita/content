---
label: "II"
subtitle: "OOP & types"
group: "Java"
groupOrder: 1
order: 2
---
Java — Part II
Classes, encapsulation, inheritance, polymorphism, interfaces, and packages.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Classes and objects
- **Class** = blueprint; **object** = instance in memory with its own field values.
- Constructors initialize state; if you declare none, a default no-arg constructor appears until you add any constructor.
- `this` refers to the current instance; constructor chaining uses `this(...)`.

```java
// Compile: javac --release 22 …
public class Counter {
  private int value;

  public Counter() {
    this(0);
  }

  public Counter(int start) {
    this.value = start;
  }

  public void increment() {
    value++;
  }

  public int getValue() {
    return value;
  }
}
```


## 2. Encapsulation
- Hide fields behind accessors (`getX`, `setX`) or clearer domain methods.
- Use the narrowest visibility: `private` fields, `public` API surface deliberately chosen.
- Immutability where possible — `final` fields set once, no mutators — simplifies reasoning in concurrent code.

```java
// Compile: javac --release 22 …
public final class EmailAddress {
  private final String value;

  public EmailAddress(String raw) {
    if (raw == null || !raw.contains("@")) {
      throw new IllegalArgumentException("invalid email");
    }
    this.value = raw.trim().toLowerCase();
  }

  public String value() {
    return value;
  }
}
```


## 3. Inheritance and polymorphism
- `extends` one superclass; Java supports single inheritance for implementation.
- **`@Override`** when replacing superclass methods — catches signature mistakes at compile time.
- **Dynamic dispatch**: virtual methods resolve to the runtime type’s implementation.
- Prefer composition over deep inheritance hierarchies; inheritance exposes brittle base-class contracts.

```java
// Compile: javac --release 22 …
abstract class Animal {
  abstract String speak();
}

class Dog extends Animal {
  @Override
  String speak() {
    return "woof";
  }
}

static void greet(Animal animal) {
  System.out.println(animal.speak()); // "woof" at runtime for Dog
}
```


## 4. Abstract classes and interfaces
- **Abstract class**: partial implementation; cannot be instantiated directly.
- **`interface`**: defines behavior contracts; methods may be `default` or `static` with bodies since Java 8.
- A class may implement multiple interfaces; use them for capability (“can compare”, “can serialize”).
- **Sealed** classes/interfaces restrict who may extend/implement — useful for exhaustive modeling.

```java
// Compile: javac --release 22 …
interface Identifiable {
  String id();
}

interface Auditable {
  default void logAccess() {
    System.out.println("access: " + id());
  }
}

record User(String id, String name) implements Identifiable, Auditable {}
```


## 5. `Object` essentials
- `equals` / `hashCode` must agree: equal objects → same hash codes.
- `toString` aids debugging and logs; `clone` is fragile — often prefer copy constructors or factories.
- Prefer **`record`** (Java 16+) for immutable data carriers — auto `equals`, `hashCode`, `toString`, accessors.

```java
// Compile: javac --release 22 …
record Point(int x, int y) {}

static void demo() {
  var a = new Point(1, 2);
  var b = new Point(1, 2);
  System.out.println(a.equals(b)); // true
  System.out.println(a);           // Point[x=1, y=2]
}
```


## 6. Packages and modules (overview)
- **`package`** declares namespace; **imports** shorten names; avoid wildcard imports in large codebases when clarity suffers.
- **`java.base`** and friends ship with the JDK; know **`java.lang`** is implicit.
- **JPMS** (`module-info.java`) adds compile-time boundaries beyond plain packages — adopt when building libraries or enforcing layering.

```java
// Compile: javac --release 22 …
package com.example.domain;

import java.util.Objects;

public final class Money {
  private final long cents;

  public Money(long cents) {
    this.cents = cents;
  }

  @Override
  public boolean equals(Object o) {
    return o instanceof Money m && cents == m.cents;
  }

  @Override
  public int hashCode() {
    return Objects.hash(cents);
  }
}
```

For tree-shaped data (BST, heaps), see **CS101 → Data structures** when you move from language basics to algorithms.
