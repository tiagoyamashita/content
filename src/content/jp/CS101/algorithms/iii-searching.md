---
label: "III"
subtitle: "検索中"
group: "データ構造とアルゴリズム"
order: 3
---
検索中

**ターゲット**がコレクション内に存在するかどうか (または、どこに存在するか) を調べます。

## 1. 線形探索
ターゲットを見つけるか構造物を使い果たすまで、端からスキャンします。

- **時間 O(n)** — **n** 要素。
- **スペース O(1)** 追加。
- **あらゆる**注文に対応します。ランダムアクセスなしで**リンクされた**リスト上で動作します。

```java
// Compile: javac --release 22 …
public static int linearSearch(int[] a, int target) {
  for (int i = 0; i < a.length; i++) {
    if (a[i] == target) {
      return i;
    }
  }
  return -1;
}
```

## 2. 二分探索
**並べ替えられた**配列 (または `Comparator` による並べ替え順序) が必要です。

- **Time O(log n)** — ステップごとに検索範囲を半分にします。
- **Space O(1)** 反復。 **O(log n)** 再帰的な場合は再帰スタック。

**不変:** ターゲットが存在する場合、そのインデックスは `[lo, hi]` にあります。

```java
// Compile: javac --release 22 …
import java.util.Arrays;

public static int binarySearchSorted(int[] sorted, int target) {
  int idx = Arrays.binarySearch(sorted, target);
  return idx >= 0 ? idx : -1;
}

/** Same logic without Arrays.binarySearch — useful for interviews. */
public static int binarySearchManual(int[] sorted, int target) {
  int lo = 0;
  int hi = sorted.length - 1;
  while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (sorted[mid] == target) {
      return mid;
    }
    if (sorted[mid] < target) {
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  return -1;
}
```

**一般的なバグ:** `mid = (lo + hi) / 2` は一部の言語でオーバーフローする可能性があります。 **`lo + (hi - lo) / 2`** を使用してください。

## 3. 答えの二分探索 (パターン)
述語 `P(x)` が false から true (単調) に反転するような **最小 x** が問題で求められている場合は、配列インデックスではなく、範囲内の **x** に対して二分探索を行います。

例: 最初の不良バージョン、D 日で荷物を発送できる能力、最小の食事速度。

## 4. ハッシュベースの検索
**ハッシュ テーブル** [ハッシュ テーブル](../data-structures/x-hash-table.md) では、平均 **O(1)** の挿入と検索が行われます。並べ替え順序は必要ありません。最悪の場合、適切なハッシュがなければ **O(n)** になります。

|方法 |前提条件 |時間 |
|------|------|------|
|リニア |なし | O(n) |
|バイナリ |並べ替え済み | O(log n) |
|ハッシュ |ハッシュ可能なキー | O(1) 平均 |

## 5. JDK による解決 (実装済み)

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

int[] sorted = { 1, 3, 5, 7 };
int idx = Arrays.binarySearch(sorted, 5); // 2 if present

List<String> names = List.of("ada", "bob");
boolean has = names.contains("ada");           // O(n) on list
Map<String, Integer> index = new HashMap<>();  // O(1) average lookup
index.put("ada", 0);
index.get("ada");

Set<Integer> seen = new HashSet<>();
for (int x : data) {
  if (!seen.add(x)) {
    // duplicate
  }
}
```

|タスク | JDK |
|------|-----|
|ソートされた配列の検索 | `Arrays.binarySearch` (最初にソート) |
|メンバーシップをリストする |多くのクエリには `list.contains` または `HashSet` |
|キー → 値 | `HashMap.get`、`getOrDefault`、`containsKey` |
|出現回数をカウントする | `Collections.frequency` (リスト) または `Map.merge` |

**インタビューと本番:** 手動二分探索ループを理解している。プロジェクトでは、ソートされたデータに対して **`Arrays.binarySearch`** を呼び出します。
