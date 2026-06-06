---
label: "VIII"
subtitle: "動的プログラミング"
group: "データ構造とアルゴリズム"
order: 8
---
動的プログラミング (DP)

**重複する部分問題**に対する回答を再利用して、最適化または計数の問題を解決します。

**要件**
1. **最適な部分構造** — 最適な部分解から構築された最適なソリューション。
2. **重複する部分問題** — 単純な再帰ツリーでは、同じ部分問題が何度も現れます。

## 1. トップダウンとボトムアップ

|スタイル |メカニズム |長所 |
|------|-----------|------|
| **メモ化** |再帰 + キャッシュ (`Map` または配列) |書くのが早い |
| **集計** |依存関係の順序でテーブルを埋める |再帰の深さはありません。多くの場合、より速くなります |

## 2. フィボナッチ (おもちゃの例)
単純な再帰 **O(2ⁿ)**;メモまたは表 **O(n)**。

```java
// Compile: javac --release 22 …
public static long fibMemo(int n, long[] memo) {
  if (n <= 1) {
    return n;
  }
  if (memo[n] != 0) {
    return memo[n];
  }
  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n];
}

public static long fibTab(int n) {
  if (n <= 1) {
    return n;
  }
  long[] dp = new long[n + 1];
  dp[0] = 0;
  dp[1] = 1;
  for (int i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}
```

## 3. 0/1 ナップザック
**n** アイテム。項目 **i** には重み **wᵢ** と値 **vᵢ** があります。容量**W**。各項目 **最大 1 回**。

**状態:** `dp[i][c]` = 容量 **c** のアイテム `0..i-1` を使用した最大値。  
**移行:** 項目 **i** をスキップするか、該当する場合はそのまま使用してください。

**時間 O(n · W)**、**スペース O(n · W)** (または 1 行の場合は O(W))。

```java
// Compile: javac --release 22 …
public static int knapsack01(int[] weight, int[] value, int capacity) {
  int n = weight.length;
  int[][] dp = new int[n + 1][capacity + 1];
  for (int i = 1; i <= n; i++) {
    for (int c = 0; c <= capacity; c++) {
      dp[i][c] = dp[i - 1][c];
      if (weight[i - 1] <= c) {
        dp[i][c] = Math.max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
      }
    }
  }
  return dp[n][capacity];
}
```

## 4. 最長共通部分列 (LCS)
**状態:** `dp[i][j]` = **A** の最初の **i** 文字と **B** の最初の **j** の LCS 長さ。

```java
// Compile: javac --release 22 …
public static int lcsLength(String a, String b) {
  int[][] dp = new int[a.length() + 1][b.length() + 1];
  for (int i = 1; i <= a.length(); i++) {
    for (int j = 1; j <= b.length(); j++) {
      if (a.charAt(i - 1) == b.charAt(j - 1)) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[a.length()][b.length()];
}
```

## 5. 距離の編集 (レーベンシュタイン)
**A** を **B** に変えるための最小限の挿入/削除/置換 — 古典的な **2D DP**、**O(|A| · |B|)**。

## 6. DP 設計チェックリスト
1. **状態** (部分問題の意味) を定義します。
2. **再発** + **基本ケース**を書きます。
3. 反復順序 (ボトムアップ) またはメモ キー (トップダウン) を決定します。
4. テーブル サイズで **時間/空間** を追跡します。

## 7. JDK を使用した解決 (実装済み)

Java には**** `DynamicProgramming.solve()` はありません。 JDK がすでに提供している **配列** と **マップ** を使用します。

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

// Bottom-up table
int[][] dp = new int[n + 1][capacity + 1];
Arrays.fill(dp[0], 0);

// Top-down memo — key is often "i,c" or a record
Map<String, Integer> memo = new HashMap<>();
String key = i + "," + c;
if (!memo.containsKey(key)) {
  memo.put(key, solve(i, c)); // fill from recurrence
}
int ans = memo.get(key);

// Edit distance / LCS — still nested loops on int[][]
```

| DP の必要性 | JDK |
|----------|-----|
| 2Dテーブル | `int[][]`、`long[][]` |
|メモ化 | `HashMap`、`Map.computeIfAbsent` |
|行を初期化する | `Arrays.fill` |
|繰り返しの最小/最大 | `Math.min`、`Math.max` |

**フィボナッチスケール**のトイ問題の場合のみ、`Map` メモで十分です。本番環境の DP は、スタックの安全性を確保するために **反復テーブル** のままです。
