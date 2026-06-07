---
label: "II"
subtitle: "仕分け"
group: "データ構造とアルゴリズム"
order: 2
---
仕分け

要素を**非減少**の順序で(または**`Comparator`**によって)配置します。 **比較ソート**では**compare**のみが使用され、特別なキー構造は使用されません。

## 1. 比較ソート（概要）

|アルゴリズム |ベスト |平均 |最悪 |余分なスペース |安定した？ |
|----------|------|----------|-------|-------------|----------|
|バブル / 挿入 | O(n) | O(n²) | O(n²) |お(1) |はい |
|選択 | O(n²) | O(n²) | O(n²) |お(1) |いいえ |
|マージソート | O(n log n) | O(n log n) | O(n log n) | O(n) |はい |
|クイックソート | O(n log n) | O(n log n) | O(n²) | O(log n) スタック |いいえ |
|ヒープソート | O(n log n) | O(n log n) | O(n log n) |お(1) |いいえ |

**安定:** 等しいキーは相対的な入力順序を維持します。 **インプレース:** 再帰スタック以外に O(1) の追加。

**Java:** `Arrays.sort(int[])` は **デュアルピボット クイックソート** を使用します。 `Arrays.sort(Object[])` は **TimSort** (マージ + 挿入、安定) を使用します。

## 2. マージソート（分割統治）
1. **配列をサイズ 1 になるまで半分に分割します**。
2. **征服** — シングルトンがソートされます。
3. **結合** — ソートされた 2 つの半分を **O(n)** 時間で結合します。

**時間 Θ(n log n)**; **典型的な補助バッファのスペース Θ(n)**。

```java
// Compile: javac --release 22 …
public static void mergeSort(int[] a, int[] buf, int lo, int hi) {
  if (hi - lo < 2) {
    return;
  }
  int mid = lo + (hi - lo) / 2;
  mergeSort(a, buf, lo, mid);
  mergeSort(a, buf, mid, hi);
  merge(a, buf, lo, mid, hi);
}

private static void merge(int[] a, int[] buf, int lo, int mid, int hi) {
  System.arraycopy(a, lo, buf, lo, hi - lo);
  int i = lo;
  int j = mid;
  int k = lo;
  while (i < mid && j < hi) {
    if (buf[i] <= buf[j]) {
      a[k++] = buf[i++];
    } else {
      a[k++] = buf[j++];
    }
  }
  while (i < mid) {
    a[k++] = buf[i++];
  }
  while (j < hi) {
    a[k++] = buf[j++];
  }
}
```

## 3. クイックソート
**ピボット**、*パーティション**を選択して、要素 ≤ ピボットが左になり、> 右にピボットされ、両側で再帰されます。

- **平均Θ(n log n)**; **ピボットが常に最小/最大の場合 (不適切なピボット ルールでソートされた入力)、最悪の Θ(n²)**。
- **軽減策:** ランダム ピボット、3 の中央値、または狭い範囲での挿入ソートに切り替えます。

```java
// Compile: javac --release 22 …
public static void quickSort(int[] a, int lo, int hi) {
  if (lo >= hi) {
    return;
  }
  int p = partition(a, lo, hi);
  quickSort(a, lo, p);
  quickSort(a, p + 1, hi);
}

private static int partition(int[] a, int lo, int hi) {
  int pivot = a[hi - 1];
  int i = lo;
  for (int j = lo; j < hi - 1; j++) {
    if (a[j] <= pivot) {
      int tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
      i++;
    }
  }
  int tmp = a[i];
  a[i] = a[hi - 1];
  a[hi - 1] = tmp;
  return i;
}
```

## 4. ヒープソート
1. 配列内に最大ヒープを **構築**します (**O(n)** ボトムアップ)。
2. ルートをソートされていない最後の位置とルートを**シンク** に繰り返し交換します — ステップあたり **O(log n)** → 合計 **O(n log n)**。

**バイナリ ヒープ** ADT [バイナリ ヒープ](../data-structures/viii-binary-heap.md); を使用します。 **インプレース** 配列自体をヒープ化する場合。

## 5. いつどれを使用するか
- **Java の汎用:** `Arrays.sort`。
- **オブジェクトの安定性が必要:** `Arrays.sort(Object[])` または明示的なマージ ソート。
- **外部ソート (ディスク上のデータ):** マージ ソート — 順次パス。
- **Top-k / 部分順序:** ヒープまたは `PriorityQueue`、フルソートではありません。

## 6. JDK による解決 (実装済み)

アプリケーション コードでマージ/クイック ソートを記述することはほとんどありません。**プリミティブかオブジェクト**、**安定か不安定**を選択した後、ライブラリを呼び出します。

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

int[] a = { 5, 2, 8, 2 };
Arrays.sort(a); // dual-pivot quicksort for primitives

Integer[] boxed = { 5, 2, 8 };
Arrays.sort(boxed, Comparator.reverseOrder()); // TimSort, stable

// Top-k largest without sorting entire array — O(n log k)
int k = 3;
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int x : a) {
  minHeap.offer(x);
  if (minHeap.size() > k) {
    minHeap.poll();
  }
}
```

|必要 | API |
|------|-----|
| `int[]` / `double[]` | 並べ替え`Arrays.sort` |
| `Object[]` または `List` を並べ替える | `Arrays.sort`、`list.sort(Comparator)`、`Collections.sort` |
|カスタムオーダー | `Comparator.comparing`、`comparingInt`、`reverseOrder` |
| k のみ最大/最小 | `PriorityQueue` サイズ **k** |

その他の例: **[JDK を使用した解決](xi-solving-with-the-jdk.md)**。
