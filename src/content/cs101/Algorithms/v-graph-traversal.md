---
label: "V"
subtitle: "Graph traversal"
group: "Data structures & algorithms"
order: 5
---
Graph traversal — BFS & DFS
On a graph **G = (V, E)**, traversal visits vertices systematically. Store the graph as an **adjacency list** for sparse graphs — **O(n + m)** space and time for traversals when **n = |V|**, **m = |E|**.

See **Graph** (`data-structures/xi-graph.md`) and **Level III — Graphs** (`iii-graphs.md`).

## 1. Breadth-first search (BFS)
Explore in **layers** by distance (in **unweighted** edges, hop count).

- **Queue** ADT — enqueue neighbors, dequeue current (`v-queue.md`).
- **Time O(n + m)** with adjacency lists.
- **Uses:** shortest path in **unweighted** graphs, level order, connectivity.

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public static List<Integer> bfsOrder(List<List<Integer>> adj, int start) {
  int n = adj.size();
  boolean[] seen = new boolean[n];
  List<Integer> order = new ArrayList<>();
  Queue<Integer> q = new ArrayDeque<>();
  seen[start] = true;
  q.offer(start);
  while (!q.isEmpty()) {
    int v = q.poll();
    order.add(v);
    for (int w : adj.get(v)) {
      if (!seen[w]) {
        seen[w] = true;
        q.offer(w);
      }
    }
  }
  return order;
}
```

**Shortest path lengths (unweighted):** store `dist[v]` when first discovered; `dist[w] = dist[v] + 1`.

## 2. Depth-first search (DFS)
Go **deep** before backtracking — **stack** or **recursion**.

- **Time O(n + m)**.
- **Uses:** cycle detection, topological sort, connected components, maze exploration.

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

public static void dfsRecursive(List<List<Integer>> adj, int v, boolean[] seen, List<Integer> order) {
  seen[v] = true;
  order.add(v);
  for (int w : adj.get(v)) {
    if (!seen[w]) {
      dfsRecursive(adj, w, seen, order);
    }
  }
}
```

**Iterative DFS** uses an explicit `Deque` as a stack (`push` / `pop` at same end).

## 3. BFS vs DFS

| | BFS | DFS |
|--|-----|-----|
| Structure | Queue | Stack / recursion |
| Unweighted shortest path | Yes | No (unless first hit by luck) |
| Memory on wide graphs | Can be large frontier | Path depth only |
| Topological sort | No | Yes (with extra state) |

## 4. Topological sort (DAG)
**Directed acyclic graph** — order vertices so every edge goes **forward** in the order.

- **Kahn (BFS):** repeatedly remove vertices with **in-degree 0**.
- **DFS:** finish-time order (reverse postorder).

If you cannot process all vertices, the graph has a **cycle**.

## 5. Connected components
Run BFS or DFS from each unvisited vertex; each run labels one **component** (undirected) or **reachable set** (directed).

## 6. Solving with the JDK (already implemented)

There is **no** `Graph.bfs()` in the standard library. You keep an **adjacency list** (`List<List<Integer>>` or `Map`) and use JDK **queues** / **sets**:

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

// BFS — Queue from ArrayDeque (FIFO)
Queue<Integer> q = new ArrayDeque<>();
Set<Integer> seen = new HashSet<>();
seen.add(start);
q.offer(start);

// DFS iterative — Deque as stack
ArrayDeque<Integer> stack = new ArrayDeque<>();
stack.push(start);

// Track visited / in-degree for topo
int[] indegree = new int[n];
List<Integer> topo = new ArrayList<>();
```

| Role | JDK type |
|------|----------|
| FIFO frontier (BFS) | `Queue` + `ArrayDeque` |
| Stack (DFS) | `ArrayDeque` `push` / `pop` |
| Visited set | `HashSet`, `boolean[]` |
| Neighbor list | `List<List<Integer>>`, `Map<Integer, List<Integer>>` |

**Topological sort:** Kahn’s algorithm = **`Queue`** + indegree array; no single `Collections.topologicalSort`.

See **`v-queue.md`**, **`iv-stack.md`**, and **`xi-solving-with-the-jdk.md`**.
