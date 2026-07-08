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

**時間 O(n)** — 各インデックスは合計で最大 **n** ステップ移動します。

## 3. プレフィックスの合計
`prefix[i]` = `a[0..i-1]` の合計 → **O(n)** 前処理後の範囲合計 **O(1)**。

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

## 4. 周波数のカウント
`Map` またはアルファベット サイズの固定配列 — アナグラム、多数要素 (Boyer-Moore による)、文字置換の問題。

## 5. 並べ替えてからスキャンする
間隔を並べ替え、重複をマージします。貪欲な間隔スケジュールのために 1 つの座標でペアを並べ替えます。

## 6. パターンピッカー

|信号 |試してみる |
|--------|-----|
|ソートされた入力、ペア/トリプレット | 2 つのポインタ |
|連続部分配列/部分文字列制約 |引き違い窓
|多くの範囲合計クエリ |プレフィックスの合計 |
| 「方法を数える」/シーケンスで最適 | DP |
|すべての組み合わせ/順列 |後戻り |
|グラフの到達可能性 | BFS / DFS |

## 7. __​​IT0__ による解決 (実装済み)

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
