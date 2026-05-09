---
label: "II"
subtitle: "Dynamic array"
group: "Data structures & algorithms"
order: 2
---
Dynamic array (vector)
Growable contiguous buffer with amortized append.

A **dynamic array** keeps `length` (logical size) and `capacity` (allocated slots). When `length == capacity`, it allocates a larger block (often **double** capacity), **copies** old elements, and frees the old block. A single append can cost **O(n)**, but over many inserts the average cost per append is **O(1)** **amortized**.

- **Typical ops:** `get`/`set` at index **O(1)**; `push_back` amortized **O(1)**; insert/erase at interior **O(n)** due to shifting.
- **Space:** Θ(n) for `n` elements; capacity is typically between n and about 2n after doubling policies.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 132" role="img" aria-label="Dynamic array doubles capacity and copies elements when full">
  <defs>
    <marker id="ds-dyn-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">length = capacity → grow</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">four slots full (capacity 4); next push allocates new block (e.g. cap 8), copies, frees old</text>
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
