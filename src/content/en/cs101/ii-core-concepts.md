---
label: "II"
subtitle: "Core concepts"
group: "CS101"
order: 1
---
Level II — Core concepts
Bits and bytes, how data sits in memory, and the memory hierarchy from CPU to disk.

## 1. Bit and byte
A **bit** (binary digit) is one symbol from `{0, 1}` — the smallest piece of information a digital machine distinguishes. All richer data (numbers, text, images, instructions) is ultimately encoded as long bit patterns.

A **byte** is a fixed group of **8 bits** (one **octet**). Most modern systems **address memory in bytes**: each byte in RAM has an integer **address** (0, 1, 2, …). Wider values span several consecutive bytes; the **width** of a type (e.g. 32-bit integer = 4 bytes) tells you how many byte slots it occupies.

- **Why 8?** Historical convergence; today “byte = 8 bits” is the default mental model.
- **Larger chunks:** processors also move data in **cache lines** and **pages** (see hierarchy below), still built from bytes underneath.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" role="img" aria-label="One byte as eight bits with index order">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">One byte = 8 bits (example pattern)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">bit index 7 (often MSB of the byte) … 0 (often LSB) — convention depends on context</text>
  <g font-family="ui-monospace" font-size="11">
    <rect x="24" y="56" width="40" height="36" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
    <text x="36" y="78" fill="#e4e4e7">1</text>
    <text x="34" y="94" fill="#71717a" font-size="8">b7</text>
    <rect x="68" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="80" y="78" fill="#e4e4e7">0</text>
    <rect x="112" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="124" y="78" fill="#e4e4e7">1</text>
    <rect x="156" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="168" y="78" fill="#e4e4e7">0</text>
    <rect x="200" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="212" y="78" fill="#e4e4e7">0</text>
    <rect x="244" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="256" y="78" fill="#e4e4e7">1</text>
    <rect x="288" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="300" y="78" fill="#e4e4e7">1</text>
    <rect x="332" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="344" y="78" fill="#e4e4e7">0</text>
    <text x="376" y="78" fill="#71717a" font-size="9">= 8 bits</text>
  </g>
  <text x="12" y="112" fill="#71717a" font-size="9">256 possible values per byte (2⁸); multi-byte integers use several bytes in a defined order (endianness).</text>
</svg></figure>


## 2. Rough picture: storing and retrieving data
**Store:** the CPU (or device) places a bit pattern into a set of byte addresses — for example a store instruction writes 4 bytes of a 32-bit integer starting at address `p`. The hardware maps that **physical address** to a RAM chip location (and, with **virtual memory**, through translation tables so each process can have its own address space).

**Retrieve:** a **load** uses the same address (or a cache line that already contains that address) to copy bits into a CPU **register** where arithmetic runs. If the data is not in registers or cache, the memory subsystem fetches from **RAM**; if it is only on **disk**, the OS brings a **page** into RAM first (much slower).

- **Addresses vs values:** an address is *where*; the contents are *what*. Pointers in high-level languages are usually addresses (or abstractions over them).
- **Alignment:** some CPUs prefer (or require) multi-byte values to start at addresses divisible by 4 or 8 for fast access.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 168" role="img" aria-label="CPU load and store to byte addressed RAM">
  <defs>
    <marker id="cc-bus-mk" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Load / store path (simplified)</text>
  <rect x="32" y="44" width="100" height="52" rx="8" fill="rgba(34,197,94,0.12)" stroke="#86efac" stroke-width="2"/>
  <text x="48" y="68" fill="#e4e4e7" font-size="11">CPU</text>
  <text x="40" y="86" fill="#a1a1aa" font-size="9">regs · ALU</text>
  <path d="M136 70 H200" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-bus-mk)"/>
  <text x="148" y="64" fill="#71717a" font-size="8">address + data</text>
  <rect x="204" y="40" width="88" height="60" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="220" y="62" fill="#e4e4e7" font-size="10">memory</text>
  <text x="212" y="78" fill="#a1a1aa" font-size="8">controller</text>
  <text x="212" y="92" fill="#71717a" font-size="8">cache · MMU</text>
  <path d="M296 70 H360" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-bus-mk)"/>
  <rect x="364" y="48" width="64" height="44" rx="6" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="376" y="74" fill="#e4e4e7" font-size="10">RAM</text>
  <text x="12" y="128" fill="#a1a1aa" font-size="10">Store: CPU sends address + value → bytes updated. Load: CPU sends address → bytes returned (often via a cache line fill).</text>
  <text x="12" y="148" fill="#71717a" font-size="9">Caches and TLBs sit between CPU and RAM; OS + disk handle data not resident in physical RAM.</text>
</svg></figure>


## 3. Memory layers (hierarchy)
Memory is not one flat speed; it is a **hierarchy** trading **capacity**, **latency**, and **cost**. Fast layers are small; large layers are slower.

| Layer | Role (rough) |
|--------|----------------|
| **CPU registers** | Fastest storage; operands live here during execution. |
| **L1 / L2 / L3 cache** | SRAM very close to cores; holds recently used **cache lines** (copies of RAM fragments) to hide RAM latency. |
| **RAM (main memory)** | DRAM: large working set for running programs; **volatile** (lost on power loss). |
| **Disk / SSD** | Persistent, much larger, **much slower** random access; OS pages data in when needed. |

**Locality:** **temporal** locality = reuse soon; **spatial** locality = use neighboring addresses soon. Good locality keeps the hot data in registers and cache.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" role="img" aria-label="Memory hierarchy pyramid from fast small registers to slow large disk">
  <text x="100" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Memory hierarchy (fast ↑ small, slow ↓ large)</text>
  <polygon points="200,40 280,72 120,72" fill="rgba(34,197,94,0.35)" stroke="#86efac" stroke-width="2"/>
  <text x="168" y="62" fill="#e4e4e7" font-size="10" font-weight="600">registers</text>
  <polygon points="120,76 280,76 300,118 100,118" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="154" y="102" fill="#e4e4e7" font-size="10">L1 / L2 / L3 cache</text>
  <polygon points="100,122 300,122 320,168 80,168" fill="rgba(96,165,250,0.15)" stroke="#60a5fa"/>
  <text x="168" y="148" fill="#e4e4e7" font-size="10">RAM (DRAM)</text>
  <polygon points="80,172 320,172 340,210 60,210" fill="rgba(113,113,122,0.4)" stroke="#71717a"/>
  <text x="150" y="196" fill="#e4e4e7" font-size="10">SSD / disk (persistent)</text>
  <text x="12" y="218" fill="#71717a" font-size="9">misses in a faster layer pull lines from the next slower layer; page faults go to disk.</text>
</svg></figure>


## 4. Virtual memory (one paragraph)
Processes usually see **virtual addresses**; the **MMU** maps them to **physical** RAM frames. That gives isolation (process A cannot touch B’s memory by mistake) and allows **overcommit** (total virtual size can exceed RAM while only active pages sit in physical memory). A **page fault** means the needed page is not in RAM — the OS loads it from disk and resumes your instruction.

## 5. Remember & rehearse
- How many bits in a byte? How many distinct values can one byte represent?
- In one sentence: what is the difference between an **address** and the **contents** at that address?
- Order the layers from smallest/fastest to largest/slowest for a typical laptop.
