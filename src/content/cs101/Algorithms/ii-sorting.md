---
label: "II"
subtitle: "Sorting"
group: "Data structures & algorithms"
order: 2
---
Sorting
Arrange elements in **non-decreasing** order (or by a **`Comparator`**). **Comparison sorts** only use **compare** — no special key structure.

## 1. Comparison sorts (summary)

| Algorithm | Best | Average | Worst | Extra space | Stable? |
|-----------|------|---------|-------|-------------|---------|
| Bubble / insertion | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) stack | No |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |

**Stable:** equal keys keep their relative input order. **In-place:** O(1) extra aside from recursion stack.

**Java:** `Arrays.sort(int[])` uses **dual-pivot quicksort**; `Arrays.sort(Object[])` uses **TimSort** (merge + insertion, stable).

## 2. Merge sort (divide & conquer)
1. **Divide** array into halves until size 1.
2. **Conquer** — singletons are sorted.
3. **Combine** — merge two sorted halves in **O(n)** time.

**Time Θ(n log n)**; **space Θ(n)** for a typical auxiliary buffer.

```java
// Compile: javac --release 22 …
public static void mergeSort(int[] a, int[] buf, int lo, int hi) {
  if (hi - lo < 2) {
    return;
  }
  int mid = lo + (hi - lo) / 2;
  mergeSort(a, buf, lo, mid);
  mergeSort(a, buf, mid, hi);
  merge(a, buf, lo, mid, hi);
}

private static void merge(int[] a, int[] buf, int lo, int mid, int hi) {
  System.arraycopy(a, lo, buf, lo, hi - lo);
  int i = lo;
  int j = mid;
  int k = lo;
  while (i < mid && j < hi) {
    if (buf[i] <= buf[j]) {
      a[k++] = buf[i++];
    } else {
      a[k++] = buf[j++];
    }
  }
  while (i < mid) {
    a[k++] = buf[i++];
  }
  while (j < hi) {
    a[k++] = buf[j++];
  }
}
```

## 3. Quicksort
Pick a **pivot**, **partition** so elements ≤ pivot are left, > pivot right, recurse on both sides.

- **Average Θ(n log n)**; **worst Θ(n²)** if pivot is always min/max (sorted input with bad pivot rule).
- **Mitigation:** random pivot, median-of-three, or switch to insertion sort on small ranges.

```java
// Compile: javac --release 22 …
public static void quickSort(int[] a, int lo, int hi) {
  if (lo >= hi) {
    return;
  }
  int p = partition(a, lo, hi);
  quickSort(a, lo, p);
  quickSort(a, p + 1, hi);
}

private static int partition(int[] a, int lo, int hi) {
  int pivot = a[hi - 1];
  int i = lo;
  for (int j = lo; j < hi - 1; j++) {
    if (a[j] <= pivot) {
      int tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
      i++;
    }
  }
  int tmp = a[i];
  a[i] = a[hi - 1];
  a[hi - 1] = tmp;
  return i;
}
```

## 4. Heapsort
1. **Build** a max-heap in the array (**O(n)** bottom-up).
2. Repeatedly swap root with last unsorted position and **sink** root — **O(log n)** per step → **O(n log n)** total.

Uses the **binary heap** ADT [Binary heap](../data-structures/viii-binary-heap.md); **in-place** if you heapify the array itself.

## 5. When to use which
- **General purpose in Java:** `Arrays.sort`.
- **Need stability on objects:** `Arrays.sort(Object[])` or explicit merge sort.
- **External sort (data on disk):** merge sort — sequential passes.
- **Top-k / partial order:** heap or `PriorityQueue`, not full sort.

## 6. Solving with the JDK (already implemented)

You rarely write merge/quick sort in application code — call the library after choosing **primitive vs object** and **stable vs unstable**.

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

int[] a = { 5, 2, 8, 2 };
Arrays.sort(a); // dual-pivot quicksort for primitives

Integer[] boxed = { 5, 2, 8 };
Arrays.sort(boxed, Comparator.reverseOrder()); // TimSort, stable

// Top-k largest without sorting entire array — O(n log k)
int k = 3;
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int x : a) {
  minHeap.offer(x);
  if (minHeap.size() > k) {
    minHeap.poll();
  }
}
```

| Need | API |
|------|-----|
| Sort `int[]` / `double[]` | `Arrays.sort` |
| Sort `Object[]` or `List` | `Arrays.sort`, `list.sort(Comparator)`, `Collections.sort` |
| Custom order | `Comparator.comparing`, `comparingInt`, `reverseOrder` |
| Only k largest / smallest | `PriorityQueue` size **k** |

More examples: **[Solving with the JDK](xi-solving-with-the-jdk.md)**.
