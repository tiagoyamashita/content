---
label: "X"
subtitle: "Common patterns"
group: "Data structures & algorithms"
order: 10
---
Common algorithmic patterns
Reusable techniques on **arrays** and **strings** — often **O(n)** or **O(n log n)** after sorting.

## 1. Two pointers
Two indices move through a structure toward each other or in the same direction.

**Sorted array pair sum** — find two values with target **T**:

```java
// Compile: javac --release 22 …
public static boolean hasPairSum(int[] sorted, int target) {
  int lo = 0;
  int hi = sorted.length - 1;
  while (lo < hi) {
    int sum = sorted[lo] + sorted[hi];
    if (sum == target) {
      return true;
    }
    if (sum < target) {
      lo++;
    } else {
      hi--;
    }
  }
  return false;
}
```

**Remove duplicates in-place** (sorted): slow pointer for write position, fast for scan.

## 2. Sliding window
Maintain a **window** `[left, right]` on an array; expand **right**, shrink **left** when a constraint breaks.

**Longest substring without repeating characters:**

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.Map;

public static int longestUniqueSubstring(String s) {
  Map<Character, Integer> last = new HashMap<>();
  int best = 0;
  int left = 0;
  for (int right = 0; right < s.length(); right++) {
    char c = s.charAt(right);
    if (last.containsKey(c) && last.get(c) >= left) {
      left = last.get(c) + 1;
    }
    last.put(c, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

**Time O(n)** — each index moves at most **n** steps total.

## 3. Prefix sums
`prefix[i]` = sum of `a[0..i-1]` → range sum **O(1)** after **O(n)** preprocess.

```java
// Compile: javac --release 22 …
public static int[] prefixSum(int[] a) {
  int[] p = new int[a.length + 1];
  for (int i = 0; i < a.length; i++) {
    p[i + 1] = p[i] + a[i];
  }
  return p;
}

/** Sum of a[lo..hi] inclusive. */
public static int rangeSum(int[] prefix, int lo, int hi) {
  return prefix[hi + 1] - prefix[lo];
}
```

## 4. Frequency counting
`Map` or fixed array for alphabet size — anagrams, majority element (with Boyer–Moore), character replacement problems.

## 5. Sort then scan
Sort intervals, merge overlapping; sort pairs by one coordinate for greedy interval scheduling.

## 6. Pattern picker

| Signal | Try |
|--------|-----|
| Sorted input, pair/triplet | Two pointers |
| Contiguous subarray / substring constraint | Sliding window |
| Many range sum queries | Prefix sums |
| "Count ways" / optimal on sequences | DP |
| All combinations / permutations | Backtracking |
| Graph reachability | BFS / DFS |

## 7. Solving with the JDK (already implemented)

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

// Two pointers — often manual indices on int[] or List.get(i)

// Sliding window + last index of char
Map<Character, Integer> last = new HashMap<>();

// Prefix sums — int[] or long[] (use long if sums overflow)
long[] prefix = new long[a.length + 1];

// Sort then scan (intervals, pair problems)
Arrays.sort(intervals, (x, y) -> Integer.compare(x[0], y[0]));

// Frequency
Map<String, Long> freq = new HashMap<>();
freq.merge(token, 1L, Long::sum);

// Stream shorthand (know the cost: sort is O(n log n))
int[] sorted = Arrays.stream(nums).sorted().toArray();
```

| Pattern | JDK helpers |
|---------|-------------|
| Two pointers | indices on array / `List` |
| Sliding window | `HashMap`, `HashSet` |
| Prefix sum | `long[]`, `Arrays` |
| Sort + scan | `Arrays.sort`, `Comparator` |
| Count | `Map.merge`, `getOrDefault` |

See **`xi-solving-with-the-jdk.md`** for a full cheat sheet.
