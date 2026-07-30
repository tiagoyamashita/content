---
label: "IV"
subtitle: "Stack"
group: "Data structures & algorithms"
order: 4
---
Stack — two backing implementations
The **stack ADT** is defined by its **operations**, not by whether you use a list or an array underneath. This note compares two standard backings: a **singly linked list** (head = top) and a **dynamic array** (top at the logical back).

**Java baseline:** snippets assume **Java SE 22** — set the language level to **22** in your IDE or compile with **`javac --release 22`**. The features used here (generics, `var` only if added, `Deque`, etc.) also run on **JDK 21 LTS**; treat **22** as the minimum this material is checked against, and use an **LTS** JDK in production if your team requires it.

## 1. Stack as an ADT (recap)
**Operations** usually include `push(x)`, `pop()`, `peek()` / `top()`, `isEmpty()`, and often `size()` / `clear()`. **Invariant:** `pop` removes the **most recently pushed** item (LIFO).

A stack is **not** meant for arbitrary **index access**, **search**, or **insert/remove in the middle**. If you need those behaviors, model a **different** structure (e.g. deque, list, or array used as a sequence).

**Uses:** DFS, undo, bracket matching, postfix evaluation, call-stack intuition.


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

### Per-operation visuals (ADT)

**`push(x)`** — new element becomes the **top**; everything already on the stack stays **below** it.

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

**`peek()`** / **`top()`** — inspect the top **without** removing it; the drawing is **unchanged** after a peek.

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

**`pop()`** — remove and return the **current** top (the same cell **`peek`** would read).

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

**`isEmpty()`** — true when there is **no** top (nothing to `peek` or `pop`).

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

**`size()`** — logical count of elements **including** the top; this stack has **three** values total.

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

**`clear()`** — drop every element; afterward **`isEmpty()`** is true and **`size()`** is **`0`**.

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

### Example usage (Java)

The **library** type you usually want is **`Deque<E>`** with **`ArrayDeque<E>`** (covered later in this note under Java). Here is the same ADT vocabulary in a few lines:

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

**Balanced brackets** is a classic stack exercise: on an opening symbol, **`push`**; on a closing symbol, **`pop`** and check it pairs with what you popped; at end of string, **`isEmpty()`** must be **true**.

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


## 2. Singly linked list as backing
Treat the **head pointer as the top**. An **empty** stack is an empty list: `head == null`.

**Push:** allocate a new node, point it at the old head, assign `head` to the new node — **Θ(1)**.  
**Pop:** read `head`, advance `head` to `head.next`, return the old top’s value — **Θ(1)**.  
You **do not need a tail pointer**: every stack operation touches only the head.

**`push(x)`** (list backing) — new node’s **`next`** is the old head; **`head`** moves to the new node.

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

**`pop()`** (list backing) — save the head’s value, set **`head = head.next`**, return the saved value.

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

### Java: head-as-top stack (teaching class)

This mirrors the **prepend / delete-first** list operations from the linked-list note: **`head`** is the **top**; no tail pointer.

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

### Walkthrough (duplicate values)
Push values in order **1**, then **3** (first occurrence), then **3** (second occurrence), then **2**. When two nodes hold the same display value, label them **3⁽¹⁾** and **3⁽²⁾** in reasoning:

1. `push(1)` — head → `1`  
2. `push(3⁽¹⁾)` — head → `3⁽¹⁾` → `1`  
3. `push(3⁽²⁾)` — head → `3⁽²⁾` → `3⁽¹⁾` → `1` (head is the **second** three)  
4. `push(2)` — head → `2` → `3⁽²⁾` → `3⁽¹⁾` → `1`

In drawings, the **top** is often placed on the **left** and older nodes extend to the **right**; new pushes arrive at the head, so older elements appear “deeper” in the chain.

**Pop:** always detach the head (same as list delete-at-head). Example pops in order return **2**, then **3⁽²⁾**, then **3⁽¹⁾**, then **1**; after the fourth pop, `head` is **null** — stack empty.

**Clear:** set `head = null` — **Θ(1)** time; nodes become unreachable and a **GC** can reclaim them (in managed languages), or you free them explicitly in C/C++.

### Why not doubly linked?
A doubly linked list still supports stack ops, but each node stores an **extra pointer** (`prev`). Stacks never need backward traversal for correct behavior, so the **memory overhead** buys nothing you use.


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


## 3. Array (dynamic array) as backing
Track a **`size`** (logical element count). **Empty** stack: `size == 0`.

**Where is the top?** If you always **insert at index 0**, every push must **shift** all existing elements — **Θ(n)** per push. Instead, grow at the **back**: the **next push** writes at index **`size`**, then increment `size`. The **top** (for `peek` / `pop`) is at index **`size - 1`**.

### Same sequence on the array
Capacity large enough; start `size = 0`.

| Step | Action | Array indices (conceptual) | size after |
|------|--------|---------------------------|------------|
| — | empty | `[ · · · · ]` | 0 |
| 1 | push 1 | `[1, ·, ·, ·]` | 1 |
| 2 | push 3⁽¹⁾ | `[1, 3, ·, ·]` | 2 |
| 3 | push 3⁽²⁾ | `[1, 3, 3, ·]` | 3 |
| 4 | push 2 | `[1, 3, 3, 2]` | 4 |

**Pop:** read `arr[size - 1]`, then `size--` — **Θ(1)** (you may clear the slot for GC or security — see below).  
**Push:** **amortized Θ(1)** on a **dynamic array** because the table occasionally **resizes** (copy all elements to a new larger block — that step is **Θ(n)**, but rare enough that the average over many pushes stays constant).

**`push(x)`** (array backing) — write at index **`size`**, then **`size++`**. No shifting when the top stays at the back.

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

**`pop()`** (array backing) — read **`arr[size - 1]`**, then decrement **`size`**; the slot above the new top may still hold a stale value until overwritten or cleared.

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

### Java: array-backed stack with grow

**Top** at **`size - 1`**; next **`push`** writes **`data[size]`** then **`size++`**. On **`pop`**, return **`data[size - 1]`**, **`size--`**, and **`null`** out the slot you left so references are not retained (matches the “sensitive data / GC” discussion below).

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

### Clearing an array-backed stack
- **Only `size = 0`:** fast, but old references may still sit in unused slots; in **Java** and similar runtimes, objects may **not** become collectable until references are dropped — problematic for **sensitive** data.  
- **Set every old slot to `null`:** secure for references, but **Θ(n)** to clear.  
- **Common compromise:** `size = 0` **and** replace the backing array with a **fresh empty array** (or shrink) so the old block is droppable — **Θ(1)** assignment of a new array reference; GC reclaims the old storage when safe.


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


## 4. Java: `Deque`, `ArrayDeque`, and the legacy `Stack` class

The **collections framework** models a stack as a **`Deque<E>`** (double-ended queue) used at **one end only**. Prefer **`Deque`** implementations over the old **`java.util.Stack`** type.

### Prefer `Deque` + `ArrayDeque` for a stack

**`ArrayDeque<E>`** is a **resizable ring buffer** (like the circular queue in these notes): **`push` / `pop` / `peek`** are **amortized O(1)** with **no per-element boxing** of nodes (unlike a linked `Deque` built from `LinkedList` entries). It is the usual default for a **single-threaded** stack or work queue.

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

On **`Deque`**, the **stack** naming maps like this (see `Deque` Javadoc): **`push(e)`** ≡ **`addFirst(e)`**, **`pop()`** ≡ **`removeFirst()`**, **`peek()`** ≡ **`peekFirst()`**. So the **top** of the stack is the **front** of the deque — the same “newest at one end” idea as a **head-based** singly linked stack in §2, not the “back at `size−1`” picture in §3 (both are valid ADT realizations; Java’s API just picked the **front** for `push`).

### Why avoid `java.util.Stack`?

**`Stack`** extends **`Vector`** (a growable array from Java 1.0). Problems in modern code:

- **Synchronized on every public method** — you pay locking even when only one thread uses it.
- **`Stack` is not an interface** — harder to swap implementations or mock in tests.
- Design is **legacy**; the library and **Effective Java**–style guidance say: **use `Deque`**.

If you truly need a **thread-safe** stack, use **`ConcurrentLinkedDeque`** (lock-free, unbounded) or wrap a **`Deque`** with **`Collections.synchronizedDeque`**, or a **`BlockingDeque`** when producers/consumers must block — not `Stack`.

### `peek` vs `element`, `remove` vs `poll`

**`Deque`** inherits **`Queue`** methods with slightly different **empty** behavior:

| Intent | Typical stack use | On empty `Deque` |
|--------|-------------------|-------------------|
| Read top without removing | **`peek()`** / **`peekFirst()`** | returns **`null`** |
| Read top (stricter) | **`element()`** | throws **`NoSuchElementException`** |
| Pop | **`pop()`** / **`removeFirst()`** | throws **`NoSuchElementException`** |
| Pop tolerant | **`pollFirst()`** | returns **`null`** |

Choose **`peek` / `poll`** when emptiness is normal; use **`element` / `remove`** when empty means a bug.

**Empty-safe pop** (no exception when the stack might already be drained):

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
String topOrNull = stack.pollFirst(); // null if empty — same end as pop()
```

### `ArrayDeque` rules and limits

- **`null` is not allowed** — `push(null)` throws **`NullPointerException`**. A **`LinkedList`** used as a **`Deque`** may still accept **`null`** in older patterns, but mixing **`null`** elements with **`peek()`** is a bad idea — **`peek()`** already returns **`null`** when the deque is **empty**.
- **No random access** — `ArrayDeque` is not a **`List`**; do not treat it like an array with indices.
- **Iterator order** is **front → back** (same as left-to-right in the `Deque` contract), **not** “pop order until you drain it” as a special mode — for a pure stack you only **`push` / `pop` / `peek`** from one end.

### JVM `StackOverflowError` (name collision)

**`StackOverflowError`** is thrown when a **thread’s call stack** (activation frames for nested method calls) grows too deep — recursion with no base case, or very deep chains. It is **unrelated** to the **`java.util.Stack`** collection type; only the word “stack” is shared.

## 5. Summary

| | **Singly linked (head = top)** | **Array (back = top)** |
|--|-------------------------------|-------------------------|
| **push** | Θ(1) prepend | amortized Θ(1); rare Θ(n) resize |
| **pop** | Θ(1) detach head | Θ(1) at `size-1` |
| **peek / empty / size** | Θ(1) | Θ(1) |
| **clear** | Θ(1) `head=null` (+ GC / free) | Θ(1) drop ref to new empty array, or Θ(n) null slots |
| **Extra** | no tail needed | index discipline; sensitive data ⇒ mind stale slots |

Both realize the **same stack ADT**; choose based on **allocation tolerance**, **cache behavior**, and **language/runtime** details (e.g. reference clearing). In **Java**, prefer **`Deque<E>`** with **`ArrayDeque<E>`** for a default stack (§4); avoid **`java.util.Stack`**.
