---
label: "V"
subtitle: "Queue"
group: "Data structures & algorithms"
order: 5
---
Queue — FIFO linear ADT
A **queue** is a **linear abstract data type**, like a **stack**, but it follows **first-in, first-out (FIFO)**: the **first** element **enqueued** is the **first** **dequeued**. Stacks use **last-in, first-out (LIFO)** — the newest leaves first.

**Java baseline:** snippets assume **Java SE 22** (`javac --release 22`). They also run on **JDK 21 LTS**. In the JDK, use **`Queue<E>`** / **`Deque<E>`** with **`ArrayDeque<E>`** for a typical FIFO queue (see examples below).

## 1. Queue as an ADT
The queue is defined by **operations**, not by whether you use a linked list or an array underneath.

**Core operations** (like **stacks**, queues almost always expose **`size()`**: **Θ(1)** via a counter on enqueue/dequeue, or from head/tail indices on a ring buffer.)

- **`enqueue(x)`** — typically **void**; accepts a data element and attaches it at the **back** of the queue.
- **`dequeue()`** — takes **no argument** and **cannot** name *which* element to remove. The contract is always: remove and return the element at the **front** — i.e. whoever was **enqueued first** among those still present. (If `1` was the first value enqueued, the **first** `dequeue()` removes `1`; you still call **`dequeue()`**, not “dequeue 1”.)
- **`peek()`** / **`front()`** — returns the front element **without** removing it (some APIs reuse “peek/top” wording from stacks).
- **`isEmpty()`** — true if the queue has no elements (often `size == 0` or **`front == null`** on a linked backing).
- **`clear()`** — empties the queue (with a linked list, dropping **`front`** may be enough in **GC** languages so unreachable nodes are reclaimed; some APIs also walk and null links explicitly).
- **`size()`** — returns how many elements are stored (same role as on a stack ADT).

**What queues are not for**  
Queues are **not** designed for **random index access**, **search**, or **insert/remove in the middle**. For that, use another structure (list, deque, array as a sequence).

**Real-life intuition**  
A **pipe** carries fluid in order: enter one end, exit the other. **Lines** and **wait lists**: first customer to arrive is first served. **Software:** print **job queues**, **ticket-purchase** waiting rooms, **BFS** in graphs, stream buffers.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 140" role="img" aria-label="Queue dequeue at front removes oldest enqueue at back adds newest">
  <defs>
    <marker id="ds-q-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">FIFO — oldest at front leaves first</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">dequeue() — no argument; FIFO picks the front · enqueue() appends at back</text>
  <text x="20" y="72" fill="#86efac" font-size="9" font-weight="600">front</text>
  <rect x="60" y="56" width="52" height="28" rx="4" fill="rgba(34,197,94,0.22)" stroke="#86efac" stroke-width="2"/>
  <rect x="118" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="176" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="234" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="300" y="72" fill="#60a5fa" font-size="9" font-weight="600">back</text>
  <text x="72" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">a</text>
  <text x="130" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">b</text>
  <text x="188" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">c</text>
  <text x="246" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">d</text>
  <path d="M40 100 H100" stroke="#86efac" stroke-width="2" marker-end="url(#ds-q-mk)"/>
  <text x="44" y="96" fill="#a1a1aa" font-size="9">dequeue</text>
  <path d="M320 100 H380" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-q-mk)"/>
  <text x="300" y="96" fill="#a1a1aa" font-size="9">enqueue ← new at back</text>
  <text x="12" y="128" fill="#71717a" font-size="10">Arrow at front illustrates one dequeue — FIFO decides it is the front cell, not a parameter.</text>
</svg></figure>

### Example usage (Java)

**`ArrayDeque`** implements **`Deque`**, which extends **`Queue`**. For FIFO, enqueue at the **back** and dequeue from the **front**:

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Queue;

Queue<String> queue = new ArrayDeque<>();
queue.offer("first");   // enqueue at back
queue.offer("second");
queue.peek();           // "first" — front unchanged
queue.poll();           // "first" — dequeue from front
queue.poll();           // "second"
queue.isEmpty();        // true
```

**BFS** (breadth-first search) is the classic queue algorithm: visit a node, then enqueue all unvisited neighbors; **`poll`** always takes the **oldest** frontier cell.

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public final class BfsExamples {

  private BfsExamples() {}

  /** Returns visit order for an undirected graph given as adjacency lists. */
  public static List<Integer> bfsOrder(List<List<Integer>> adj, int start) {
    int n = adj.size();
    boolean[] seen = new boolean[n];
    Queue<Integer> q = new ArrayDeque<>();
    List<Integer> order = new ArrayList<>();

    seen[start] = true;
    q.offer(start);

    while (!q.isEmpty()) {
      int v = q.poll();
      order.add(v);
      for (int w : adj.get(v)) {
        if (!seen[w]) {
          seen[w] = true;
          q.offer(w);
        }
      }
    }
    return order;
  }
}
```


## 2. Singly linked list as backing (head + tail)
Because work happens at **two different ends**, a singly linked queue almost always keeps **`front`** (head) **and** **`tail`** pointers.

**Which end for which operation?** (singly linked costs)

| add at | remove at | add cost | remove cost | queue-shaped? |
|--------|-----------|----------|-------------|----------------|
| head | head | Θ(1) | Θ(1) | both same end → **stack**, not FIFO between ends |
| tail | tail | Θ(1) | **Θ(n)** | need predecessor to cut tail |
| head | tail | Θ(1) | **Θ(n)** | tail delete without `prev` |
| **tail** | **head** | **Θ(1)** | **Θ(1)** | **enqueue at tail, dequeue at head** ✓ |

So: **`enqueue` at the `tail`**, **`dequeue` at the `front`**. Both **Θ(1)** with only a **singly** linked list.

**Enqueue (e.g. value 5):** allocate node, link old `tail.next` to the new node, advance **`tail`** to the new node; if the queue was empty, set **`front`** and **`tail`** to that node.

**Dequeue:** copy data from `front`, set **`front = front.next`**; if the queue becomes empty, set **`tail = null`**; optionally clear the old node’s `next` to **null** so it is detached.

**Example queue content** `1 → 3 → 3 → 2` from front to back (FIFO order of service). **`enqueue(5)`:** append after `2` at the tail and move **`tail`** to `5`. After that, a single **`dequeue()`** removes **whatever is at the front** — still **`1`**, because it was the first enqueued; the operation is not written as “dequeue the 1.”

### Why not doubly linked?
A **doubly** linked list can implement the same operations, but each node carries an **extra pointer** (`prev`). A singly linked queue with **head + tail** already gives **Θ(1)** enqueue and dequeue, so the extra memory usually **is not worth it** unless you need **Θ(1)** deletes at the back as well (then consider a **deque**).


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 118" role="img" aria-label="Singly linked queue with front head and tail for enqueue and dequeue">
  <defs>
    <marker id="ds-qll-ar" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Singly linked queue — front &amp; tail</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">enqueue links past old tail · dequeue advances front</text>
  <text x="8" y="72" fill="#86efac" font-size="9" font-weight="600">front</text>
  <path d="M44 68 H58" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="62" y="54" width="44" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="76" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M108 70 H122" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="126" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="140" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <path d="M172 70 H186" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="190" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="204" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <path d="M236 70 H250" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="254" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="268" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M300 70 H314" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <text x="322" y="74" fill="#71717a" font-size="10">…</text>
  <text x="360" y="72" fill="#60a5fa" font-size="9" font-weight="600">tail</text>
  <path d="M348 78 L320 78" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="12" y="106" fill="#71717a" font-size="9">new enqueue attaches after tail; dequeue only rewires front</text>
</svg></figure>

### Java: singly linked FIFO queue (teaching class)

**`enqueue`** at **`tail`**, **`dequeue`** at **`front`** — matches §2.

```java
// Compile: javac --release 22 …
import java.util.NoSuchElementException;
import java.util.Objects;

public class LinkedQueue<E> {

  private static final class Node<E> {
    final E item;
    Node<E> next;

    Node(E item) {
      this.item = item;
    }
  }

  private Node<E> front;
  private Node<E> tail;
  private int size;

  public void enqueue(E item) {
    Objects.requireNonNull(item, "item");
    Node<E> node = new Node<>(item);
    if (tail == null) {
      front = tail = node;
    } else {
      tail.next = node;
      tail = node;
    }
    size++;
  }

  public E dequeue() {
    if (front == null) {
      throw new NoSuchElementException();
    }
    E out = front.item;
    front = front.next;
    if (front == null) {
      tail = null;
    }
    size--;
    return out;
  }

  public E peek() {
    if (front == null) {
      throw new NoSuchElementException();
    }
    return front.item;
  }

  public boolean isEmpty() {
    return front == null;
  }

  public int size() {
    return size;
  }

  public void clear() {
    front = null;
    tail = null;
    size = 0;
  }
}
```


## 3. Array-backed queue: circular (wrap-around) buffer
This is the **second** standard backing (after §2’s linked list). The goal is the same **FIFO** contract: **enqueue at the back**, **dequeue from the front** — but a **plain contiguous array** makes the **front** expensive if you always delete index `0` and **shift** everything left (**Θ(n)** per dequeue). To **avoid shifting entirely**, use a **fixed-capacity ring buffer** (also called a **circular** or **wrap-around** array): indices **reuse** after they reach the end of the physical array by taking indices **modulo `capacity`**.

This is **not** the same structure as a **circular linked list** (that is pointer topology); here nothing “cycles” in memory — only the **index arithmetic** wraps.

**Why not a naive “array list at the front”?**  
Some language library lists expose **O(n)** shifts when you repeatedly remove from index 0. A ring buffer queue keeps **logical** front/back in **Θ(1)** without moving stored elements.

### State you must track
- **`capacity`** — length of the backing array (slots `0 … capacity−1`).
- **`size`** — how many elements are **currently** in the queue (`0 … capacity` depending on full policy).
- **`front`** — index of the **first** element (next to dequeue).
- **`back`** — index of the **next empty slot** where the next **enqueue** will write (common convention in this lesson). Then **`back == (front + size) % capacity`** whenever the queue is not in an ambiguous “full” edge case; **do not assume** `back == size` in general once **`front`** has moved.

**Enqueue:** write `data` at `arr[back]`; `back = (back + 1) % capacity`; `size++`.  
**Dequeue:** read `arr[front]`; `front = (front + 1) % capacity`; `size--`; **`back` does not move** on dequeue in this model.

### Walkthrough: `RAMBLIN` then dequeues, then `WR` (capacity **7**, ignore resize)
Start **empty:** `size = 0`, `front = 0`, `back = 0`.

**Enqueues** `R, A, M, B, L, I, N` (the letters of **ramblin**, length **7**): after each enqueue, **`front` stays 0** while **`back`** advances `1, 2, …`. After seven inserts, `size = 7`. The naive next `back` would be `7` (out of range); **wrap:** `back = 7 % 7 = 0`. Indices always use **`% capacity`** when they step past the last slot.

**Four `dequeue()` calls** remove `R`, `A`, `M`, `B` in order: each time **`size`** decrements and **`front`** advances (`1`, `2`, `3`, `4`) with **`back` unchanged** at `0` in this stretch.

**Enqueue `W`:** the next free slot is index **`0`** again — **wrap-around** for **`back`**. Write `W` there, `size` becomes `4`, **`back`** becomes `1`, **`front`** still **`4`** (the logical queue lives in the middle of the ring).

**Enqueue `R`:** place at index `1`, `size = 5`, `back = 2`, `front = 4`.

When **`dequeue`** later walks **`front`** toward the end of the array, it also uses **`(front + 1) % capacity`** so **`front`** wraps the same way.

### Complexity (summary)
| Operation | Time | Notes |
|-----------|------|--------|
| `enqueue` / `dequeue` / `peek` / `isEmpty` / `size` / `clear` (reset indices) | **Θ(1)** | no shifting; index wrap only |
| Grow **capacity** (resize) | **Θ(n)** | copy all slots to a new array; **enqueue** stays **amortized Θ(1)** if you double like a dynamic array |

Linked list backing: **no resize** in the array sense — “growth” is **Θ(1)** new nodes. Ring buffer: **resize** is the expensive rare step.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Circular buffer indices wrap with modulo capacity">
  <defs>
    <marker id="ds-qcb-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Ring buffer — same physical array, wrapping indices</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">capacity = 7 → valid indices 0…6; after index 6, next is (i+1) mod 7</text>
  <rect x="20" y="52" width="40" height="26" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <rect x="64" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="108" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="152" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="196" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="240" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="284" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="32" y="70" fill="#e4e4e7" font-size="10" font-family="ui-monospace">0</text>
  <text x="76" y="70" fill="#71717a" font-size="10">…</text>
  <text x="120" y="70" fill="#71717a" font-size="10">…</text>
  <text x="164" y="70" fill="#71717a" font-size="10">…</text>
  <text x="208" y="70" fill="#71717a" font-size="10">…</text>
  <text x="252" y="70" fill="#71717a" font-size="10">…</text>
  <text x="296" y="70" fill="#71717a" font-size="10">6</text>
  <path d="M328 64 H380" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-qcb-mk)"/>
  <path d="M380 64 Q396 64 396 50 Q396 36 380 36 Q364 36 364 50" stroke="#a1a1aa" stroke-width="1.5" fill="none"/>
  <path d="M364 50 H24" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-qcb-mk)"/>
  <text x="12" y="112" fill="#71717a" font-size="9">front / back / size track the logical queue inside the ring — see also i-foundations.md</text>
</svg></figure>


See **Level I — Foundations** (`i-foundations.md`) for another circular-buffer diagram with head/tail labels.

### Java: ring-buffer queue with grow

**`back`** is the **next write index**; **`front`** is the next dequeue index; both wrap with **`% capacity`**. On **`dequeue`**, **`back` does not move** (this lesson’s model).

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.NoSuchElementException;
import java.util.Objects;

public class ArrayRingQueue<E> {

  private Object[] data;
  private int front;
  private int back;
  private int size;

  public ArrayRingQueue() {
    this.data = new Object[8];
  }

  private int capacity() {
    return data.length;
  }

  public void enqueue(E item) {
    Objects.requireNonNull(item, "item");
    if (size == capacity()) {
      grow();
    }
    data[back] = item;
    back = (back + 1) % capacity();
    size++;
  }

  @SuppressWarnings("unchecked")
  public E dequeue() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    E out = (E) data[front];
    data[front] = null;
    front = (front + 1) % capacity();
    size--;
    return out;
  }

  @SuppressWarnings("unchecked")
  public E peek() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    return (E) data[front];
  }

  public boolean isEmpty() {
    return size == 0;
  }

  public int size() {
    return size;
  }

  public void clear() {
    Arrays.fill(data, null);
    front = 0;
    back = 0;
    size = 0;
  }

  /** Copy logical order into a larger ring; reset indices to 0..size-1. */
  private void grow() {
    Object[] next = new Object[capacity() * 2];
    for (int i = 0; i < size; i++) {
      next[i] = data[(front + i) % capacity()];
    }
    data = next;
    front = 0;
    back = size;
  }
}
```

### Java: `Queue` vs `ArrayDeque` vs `LinkedList`

| API | FIFO queue use | Notes |
|-----|----------------|-------|
| **`Queue.offer` / `poll` / `peek`** | **`ArrayDeque`** as implementation | **`offer`** = enqueue back, **`poll`** = dequeue front |
| **`Deque.addLast` / `removeFirst`** | Same ends as above | Explicit names for back/front |
| **`LinkedList`** | Implements **`Deque`** | **Θ(1)** at both ends, but **more memory** per element than **`ArrayDeque`** |

**Do not** use **`ArrayList`** as a queue if you **`remove(0)`** on every dequeue — that shifts the whole array (**Θ(n)** per dequeue). **`ArrayDeque`** is the usual JDK choice.

**Empty-safe dequeue:** **`poll()`** returns **`null`** when empty; **`remove()`** throws **`NoSuchElementException`**.

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Queue;

Queue<Integer> q = new ArrayDeque<>();
q.offer(1);
Integer x = q.poll();  // 1
Integer y = q.poll();  // null — queue empty
```

## 4. Summary

| Topic | Detail |
|--------|--------|
| **Rule** | FIFO — first enqueued, first dequeued |
| **Singly linked** | **`front`** (head) + **`tail`**; enqueue **tail**, dequeue **head** — Θ(1); **`size`**, **`isEmpty`**, **`clear`** Θ(1); “resize” = new node Θ(1) |
| **Ring buffer array** | **`capacity`**, **`size`**, **`front`**, **`back`**; wrap with **`% capacity`**; enqueue/dequeue/peek/empty/size/clear (index reset) **Θ(1)**; **enqueue amortized Θ(1)**; **resize copy Θ(n)** |
| **Doubly linked** | Works, but extra `prev` per node — usually skipped for a plain queue |
| **Not supported** | Random index, search, interior insert/remove — use another ADT |
| **Java default** | **`Queue<E>`** with **`ArrayDeque<E>`** — **`offer` / `poll` / `peek`** |
