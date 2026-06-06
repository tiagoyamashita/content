---
label: "V"
subtitle: "配列、可変引数、リスト"
group: "Java"
groupOrder: 1
order: 5
---
Java — パート V





固定サイズの配列、可変引数、`java.util.Arrays`、そしていつを好むか`ArrayList`。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. 宣言とインデックスの付与

配列は **固定長**、** からインデックス付けされます`0`**、**付き`length`** フィールド (メソッドではありません)。

```java
// Compile: javac --release 22 …
int[] scores = new int[] {90, 85, 72};
scores[1] = 88;                    // mutate element
int n = scores.length;             // 3

String[][] grid = {{"a", "b"}, {"c", "d"}}; // array of arrays
```

- **`int[] a`** そして **`int a[]`** は同等です - ** を優先します`int[]`** 読みやすさのため。
- 多次元配列は**ギザギザ**です。各行は異なる長さを持つことができます。

＃＃２。`java.util.Arrays`ヘルパー

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

メソッドは、0個以上の1つの型の末尾引数を受け取ることができます。

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

メソッド内では、**`rest`**は**です`int[]`**。可変引数パラメータはメソッドごとに **1 つ** のみであり、最後になければなりません。

## 4. 配列との比較`List`

| |`int[]`/`T[]`|`ArrayList<T>`|
|--|--|--|
|サイズ |作成時に修正 |必要に応じて成長します |
|プリミティブ |ネイティブ (`int[]`) |ボックス (`Integer`) 特殊な APIs を除く。
| API |`length`、`Arrays.*`|`add`、`remove`、`size()`|
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

好む **`List.of(...)`** または **`List.copyOf(...)`** 小さな不変スナップショットの場合。

## 5. と境界のために拡張された

```java
// Compile: javac --release 22 …
for (int score : scores) {
  System.out.println(score); // read-only view of elements
}
```

範囲外アクセスによるスロー **`ArrayIndexOutOfBoundsException`** — ユーザー入力から取得されたインデックスを検証します。
