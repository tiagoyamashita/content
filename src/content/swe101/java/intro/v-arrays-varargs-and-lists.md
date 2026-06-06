---
label: "V"
subtitle: "Arrays, varargs & lists"
group: "Java"
groupOrder: 1
order: 5
---
Java — Part V
Fixed-size arrays, varargs, `java.util.Arrays`, and when to prefer `ArrayList`.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Declaring and indexing

Arrays are **fixed length**, indexed from **`0`**, with a **`length`** field (not a method).

```java
// Compile: javac --release 22 …
int[] scores = new int[] {90, 85, 72};
scores[1] = 88;                    // mutate element
int n = scores.length;             // 3

String[][] grid = {{"a", "b"}, {"c", "d"}}; // array of arrays
```

- **`int[] a`** and **`int a[]`** are equivalent — prefer **`int[]`** for readability.
- Multi-dimensional arrays are **jagged**: each row can have a different length.

## 2. `java.util.Arrays` helpers

```java
// Compile: javac --release 22 …
import java.util.Arrays;

int[] data = {5, 1, 4, 2, 8};
Arrays.sort(data);                          // in-place sort
int idx = Arrays.binarySearch(data, 4);     // requires sorted input
int[] copy = Arrays.copyOf(data, data.length);
Arrays.fill(copy, 0);
```

For algorithmic detail (complexity, when binary search applies), see **CS101 → Data structures → Array** and **Algorithms → Searching**.

## 3. Varargs (`...`)

A method can accept zero or more trailing arguments of one type:

```java
// Compile: javac --release 22 …
static int sum(int first, int... rest) {
  int total = first;
  for (int v : rest) {
    total += v;
  }
  return total;
}

// calls: sum(1), sum(1, 2, 3)
```

Inside the method, **`rest`** is a **`int[]`**. Only **one** varargs parameter per method, and it must be last.

## 4. Array vs `List`

| | `int[]` / `T[]` | `ArrayList<T>` |
|--|-----------------|----------------|
| Size | Fixed at creation | Grows as needed |
| Primitives | Native (`int[]`) | Boxes (`Integer`) unless specialized APIs |
| API | `length`, `Arrays.*` | `add`, `remove`, `size()` |
| When to use | Hot numeric buffers, interop | Most application collections |

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

List<String> names = new ArrayList<>();
names.add("Ada");
names.add("Grace");
for (String name : names) {
  System.out.println(name);
}
```

Prefer **`List.of(...)`** or **`List.copyOf(...)`** for small immutable snapshots.

## 5. Enhanced for and bounds

```java
// Compile: javac --release 22 …
for (int score : scores) {
  System.out.println(score); // read-only view of elements
}
```

Out-of-range access throws **`ArrayIndexOutOfBoundsException`** — validate indices when they come from user input.
