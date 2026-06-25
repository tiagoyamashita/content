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
- **Prefer composition over deep inheritance hierarchies:**  
  *Composition* means building classes by assembling them from component objects that provide specific functionality, rather than inheriting from a chain of parent classes.  
  For example, in a hotel booking system, a `Reservation` should not *extend* a `Customer`, since a reservation "belongs to" or "references" a customer—it is not a type of customer. Making `Reservation` extend `Customer` would be an inappropriate use of inheritance, creating a confusing and fragile class hierarchy.  
  Instead, use composition: a `Reservation` class would simply have a field that refers to a `Customer` object. This *has-a* relationship keeps the code base more understandable and maintainable.  
  Deep inheritance creates "brittle base-class contracts," making it easy for changes in a parent class to accidentally break subclasses. Favoring composition allows more flexible reuse and safer evolution of your system.

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
- **Static methods in interfaces**: Often used for helper or factory methods tied to the interface concept.
- **Default methods**: Provide inheritable behavior—implementing classes can override them.
- **Overriding**: When a class redefines an interface default method or abstract superclass method with its own implementation.
- A class may implement multiple interfaces; use them for defining capabilities (“can compare”, “can serialize”).
- **Sealed** classes and interfaces restrict who may extend or implement them—useful for exhaustive, well-defined model hierarchies.

```java
// Compile: javac --release 22 …

interface Identifiable {
  String id();

  // Static method in interface
  static Identifiable of(String idValue) {
    return () -> idValue;
  }
}

interface Auditable {
  default void logAccess() {
    System.out.println("access: " + id());
  }

  // Overridable default method
  default void logCustom(String message) {
    System.out.println("[" + id() + "] " + message);
  }

  String id();
}

// Example of overriding a default method
class AdminUser implements Identifiable, Auditable {
  private final String id;
  private final String name;

  AdminUser(String id, String name) {
    this.id = id;
    this.name = name;
  }

  @Override
  public String id() {
    return id;
  }

  // Override default method
  @Override
  public void logCustom(String message) {
    System.out.println("ADMIN LOG: [" + id + "] " + message);
  }
}

// Java 17+ sealed class example
sealed abstract class Command permits AddCommand, RemoveCommand, InterfaceCommand {}

final class AddCommand extends Command {}
final class RemoveCommand extends Command {}

/**
 * /interface - A sealed class acting as a marker for interface-related commands.
 */
final class InterfaceCommand extends Command {
  // This could execute/describe interface-related actions
  static void run() {
    System.out.println("Executing /interface skill logic...");
  }
}
```

**Example usage:**

```java
public class Demo {
  public static void main(String[] args) {
    // Use Identifiable.of to create an anonymous user
    Identifiable anon = Identifiable.of("guest123");
    System.out.println("Anon ID: " + anon.id()); // static method usage

    // Create an admin user, show both default and overridden behaviors
    AdminUser admin = new AdminUser("a1", "Dana");
    admin.logAccess(); // inherited default
    admin.logCustom("Changed settings"); // overridden method

    // Implement AddCommand so it does something on construction or via a method
    Command[] commands = {
      new AddCommand() {
        @Override
        public String toString() {
          System.out.println("Adding a new record ...");
          return "AddCommand";
        }
      },
      new RemoveCommand(),
      new InterfaceCommand()
    };

    for (Command cmd : commands) {
      if (cmd instanceof InterfaceCommand ic) {
        System.out.print("Running interface command: ");
        InterfaceCommand.run(); // sealed class in action
      } else if (cmd instanceof AddCommand) {
        // The overridden toString triggers an action
        System.out.println("Command: " + cmd);
      } else if (cmd instanceof RemoveCommand) {
        System.out.println("Command: Remove");
      }
    }
  }
}
```

## 5. `Object` essentials
- `equals` / `hashCode` must agree: equal objects → same hash codes.
- `toString` aids debugging and logs; `clone` is fragile — instead, use **copy constructors** or **factory methods** to create new instances in a safe and controlled way.
- Prefer **`record`** (Java 16+) for immutable data carriers — auto-generates `equals`, `hashCode`, `toString`, and accessors.

- A **factory method** is a static method for obtaining a new instance. For example, you often see `origin()` or `empty()` methods that return a canonical or default value — like a `Point` at (0, 0). The factory method doesn't take parameters because its main purpose is to return a standard, agreed-upon version of the object, not a copy of a supplied instance (that's the copy constructor's job).
- A **copy constructor** lets you create a new instance by copying an existing object, providing a simple and explicit alternative to `clone`. This is helpful if you want to duplicate an object (copy its state).


```java
// Compile: javac --release 22 …
record Point(int x, int y) {
  // Copy constructor: create a new Point by copying another
  public Point(Point other) {
    this(other.x, other.y);
  }

  // Factory method: always returns the default Point at the origin (0,0)
  public static Point origin() {
    return new Point(0, 0);
  }
}

static void demo() {
  var a = new Point(3, 4);
  var b = new Point(a);           // Use copy constructor to duplicate 'a'
  var o = Point.origin();         // Use factory to get the default origin
  System.out.println(a.equals(b)); // true
  System.out.println(b);           // Point[x=3, y=4]
  System.out.println(o);           // Point[x=0, y=0]
}
```


## 6. Packages and modules (overview)
- **`package`** declares namespace; **imports** shorten names; avoid wildcard imports in large codebases when clarity suffers.
- **`java.base`** and friends ship with the JDK; know **`java.lang`** is implicit.
- **JPMS** (`module-info.java`) adds compile-time boundaries beyond plain packages — adopt when building libraries or enforcing layering.

  ```java
  // Example: minimal module declaration
  // File: module-info.java
  module com.example.app {
      // exports or requires statements here
      exports com.example.api;
      requires java.sql;
  }
  ```

  - Place `module-info.java` at the root of your source directory (next to package folders).
  - The `module` name should match the folder/jar structure.
  - Use `exports` to make packages available to other modules; use `requires` to depend on other modules.
  - Compiling and running with modules:
    ```sh
    javac --release 22 -d out src/module-info.java src/com/example/app/*.java
    java --module-path out -m com.example.app/com.example.app.Main
    ```
    (Replace `com.example.app.Main` with your entry class.)

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
