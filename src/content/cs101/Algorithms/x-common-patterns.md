---
label: "X"
subtitle: "よくあるパターン"
group: "データ構造とアルゴリズム"
order: 10
---
一般的なアルゴリズム パターン

**配列**および**文字列**に対する再利用可能な手法。多くの場合、ソート後に**O(n)**または**O(n log n)**。

## 1. 2 つのポインタ
2 つのインデックスは、構造内を互いに向かって、または同じ方向に移動します。

**ソートされた配列ペアの合計** — ターゲット **T** で 2 つの値を検索します。

```java
// Compile: javac --release 22 …
public static boolean hasPairSum(int[] sorted, int target) {
  int lo = 0;
  int hi = sorted.length - 1;
  while (lo < hi) {
    int sum = sorted[lo] + sorted[hi];
    if (sum == target) {
      return true;
    }
    if (sum < target) {
      lo++;
    } else {
      hi--;
    }
  }
  return false;
}
```

**重複をその場で削除** (並べ替え): 書き込み位置のポインターは遅く、スキャンは高速です。

## 2. スライディングウィンドウ
配列上で **ウィンドウ** `[left, right]` を維持します。制約が壊れると **右** に拡張し、**左** に縮小します。

**繰り返し文字を含まない最長の部分文字列:**

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.Map;

public static int longestUniqueSubstring(String s) {
  Map<Character, Integer> last = new HashMap<>();
  int best = 0;
  int left = 0;
  for (int right = 0; right < s.length(); right++) {
    char c = s.charAt(right);
    if (last.containsKey(c) && last.get(c) >= left) {
      left = last.get(c) + 1;
    }
    last.put(c, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

**Time O(n)** — each index moves at most **n** steps total.

## 3. Prefix sums
`prefix[i]` = sum of `a[0..i-1]` → range sum **O(1)** after **O(n)** preprocess.

```java
// Compile: javac --release 22 …
public static int[] prefixSum(int[] a) {
  int[] p = new int[a.length + 1];
  for (int i = 0; i < a.length; i++) {
    p[i + 1] = p[i] + a[i];
  }
  return p;
}

/** Sum of a[lo..hi] inclusive. */
public static int rangeSum(int[] prefix, int lo, int hi) {
  return prefix[hi + 1] - prefix[lo];
}
```

## 4. Frequency counting
`Map` or fixed array for alphabet size — anagrams, majority element (with Boyer–Moore), character replacement problems.

## 5. Sort then scan
Sort intervals, merge overlapping; sort pairs by one coordinate for greedy interval scheduling.

## 6. パターンピッカー

|信号 |試してみる |
|--------|-----|
|ソートされた入力、ペア/トリプレット | 2 つのポインタ |
|連続部分配列/部分文字列制約 |引き違い窓
|多くの範囲合計クエリ |プレフィックスの合計 |
| 「方法を数える」/シーケンスで最適 | DP |
|すべての組み合わせ/順列 |後戻り |
|グラフの到達可能性 | BFS / DFS |

## 7. JDK を使用した解決 (実装済み)

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

// Two pointers — often manual indices on int[] or List.get(i)

// Sliding window + last index of char
Map<Character, Integer> last = new HashMap<>();

// Prefix sums — int[] or long[] (use long if sums overflow)
long[] prefix = new long[a.length + 1];

// Sort then scan (intervals, pair problems)
Arrays.sort(intervals, (x, y) -> Integer.compare(x[0], y[0]));

// Frequency
Map<String, Long> freq = new HashMap<>();
freq.merge(token, 1L, Long::sum);

// Stream shorthand (know the cost: sort is O(n log n))
int[] sorted = Arrays.stream(nums).sorted().toArray();
```

|パターン | JDK ヘルパー |
|----------|---------------|
| 2 つのポインタ |配列のインデックス / `List` |
|引き違い窓`HashMap`、`HashSet` |
|プレフィックスの合計 | `long[]`、`Arrays` |
|並べ替え + スキャン | `Arrays.sort`、`Comparator` |
|カウント | `Map.merge`、`getOrDefault` |

完全なチートシートについては、**[JDK を使用した解決](xi-solving-with-the-jdk.md)** を参照してください。
