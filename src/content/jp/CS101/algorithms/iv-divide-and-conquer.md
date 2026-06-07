---
label: "IV"
subtitle: "分割して征服する"
group: "データ構造とアルゴリズム"
order: 4
---
分割して征服する

**レシピ:** 問題を小さなサブ問題に分割し、(多くの場合再帰的に) 解決し、**結果を結合します**。

## 1. テンプレート
1. **基本ケース** — 小さい **n** は直接解決されます。
2. **分割** — 入力を **n/b** 程度のサイズの **a** 部分に分割します。
3. **征服** — 各部分を再帰します。
4. **結合** — 部分的な回答を **O(n)** などに結合します。

例: **マージ ソート**、**二分探索**、**最大部分配列** (中間点をまたぐ場合)、**カラツバ** 乗算 (上級)。

## 2. 再発 (スケッチ)
多くのアルゴリズムは **T(n) = a T(n/b) + f(n)** を満たします。

- **a** = 呼び出しごとの副問題の数。
- **n/b** = 副問題のサイズ。
- **f(n)** = 除算 + 結合コスト。

**マージソート:** **a = 2**、**b = 2**、**f(n) = Θ(n)** → **T(n) = Θ(n log n)**。

**二分探索:** 半分のサイズの 1 つの部分問題、**O(1)** 作業 → **T(n) = T(n/2) + O(1) = O(log n)**。

**マスター定理** ([パラダイムと限界](../iv-paradigms-and-limits.md) を参照) は、再帰ツリーを展開することなく、そのような多くの再帰を分類します。

## 3. 最大部分配列 (カダン vs 分割統治)
**Kadane** (リニア スキャン) は実用的な **O(n)** ソリューションです。

```java
// Compile: javac --release 22 …
/** Largest sum of any contiguous subarray. */
public static int maxSubarraySum(int[] a) {
  int best = a[0];
  int cur = a[0];
  for (int i = 1; i < a.length; i++) {
    cur = Math.max(a[i], cur + a[i]);
    best = Math.max(best, cur);
  }
  return best;
}
```

**分割統治** バージョン: 最大合計は完全に左半分、右半分、または中央を**交差**します。半分で再帰し、**O(n)** 交差スキャンと結合します。それでも全体としては **O(n log n)** です。 **結合**ステップを教えます。

## 4. 分割統治だけでは不十分な場合
部分問題が **重複** (同じ部分問題が何度も解決される) 場合、純粋な再帰では無駄な作業が行われます。**メモ化** または **表作成** (**動的プログラミング**、[動的プログラミング](viii-dynamic-programming.md)) を使用します。

|副次的な問題が重複していますか? |典型的なアプローチ |
|----------------------|------|
|いいえ |分割統治 |
|はい |動的プログラミング |

## 5. JDK による解決 (実装済み)

実際の分割統治は、主に **ライブラリ呼び出し** に **結合** ロジックを加えたものです。

```java
// Compile: javac --release 22 …
import java.util.Arrays;

// "Conquer" half — binary search on sorted half
int[] sorted = { 1, 4, 9, 16 };
int i = Arrays.binarySearch(sorted, 9);

// "Combine" step often needs sorted halves
Arrays.sort(leftHalf);
Arrays.sort(rightHalf);
// then merge with a loop, or System.arraycopy + merge

// Max subarray — Kadane is O(n); no JDK one-liner, but simple loop (see §3)
```

| D&C のアイデア | JDKヘルパー |
|----------|-----------|
|ソート範囲を検索 | `Arrays.binarySearch` |
|マージ前に部分範囲を並べ替える | `Arrays.sort(from, to)` |
|ブロックをコピー | `System.arraycopy`、`Arrays.copyOfRange` |
