---
label: "IV"
subtitle: "Divide & conquer"
group: "Data structures & algorithms"
order: 4
---
Divide & conquer
**Recipe:** split the problem into smaller subproblems, solve them (often recursively), **combine** results.

## 1. Template
1. **Base case** — small **n** solved directly.
2. **Divide** — split input into **a** parts of size about **n/b**.
3. **Conquer** — recurse on each part.
4. **Combine** — merge partial answers in **O(n)** or similar.

Examples: **merge sort**, **binary search**, **maximum subarray** (cross-midpoint case), **Karatsuba** multiplication (advanced).

## 2. Recurrence (sketch)
Many algorithms satisfy **T(n) = a T(n/b) + f(n)**:

- **a** = number of subproblems per call.
- **n/b** = subproblem size.
- **f(n)** = divide + combine cost.

**Merge sort:** **a = 2**, **b = 2**, **f(n) = Θ(n)** → **T(n) = Θ(n log n)**.

**Binary search:** one subproblem of half size, **O(1)** work → **T(n) = T(n/2) + O(1) = O(log n)**.

The **Master theorem** (see [Paradigms & limits](../iv-paradigms-and-limits.md)) classifies many such recurrences without expanding the recursion tree.

## 3. Maximum subarray (Kadane vs divide & conquer)
**Kadane** (linear scan) is the practical **O(n)** solution:

```java
// Compile: javac --release 22 …
/** Largest sum of any contiguous subarray. */
public static int maxSubarraySum(int[] a) {
  int best = a[0];
  int cur = a[0];
  for (int i = 1; i < a.length; i++) {
    cur = Math.max(a[i], cur + a[i]);
    best = Math.max(best, cur);
  }
  return best;
}
```

**Divide & conquer** version: max sum is either entirely in left half, right half, or **crossing** the middle — recurse on halves and combine with an **O(n)** crossing scan. Still **O(n log n)** overall; teaches the **combine** step.

## 4. When divide & conquer is not enough
If subproblems **overlap** (same subproblem solved many times), pure recursion wastes work — use **memoization** or **tabulation** (**dynamic programming**, [Dynamic programming](viii-dynamic-programming.md)).

| Overlapping subproblems? | Typical approach |
|------------------------|------------------|
| No | Divide & conquer |
| Yes | Dynamic programming |

## 5. Solving with the JDK (already implemented)

Divide & conquer in the wild is mostly **library calls** plus your **combine** logic:

```java
// Compile: javac --release 22 …
import java.util.Arrays;

// "Conquer" half — binary search on sorted half
int[] sorted = { 1, 4, 9, 16 };
int i = Arrays.binarySearch(sorted, 9);

// "Combine" step often needs sorted halves
Arrays.sort(leftHalf);
Arrays.sort(rightHalf);
// then merge with a loop, or System.arraycopy + merge

// Max subarray — Kadane is O(n); no JDK one-liner, but simple loop (see §3)
```

| D&C idea | JDK helper |
|----------|------------|
| Search sorted range | `Arrays.binarySearch` |
| Sort subranges before merge | `Arrays.sort(from, to)` |
| Copy block | `System.arraycopy`, `Arrays.copyOfRange` |
