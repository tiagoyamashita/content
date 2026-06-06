---
label: "VI"
subtitle: "最短パスと MST"
group: "データ構造とアルゴリズム"
order: 6
---
最短パスと最小スパニングツリー

重み付けされたグラフ: エッジは **コスト** または **距離** を伝えます。

## 1. 単一ソースの最短パス

|アルゴリズム |グラフ |重み |時間 (通常) |
|----------|----------|----------|-----|
| **BFS** |任意 |すべて等しい (加重なし) | O(n + m) |
| **ディクストラ** |有向/無向 | **非ネガティブ** | O((n + m) log n) バイナリ ヒープ |
| **ベルマン – フォード** |任意 |負のサイクルを許可します (負のサイクルは禁止) | O(nm) |

### ダイクストラ (非負の重み)
貪欲: **最小優先順位キュー** [優先順位キュー](../data-structures/ix-priority-queue.md) を使用して、**最も近い**未解決の頂点を常に解決します。

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

**負**のエッジ重みを調整せずにグラフに対してダイクストラを実行しないでください**。代わりに**ベルマン-フォード**を使用してください。

## 2. すべてのペアの最短パス (名前のみ)
- **フロイド–ウォーシャル:** **O(n³)**、トリプルの動的計画法 - 密なグラフ、小さい **n**。
- **Johnson:** 各頂点からの重み付け + ダイクストラ — 否定的な可能性のあるスパース グラフ (上級)。

## 3. 最小スパニングツリー (MST)
**無向**、接続、重み付け: **最小総重み**、**サイクルなし**ですべての頂点を接続する**n − 1** エッジを選択します。

|アルゴリズム |アイデア |時間 |
|-----------|------|------|
| **クラスカル** |エッジを並べ替えます。サイクルがない場合は追加 (union–find) | O(m log m) |
| **プリム** |最初から木を育てます。常に最も安いエッジをツリーに追加します。 O((n + m) log n) ヒープあり |

どちらも**貪欲**です。正しさの証明は **カット プロパティ** / **交換引数** [貪欲](vii-greedy.md) を使用します。

## 4. いつ何を使用するか
- **マップ/ルーティング (非ネガティブ):** ダイクストラ。
- **通貨裁定取引 (マイナスサイクル検出):** ベルマン-フォード。
- **ネットワーク設計 (すべてのサイトを安価に接続):** MST (Kruskal または Prim)。

## 5. JDK による解決 (実装済み)

**Dijkstra** と **Prim** は **`PriorityQueue`** (JDK のバイナリ ヒープ) を使用します。 **Kruskal** は、エッジ + **union–find** で **`Arrays.sort`** を使用します (UF を実装するか、小さなヘルパー クラスを使用します)。

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

|アルゴリズム | JDK ビルディング ブロック |
|----------|----------|
| BFS (重み付けされていない最短) | `ArrayDeque`、`Queue` |
|ディクストラ / プリム | `PriorityQueue`、`Comparator` |
|クラスカル | `Arrays.sort`、union–find (カスタム ~20 行) |
|非ネガティブエッジリラックス | `int[] dist` の `Math.min` |

サードパーティのライブラリ (JGraphT など) は完全なグラフ アルゴリズムを追加します。 **CS101** とインタビューでは、**`PriorityQueue`** を使用して **短いループ**を作成することが求められます。
