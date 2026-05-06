---
label: "III"
subtitle: "Graphs"
group: "Data structures & algorithms"
order: 3
---
Level III — Graphs
Representations, traversal, DAGs, SCCs, shortest paths.

## 1. Representations
- G = (V, E); n = |V|, m = |E| (often use n, m in complexity).
- Adjacency matrix: n×n bits/weights; edge query O(1); space Θ(n²).
- Adjacency list: per vertex list of neighbors; space Θ(n + m); iterate edges fast.
- Sparse graphs (m ≪ n²): lists win; dense or all-pairs closeness → matrix handy.
- Directed vs undirected: undirected edge {u,v} often stored twice for simplicity.

## 2. Breadth-first search (BFS)
- Layer-by-layer from source s using a queue; visits increasing distance in unweighted graphs.
- Time O(n + m): each vertex dequeued once; edges explored once (directed view).
- Shortest path (fewest edges) from s in unweighted undirected/directed graph.
- BFS tree: layers partition vertices by distance from s.

## 3. Depth-first search (DFS)
- Go deep with stack (explicit or recursion); backtrack when stuck.
- Time O(n + m); timestamps discovery/finish useful for classifications.
- Edge types (directed): tree, back, forward, cross — know back edge ⇔ cycle.
- DFS orderings: preorder, postorder — used in SCC and topo algorithms.

## 4. Topological sort
- Only for DAG (directed acyclic graph); ordering where all edges go forward.
- Kahn: repeatedly remove vertex with in-degree 0 (queue).
- Or: DFS postorder reverse (finish times); cycle ⇒ no valid topo order.
- Applications: task scheduling, build systems, course prerequisites.

## 5. Strongly connected components (SCC)
- Directed graph: SCC = maximal mutually reachable subgraphs.
- Kosaraju / Tarjan: two DFS passes or one with lowlink — O(n + m).
- Condensation graph (SCCs contracted) is always a DAG.
- Useful for 2-SAT-style reasoning at advanced level.

## 6. Shortest paths — Dijkstra
- Non-negative edge weights; greedy from closest unsettled vertex.
- Min-priority queue by tentative distance; relax edges — O((n+m) log n) with binary heap.
- Works because relaxing shortest-known path first is safe when weights ≥ 0.
- Fails with negative edges: longer paths can improve via negative weight later.

## 7. Shortest paths — Bellman-Ford
- Allows negative weights (no negative cycle reachable from source).
- Relax all edges n−1 rounds; nth round detects negative cycles.
- O(nm) — slower than Dijkstra but handles negatives and cycle detection.
- SPFA is queue optimization; worst case still poor — know textbook BF first.

## 8. All-pairs & Floyd–Warshall (mention)
- Floyd–Warshall: dynamic programming over intermediate vertices k — O(n³).
- Fine for small n; negative edges OK unless negative cycle on path.
- Johnson: combine Dijkstra + reweighting for sparse graphs — optional depth.

## 9. Remember & rehearse
- Same graph: write BFS layers vs DFS preorder on paper.
- When is topo sort impossible? Draw a directed triangle cycle.
- One scenario each: choose Dijkstra vs Bellman-Ford and justify.
