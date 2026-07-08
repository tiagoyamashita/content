---
label: "VII"
subtitle: "Greedy"
group: "Data structures & algorithms"
order: 7
---
Greedy algorithms
At each step, take the **locally best** option that looks good now — **without** revisiting past choices.

**When it works:** you can prove the local choice is safe (exchange argument, matroid, or known theorem). **When it fails:** a counterexample where greedy misses the global optimum (e.g. **0/1 knapsack** — use DP).

See also **Level IV — Paradigms** [Paradigms & limits](../iv-paradigms-and-limits.md).

## 1. Classic problems

| Problem | Greedy rule | Notes |
|---------|-------------|-------|
| Activity selection | Pick earliest **finishing** compatible activity | Sort by finish time |
| Huffman coding | Merge two least frequent symbols | Uses min-heap |
| Fractional knapsack | Take items by **value/weight** ratio | Optimal; 0/1 version is not greedy |
| MST (Prim / Kruskal) | Cheapest safe edge | [Shortest paths & MST](vi-shortest-paths-and-mst.md) |
| Dijkstra | Settle smallest tentative distance | Needs non-negative weights |

## 2. Activity selection (sketch)
Sort activities by **finish time**. Take the next activity that **starts after** the last chosen finish.

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Comparator;

record Activity(int start, int finish) {}

public static int maxActivities(Activity[] acts) {
  Arrays.sort(acts, Comparator.comparingInt(Activity::finish));
  int count = 0;
  int lastFinish = Integer.MIN_VALUE;
  for (Activity a : acts) {
    if (a.start() >= lastFinish) {
      count++;
      lastFinish = a.finish();
    }
  }
  return count;
}
```

## 3. Proof habit
1. **Greedy choice property:** some optimal solution can use the greedy first pick.
2. **Optimal substructure:** after that pick, solve the rest optimally.

If step 1 fails, try **DP** or **branch and bound**.

## 4. Greedy vs dynamic programming

| | Greedy | DP |
|--|--------|-----|
| Choices | One committed step | Explore subproblem table |
| Subproblems | Usually non-overlapping | Overlapping |
| Time | Often sort + linear scan | Often pseudo-polynomial or O(n²) |
| Example win | MST, Huffman | 0/1 knapsack, LCS |

## 5. Solving with the JDK (already implemented)

Greedy code is usually **sort** + **one pass** + sometimes a **heap**:

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

// Activity selection — sort then scan (see §2)
Activity[] acts = { /* … */ };
Arrays.sort(acts, Comparator.comparingInt(Activity::finish));

// Huffman-style "always take two smallest" — min-heap
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(3);
pq.offer(1);
int a = pq.poll();
int b = pq.poll();

// Fractional knapsack — sort by ratio
record Item(int w, int v) {}
Item[] items = { /* … */ };
Arrays.sort(items, Comparator.comparingDouble(it -> -(double) it.v / it.w));
```

| Greedy step | JDK |
|-------------|-----|
| Order candidates | `Arrays.sort`, `Comparator` |
| Repeatedly take smallest | `PriorityQueue` |
| Take current max | `Collections.max`, `stream().max` |
