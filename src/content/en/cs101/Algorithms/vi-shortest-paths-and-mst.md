---
label: "VI"
subtitle: "Shortest paths & MST"
group: "Data structures & algorithms"
order: 6
---
Shortest paths & minimum spanning trees
Weighted graphs: edges carry **cost** or **distance**.

## 1. Single-source shortest paths

| Algorithm | Graph | Weights | Time (typical) |
|-----------|-------|---------|----------------|
| **BFS** | Any | All equal (unweighted) | O(n + m) |
| **Dijkstra** | Directed/undirected | **Non-negative** | O((n + m) log n) with binary heap |
| **Bellman–Ford** | Any | Allows negative (no neg cycles) | O(nm) |

### Dijkstra (non-negative weights)
Greedy: always settle the **closest** unsettled vertex using a **min-priority queue** [Priority queue](../data-structures/ix-priority-queue.md).

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.PriorityQueue;

/** adj.get(u) = list of (neighbor, weight); non-negative weights only. */
public static int[] dijkstra(List<List<int[]>> adj, int source) {
  int n = adj.size();
  int[] dist = new int[n];
  Arrays.fill(dist, Integer.MAX_VALUE);
  dist[source] = 0;
  PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
  pq.offer(new int[] { source, 0 });
  while (!pq.isEmpty()) {
    int[] cur = pq.poll();
    int u = cur[0];
    int d = cur[1];
    if (d != dist[u]) {
      continue;
    }
    for (int[] edge : adj.get(u)) {
      int v = edge[0];
      int w = edge[1];
      int nd = d + w;
      if (nd < dist[v]) {
        dist[v] = nd;
        pq.offer(new int[] { v, nd });
      }
    }
  }
  return dist;
}
```

**Do not** run Dijkstra on graphs with **negative** edge weights without adjustment — use **Bellman–Ford** instead.

## 2. All-pairs shortest paths (names only)
- **Floyd–Warshall:** **O(n³)**, dynamic programming on triples — dense graphs, small **n**.
- **Johnson:** reweight + Dijkstra from each vertex — sparse graphs with possible negatives (advanced).

## 3. Minimum spanning tree (MST)
**Undirected**, connected, weighted: pick **n − 1** edges connecting all vertices with **minimum total weight**, **no cycles**.

| Algorithm | Idea | Time |
|-----------|------|------|
| **Kruskal** | Sort edges; add if no cycle (union–find) | O(m log m) |
| **Prim** | Grow tree from a start; always add cheapest edge to tree | O((n + m) log n) with heap |

Both are **greedy**; correctness proofs use **cut property** / **exchange argument** [Greedy](vii-greedy.md).

## 4. When to use what
- **Maps / routing (non-negative):** Dijkstra.
- **Currency arbitrage (negative cycle detection):** Bellman–Ford.
- **Network design (connect all sites cheaply):** MST (Kruskal or Prim).

## 5. Solving with the JDK (already implemented)

**Dijkstra** and **Prim** use **`PriorityQueue`** (binary heap in the JDK). **Kruskal** uses **`Arrays.sort`** on edges + **union–find** (you still implement UF, or use a small helper class).

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

// Min-heap for Dijkstra / Prim — already in §1
PriorityQueue<int[]> pq = new PriorityQueue<>(
    Comparator.comparingInt(e -> e[1]));

// Kruskal: sort edges by weight, then union–find scan
record Edge(int u, int v, int w) {}
Edge[] edges = { /* … */ };
Arrays.sort(edges, Comparator.comparingInt(Edge::w));

// Multi-source BFS (unweighted) — one Queue per wave or one BFS with Queue
```

| Algorithm | JDK building blocks |
|-----------|---------------------|
| BFS (unweighted shortest) | `ArrayDeque`, `Queue` |
| Dijkstra / Prim | `PriorityQueue`, `Comparator` |
| Kruskal | `Arrays.sort`, union–find (custom ~20 lines) |
| Non-negative edge relax | `Math.min` on `int[] dist` |

Third-party libraries (e.g. JGraphT) add full graph algorithms; **CS101** and interviews expect you to write the **short loop** using **`PriorityQueue`**.
