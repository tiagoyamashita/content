---
label: "IV"
subtitle: "Stack"
group: "Data structures & algorithms"
order: 4
---
Stack — two backing implementations
The **stack ADT** is defined by its **operations**, not by whether you use a list or an array underneath. This note compares two standard backings: a **singly linked list** (head = top) and a **dynamic array** (top at the logical back).

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


## 2. Singly linked list as backing
Treat the **head pointer as the top**. An **empty** stack is an empty list: `head == null`.

**Push:** allocate a new node, point it at the old head, assign `head` to the new node — **Θ(1)**.  
**Pop:** read `head`, advance `head` to `head.next`, return the old top’s value — **Θ(1)**.  
You **do not need a tail pointer**: every stack operation touches only the head.

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
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
stack.push("a");       // same contract as addFirst
stack.push("b");
String top = stack.peek();   // "b" — empty deque ⇒ null (not an exception)
String out = stack.pop();    // "b" — empty ⇒ NoSuchElementException
```

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
