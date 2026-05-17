---
label: "IX"
subtitle: "Priority queue"
group: "Data structures & algorithms"
order: 9
---
Priority queue — “who goes next?” by importance, not arrival time
A **priority queue** is an **abstract data type** for a collection where each item has a **priority** (often just a number or anything **comparable**). The defining behavior: you can **insert** in any order, but **extract** always removes the item with the **highest** or **lowest** priority among those still inside — **not** the oldest (that would be a **FIFO queue**) and **not** the newest (that would be a **stack**).

**Java baseline:** `PriorityQueue` snippets assume **Java SE 22** (`javac --release 22`). They use **`record`** and other features available since **Java 16**; they also run on **JDK 21 LTS**.

If you picture a **hospital triage** desk: arrivals are not served strictly first-come-first-served; the **most urgent** case jumps ahead. A normal **queue** is a single orderly line; a **priority queue** is “always serve whoever is currently most important.”


## 1. Queue vs stack vs priority queue (one minute)

| ADT | Who leaves on “remove best” or dequeue/pop? | Typical mental model |
|-----|-----------------------------------------------|----------------------|
| **Queue** | The **oldest** still waiting (**FIFO**) | Line at a shop |
| **Stack** | The **newest** still there (**LIFO**) | Pile of plates |
| **Priority queue** | The **smallest** or **largest** key still there (by your ordering rule) | Triage, CPU scheduling |

**Peek** (or **find-min** / **find-max**) reads that same “best” element **without** removing it. **Insert** adds something with its own priority; it does **not** have to sit at the “front” of anything — the structure keeps the invariant internally.


## 2. Operations (what APIs usually expose)

Names vary by language and textbook; mentally map them like this:

- **`insert(x)`** / **`add(x)`** / **`offer(x)`** — put `x` in the collection.
- **`extract-min()`** or **`extract-max()`** — remove and return the best element under the queue’s ordering. On an **empty** structure, behavior is either **error** or a **sentinel** value (Java’s `poll()` returns **`null`** for empty).
- **`peek-min()`** / **`peek-max()`** — return the best element **without** removing it (Java: **`peek()`**).
- **`isEmpty()`**, **`size()`** — usual bookkeeping.
- **`clear()`** — drop everything.

**Optional (advanced):** **`decrease-key`** / **`increase-key`** when you already have a **handle** to an item inside the structure and its priority changes — needed for a fast **Dijkstra** shortest-path implementation with a **binary heap** that can update priorities. The standard **`java.util.PriorityQueue`** does **not** support efficient decrease-key on arbitrary elements; for that you either use a **indexed heap** pattern, a **Fibonacci heap** in theory-heavy settings, or another graph library.

**Merge** (combine two priority queues) appears in some theoretic APIs; practical code often just inserts from one heap into another.


## 3. Min-heap vs max-heap (same idea, flipped order)

- **Min-priority queue:** “best” = **smallest** key. **Extract** = **extract-min**. Used for **Dijkstra** (smallest tentative distance first), **Prim** on graphs, **merging sorted streams** with a small heap of “current heads.”
- **Max-priority queue:** “best” = **largest** key. Used for “top **k**” style problems, **heapsort** descending, **Huffman**-style constructions where you repeatedly take the two **largest** (depending on formulation).

Implementation-wise, a **min-heap** is a complete binary tree where each parent is **≤** its children; a **max-heap** flips to **≥**. One implementation can do both by swapping the comparison or using a **reversed comparator** in Java.


## 4. Tie-breaking and “duplicate priorities”

If two items have the **same** numeric priority, the ADT often does **not** guarantee which one comes out first unless the implementation documents **FIFO stability** within equal keys (many heaps are **not** stable). If order among equals matters, common fixes:

- Pack a **secondary key** (e.g. `(priority, sequenceNumber)` with lexicographic comparison so older entries sort first among ties), or
- Store **unique ids** and break ties explicitly in a **`Comparator`**.


## 5. Implementations and time bounds

Naive ideas:

- **Unsorted array or list:** **insert** **O(1)** (append), but **extract-min** scans everything — **O(n)**.
- **Sorted array:** **extract-min** from one end **O(1)**, but **insert** may shift — **O(n)** in the worst case.

The usual sweet spot for a general mutable priority queue is a **binary heap** (see **Binary heap** in this submenu, `viii-binary-heap.md`): store a **complete binary tree** in an array, restore **heap order** after each insert (**bubble up** / **swim**) and after each extract (**sink down** / **sift**). Height is **O(log n)**, so:

| Operation | Binary heap (typical) |
|-----------|------------------------|
| **insert** | **O(log n)** |
| **peek** best | **O(1)** |
| **extract** best | **O(log n)** |
| **build** from **n** keys (bottom-up) | **O(n)** — better than **n** separate inserts |

**Fibonacci heaps** and friends improve some **amortized** bounds for specialized graph algorithms in theory; in day-to-day libraries you still see **binary heaps** first.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 212" role="img" aria-label="Min heap before extract min and after moving last leaf to root and sinking down">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">extract-min restores heap in O(log n)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">pop root (min), replace with last array element, compare with children and swap with smaller child until order holds</text>
  <text x="12" y="64" fill="#86efac" font-size="9" font-weight="600">min-heap before</text>
  <circle cx="100" cy="108" r="18" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="92" y="114" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <line x1="88" y1="120" x2="56" y2="148" stroke="#71717a" stroke-width="2"/>
  <line x1="112" y1="120" x2="144" y2="148" stroke="#71717a" stroke-width="2"/>
  <circle cx="56" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="50" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">4</text>
  <circle cx="144" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="138" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">6</text>
  <line x1="48" y1="168" x2="32" y2="188" stroke="#71717a" stroke-width="2"/>
  <circle cx="32" cy="196" r="11" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="199" fill="#e4e4e7" font-size="9" font-family="ui-monospace">9</text>
  <path d="M100 88 L100 76" stroke="#fbbf24" stroke-width="2"/>
  <text x="40" y="74" fill="#fbbf24" font-size="9" font-weight="600">return 2</text>
  <text x="220" y="64" fill="#60a5fa" font-size="9" font-weight="600">after sink-down</text>
  <circle cx="300" cy="108" r="18" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="292" y="114" fill="#e4e4e7" font-size="11" font-family="ui-monospace">4</text>
  <line x1="288" y1="120" x2="256" y2="148" stroke="#71717a" stroke-width="2"/>
  <line x1="312" y1="120" x2="344" y2="148" stroke="#71717a" stroke-width="2"/>
  <circle cx="256" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="250" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">9</text>
  <circle cx="344" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="338" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">6</text>
  <text x="220" y="188" fill="#71717a" font-size="9">root was 9 (last leaf); one swap with 4 yields valid min-heap</text>
</svg></figure>


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="FIFO queue front versus priority queue always smallest at root">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">FIFO queue — order fixed by arrival</text>
  <rect x="12" y="36" width="40" height="26" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="24" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">1</text>
  <rect x="56" y="36" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="68" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">5</text>
  <rect x="100" y="36" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="112" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3</text>
  <text x="12" y="78" fill="#71717a" font-size="9">dequeue always removes left (oldest), even if 3 is “smaller”</text>
  <text x="230" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Min priority queue — order by key</text>
  <circle cx="288" cy="48" r="16" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="282" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">1</text>
  <line x1="276" y1="58" x2="256" y2="78" stroke="#71717a" stroke-width="2"/>
  <line x1="300" y1="58" x2="320" y2="78" stroke="#71717a" stroke-width="2"/>
  <circle cx="256" cy="90" r="12" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="250" y="94" fill="#e4e4e7" font-size="9" font-family="ui-monospace">5</text>
  <circle cx="320" cy="90" r="12" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="314" y="94" fill="#e4e4e7" font-size="9" font-family="ui-monospace">3</text>
  <text x="230" y="112" fill="#71717a" font-size="9">extract-min always returns 1 while it remains — not insertion order</text>
</svg></figure>


## 6. Java `PriorityQueue`

**`java.util.PriorityQueue<E>`** is a **min-heap** when elements use **natural ordering** (`Comparable`), or a heap ordered by an explicit **`Comparator`**. It is **not thread-safe**. Iterator order is **not** “priority order”; use **`poll()`** in a loop to drain in sorted order.

**Min-heap of integers** (smallest `poll` first):

```java
// Compile: javac --release 22 …
import java.util.PriorityQueue;

PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(30);
pq.offer(10);
pq.offer(20);
pq.peek();  // 10
pq.poll();  // 10
pq.poll();  // 20
```

**Max-heap** (largest first): reverse the comparison.

```java
// Compile: javac --release 22 …
import java.util.Collections;
import java.util.PriorityQueue;

PriorityQueue<Integer> maxPq = new PriorityQueue<>(Collections.reverseOrder());
maxPq.offer(10);
maxPq.offer(30);
maxPq.peek();  // 30
```

**Custom type** (e.g. jobs with deadlines — **earlier deadline = higher priority** here as smaller integer wins):

```java
// Compile: javac --release 22 …
import java.util.Objects;
import java.util.PriorityQueue;

record Job(String name, int deadline) implements Comparable<Job> {
  Job {
    Objects.requireNonNull(name, "name");
  }

  @Override
  public int compareTo(Job o) {
    return Integer.compare(deadline, o.deadline);
  }
}

PriorityQueue<Job> jobs = new PriorityQueue<>();
jobs.offer(new Job("backup", 5));
jobs.offer(new Job("patch", 2));
jobs.poll();  // patch — deadline 2 first
```

(You can instead use a `class` with **`Comparable`** or pass **`Comparator.comparingInt(Job::deadline)`** to the **`PriorityQueue`** constructor — same ordering.)

**Empty-safe:** **`poll()`** and **`peek()`** return **`null`** when empty; **`remove()`** throws **`NoSuchElementException`**.

**Gotchas**

- **`null`** elements are **not** allowed.
- If you change a field that participates in ordering **after** inserting an object, the heap **does not** automatically reorder — you must **remove and re-insert**, or use a structure designed for **decrease-key**.
- Initial capacity is a **hint** only; the heap grows as needed.


## 7. Where priority queues appear

- **Graph algorithms:** **Dijkstra** (closest unvisited vertex first), **Prim** (cheapest edge to the growing tree), **A-star** (`A*`) search with a heuristic.
- **CPU / OS scheduling:** pick the next runnable process by priority (real schedulers add fairness, aging, etc.).
- **Discrete-event simulation:** next event is the one with the **minimum** simulated time.
- **Streaming “top k”:** keep a **size-k** max-heap while scanning values (see max-heap pattern above).
- **Merge k sorted lists / files:** one heap entry per list holding `(nextValue, listId)`; repeatedly **poll** smallest and advance that list.


## 8. Related notes

- **Binary heap** in this submenu (`viii-binary-heap.md`) — array layout, index formulas, **buildHeap**, **heapsort**.
- **Queue** (`v-queue.md`) — strict **FIFO**; no per-item priority unless you simulate it badly.
- **Level II** overview: `ii-trees-heaps-hashing.md` (if present in your curriculum track).

Once you are comfortable with “insert anywhere, always take best,” the heap note is the natural next step: it is the standard **machinery** behind this ADT.
