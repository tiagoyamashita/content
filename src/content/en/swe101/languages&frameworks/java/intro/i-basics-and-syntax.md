---
label: "I"
subtitle: "Basics & syntax"
group: "Java"
groupOrder: 1
order: 1
---
Java — Part I
JDK, program shape, types, control flow, methods, and arrays.

**How this section is organized:** **`intro/`** (this group) covers core language through Part VI. The **`springboot/`** submenu holds hands-on examples; sibling pages at **`java/`** root with **`group: "Spring Boot"`** cover the main track after you are comfortable with classes, collections, and tests.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. JDK, JVM, and your first program
- **JDK** = compiler (`javac`), standard libraries, tooling; **JVM** = runtime that executes bytecode.
- Source `.java` → `javac` → bytecode `.class` → `java` launches JVM and loads the entry class.
- Every runnable program needs `public static void main(String[] args)` as an entry point.
- Packages (`package com.example.app;`) map to folder paths; avoid default package for real projects.

```java
// Compile: javac --release 22 App.java && java App
package com.example.app;

public class App {
  public static void main(String[] args) {
    System.out.println("Hello, " + (args.length > 0 ? args[0] : "world"));
  }
}
```

```text
javac --release 22 com/example/app/App.java
java com.example.app.App Ada
```


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" role="img" aria-label="From Java source to JVM execution">
  <text x="110" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Edit → compile → run</text>
  <rect x="28" y="36" width="88" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="44" y="58" fill="#e4e4e7" font-size="10">App.java</text>
  <path d="M116 54 H148" stroke="#a1a1aa" stroke-width="2"/>
  <text x="152" y="58" fill="#71717a" font-size="10">javac</text>
  <path d="M198 54 H230" stroke="#a1a1aa" stroke-width="2"/>
  <rect x="232" y="36" width="88" height="36" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="248" y="58" fill="#e4e4e7" font-size="10">App.class</text>
  <path d="M320 54 H352" stroke="#a1a1aa" stroke-width="2"/>
  <text x="356" y="58" fill="#71717a" font-size="10">java</text>
  <rect x="118" y="84" width="184" height="28" rx="4" fill="rgba(96,165,250,0.1)" stroke="#60a5fa"/>
  <text x="132" y="102" fill="#a1a1aa" font-size="9">JVM loads classes, JIT may optimize hot bytecode → machine code</text>
</svg></figure>


## 2. Primitive types and references
- Primitives: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean` — stored by value in locals and fields when declared as primitives.
- Everything else is a **reference type** (objects): variables hold references; `null` means “no object”.
- Wrapper types (`Integer`, `Double`, …) box primitives for collections and nullable APIs; prefer primitives where hot and non-null.
- `var` (Java 10+) infers local type from the initializer — still statically typed.

```java
// Compile: javac --release 22 …
int count = 42;
var name = "Ada";              // inferred String
Integer boxed = count;         // autoboxing
int again = boxed;             // unboxing
```


## 3. Operators and control flow
- Arithmetic (`+`, `-`, `*`, `/`, `%`), comparisons, logical `&&`, `||`, `!`, short-circuit behavior.
- `if / else`, `switch` (classic and modern **switch expressions** with `->` and exhaustiveness on enums/sealed types).
- Loops: `while`, `do-while`, `for`, **enhanced for** (`for (String s : items)`).
- `break` / `continue` with optional labels for nested loops.

```java
// Compile: javac --release 22 …
enum Status { OPEN, CLOSED }

static String describe(Status s) {
  return switch (s) {
    case OPEN -> "accepting requests";
    case CLOSED -> "maintenance";
  };
}

static int sum(int[] values) {
  int total = 0;
  for (int v : values) {
    total += v;
  }
  return total;
}
```


## 4. Methods and parameters
- Signature: modifiers, return type, name, parameter list, optional `throws`; **overloading** by parameter types/count.
- **Pass-by-value**: primitives copy bits; references copy the pointer — mutating the object is visible to caller, reassigning the parameter is not.
- `final` parameters prevent reassignment inside the method (still mutable object state).

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

static void addTag(List<String> tags, final String tag) {
  tags.add(tag);   // mutates caller's list
  // tag = "x";    // compile error — final parameter
}

static int max(int a, int b) {
  return a >= b ? a : b;
}
```


## 5. Arrays and `String`
- Arrays are fixed-size, indexed from `0`; `length` field; multi-dimensional arrays are arrays of arrays.
- `java.util.Arrays` provides sort, binary search, fill, copy helpers.
- `String` is immutable; use `StringBuilder` / `StringBuffer` for repeated concatenation in loops.
- Text blocks (`""" ... """`) simplify multiline literals.

See **Part V (Arrays, varargs & lists)** for varargs, `ArrayList`, and CS101 cross-links.

```java
// Compile: javac --release 22 …
String json = """
    {
      "name": "Ada"
    }
    """;

StringBuilder buf = new StringBuilder();
for (char c : json.toCharArray()) {
  if (!Character.isWhitespace(c)) {
    buf.append(c);
  }
}
```


## 6. Style and readability
- Naming: `camelCase` methods/locals, `PascalCase` types, `SCREAMING_SNAKE` constants.
- Prefer small methods, early returns, meaningful names over comments that repeat the code.
- Format consistently (IDE formatter); keep `public` APIs documented where intent is non-obvious.
