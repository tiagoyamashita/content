---
label: "IX"
subtitle: "Backtracking"
group: "Data structures & algorithms"
order: 9
---
Backtracking
**Systematic trial and error:** build a candidate solution step by step; when a choice leads to a dead end, **undo** (backtrack) and try the next option.

Same idea as **DFS** on an implicit **state tree** of decisions.

## 1. Template
1. **Choose** — make a decision.
2. **Recurse** — solve the rest.
3. **Unchoose** — restore state (backtrack).

Often prune branches early with **constraints** (invalid partial solutions).

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

/** All subsets of {0, 1, …, n-1} as bit-style lists. */
public static void subsets(int n, int start, List<Integer> cur, List<List<Integer>> out) {
  out.add(new ArrayList<>(cur));
  for (int i = start; i < n; i++) {
    cur.add(i);
    subsets(n, i + 1, cur, out);
    cur.remove(cur.size() - 1);
  }
}
```

## 2. Classic problems

| Problem | State | Pruning |
|---------|-------|---------|
| **Subsets / combinations** | Include or skip each element | None or size limit |
| **Permutations** | Used flags on elements | — |
| **N-queens** | Row-by-row column placement | No two queens attack |
| **Sudoku** | Empty cell choices | Row/col/box conflicts |
| **Graph coloring** | Color next vertex | Adjacent colors differ |

## 3. N-queens (sketch)
Place queens row by row; in row **r**, try each column **c** not attacked by prior queens.

```java
// Compile: javac --release 22 …
public static void nQueens(int n, int row, int[] cols, List<int[]> solutions) {
  if (row == n) {
    solutions.add(cols.clone());
    return;
  }
  for (int c = 0; c < n; c++) {
    if (safe(cols, row, c)) {
      cols[row] = c;
      nQueens(n, row + 1, cols, solutions);
    }
  }
}

private static boolean safe(int[] cols, int row, int col) {
  for (int r = 0; r < row; r++) {
    if (cols[r] == col || Math.abs(cols[r] - col) == row - r) {
      return false;
    }
  }
  return true;
}
```

## 4. Complexity
Worst case is often **exponential** in branching factor × depth — backtracking is for **small** search spaces or **heavy pruning**.

## 5. Backtracking vs DP
- **Backtracking:** enumerate **all** valid configurations (or count them).
- **DP:** when subproblems **overlap** and you need **optimal value**, not every solution listing.
