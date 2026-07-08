---
label: "IX"
subtitle: "後戻り"
group: "データ構造とアルゴリズム"
order: 9
---
後戻り

**体系的な試行錯誤:** 候補となるソリューションを段階的に構築します。選択が行き止まりになった場合は、**元に戻し** (バックトラック)、次のオプションを試してください。

暗黙的な決定の**状態ツリー**に関する**DFS**と同じ考え。

## 1. テンプレート
1. **選択** — 決定を下します。
2. **再帰** — 残りを解決します。
3. **選択を解除** — 状態を復元します (バックトラック)。

多くの場合、**制約** (無効な部分ソリューション) を使用してブランチを早期にプルーニングします。

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

/** All subsets of {0, 1, …, n-1} as bit-style lists. */
public static void subsets(int n, int start, List<Integer> cur, List<List<Integer>> out) {
  out.add(new ArrayList<>(cur));
  for (int i = start; i < n; i++) {
    cur.add(i);
    subsets(n, i + 1, cur, out);
    cur.remove(cur.size() - 1);
  }
}
```

## 2. 典型的な問題

|問題 |状態 |剪定 |
|----------|-------|----------|
| **サブセット/組み合わせ** |各要素を含めるかスキップする |なし、またはサイズ制限あり |
| **順列** |要素で使用されるフラグ | — |
| **N-クイーン** |行ごとの列の配置 | 2 人の女王が攻撃することはありません。
| **数独** |空のセルの選択肢 |行/列/ボックスの競合 |
| **グラフの色分け** |次の頂点に色を付ける |隣り合う色が違う |

## 3. N-queens (スケッチ)
クイーンを一行ずつ配置します。行 **r** では、前の女王によって攻撃されていない各列 **c** を試します。

```java
// Compile: javac --release 22 …
public static void nQueens(int n, int row, int[] cols, List<int[]> solutions) {
  if (row == n) {
    solutions.add(cols.clone());
    return;
  }
  for (int c = 0; c < n; c++) {
    if (safe(cols, row, c)) {
      cols[row] = c;
      nQueens(n, row + 1, cols, solutions);
    }
  }
}

private static boolean safe(int[] cols, int row, int col) {
  for (int r = 0; r < row; r++) {
    if (cols[r] == col || Math.abs(cols[r] - col) == row - r) {
      return false;
    }
  }
  return true;
}
```

## 4. 複雑さ
最悪のケースは、多くの場合、分岐係数 × 深さにおいて **指数関数的**です。バックトラッキングは、**小さな**検索スペースまたは**重度の枝刈り**の場合に行われます。

## 5. バックトラッキング vs DP
- **バックトラッキング:** 有効な構成を**すべて**列挙します (またはそれらをカウントします)。
- **DP:** 部分問題が **重複**しており、すべての解決策リストではなく **最適値**が必要な場合。

## 6. JDK による解決 (実装済み)

バックトラッキングは**カスタム再帰**です。 JDK は **コンテナ** と **簿記**に役立ちます。

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

List<Integer> path = new ArrayList<>();
List<List<Integer>> answers = new ArrayList<>();

path.add(choice);
backtrack(/* … */);
path.remove(path.size() - 1); // unchoose

// Try candidates in different order (heuristic)
List<Integer> candidates = new ArrayList<>(List.of(1, 2, 3));
Collections.shuffle(candidates); // needs Random seed for reproducibility
```

|バックトラッキングの必要性 | JDK |
|---------------------|-----|
|現在のパス | `ArrayList` |
|すべてのソリューション | `List<List<T>>` |
|使用されるフラグ | `boolean[]`、`HashSet` |
|状態をコピー | `new ArrayList<>(path)`、`Arrays.copyOf` |

小さな **n** のみの **順列 / 組み合わせ**: ライブラリは存在しますが、インタビューでは §1 の **再帰的** テンプレートが必要です。
