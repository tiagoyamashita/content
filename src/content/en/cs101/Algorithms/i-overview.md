---
label: "I"
subtitle: "Algorithms overview"
group: "Data structures & algorithms"
order: 1
---
Algorithms — overview
An **algorithm** is a finite, step-by-step procedure that takes **input** and produces **output**. In CS101 you care about three questions: **Is it correct?** **How much time?** **How much memory?**

**Java baseline:** code snippets use **Java SE 22** (`javac --release 22`); they also run on **JDK 21 LTS**.

## 1. Correctness vs efficiency
- **Correctness:** for every valid input, the output matches the problem definition (often proved by **invariant** or **induction**).
- **Efficiency:** measured with **asymptotic notation** — **O**, **Θ**, **Ω** — ignoring constant factors and lower-order terms for large **n**.
- **Worst case** is the usual default in coursework unless the problem asks for **average** or **amortized** cost.

| Symbol | Meaning (informal) |
|--------|-------------------|
| **O(f(n))** | Grows no faster than **f** (upper bound) |
| **Θ(f(n))** | Tight bound — same order as **f** |
| **Ω(f(n))** | Grows at least as fast as **f** (lower bound) |

## 2. Common algorithm families (map)

| Family | Idea | Examples in this submenu |
|--------|------|-------------------------|
| **Sorting** | Arrange keys in order | merge sort, quicksort, heapsort |
| **Searching** | Find a target | linear search, binary search |
| **Divide & conquer** | Split, solve, combine | merge sort, binary search |
| **Graph** | Traverse or optimize on **V, E** | BFS, DFS, Dijkstra |
| **Greedy** | Local best choice | activity selection, MST |
| **Dynamic programming** | Optimal substructure + overlapping subproblems | knapsack, LCS, edit distance |
| **Backtracking** | Explore choices, undo on failure | N-queens, subsets |
| **Patterns** | Reuse idioms on arrays/strings | two pointers, sliding window |

**Data structures** (array, list, stack, queue, heap, hash table, graph storage) live in the **Data structures** submenu; **algorithms** are the **procedures** that use them.

## 3. How to read a complexity claim
- **O(n log n)** sort comparisons for comparison-based sorts (lower bound for general comparison sorts).
- **O(n)** BFS/DFS on a graph stored as adjacency lists when **n = |V|**, **m = |E|** — often written **O(n + m)**.
- **Space** counts **extra** memory beyond the input (output not always counted).

## 4. Learn the algorithm, solve with the JDK
1. **Study** the hand-rolled version in each note (merge sort, BFS loop, knapsack table).
2. **Ship** with **`java.util`** / **`Arrays`**: `Arrays.sort`, `Arrays.binarySearch`, `HashMap`, `ArrayDeque`, `PriorityQueue`.
3. The JDK gives you **O(1) amortized** map ops, **O(log n)** heap ops, and **O(n log n)** sort — you write the **problem-specific loop**, not another heap from scratch.

Full **problem → API** tables and copy-paste examples: **[Solving with the JDK](xi-solving-with-the-jdk.md)**.

## 5. Pseudocode → Java habit
1. State **input size** **n** (or **n, m** for graphs).
2. Name the **loop invariant** or **recurrence**.
3. Implement with clear types; prefer library structures when teaching ADTs (`Queue`, `PriorityQueue`, `Arrays.sort`).

```java
// Compile: javac --release 22 …
/** Return index of target in sorted arr, or -1. See iii-searching.md */
public static int binarySearch(int[] arr, int target) {
  int lo = 0;
  int hi = arr.length - 1;
  while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] == target) {
      return mid;
    }
    if (arr[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}
```

## 6. Related notes
- **Solving with the JDK** [Solving with the JDK](xi-solving-with-the-jdk.md) — cheat sheet for production Java.
- **Data structures** submenu — stacks, queues, heaps, graphs.
- **Level V — Paradigms & limits** [Paradigms & limits](../v-paradigms-and-limits.md) — theory: greedy proofs, DP vs divide & conquer, NP-hardness.
- **Level III — Graphs** (`iii-graphs.md`) — graph modeling at course level.
