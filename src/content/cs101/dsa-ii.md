---
label: "II"
subtitle: "Trees, heaps, hashing"
group: "Data structures & algorithms"
order: 2
---
Level II — Trees, heaps, hashing
BSTs, balancing, binary heaps, priority queues, hash tables.

## 1. Binary search trees (BST)
- In-order traversal of a BST visits keys in sorted order.
- Search / insert / delete: follow left/right from root; height determines cost.
- Balanced BST aim: height O(log n) so ops stay O(log n).
- Unbalanced insert order can degenerate to a chain → height Θ(n).
- Rank / select: augment nodes with subtree sizes if your curriculum covers order stats.

## 2. Balancing intuition (AVL, red-black)
- AVL: enforce |balance(child)| ≤ 1 via rotations after insert/delete.
- Rotations (left/right) preserve BST property; fix height imbalance locally.
- Red-black: color bits + rules (black height, no double red) keep height O(log n).
- Both give O(log n) search/insert/delete worst case; implement details differ.
On paper: trace a small tree; after insert, spot violation and one rotation.

## 3. Heaps (binary heap)
- Max-heap: parent ≥ children; min-heap: parent ≤ children.
- Store as array: index i → children 2i+1, 2i+2; parent ⌊(i-1)/2⌋.
- bubbleUp / sinkDown (heapify) after change — O(log n) along tree height.
- buildHeap from n items: O(n) using bottom-up sink (not n separate inserts).
- Heapsort: build max-heap, repeatedly extract max to end — O(n log n) worst case.

## 4. Priority queues
- abstract ops: insert, extract-min/max, sometimes decrease-key / merge.
- Binary heap: insert & extract O(log n); peek O(1).
- Decrease-key with indices → needed later for Dijkstra with heaps.
- Fibonacci heap (theory): better amortized bounds for some algorithms.

## 5. Hash tables — ideas
- Map keys → slots via hash function h(key); ideal O(1) average lookup.
- Collision: two keys map to same slot — unavoidable in finite table.
- Chaining: each slot is a list; simple; load α = n/m affects chain length.
- Open addressing: probe sequence (linear, quadratic, double hashing);
clustering matters; deletion needs tombstones or careful rehashing.
- Rehash when load factor crosses threshold (e.g. grow table, new hash).

## 6. Hash quality & universal hashing (overview)
- Bad hash → many collisions → linear scan behavior despite "hash" name.
- Universal family: random choice of h from family keeps expected collisions low.
- Crypto hashes ≠ minimal requirement for tables; speed vs distribution tradeoff.
- Strings: rolling hash used in Rabin-Karp pattern matching (related pattern).

## 7. Remember & rehearse
- Insert a sorted sequence into BST — draw resulting shape (skew).
- Given array, simulate buildHeap vs repeated insert heap complexity.
- Pick chaining vs open addressing for a scenario (memory, cache, deletion).
