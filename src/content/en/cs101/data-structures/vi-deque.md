---
label: "VI"
subtitle: "Deque"
group: "Data structures & algorithms"
order: 6
---
Deque (double-ended queue)
Insert and remove at **both** ends in **O(1)**.

A **deque** generalizes **stack** (one end) and **queue** (opposite ends only): you can push/pop at front **and** back depending on API naming (`push_front`, `push_back`, etc.).

**Implementations:** **doubly linked list**, or **circular array** with two indices moving toward each other with wrap.

**Uses:** sliding-window algorithms, work-stealing queues, palindrome checks with two pointers.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="Deque allows push and pop at both front and back ends">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Four O(1) end operations</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">stack = one end only · queue = opposite ends · deque = both</text>
  <text x="24" y="78" fill="#86efac" font-size="10" font-weight="600">front</text>
  <rect x="72" y="62" width="56" height="30" rx="4" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <rect x="134" y="62" width="56" height="30" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="196" y="62" width="56" height="30" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="258" y="62" width="56" height="30" rx="4" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="360" y="78" fill="#60a5fa" font-size="10" font-weight="600">back</text>
  <path d="M24 52 L68 62" stroke="#86efac" stroke-width="1.5"/>
  <path d="M24 100 L68 88" stroke="#86efac" stroke-width="1.5"/>
  <text x="8" y="56" fill="#86efac" font-size="8">push_front</text>
  <text x="8" y="104" fill="#86efac" font-size="8">pop_front</text>
  <path d="M400 52 L356 62" stroke="#60a5fa" stroke-width="1.5"/>
  <path d="M400 100 L356 88" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="332" y="56" fill="#60a5fa" font-size="8">push_back</text>
  <text x="336" y="104" fill="#60a5fa" font-size="8">pop_back</text>
  <text x="120" y="110" fill="#71717a" font-size="9">end cells highlighted — interior not exposed by the ADT</text>
</svg></figure>
