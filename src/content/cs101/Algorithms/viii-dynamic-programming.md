---
label: "VIII"
subtitle: "Dynamic programming"
group: "Data structures & algorithms"
order: 8
---
Dynamic programming (DP)
Solve optimization or counting problems by reusing answers to **overlapping subproblems**.

**Requirements**
1. **Optimal substructure** — optimal solution built from optimal subsolutions.
2. **Overlapping subproblems** — same subproblem appears many times in a naive recursion tree.

## 1. Top-down vs bottom-up

| Style | Mechanism | Pros |
|-------|-----------|------|
| **Memoization** | Recursion + cache (`Map` or array) | Fast to write |
| **Tabulation** | Fill table in dependency order | No recursion depth; often faster |

## 2. Fibonacci (toy example)
Naive recursion **O(2ⁿ)**; memo or table **O(n)**.

```java
// Compile: javac --release 22 …
public static long fibMemo(int n, long[] memo) {
  if (n <= 1) {
    return n;
  }
  if (memo[n] != 0) {
    return memo[n];
  }
  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n];
}

public static long fibTab(int n) {
  if (n <= 1) {
    return n;
  }
  long[] dp = new long[n + 1];
  dp[0] = 0;
  dp[1] = 1;
  for (int i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}
```

## 3. 0/1 knapsack
**n** items; item **i** has weight **wᵢ** and value **vᵢ**; capacity **W**. Each item **at most once**.

**State:** `dp[i][c]` = max value using items `0..i-1` with capacity **c**.  
**Transition:** skip item **i** or take it if it fits.

**Time O(n · W)**, **space O(n · W)** (or O(W) with one row).

```java
// Compile: javac --release 22 …
public static int knapsack01(int[] weight, int[] value, int capacity) {
  int n = weight.length;
  int[][] dp = new int[n + 1][capacity + 1];
  for (int i = 1; i <= n; i++) {
    for (int c = 0; c <= capacity; c++) {
      dp[i][c] = dp[i - 1][c];
      if (weight[i - 1] <= c) {
        dp[i][c] = Math.max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
      }
    }
  }
  return dp[n][capacity];
}
```

## 4. Longest common subsequence (LCS)
**State:** `dp[i][j]` = LCS length of first **i** chars of **A** and first **j** of **B**.

```java
// Compile: javac --release 22 …
public static int lcsLength(String a, String b) {
  int[][] dp = new int[a.length() + 1][b.length() + 1];
  for (int i = 1; i <= a.length(); i++) {
    for (int j = 1; j <= b.length(); j++) {
      if (a.charAt(i - 1) == b.charAt(j - 1)) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[a.length()][b.length()];
}
```

## 5. Edit distance (Levenshtein)
Minimum insert / delete / replace to turn **A** into **B** — classic **2D DP**, **O(|A| · |B|)**.

## 6. DP design checklist
1. Define **state** (what subproblem means).
2. Write **recurrence** + **base cases**.
3. Decide iteration order (bottom-up) or memo keys (top-down).
4. Track **time/space** in table size.

## 7. Solving with the JDK (already implemented)

There is **no** `DynamicProgramming.solve()` in Java. You use **arrays** and **maps** the JDK already provides:

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

// Bottom-up table
int[][] dp = new int[n + 1][capacity + 1];
Arrays.fill(dp[0], 0);

// Top-down memo — key is often "i,c" or a record
Map<String, Integer> memo = new HashMap<>();
String key = i + "," + c;
if (!memo.containsKey(key)) {
  memo.put(key, solve(i, c)); // fill from recurrence
}
int ans = memo.get(key);

// Edit distance / LCS — still nested loops on int[][]
```

| DP need | JDK |
|---------|-----|
| 2D table | `int[][]`, `long[][]` |
| Memoization | `HashMap`, `Map.computeIfAbsent` |
| Initialize row | `Arrays.fill` |
| Min/max in recurrence | `Math.min`, `Math.max` |

For **Fibonacci-scale** toy problems only, `Map` memo is enough; production DP stays **iterative tables** for stack safety.
