---
label: "V"
subtitle: "グラフのトラバーサル"
group: "データ構造とアルゴリズム"
order: 5
---
グラフの走査 — BFS および DFS

グラフ **G = (V, E)** では、走査は系統的に頂点を訪問します。グラフをスパース グラフの **隣接リスト**として保存します。**n = |V|**、**m = |E|** の場合、走査には **O(n + m)** の空間と時間がかかります。

**グラフ** [グラフ](../data-structures/xi-graph.md) および **レベル III - グラフ** (`iii-graphs.md`) を参照してください。

## 1. 幅優先検索 (BFS)
距離に基づいて **レイヤー** で探索します (**重み付けされていない** エッジ、ホップ数で)。

- **キュー** ADT — 近隣のキューをエンキューし、現在の [キュー](../data-structures/v-queue.md) をデキューします。
- 隣接リストを使用した場合の **時間 O(n + m)**。
- **用途: **重み付けされていない**グラフの最短パス、レベル順序、接続性。

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

**最短パス長 (重みなし):** 最初に検出されたときに `dist[v]` を保存します。 `dist[w] = dist[v] + 1`。

## 2. 深さ優先検索 (DFS)
バックトラックする前に **深く**してください — **スタック** または **再帰**。

- **時間 O(n + m)**。
- **用途:** サイクル検出、トポロジカルソート、接続コンポーネント、迷路探索。

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

**反復 DFS** は、スタックとして明示的な `Deque` を使用します (同じ端の `push` / `pop`)。

## 3. BFS 対 DFS

| | BFS | DFS |
|--|-----|-----|
|構造 |キュー |スタック / 再帰 |
|重み付けされていない最短パス |はい |いいえ (最初に幸運に恵まれない限り) |
|幅の広いグラフ上のメモリ |大きなフロンティアになる可能性があります |パスの深さのみ |
|トポロジカルソート |いいえ |はい (追加の状態あり) |

## 4. トポロジカルソート (DAG)
**有向非巡回グラフ** — すべてのエッジが順序で **前方**になるように頂点を順序付けします。

- **カーン (BFS):** は **次数 0** の頂点を繰り返し削除します。
- **DFS:** 終了時間順序 (逆事後順序)。

すべての頂点を処理できない場合、グラフには **サイクル** が発生します。

## 5. 接続されたコンポーネント
未訪問の各頂点から BFS または DFS を実行します。各実行には、1 つの **コンポーネント** (無指向) または **到達可能なセット** (有向) のラベルが付けられます。

## 6. JDK による解決 (実装済み)

標準ライブラリには `Graph.bfs()` は**ありません**。 **隣接リスト** (`List<List<Integer>>` または `Map`) を保持し、JDK **キュー** / **セット**を使用します。

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

|役割 | JDK タイプ |
|------|----------|
| FIFO フロンティア (BFS) | `Queue` + `ArrayDeque` |
|スタック (DFS) | `ArrayDeque` `push` / `pop` |
|訪問セット | `HashSet`、`boolean[]` |
|近隣リスト | `List<List<Integer>>`、`Map<Integer, List<Integer>>` |

**トポロジカルソート:** カーンのアルゴリズム = **`Queue`** + 度数配列;単一の `Collections.topologicalSort` はありません。

**[キュー](../data-structures/v-queue.md)**、**[スタック](../data-structures/iv-stack.md)**、**[JDK を使用した解決](xi-solving-with-the-jdk.md)** を参照してください。
