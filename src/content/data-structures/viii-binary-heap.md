---
label: "VIII"
subtitle: "Binary heap"
group: "Data structures & algorithms"
order: 8
---
Binary heap
Complete binary tree stored in an array: heap order + compact indices.

**Max-heap:** parent key ≥ both children; **min-heap:** parent ≤ both children. For 0-based index `i`: children at **`2i+1`**, **`2i+2`**; parent at **`⌊(i−1)/2⌋`**.

**Ops:** `insert` / `bubble-up` and `extract-min` or `extract-max` / `sink-down` run along tree height — **O(log n)**. **Peek** min/max: **O(1)**.

**buildHeap** on `n` items bottom-up: **O(n)** (not `n` separate inserts).

**Related:** **Heapsort** and **priority queues**; see **Level II** (`ii-trees-heaps-hashing.md`).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 248" role="img" aria-label="Max heap as tree and same keys in array level order">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Max-heap: parent ≥ children</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">complete tree → packed into array by level order; index formulas link parent/children</text>
  <circle cx="220" cy="68" r="20" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="210" y="74" fill="#e4e4e7" font-size="12" font-family="ui-monospace" font-weight="600">9</text>
  <line x1="204" y1="82" x2="160" y2="112" stroke="#71717a" stroke-width="2"/>
  <line x1="236" y1="82" x2="280" y2="112" stroke="#71717a" stroke-width="2"/>
  <circle cx="160" cy="126" r="18" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="152" y="132" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <circle cx="280" cy="126" r="18" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="272" y="132" fill="#e4e4e7" font-size="11" font-family="ui-monospace">8</text>
  <line x1="148" y1="138" x2="120" y2="158" stroke="#71717a" stroke-width="2"/>
  <line x1="172" y1="138" x2="200" y2="158" stroke="#71717a" stroke-width="2"/>
  <circle cx="120" cy="172" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="114" y="176" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3</text>
  <circle cx="200" cy="172" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="194" y="176" fill="#e4e4e7" font-size="10" font-family="ui-monospace">2</text>
  <text x="320" y="124" fill="#71717a" font-size="9">children of i:</text>
  <text x="320" y="138" fill="#86efac" font-size="9" font-family="ui-monospace">2i+1, 2i+2</text>
  <text x="12" y="206" fill="#a1a1aa" font-size="10" font-family="ui-monospace">array A (level order):</text>
  <rect x="140" y="214" width="36" height="24" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="148" y="230" fill="#e4e4e7" font-size="11" font-family="ui-monospace">9</text>
  <rect x="180" y="214" width="36" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="188" y="230" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <rect x="220" y="214" width="36" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="228" y="230" fill="#e4e4e7" font-size="11" font-family="ui-monospace">8</text>
  <rect x="260" y="214" width="36" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="268" y="230" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="300" y="214" width="36" height="24" rx="2" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="308" y="230" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <text x="344" y="230" fill="#71717a" font-size="9">indices 0…4</text>
</svg></figure>
