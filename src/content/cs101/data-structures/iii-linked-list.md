---
label: "III"
subtitle: "Linked list"
group: "Data structures & algorithms"
order: 3
---
Linked list
Pointer-based sequence: singly and doubly linked.

**Singly linked:** each node holds `value` and `next`. The list is reached from a **head** pointer. Insert after a node you already hold: **O(1)**. Find the k-th element by walking: **O(k)**; search by value without index: **O(n)**.

**Doubly linked:** nodes add `prev`, so you can remove a node in **O(1)** when you hold its address, and walk backward without scanning from the head.

- **vs array:** lists win on **O(1) splice** at a known node; arrays win on **O(1) index** and sequential **cache** behavior.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 168" role="img" aria-label="Singly linked list and O(1) insert after a known node">
  <defs>
    <marker id="ds-ll-n" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Singly linked — walk with next</text>
  <text x="12" y="40" fill="#71717a" font-size="10">head → nodes; no index arithmetic</text>
  <text x="12" y="62" fill="#86efac" font-size="9" font-weight="600">head</text>
  <path d="M44 58 H68" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="72" y="44" width="64" height="36" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="88" y="66" fill="#e4e4e7" font-size="11">A</text>
  <path d="M138 62 H162" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="166" y="44" width="64" height="36" rx="6" fill="rgba(251,191,36,0.15)" stroke="#fbbf24" stroke-width="2"/>
  <text x="186" y="66" fill="#e4e4e7" font-size="11">B</text>
  <path d="M232 62 H256" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="260" y="44" width="64" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="280" y="66" fill="#e4e4e7" font-size="11">C</text>
  <path d="M326 62 H350" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <text x="358" y="66" fill="#71717a" font-size="11">null</text>
  <text x="12" y="108" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Insert N after B (you hold B)</text>
  <text x="12" y="126" fill="#a1a1aa" font-size="10">rewire: B.next → N, N.next → old B.next — no shifting of A or C in memory</text>
  <rect x="166" y="132" width="64" height="32" rx="6" fill="rgba(251,191,36,0.15)" stroke="#fbbf24" stroke-width="2"/>
  <text x="186" y="152" fill="#e4e4e7" font-size="11">B</text>
  <path d="M232 148 H248" stroke="#60a5fa" stroke-width="2" stroke-dasharray="4 2" marker-end="url(#ds-ll-n)"/>
  <rect x="252" y="132" width="64" height="32" rx="6" fill="rgba(96,165,250,0.2)" stroke="#60a5fa" stroke-width="2"/>
  <text x="272" y="152" fill="#e4e4e7" font-size="11">N</text>
  <path d="M318 148 H334" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="338" y="132" width="64" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="358" y="152" fill="#e4e4e7" font-size="11">C</text>
</svg></figure>

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 88" role="img" aria-label="Doubly linked list prev and next pointers">
  <defs>
    <marker id="ds-ll-df" markerWidth="7" markerHeight="7" refX="7" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#60a5fa"/></marker>
    <marker id="ds-ll-db" markerWidth="7" markerHeight="7" refX="0" refY="3.5" orient="auto"><path d="M7 0 L0 3.5 L7 7 Z" fill="#fbbf24"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-family="system-ui,sans-serif" font-weight="600">Doubly linked — O(1) cut-out with node pointer</text>
  <rect x="40" y="36" width="88" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="58" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <path d="M130 54 H146" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-ll-df)"/>
  <path d="M146 48 H130" stroke="#fbbf24" stroke-width="2" marker-end="url(#ds-ll-db)"/>
  <rect x="150" y="36" width="88" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <path d="M240 54 H256" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-ll-df)"/>
  <path d="M256 48 H240" stroke="#fbbf24" stroke-width="2" marker-end="url(#ds-ll-db)"/>
  <rect x="260" y="36" width="88" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="278" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <text x="12" y="82" fill="#71717a" font-size="9">rewire prev/next of neighbors — no scan from head</text>
</svg></figure>
