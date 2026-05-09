---
label: "V"
subtitle: "Queue"
group: "Data structures & algorithms"
order: 5
---
Queue (FIFO)
First-in, first-out at two ends: **enqueue** at the **back**, **dequeue** at the **front**.

**ADT:** the oldest waiting element leaves next; you cannot remove the newest without breaking FIFO semantics.

**Implementations:** **circular buffer** (fixed array, head/tail indices with wrap modulo capacity) — **O(1)** enqueue/dequeue without per-element allocation; or linked list with **head** and **tail** pointers.

**Uses:** BFS, job scheduling, buffering streams.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 140" role="img" aria-label="Queue dequeue at front removes oldest enqueue at back adds newest">
  <defs>
    <marker id="ds-q-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">FIFO — oldest at front leaves first</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">dequeue() removes front · enqueue() appends at back</text>
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
  <text x="44" y="96" fill="#a1a1aa" font-size="9">dequeue → a out</text>
  <path d="M320 100 H380" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-q-mk)"/>
  <text x="300" y="96" fill="#a1a1aa" font-size="9">enqueue ← new at back</text>
  <text x="12" y="128" fill="#71717a" font-size="10">linked head/tail or ring buffer — both ends O(1)</text>
</svg></figure>
