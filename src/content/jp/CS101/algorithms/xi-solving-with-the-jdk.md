---
label: "XI"
subtitle: "JDK で解決する"
group: "データ構造とアルゴリズム"
order: 11
---
JDK を使用してアルゴリズムの問​​題を解決する

コースワークでは、アルゴリズムを手動で実装して、アルゴリズムが**どのように機能する**かを学びます。 **実際の Java** では、**`java.util`** および **`java.util.Arrays`** から **すでに実装されている** 型を構成します。これらは、実稼働用に接続された **データ構造** サブメニューの同じ ADT です。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. 考え方

|目標 |手巻き（学習） | JDK (出荷コード) |
|-----|--------------------------|----------|
|配列をソートする |マージ/クイックソート | `Arrays.sort`、`List.sort` |
|並べ替えられたデータ内で検索 |二分探索ループ | `Arrays.binarySearch` |
|素早く検索/数える |リニアスキャン | `HashMap`、`HashSet` |
| FIFO トラバーサル |リンクされたキュー クラス | `ArrayDeque` + `Queue` |
| Best-next (ダイクストラ、プリム) | エクスペディアヒープシフトコード | `PriorityQueue` |
|グラフの到達可能性 | BFS/DFS ループ | `ArrayDeque` + 構築する隣接リスト |

**JDK は、ダイクストラまたは MST が組み込まれた `Graph` クラスを同梱していません**。**短いループ**を作成することはできますが、キュー、ヒープ、マップ、ソートを再実装する代わりに**再利用**します。

## 2. チートシート: 問題 → API

|問題の種類 |主要な JDK ツール |
|--------------|-------------------|
|ソートキー | `Arrays.sort`、`Collections.sort`、`Comparator` |
|ソートされた配列を検索 | `Arrays.binarySearch`、`Collections.binarySearch` |
|ルックアップ / 重複排除 | `HashMap`、`HashSet`、`Map.computeIfAbsent` |
|キュー (BFS) | `ArrayDeque`、`Queue.offer` / `poll` |
|スタック (DFS 反復) | `ArrayDeque` を `Deque`、`push` / `pop` として |
|次の最小/最大 | `PriorityQueue` (デフォルトの最小ヒープ) |
|トップ k 最大 | `PriorityQueue` (最小ヒープ サイズ k) または `stream().sorted().limit(k)` |
|安定したソートオブジェクト | `Arrays.sort(Object[])` (ティムソート) |
|マージ間隔 | `Arrays.sort` 開始 + スキャン |
|周波数を数える | `HashMap.merge`、`getOrDefault` |
|範囲合計クエリ |プレフィックス配列 (手動) または `long[]` + ループ |
|順列 / サブセット (小さい n) |自分自身を後戻りさせます。オプションの `Stream` ヘルパー |

## 3. 並べ替えと検索

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

int[] nums = { 3, 1, 4, 1, 5 };
Arrays.sort(nums);

List<String> names = List.of("bob", "ada", "grace");
List<String> sorted = names.stream().sorted().toList();
// or mutate a copy:
List<String> copy = new java.util.ArrayList<>(names);
Collections.sort(copy);

record Job(int deadline, String name) {}
Job[] jobs = { new Job(5, "a"), new Job(2, "b") };
Arrays.sort(jobs, Comparator.comparingInt(Job::deadline));

int idx = Arrays.binarySearch(nums, 4); // >= 0 if found
```

**`Arrays.binarySearch`** は、見つかった場合は **≥ 0** を返し、それ以外の場合は **`-(insertionPoint) - 1`** を返します。配列は最初に**ソート**する必要があります。

## 4. マップとセット

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

Map<String, Integer> freq = new HashMap<>();
for (String word : words) {
  freq.merge(word, 1, Integer::sum);
}

Set<Integer> seen = new HashSet<>();
if (seen.add(x)) {
  // first time we saw x
}
```

## 5. キュー、スタック、ヒープ (グラフと貪欲)

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Queue;

// BFS
Queue<Integer> q = new ArrayDeque<>();
q.offer(start);

// Dijkstra-style (non-negative weights) — see vi-shortest-paths-and-mst.md
PriorityQueue<int[]> pq = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[] { source, 0 });

// Top-k largest: keep min-heap of size k
PriorityQueue<Integer> heap = new PriorityQueue<>();
for (int x : nums) {
  heap.offer(x);
  if (heap.size() > k) {
    heap.poll();
  }
}
```

## 6. コレクションユーティリティ

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

int max = Collections.max(List.of(3, 1, 4));
Collections.reverse(Arrays.asList(boxed)); // array as list view
Collections.swap(list, i, j);
int freq = Collections.frequency(list, target);
```

## 7. ストリーム (オプション、同じ複雑さのクラス)

可読性が優先される場合に使用します。基礎となるアルゴリズムを知っている (ソートは **O(n log n)**)。

```java
// Compile: javac --release 22 …
import java.util.Arrays;

int[] a = { 3, 1, 4 };
boolean anyEven = Arrays.stream(a).anyMatch(x -> x % 2 == 0);
int sum = Arrays.stream(a).sum();
int[] sorted = Arrays.stream(a).sorted().toArray();
```

## 8. まだ自分で実装しているもの

- **グラフ** ストレージ (隣接リスト/行列)。
- **BFS / DFS / Dijkstra / MST** 制御ループ (JDK キュー/ヒープを使用)。
- **DP** テーブルフィル (配列 + ループ、場合によっては `HashMap` メモキー)。
- **選択/選択解除による**バックトラッキング**再帰。

## 9. トピックごとのポインター

|注 | JDK の焦点 |
|------|-----------|
| [ソート](ii-sorting.md) | `Arrays.sort`、`Comparator` |
| [検索中](iii-searching.md) | `binarySearch`、`HashMap` |
| [グラフ走査](v-graph-traversal.md) | `ArrayDeque`、`Queue` |
| [最短パスと MST](vi-shortest-paths-and-mst.md) | `PriorityQueue`、Kruskal のエッジをソート |
| [貪欲](vii-greedy.md) |ソート + `PriorityQueue` |
| [動的プログラミング](viii-dynamic-programming.md) | `int[][]`、`HashMap` メモ |
| [よくあるパターン](x-common-patterns.md) | `HashMap`、`Arrays.sort`、ストリーム |
