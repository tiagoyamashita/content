---
label: "V"
subtitle: "配列、可変引数、リスト"
group: "ジャワ"
groupOrder: 1
order: 5
---
Java — パート V

固定サイズの配列、可変長引数、`java.util.Arrays`、および `ArrayList` を優先する場合。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. 宣言とインデックス付け

配列は **固定長**で、**`0`** からインデックス付けされ、**`length`** フィールド (メソッドではありません) を持ちます。

```java
// Compile: javac --release 22 …
int[] scores = new int[] {90, 85, 72};
scores[1] = 88;                    // mutate element
int n = scores.length;             // 3

String[][] grid = {{"a", "b"}, {"c", "d"}}; // array of arrays
```

- **`int[] a`** と **`int a[]`** は同等です。読みやすいように **`int[]`** を推奨します。
- 多次元配列は**ギザギザ**です。各行は異なる長さを持つことができます。

## 2. `java.util.Arrays` ヘルパー

```java
// Compile: javac --release 22 …
import java.util.Arrays;

int[] data = {5, 1, 4, 2, 8};
Arrays.sort(data);                          // in-place sort
int idx = Arrays.binarySearch(data, 4);     // requires sorted input
int[] copy = Arrays.copyOf(data, data.length);
Arrays.fill(copy, 0);
```

アルゴリズムの詳細 (二分探索が適用される場合の複雑さ) については、**CS101 → データ構造 → 配列** および **アルゴリズム → 検索** を参照してください。

## 3. 可変引数 (`...`)

メソッドは、0 個以上の 1 つの型の末尾引数を受け入れることができます。

```java
// Compile: javac --release 22 …
static int sum(int first, int... rest) {
  int total = first;
  for (int v : rest) {
    total += v;
  }
  return total;
}

// calls: sum(1), sum(1, 2, 3)
```

メソッド内では、**`rest`** は **`int[]`** です。可変引数パラメータはメソッドごとに **1 つ** のみであり、最後になければなりません。

## 4. 配列と `List`

| | `int[]` / `T[]` | `ArrayList<T>` |
|--|--|--|
|サイズ |作成時に修正 |必要に応じて成長します |
|プリミティブ |ネイティブ (`int[]`) |特殊な API を除くボックス (`Integer`) |
| API | `length`、`Arrays.*` | `add`、`remove`、`size()` |
|いつ使用するか |ホットな数値バッファー、相互運用性 |ほとんどのアプリケーション コレクション |

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

List<String> names = new ArrayList<>();
names.add("Ada");
names.add("Grace");
for (String name : names) {
  System.out.println(name);
}
```

小さな不変スナップショットには **`List.of(...)`** または **`List.copyOf(...)`** を推奨します。

## 5. 拡張された for と境界

```java
// Compile: javac --release 22 …
for (int score : scores) {
  System.out.println(score); // read-only view of elements
}
```

範囲外のアクセスにより **`ArrayIndexOutOfBoundsException`** がスローされる — ユーザー入力からのインデックスを検証します。
