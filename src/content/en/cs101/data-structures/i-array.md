---
label: "I"
subtitle: "Array"
group: "Data structures & algorithms"
order: 1
---
Array (static)
Contiguous indexed storage in the RAM model.

An **array** stores elements in consecutive memory words. In Java, when you declare an array, you must always specify its size explicitly (for example, `int[] arr = new int[5];`). There is **no default size** for arrays in Java—if you simply write `int[] arr;`, the variable `arr` just points to null and no array is actually allocated. You must use `new` and provide the exact length. Once created, a Java array's length cannot change.

Index `i` reaches `A[i]` in **O(1)** time in the standard RAM model because the address is `base + i × wordSize`.

- **Strengths:** random access, cache-friendly scans, simple layout.
- **Limits:** fixed length (static array); inserting in the middle requires shifting **O(n)** elements to keep indices dense.
- **Related:** see **Dynamic array** in this submenu for growable vectors; the full complexity and ADT context live in **Level II — Foundations** [Foundations](../iii-foundations.md).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 200" role="img" aria-label="Array index maps to contiguous memory; middle insert shifts elements right">
  <defs>
    <marker id="ds-arr-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">O(1) index access</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">base address + i × stride → element A[i]</text>
  <text x="32" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">0</text>
  <text x="92" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">1</text>
  <text x="152" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">2</text>
  <text x="212" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">3</text>
  <rect x="16" y="84" width="56" height="32" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <rect x="76" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <rect x="136" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <rect x="196" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="36" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">A</text>
  <text x="96" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">B</text>
  <text x="156" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">C</text>
  <text x="216" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">D</text>
  <path d="M124 100 L124 52" stroke="#86efac" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="132" y="48" fill="#86efac" font-size="10" font-weight="600">read A[1] in O(1)</text>
  <text x="12" y="138" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Middle insert → shift right</text>
  <text x="12" y="156" fill="#a1a1aa" font-size="10">insert X at index 1: every element from that slot moves one step</text>
  <rect x="16" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="76" y="164" width="56" height="28" rx="4" fill="rgba(251,191,36,0.25)" stroke="#fbbf24" stroke-width="2"/>
  <rect x="136" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="196" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="256" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="96" y="182" fill="#fbbf24" font-size="11" font-family="ui-monospace" font-weight="600">X</text>
  <text x="36" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">A</text>
  <text x="156" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">B</text>
  <text x="216" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">C</text>
  <text x="276" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">D</text>
  <path d="M200 178 H320" stroke="#86efac" stroke-width="1.5" marker-end="url(#ds-arr-mk)"/>
  <text x="300" y="172" fill="#71717a" font-size="9">Θ(n) worst case</text>
</svg></figure>
