---
label: "X"
subtitle: "Hash table"
group: "Data structures & algorithms"
order: 10
---
Hash table
Map keys to table slots via a **hash function** `h(key)`; average-case **O(1)** lookup when load is reasonable.

**Collisions** are inevitable in a finite table. **Chaining:** each slot holds a list of entries sharing that hash; load factor **α = n/m** drives expected chain length. **Open addressing:** probe sequences (linear, quadratic, double hashing) place alternatives in the same array.

**Costs:** average **O(1)** insert/lookup/delete with a good hash and load control; worst case **Θ(n)** if all keys collide.

**Related:** **Level II** (`ii-trees-heaps-hashing.md`).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 168" role="img" aria-label="Hash function maps keys into buckets with collision chaining">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Chaining: same slot, many keys</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">h(key) mod m picks a bucket; collisions stored as a short linked list at that bucket</text>
  <text x="20" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 0</text>
  <text x="92" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 1</text>
  <text x="164" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 2</text>
  <text x="236" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 3</text>
  <rect x="16" y="84" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="88" y="84" width="56" height="28" rx="4" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <rect x="160" y="84" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="232" y="84" width="56" height="28" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <path d="M116 112 L116 130" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="100" y="132" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="108" y="147" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k1</text>
  <rect x="100" y="158" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="108" y="173" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k4</text>
  <path d="M260 112 L260 126" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="244" y="128" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="252" y="143" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k9</text>
  <text x="300" y="104" fill="#60a5fa" font-size="9">lookup: hash → scan chain</text>
  <path d="M340 44 L116 84" stroke="#60a5fa" stroke-width="1" stroke-dasharray="4 3" fill="none"/>
  <text x="344" y="42" fill="#60a5fa" font-size="9" font-family="ui-monospace">h(k4)=1</text>
</svg></figure>
