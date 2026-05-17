---
label: "XI"
subtitle: "Solving with the JDK"
group: "Data structures & algorithms"
order: 11
---
Solving algorithm problems with the JDK
In coursework you implement algorithms by hand to learn **how** they work. In **real Java**, you compose **already implemented** types from **`java.util`** and **`java.util.Arrays`** — the same ADTs from the **Data structures** submenu, wired for production.

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Mindset

| Goal | Hand-rolled (learning) | JDK (shipping code) |
|------|------------------------|---------------------|
| Sort an array | merge / quick sort | `Arrays.sort`, `List.sort` |
| Find in sorted data | binary search loop | `Arrays.binarySearch` |
| Find / count fast | linear scan | `HashMap`, `HashSet` |
| FIFO traversal | linked queue class | `ArrayDeque` + `Queue` |
| Best-next (Dijkstra, Prim) | heap sift code | `PriorityQueue` |
| Graph reachability | BFS/DFS loops | `ArrayDeque` + adjacency list you build |

The **JDK does not** ship a `Graph` class with Dijkstra or MST built in — you still write **short loops**, but you **reuse** queues, heaps, maps, and sorts instead of reimplementing them.

## 2. Cheat sheet: problem → API

| Problem type | Primary JDK tools |
|--------------|-------------------|
| Sort keys | `Arrays.sort`, `Collections.sort`, `Comparator` |
| Search sorted array | `Arrays.binarySearch`, `Collections.binarySearch` |
| Lookup / dedupe | `HashMap`, `HashSet`, `Map.computeIfAbsent` |
| Queue (BFS) | `ArrayDeque`, `Queue.offer` / `poll` |
| Stack (DFS iterative) | `ArrayDeque` as `Deque`, `push` / `pop` |
| Min / max next | `PriorityQueue` (min-heap by default) |
| Top-k largest | `PriorityQueue` (min-heap size k) or `stream().sorted().limit(k)` |
| Stable sort objects | `Arrays.sort(Object[])` (TimSort) |
| Merge intervals | `Arrays.sort` by start + scan |
| Count frequencies | `HashMap.merge`, `getOrDefault` |
| Range sum queries | prefix array (manual) or `long[]` + loops |
| Permutations / subsets (small n) | backtrack yourself; optional `Stream` helpers |

## 3. Sorting and searching

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

int[] nums = { 3, 1, 4, 1, 5 };
Arrays.sort(nums);

List<String> names = List.of("bob", "ada", "grace");
List<String> sorted = names.stream().sorted().toList();
// or mutate a copy:
List<String> copy = new java.util.ArrayList<>(names);
Collections.sort(copy);

record Job(int deadline, String name) {}
Job[] jobs = { new Job(5, "a"), new Job(2, "b") };
Arrays.sort(jobs, Comparator.comparingInt(Job::deadline));

int idx = Arrays.binarySearch(nums, 4); // >= 0 if found
```

**`Arrays.binarySearch`** returns **≥ 0** if found, else **`-(insertionPoint) - 1`**. Array must be **sorted** first.

## 4. Maps and sets

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

Map<String, Integer> freq = new HashMap<>();
for (String word : words) {
  freq.merge(word, 1, Integer::sum);
}

Set<Integer> seen = new HashSet<>();
if (seen.add(x)) {
  // first time we saw x
}
```

## 5. Queues, stacks, heaps (graphs and greedy)

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Queue;

// BFS
Queue<Integer> q = new ArrayDeque<>();
q.offer(start);

// Dijkstra-style (non-negative weights) — see vi-shortest-paths-and-mst.md
PriorityQueue<int[]> pq = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[] { source, 0 });

// Top-k largest: keep min-heap of size k
PriorityQueue<Integer> heap = new PriorityQueue<>();
for (int x : nums) {
  heap.offer(x);
  if (heap.size() > k) {
    heap.poll();
  }
}
```

## 6. Collections utilities

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

int max = Collections.max(List.of(3, 1, 4));
Collections.reverse(Arrays.asList(boxed)); // array as list view
Collections.swap(list, i, j);
int freq = Collections.frequency(list, target);
```

## 7. Streams (optional, same complexity class)

Use when readability wins; know the underlying algorithm (sort is **O(n log n)**).

```java
// Compile: javac --release 22 …
import java.util.Arrays;

int[] a = { 3, 1, 4 };
boolean anyEven = Arrays.stream(a).anyMatch(x -> x % 2 == 0);
int sum = Arrays.stream(a).sum();
int[] sorted = Arrays.stream(a).sorted().toArray();
```

## 8. What you still implement yourself

- **Graph** storage (adjacency list / matrix).
- **BFS / DFS / Dijkstra / MST** control loops (using JDK queues/heaps).
- **DP** table fill (arrays + loops, sometimes `HashMap` memo keys).
- **Backtracking** recursion with choose / unchoose.

## 9. Per-topic pointers

| Note | JDK focus |
|------|-----------|
| `ii-sorting.md` | `Arrays.sort`, `Comparator` |
| `iii-searching.md` | `binarySearch`, `HashMap` |
| `v-graph-traversal.md` | `ArrayDeque`, `Queue` |
| `vi-shortest-paths-and-mst.md` | `PriorityQueue`, sort edges for Kruskal |
| `vii-greedy.md` | sort + `PriorityQueue` |
| `viii-dynamic-programming.md` | `int[][]`, `HashMap` memo |
| `x-common-patterns.md` | `HashMap`, `Arrays.sort`, streams |
