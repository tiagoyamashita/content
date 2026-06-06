---
label: "VII"
subtitle: "よく深い"
group: "データ構造とアルゴリズム"
order: 7
---
貪欲なアルゴリズム

各ステップで、**過去の選択を再検討することなく**、現時点で適切と思われる**ローカルで最適**なオプションを選択します。

**それが機能すると:** ローカルの選択が安全であることを証明できます (交換引数、マトロイド、または既知の定理)。 **失敗した場合:** 貪欲が全体最適を逃す反例 (例: **0/1 ナップザック** — DP を使用)。

See also **Level IV — Paradigms** [Paradigms & limits](../iv-paradigms-and-limits.md).

## 1. 典型的な問題

| Problem | Greedy rule | Notes |
|---------|-------------|-------|
| Activity selection | Pick earliest **finishing** compatible activity | Sort by finish time |
| Huffman coding | Merge two least frequent symbols | Uses min-heap |
| Fractional knapsack | Take items by **value/weight** ratio | Optimal; 0/1 version is not greedy |
| MST (Prim / Kruskal) | Cheapest safe edge | [Shortest paths & MST](vi-shortest-paths-and-mst.md) |
| Dijkstra | Settle smallest tentative distance | Needs non-negative weights |

## 2. アクティビティの選択 (スケッチ)
**終了時間**でアクティビティを並べ替えます。最後に選択した終了後に**開始される次のアクティビティを実行します。

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

## 3. 証拠の習慣
1. **貪欲な選択プロパティ:** 一部の最適解では貪欲な最初の選択を使用できます。
2. **最適な部分構造:** その選択の後、残りを最適に解決します。

ステップ 1 が失敗した場合は、**DP** または **分岐とバインド** を試してください。

## 4. 貪欲なプログラミングと動的プログラミング

| |貪欲 | DP |
|---|--------|-----|
|選択肢 |コミットされた 1 つのステップ |サブ問題テーブルを探索する |
|サブ問題 |通常は重複しない |重なる |
|時間 |多くの場合、ソート + リニア スキャン |多くの場合、擬似多項式または O(n²) |
|勝利の例 | MST、ハフマン | 0/1 ナップザック、LCS |

## 5. JDK による解決 (実装済み)

貪欲なコードは通常、**sort** + **1 パス** + 場合によっては **ヒープ** です。

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
