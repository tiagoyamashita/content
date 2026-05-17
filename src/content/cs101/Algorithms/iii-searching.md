---
label: "III"
subtitle: "Searching"
group: "Data structures & algorithms"
order: 3
---
Searching
Find whether a **target** exists (or where it sits) in a collection.

## 1. Linear search
Scan from one end until you find the target or exhaust the structure.

- **Time O(n)** — **n** elements.
- **Space O(1)** extra.
- Works on **any** order; works on **linked** lists without random access.

```java
// Compile: javac --release 22 …
public static int linearSearch(int[] a, int target) {
  for (int i = 0; i < a.length; i++) {
    if (a[i] == target) {
      return i;
    }
  }
  return -1;
}
```

## 2. Binary search
Requires a **sorted** array (or sorted order by `Comparator`).

- **Time O(log n)** — halve the search range each step.
- **Space O(1)** iterative; **O(log n)** recursion stack if recursive.

**Invariant:** if target is present, its index lies in `[lo, hi]`.

```java
// Compile: javac --release 22 …
import java.util.Arrays;

public static int binarySearchSorted(int[] sorted, int target) {
  int idx = Arrays.binarySearch(sorted, target);
  return idx >= 0 ? idx : -1;
}

/** Same logic without Arrays.binarySearch — useful for interviews. */
public static int binarySearchManual(int[] sorted, int target) {
  int lo = 0;
  int hi = sorted.length - 1;
  while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (sorted[mid] == target) {
      return mid;
    }
    if (sorted[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}
```

**Common bug:** `mid = (lo + hi) / 2` can overflow in some languages; use **`lo + (hi - lo) / 2`**.

## 3. Binary search on answer (pattern)
When the problem asks for the **minimum x** such that a predicate `P(x)` flips from false to true (monotone), binary search on **x** in a range — not on array indices.

Examples: first bad version, capacity to ship packages in D days, minimum eating speed.

## 4. Hash-based lookup
With a **hash table** (`x-hash-table.md`), average **O(1)** insert and lookup — no sorted order required; worst case **O(n)** without good hashing.

| Method | Preconditions | Time |
|--------|---------------|------|
| Linear | None | O(n) |
| Binary | Sorted | O(log n) |
| Hash | Hashable keys | O(1) average |

## 5. Solving with the JDK (already implemented)

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

int[] sorted = { 1, 3, 5, 7 };
int idx = Arrays.binarySearch(sorted, 5); // 2 if present

List<String> names = List.of("ada", "bob");
boolean has = names.contains("ada");           // O(n) on list
Map<String, Integer> index = new HashMap<>();  // O(1) average lookup
index.put("ada", 0);
index.get("ada");

Set<Integer> seen = new HashSet<>();
for (int x : data) {
  if (!seen.add(x)) {
    // duplicate
  }
}
```

| Task | JDK |
|------|-----|
| Sorted array lookup | `Arrays.binarySearch` (sort first) |
| List membership | `list.contains`, or `HashSet` for many queries |
| Key → value | `HashMap.get`, `getOrDefault`, `containsKey` |
| Count occurrences | `Collections.frequency` (list) or `Map.merge` |

**Interview vs production:** know the manual binary search loop; in projects call **`Arrays.binarySearch`** on sorted data.
