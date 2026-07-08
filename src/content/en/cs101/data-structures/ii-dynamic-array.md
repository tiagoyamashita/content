---
label: "II"
subtitle: "Dynamic array"
group: "Data structures & algorithms"
order: 2
---
Dynamic array (vector)
Growable contiguous buffer with efficient append.

### What happens in Java when you push to a fixed-size array or dynamic array?

#### Fixed-Size Array (`int[] arr = new int[4];`)

In Java, if you use a fixed-size array, the size is determined at creation and **cannot change**.  
- If you try to assign a value past the last valid index (e.g., `arr[4] = 42` for array of length 4), Java will throw an **`ArrayIndexOutOfBoundsException`** at runtime.
- There is **no automatic resizing, copying, or growing**. The array size is fixed, and you must manually create a new (larger) array and copy elements yourself if you want to "extend" it.

#### Dynamic Array (`ArrayList<E>`)

Java provides the `ArrayList<E>` class, which behaves as a dynamic array:
- When you call `add(e)` and the underlying array is *not* full (`size < capacity`), Java inserts the element at the next slot (**O(1)** time).
- If you call `add(e)` when the internal array *is* full (`size == capacity`), Java does the following:
  1. **Allocates** a new, larger internal array (by default, capacity grows by ~50% in Java 8+).
  2. **Copies** all existing elements into the new array.
  3. **Frees** the old array (for garbage collection).
  4. **Appends** the new element.
- The resizing and copying step is *expensive* (`O(n)` for n elements), but since it happens infrequently, average time per `add` remains **amortized O(1)**.

#### Edge Cases (Java)

- **Initial Capacity Zero:** If you create an `ArrayList` with no initial capacity and immediately add, the list must allocate storage on the first add.
- **Repeated Adds:** If you push many items in a short time, Java may reallocate and copy several times in succession depending on growth policy.
- **Maximum Array Size:** Java arrays have a maximum size (`Integer.MAX_VALUE`). Trying to grow past this throws an `OutOfMemoryError`.
- **Bulk Addition (`addAll`):** Adding many elements at once may trigger immediate resizing to fit all new items.

#### What *Doesn't* Happen (Java)

- For **fixed-size arrays**, pushing ("adding past capacity") never resizes—they throw exceptions.
- For `ArrayList`, Java handles resizes automatically, but at the cost of time and occasionally triggering a garbage collection pause because of large memory allocations.
- For custom policies (e.g., always resizing by +1 each add), the performance can degrade to quadratic — Java's default is more efficient.

---

- **Typical ops:** `get`/`set` at index (**O(1)**); `add` to end amortized **O(1)**; insert/remove in middle **O(n)** because of shifting.
- **Space:** Θ(n) for `n` elements; actual internal capacity may be more (due to resizing, typically between n and about 1.5n).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 132" role="img" aria-label="Dynamic array doubles capacity and copies elements when full">
  <defs>
    <marker id="ds-dyn-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">size = capacity → grow (ArrayList)</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">four slots full (capacity 4); next add allocates new block (e.g., capacity 6), copies, frees old</text>
  <text x="12" y="58" fill="#86efac" font-size="9" font-weight="600">before</text>
  <rect x="16" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="92" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="168" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="244" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <text x="12" y="108" fill="#60a5fa" font-size="9" font-weight="600">after</text>
  <rect x="16" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="68" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="120" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="172" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="224" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="276" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="328" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="380" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <path d="M280 76 L280 92" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-dyn-mk)"/>
  <text x="288" y="88" fill="#71717a" font-size="9">copy + spare room</text>
</svg></figure>
