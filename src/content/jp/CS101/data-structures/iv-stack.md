---
label: "IV"
subtitle: "スタック"
group: "データ構造とアルゴリズム"
order: 4
---
スタック — 2つのバッキング実装

**スタック ADT** は、その下でリストを使用するか配列を使用するかによってではなく、**操作**によって定義されます。このノートでは、**単一リンク リスト** (先頭 = 先頭) と **動的配列** (論理先頭の先頭) という 2 つの標準的なバッキングを比較します。

**Java ベースライン:** スニペットは **Java SE 22** を想定しています — IDE で言語レベルを **22** に設定するか、** でコンパイルします`javac --release 22`**。 The features used here (generics,`var`追加された場合のみ、`Deque`、など）**JDK 21 LTS** でも実行されます。 **22** をこのマテリアルがチェックされる最小値として扱い、チームが必要に応じて運用環境で **LTS** JDK を使用します。

## 1. ADT としてスタックする (要約)
**操作**には通常、次のものが含まれます`push(x)`、`pop()`、`peek()`/`top()`、`isEmpty()`、そしてしばしば`size()`/`clear()`。 **不変:**`pop`**最近プッシュされた**項目 (LIFO) を削除します。

スタックは、任意の **インデックス アクセス**、**検索**、または **途中での挿入/削除**を目的としたものではありません**。これらの動作が必要な場合は、**異なる** 構造 (シーケンスとして使用される両端キュー、リスト、または配列など) をモデル化します。

**用途:** DFS、元に戻す、括弧の一致、後置評価、コールスタックの直感。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 168" role="img" aria-label="Stack after three pushes then one pop removes newest item at top">
  <defs>
    <marker id="ds-st-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After push(1) push(2) push(3)</text>
  <text x="48" y="42" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="40" y="48" width="80" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="76" y="65" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="40" y="78" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="76" y="95" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="40" y="108" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="76" y="125" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M140 88 H200" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-mk)"/>
  <text x="148" y="82" fill="#a1a1aa" font-size="10">pop()</text>
  <text x="148" y="96" fill="#fbbf24" font-size="10" font-weight="600">returns 3</text>
  <text x="220" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After one pop (LIFO)</text>
  <text x="256" y="42" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="248" y="48" width="80" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="284" y="65" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="248" y="78" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="284" y="95" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <text x="12" y="154" fill="#71717a" font-size="10">Only the top changes on push/pop — both backings keep every op O(1) at the top.</text>
</svg></figure>

### 操作ごとのビジュアル (ADT)

**`push(x)`** — 新しい要素が **最上位** になります。スタック上にすでにあるものはすべてスタックの**下**に残ります。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 130" role="img" aria-label="push adds a new top element">
  <defs>
    <marker id="op-push-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">push(4)</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M92 55 H130" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-push-ar)"/>
  <text x="96" y="50" fill="#60a5fa" font-size="10" font-weight="600">push(4)</text>
  <text x="140" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="140" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="138" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="168" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">4</text>
  <rect x="138" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="138" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <text x="230" y="18" fill="#71717a" font-size="10">Older values sink one step;</text>
  <text x="230" y="32" fill="#71717a" font-size="10">the new value is always LIFO “first out” next.</text>
</svg></figure>

**`peek()`** / **`top()`** — 上部を取り外さずに**検査します。描画はピーク後も**変更されていません**。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 126" role="img" aria-label="peek reads top without changing stack">
  <text x="10" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">peek() / top()</text>
  <text x="10" y="38" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="44" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="38" y="61" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="74" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="91" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="104" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="121" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M100 57 Q140 28 200 28" stroke="#fbbf24" stroke-width="2" fill="none"/>
  <text x="148" y="22" fill="#fbbf24" font-size="11" font-family="ui-monospace" font-weight="600">returns 3</text>
  <text x="200" y="70" fill="#71717a" font-size="10">Same stack after peek —</text>
  <text x="200" y="84" fill="#71717a" font-size="10">no pop, no size change.</text>
</svg></figure>

**`pop()`** — **現在の**先頭（同じセル**）を削除して返します`peek`** と読みます)。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 126" role="img" aria-label="pop removes and returns top element">
  <defs>
    <marker id="op-pop-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">pop()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M92 55 H128" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-pop-ar)"/>
  <text x="96" y="50" fill="#fbbf24" font-size="10" font-weight="600">returns 3</text>
  <text x="138" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="138" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="136" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="166" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="136" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="166" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <text x="228" y="62" fill="#71717a" font-size="10">Top moves down; size drops by 1.</text>
</svg></figure>

**`isEmpty()`** — **no** の場合は true (何もない)`peek`または`pop`）。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="isEmpty true when stack has no elements">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">isEmpty()</text>
  <rect x="10" y="38" width="100" height="44" rx="6" fill="rgba(24,24,27,0.5)" stroke="#52525b" stroke-dasharray="6 4"/>
  <text x="34" y="64" fill="#71717a" font-size="11">no elements</text>
  <text x="128" y="64" fill="#86efac" font-size="11" font-weight="600">→ true</text>
  <text x="220" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">not empty</text>
  <text x="220" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="218" y="42" width="56" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="240" y="60" fill="#e4e4e7" font-size="12" font-family="ui-monospace">x</text>
  <text x="290" y="64" fill="#86efac" font-size="11" font-weight="600">→ false</text>
</svg></figure>

**`size()`** - 先頭を含む**要素の論理数。このスタックには合計 **3 つの**値があります。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 128" role="img" aria-label="size counts elements in stack">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">size()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">c</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">b</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">a</text>
  <text x="100" y="78" fill="#60a5fa" font-size="12" font-family="ui-monospace" font-weight="600">size = 3</text>
</svg></figure>

**`clear()`** — すべての要素を削除します。その後**`isEmpty()`** は真実であり、**`size()`** は **`0`**。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" role="img" aria-label="clear removes all stack elements">
  <defs>
    <marker id="op-clr-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">clear()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="56" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="30" y="59" fill="#e4e4e7" font-size="11" font-family="ui-monospace">z</text>
  <rect x="8" y="72" width="56" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="30" y="89" fill="#e4e4e7" font-size="11" font-family="ui-monospace">y</text>
  <path d="M78 55 H118" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-clr-ar)"/>
  <text x="82" y="48" fill="#a1a1aa" font-size="10">clear</text>
  <rect x="128" y="48" width="120" height="44" rx="6" fill="rgba(24,24,27,0.5)" stroke="#52525b" stroke-dasharray="6 4"/>
  <text x="158" y="74" fill="#71717a" font-size="11">empty stack</text>
  <text x="268" y="74" fill="#86efac" font-size="10" font-weight="600">size = 0</text>
</svg></figure>

### 使用例 (Java)

通常必要な **ライブラリ** タイプは ** です`Deque<E>`** と **`ArrayDeque<E>`** (このノートの後半の Java で説明します)。以下に、同じ ADT 語彙を数行で示します。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);
stack.push(20);
stack.peek();     // 20 — top unchanged
stack.pop();      // 20
stack.isEmpty();  // false (10 still inside)
stack.size();     // 1
stack.clear();
stack.isEmpty();  // true
```

**バランスの取れた括弧**は古典的なスタックの練習です: 開始シンボル上で、**`push`**;終了記号、**`pop`** そして、ポップしたものとペアになっているかどうかを確認します。文字列の末尾、**`isEmpty()`** は **true** である必要があります。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

public final class BracketExamples {

  private BracketExamples() {}

  public static boolean bracketsBalanced(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      if (c == '(' || c == '[' || c == '{') {
        stack.push(c);
      } else if (c == ')' || c == ']' || c == '}') {
        if (stack.isEmpty()) {
          return false;
        }
        char o = stack.pop();
        if (!pairs(o, c)) {
          return false;
        }
      }
    }
    return stack.isEmpty();
  }

  private static boolean pairs(char open, char close) {
    return switch (open) {
      case '(' -> close == ')';
      case '[' -> close == ']';
      case '{' -> close == '}';
      default -> false;
    };
  }
}
```


## 2. バッキングとしての単一リンクリスト
**先頭ポインタを先頭**として扱います。 **空**スタックは空のリストです。`head == null`。

**プッシュ:** 新しいノードを割り当て、古いノードをポイントし、割り当てます`head`新しいノード — **Θ(1)** に。  
**ポップ:**読む`head`、 前進`head`に`head.next`、古いトップの値 — **Θ(1)** を返します。  
**テール ポインタは必要ありません**。すべてのスタック操作はヘッドのみに影響します。

**`push(x)`** (リストバッキング) — 新しいノードの **`next`** は古いヘッドです。 **`head`** 新しいノードに移動します。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 108" role="img" aria-label="Linked list push prepends new node at head">
  <defs>
    <marker id="ll-push-mk" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="8" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before push(9)</text>
  <text x="8" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="48" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="62" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M90 60 H102" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="106" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="120" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M148 60 H160" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="168" y="64" fill="#71717a" font-size="11">null</text>
  <path d="M220 58 H268" stroke="#60a5fa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="224" y="52" fill="#60a5fa" font-size="10" font-weight="600">push(9)</text>
  <text x="278" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="278" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="318" y="44" width="40" height="32" rx="6" fill="rgba(96,165,250,0.2)" stroke="#60a5fa" stroke-width="2"/>
  <text x="328" y="62" fill="#e4e4e7" font-size="10" font-family="ui-monospace">9 new</text>
  <path d="M360 60 H372" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="376" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="390" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M418 60 H430" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="434" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="448" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M476 60 H488" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="496" y="64" fill="#71717a" font-size="11">null</text>
  <text x="8" y="98" fill="#71717a" font-size="9">One pointer write for the new node’s next, one for head — both O(1).</text>
</svg></figure>

**`pop()`** (リストバッキング) — ヘッドの値を保存し、** を設定します`head = head.next`**、保存された値を返します。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 108" role="img" aria-label="Linked list pop advances head and returns old top">
  <defs>
    <marker id="ll-pop-mk" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="8" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before pop()</text>
  <text x="8" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="48" y="44" width="40" height="32" rx="6" fill="rgba(251,191,36,0.25)" stroke="#fbbf24" stroke-width="2"/>
  <text x="62" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">9</text>
  <path d="M90 60 H102" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="106" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="120" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M148 60 H160" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="164" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="178" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M206 60 H218" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="226" y="64" fill="#71717a" font-size="11">null</text>
  <path d="M248 58 H296" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="252" y="52" fill="#fbbf24" font-size="10" font-weight="600">returns 9</text>
  <text x="306" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="306" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="346" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="360" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M388 60 H400" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="404" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="418" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M446 60 H458" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="466" y="64" fill="#71717a" font-size="11">null</text>
  <text x="8" y="98" fill="#71717a" font-size="9">Old top becomes unreachable (GC) unless you keep a reference elsewhere.</text>
</svg></figure>

### Java: head-as-top スタック (指導クラス)

これは、リンク リストの注: ** の **prepend / delete-first** リスト操作を反映しています。`head`**は**トップ**です。テールポインタはありません。

```java
// Compile: javac --release 22 …
import java.util.NoSuchElementException;
import java.util.Objects;

public class LinkedStack<E> {

  private static final class Node<E> {
    final E item;
    Node<E> next;

    Node(E item, Node<E> next) {
      this.item = item;
      this.next = next;
    }
  }

  private Node<E> head;
  private int size;

  public void push(E item) {
    head = new Node<>(Objects.requireNonNull(item), head);
    size++;
  }

  public E pop() {
    if (head == null) {
      throw new NoSuchElementException();
    }
    E out = head.item;
    head = head.next;
    size--;
    return out;
  }

  public E peek() {
    if (head == null) {
      throw new NoSuchElementException();
    }
    return head.item;
  }

  public boolean isEmpty() {
    return head == null;
  }

  public int size() {
    return size;
  }

  /** O(1): drop the chain; nodes become unreachable for the GC. */
  public void clear() {
    head = null;
    size = 0;
  }
}
```

### ウォークスルー (重複した値)
**1**、**3** (最初の出現)、**3** (2 番目の出現)、**2** の順に値をプッシュします。 2 つのノードが同じ表示値を保持する場合、推論ではそれらに **3⁽¹⁾** および **3⁽²⁾** というラベルを付けます。

1.`push(1)`— 頭 →`1`2.`push(3⁽¹⁾)`— 頭 →`3⁽¹⁾`→`1`3.`push(3⁽²⁾)`— 頭 →`3⁽²⁾`→`3⁽¹⁾`→`1`(先頭は**2番目**の3番目です)  
4.`push(2)`— 頭 →`2`→`3⁽²⁾`→`3⁽¹⁾`→`1`

図面では、**上**は**左**に配置され、古いノードは**右**に伸びていることがよくあります。新しいプッシュは先頭に到着するため、古い要素はチェーンの「より深く」表示されます。

**ポップ:** 常に先頭を切り離します (list delete-at-head と同じ)。ポップの例は、**2**、**3⁽²⁾**、**3⁽¹⁾**、**1** の順に返されます。 4回目のポップの後、`head`**null** です — スタックは空です。

**クリア:** セット`head = null`— **Θ(1)** 時間;ノードが到達不能になった場合は、**GC** がそれらのノードを (マネージ言語で) 再利用するか、C/C++ で明示的に解放することができます。

### なぜ二重リンクしないのでしょうか?
二重リンクリストは引き続きスタック演算をサポートしますが、各ノードは **追加のポインター** (`prev`）。スタックは正しい動作のために逆方向のトラバースを必要としないため、**メモリ オーバーヘッド**によって使用されるものは何もありません。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Singly linked stack head on left as top nodes to the right">
  <defs>
    <marker id="ds-st-ll" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Head = top (left in this sketch)</text>
  <text x="12" y="40" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="52" y="48" width="44" height="36" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="66" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M98 66 H112" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="116" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="128" y="68" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₂</text>
  <path d="M162 66 H176" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="180" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="192" y="68" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₁</text>
  <path d="M226 66 H240" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="244" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="258" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M290 66 H304" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <text x="312" y="70" fill="#71717a" font-size="11">null</text>
  <text x="12" y="94" fill="#71717a" font-size="9">push/pop only rewire head — no tail, no index scans</text>
</svg></figure>


## 3. バッキングとしての配列 (動的配列)
**を追跡する`size`** (論理要素数)。 **空の**スタック:`size == 0`。

**先頭はどこですか?** 常に **インデックス 0** に挿入する場合、プッシュごとに既存のすべての要素を**シフト**する必要があります (プッシュごとに **Θ(n)**)。代わりに、**後方**で拡張します: **次のプッシュ**はインデックス**に書き込みます`size`**、その後インクリメントします`size`。 **トップ** (`peek`/`pop`) はインデックス ** にあります`size - 1`**。

### 配列上の同じシーケンス
十分な容量。始める`size = 0`。

|ステップ |アクション |配列インデックス (概念的) |後のサイズ |
|-----|----------|--------------------|---------------|
| — |空 |`[ · · · · ]`| 0 |
| 1 | 1を押します |`[1, ·, ·, ·]`| 1 |
| 2 | 3⁽¹⁾を押してください`[1, 3, ·, ·]`| 2 |
| 3 | 3⁽²⁾を押してください。`[1, 3, 3, ·]`| 3 |
| 4 |プッシュ2 |`[1, 3, 3, 2]`| 4 |

**ポップ:**読む`arr[size - 1]`、 それから`size--`— **Θ(1)** (GC またはセキュリティ用のスロットをクリアできます。以下を参照)。  
**プッシュ:** **動的配列**上で Θ(1)** が償却されます。これは、テーブルが時々 **サイズ変更**するためです (すべての要素を新しい大きなブロックにコピーします。そのステップは **Θ(n)** ですが、多くのプッシュにわたる平均が一定のままであることは十分にまれです)。

**`push(x)`** (配列バッキング) — インデックスに書き込みます **`size`**、 それから **`size++`**。トップが後ろにあるときは移動しません。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 124" role="img" aria-label="Array push writes at index size then increments size">
  <defs>
    <marker id="arr-push-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before push(7) — size = 2</text>
  <text x="18" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="54" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="90" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="126" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="14" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="54" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="64" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="94" y="52" width="36" height="28" rx="3" fill="rgba(96,165,250,0.15)" stroke="#60a5fa" stroke-dasharray="4 3"/>
  <text x="106" y="70" fill="#60a5fa" font-size="10" font-weight="600">?</text>
  <text x="132" y="70" fill="#60a5fa" font-size="9" font-weight="600">← index size</text>
  <path d="M168 66 H220" stroke="#60a5fa" stroke-width="2" marker-end="url(#arr-push-mk)"/>
  <text x="176" y="60" fill="#60a5fa" font-size="10" font-weight="600">write 7</text>
  <text x="232" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After — size = 3</text>
  <text x="240" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="276" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="312" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="348" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="236" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="248" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="276" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="286" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="316" y="52" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="328" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <text x="360" y="70" fill="#86efac" font-size="9" font-weight="600">← top (size−1)</text>
  <text x="10" y="108" fill="#71717a" font-size="9">Resize copies everything only when capacity is exceeded — usual push stays O(1) amortized.</text>
</svg></figure>

**`pop()`** (配列バッキング) — 読み取り **`arr[size - 1]`**、次に ** をデクリメントします`size`**;新しい上部の上のスロットは、上書きまたはクリアされるまで古い値を保持する可能性があります。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 118" role="img" aria-label="Array pop reads top index then decrements size">
  <defs>
    <marker id="arr-pop-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before pop() — size = 3</text>
  <text x="18" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="54" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="90" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <rect x="14" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="54" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="64" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="94" y="50" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="106" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <text x="138" y="68" fill="#86efac" font-size="9" font-weight="600">read &amp; return</text>
  <path d="M168 64 H220" stroke="#a1a1aa" stroke-width="2" marker-end="url(#arr-pop-mk)"/>
  <text x="176" y="58" fill="#fbbf24" font-size="10" font-weight="600">size−−</text>
  <text x="232" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After — size = 2</text>
  <text x="240" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="276" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="312" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <rect x="236" y="50" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="248" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="276" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="286" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="316" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.45)" stroke="#52525b" stroke-dasharray="3 3"/>
  <text x="326" y="68" fill="#71717a" font-size="9" font-family="ui-monospace">7?</text>
  <text x="360" y="68" fill="#71717a" font-size="9">stale / optional clear</text>
</svg></figure>

### Java: 拡張機能を備えた配列ベースのスタック

**トップ**、**`size - 1`**;次 **`push`**は**を書きます`data[size]`** それから **`size++`**。の上 **`pop`**、 戻る **`data[size - 1]`**、**`size--`**、 そして **`null`** 残したスロットから削除されるため、参照は保持されません (以下の「機密データ / GC」の説明と一致します)。

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.NoSuchElementException;
import java.util.Objects;

public class ArrayStack<E> {

  private Object[] data;
  private int size;

  public ArrayStack() {
    this.data = new Object[8];
  }

  public void push(E item) {
    Objects.requireNonNull(item, "item");
    if (size == data.length) {
      data = Arrays.copyOf(data, data.length * 2);
    }
    data[size++] = item;
  }

  @SuppressWarnings("unchecked")
  public E pop() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    int i = --size;
    E out = (E) data[i];
    data[i] = null;
    return out;
  }

  @SuppressWarnings("unchecked")
  public E peek() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    return (E) data[size - 1];
  }

  public boolean isEmpty() {
    return size == 0;
  }

  public int size() {
    return size;
  }

  /** Θ(n): null used slots so references are dropped (see clearing notes for array-backed stacks below). */
  public void clear() {
    Arrays.fill(data, 0, size, null);
    size = 0;
  }
}
```

### 配列ベースのスタックのクリア
- **のみ`size = 0`:** 高速ですが、古い参照が未使用のスロットに残っている可能性があります。 **Java** および同様のランタイムでは、参照が削除されるまでオブジェクトは**収集可能にならない可能性があります。これは**機密**データにとって問題です。  
- **すべての古いスロットを次のように設定します`null`:** 参照用に確保されていますが、**Θ(n)** はクリアされません。  
- **よくある妥協策:**`size = 0`**そして**、バッキング配列を**新しい空の配列**に置き換える(または縮小する)ことで、古いブロックが削除可能になります。 — **Θ(1)** 新しい配列参照の代入。 GC は、安全な場合に古いストレージを再利用します。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 108" role="img" aria-label="Array backed stack top at index size minus one">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Array backing — top at size − 1</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">push at index size · pop reads size−1 then size−−</text>
  <text x="20" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="56" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="92" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="128" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="16" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="86" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="56" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="66" y="86" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₁</text>
  <rect x="96" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="106" y="86" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₂</text>
  <rect x="136" y="68" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="148" y="86" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <text x="188" y="86" fill="#86efac" font-size="9" font-weight="600">← top (size−1)</text>
  <text x="188" y="62" fill="#60a5fa" font-size="9" font-weight="600">size = 4</text>
  <text x="260" y="86" fill="#71717a" font-size="9">next push at index 4</text>
</svg></figure>


## 4. Java:`Deque`、`ArrayDeque`、そしてその遺産`Stack`クラス

**コレクション フレームワーク** は、スタックを ** としてモデル化します。`Deque<E>`** (両端キュー) **一方の端のみ**で使用されます。好む **`Deque`** 古い ** に対する実装`java.util.Stack`** タイプ。

＃＃＃ 好む`Deque`+`ArrayDeque`スタック用

**`ArrayDeque<E>`** は **サイズ変更可能なリング バッファ** (これらのメモの循環キューのような): **`push`/`pop`/`peek`** は **O(1)** で償却され、ノードの **要素ごとのボックス化はありません** (リンクされたノードとは異なります)`Deque`から構築された`LinkedList`エントリ）。これは、**シングルスレッド** スタックまたはワーク キューの通常のデフォルトです。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
stack.push("a");       // same contract as addFirst
stack.push("b");
String top = stack.peek();   // "b" — empty deque ⇒ null (not an exception)
String out = stack.pop();    // "b" — empty ⇒ NoSuchElementException
```

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 218" role="img" aria-label="Java Deque stack methods operate at the front left to right">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Deque used as a stack — front = top (left → right is deque order)</text>
  <text x="10" y="36" fill="#a1a1aa" font-size="10">After push(&quot;a&quot;) then push(&quot;b&quot;)</text>
  <text x="10" y="56" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="48" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="102" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;b&quot;</text>
  <rect x="140" y="48" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="152" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <path d="M200 64 H248" stroke="#fbbf24" stroke-width="2" fill="none"/>
  <text x="208" y="58" fill="#fbbf24" font-size="10" font-weight="600">peek()</text>
  <text x="256" y="68" fill="#fbbf24" font-size="10" font-family="ui-monospace">→ &quot;b&quot;</text>
  <text x="10" y="104" fill="#a1a1aa" font-size="10">peek() leaves order unchanged</text>
  <text x="10" y="122" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="114" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="102" y="134" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;b&quot;</text>
  <rect x="140" y="114" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="152" y="134" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <path d="M200 130 H248" stroke="#a1a1aa" stroke-width="2" fill="none"/>
  <text x="208" y="124" fill="#fbbf24" font-size="10" font-weight="600">pop()</text>
  <text x="256" y="134" fill="#fbbf24" font-size="10" font-family="ui-monospace">→ &quot;b&quot;</text>
  <text x="10" y="170" fill="#a1a1aa" font-size="10">After pop() — only &quot;a&quot; remains at the front</text>
  <text x="10" y="188" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="180" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="100" y="200" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <text x="320" y="130" fill="#71717a" font-size="10">Same ADT as §1; API pins “top” to</text>
  <text x="320" y="144" fill="#71717a" font-size="10">the deque’s head, not index size−1.</text>
</svg></figure>

の上 **`Deque`**、**スタック**の名前付けマップは次のようになります (「`Deque`Javadoc): **`push(e)`** ≡ **`addFirst(e)`**、**`pop()`** ≡ **`removeFirst()`**、**`peek()`** ≡ **`peekFirst()`**。したがって、スタックの**先頭**は両端キューの**前**です。これは、§2の**ヘッドベース**の単一リンクスタックと同じ「一方の端で最新」の考え方であり、「後方」ではありません。`size−1`§3 の図 (どちらも有効な ADT 実現です。Java の API は、**前** を選択しただけです)`push`）。

### なぜ避けるのか`java.util.Stack`?

**`Stack`** 延長 **`Vector`** (Java 1.0 からの拡張可能な配列)。最新のコードの問題:

- **すべてのパブリック メソッドで同期** — 1 つのスレッドのみが使用する場合でもロックの料金が発生します。
- **`Stack`はインターフェイスではありません**。実装を交換したり、テストでモックしたりするのが困難です。
- デザインは**レガシー**です。ライブラリと **効果的な Java** スタイルのガイダンスでは次のように述べられています: **使用してください`Deque`**。

**スレッドセーフ** スタックが本当に必要な場合は、** を使用してください`ConcurrentLinkedDeque`** (ロックなし、無制限) または ** をラップする`Deque`** と **`Collections.synchronizedDeque`**、または **`BlockingDeque`** 生産者/消費者がブロックする必要がある場合 — ではない`Stack`。

###`peek`対`element`、`remove`対`poll`

**`Deque`** は ** を継承します`Queue`** 空** の動作がわずかに異なる ** メソッド:

|意図 |一般的なスタックの使用法 |空の場合`Deque`|
|--------|-------------------|--------|
| | を削除せずに先頭をお読みください。 **`peek()`** / **`peekFirst()`** | **を返します`null`** |
|トップを読む (より厳密) | **`element()`** |投げる**`NoSuchElementException`** |
|ポップ | **`pop()`** / **`removeFirst()`** |投げる**`NoSuchElementException`** |
|ポップに寛容 | **`pollFirst()`** | **を返します`null`** |

選ぶ **`peek`/`poll`** 空が正常な場合。使用 **`element`/`remove`** 空の場合はバグを意味します。

**空でも安全なポップ** (スタックがすでに空になっている場合は例外なし):

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
String topOrNull = stack.pollFirst(); // null if empty — same end as pop()
```

###`ArrayDeque`ルールと制限

- **`null`は許可されません** —`push(null)`投げる**`NullPointerException`**。 A**`LinkedList`** は ** として使用されます`Deque`** まだ受け入れられる可能性があります **`null`** 古いパターンですが、** が混在しています`null`** 要素に **`peek()`** は悪い考えです — **`peek()`** すでに返されています **`null`**両端キューが**空**の場合。
- **ランダムアクセスなし** —`ArrayDeque`**ではありません`List`**;インデックスを持つ配列のように扱わないでください。
- **イテレータの順序**は**前→後**です(左から右と同じ)`Deque`契約)、**「排出するまでポップ注文」を特別なモードとして使用することはできません**。純粋なスタックの場合のみ **`push`/`pop`/`peek`**片端から。

### JVM`StackOverflowError`(名前の衝突)

**`StackOverflowError`** は、**スレッドの呼び出しスタック** (入れ子になったメソッド呼び出しのアクティブ化フレーム) が深くなりすぎる場合 (基本ケースのない再帰、または非常に深いチェーン) にスローされます。 **とは**無関係**です`java.util.Stack`** コレクションタイプ; 「スタック」という単語のみが共有されます。

## 5. まとめ

| | **単一リンク (ヘッド = 上部)** | **配列 (後ろ = 上)** |
|-|----------------------------|----------------------|
| **プッシュ** | Θ(1) 先頭に追加 |償却されたΘ(1);レア Θ(n) サイズ変更 |
| **ポップ** | Θ(1) ヘッドを切り離す | Θ(1) で`size-1`|
| **ピーク/空/サイズ** | Θ(1) | Θ(1) |
| **クリア** | Θ(1)`head=null`(+ GC / 無料) | Θ(1) 参照を新しい空の配列にドロップするか、Θ(n) 個の null スロット |
| **おまけ** |尻尾は必要ありません |インデックス規律。機密データ ⇒ 古いスロットに注意 |

どちらも **同じスタック ADT** を実現します。 **割り当て許容度**、**キャッシュ動作**、**言語/ランタイム**の詳細 (参照のクリアなど) に基づいて選択します。 **Java** では ** を優先します`Deque<E>`** と **`ArrayDeque<E>`** デフォルトのスタック (§4);避ける **`java.util.Stack`**。
