---
label: "IX"
subtitle: "Priority queue"
group: "Data structures & algorithms"
order: 9
---
Priority queue
Abstract type: insert items with priorities; repeatedly **extract** the highest (or lowest) priority.

**Typical ops:** `insert`, `extract-min` / `extract-max`, sometimes `decrease-key` (needed for **Dijkstra** with a heap), `merge`.

**Implementation:** **binary heap** gives **O(log n)** insert and extract, **O(1)** peek. Fibonacci heaps (theory) improve some amortized bounds for advanced graph algorithms.

**Related:** **Binary heap** in this submenu; **Level II** (`ii-trees-heaps-hashing.md`).

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
