---
label: "I"
subtitle: "Core concepts"
group: "Data structures & algorithms"
order: 1
---
Level I — Core concepts
Binary and bit widths, how data is sized in memory, how different storage layers behave, instruction sets (ISAs), queues on the memory path, and the hierarchy from CPU to disk.

## 1. Bits, binary, sizes, and instruction sets

### Binary and bits
Digital hardware works in **base 2**. Reading a bit string from **right to left**, each position is worth twice the previous: for `1011` the rightmost bit is worth 1, then 2, then 4, then 8 — here that sums to **11** in decimal. **Unsigned** *n*-bit integers can represent **2ⁿ** distinct values, usually mapped to **0 … 2ⁿ−1**. **Signed** integers in modern machines almost always use **two’s complement** in the same *n* bits.

A **bit** is one digit from `{0, 1}`. All data (numbers, text, images, **machine instructions**) is ultimately bit patterns; the **meaning** comes from **encoding rules** (ASCII, IEEE floats, ELF/PE binaries, …).

### Bytes and common widths
A **byte** is **8 bits** (an **octet**). Most systems **address RAM in bytes** (addresses 0, 1, 2, …). Wider values occupy **several consecutive bytes**; **endianness** fixes the order.

| Typical use | Bits | Bytes | Note |
|-------------|------|-------|------|
| byte / `uint8` | 8 | 1 | smallest common addressable unit |
| half / short (often) | 16 | 2 | still common in media / embedded |
| `int` / `float` (often) | 32 | 4 | classic “word” on 32-bit era |
| pointer / `long` (LP64) | 64 | 8 | typical on **64-bit** desktops/servers |
| cache line (typical) | 512 | 64 | one L1 fill moves a whole line |

**“32-bit vs 64-bit machine”** refers mainly to **GPR width**, **pointer size**, and the **virtual address space** layout the ISA exposes — not to DRAM being “64-bit wide” in the same sense. Arithmetic and pointers usually match the ISA generation; **I/O and caches** still move **lines** and **pages** larger than one byte.

### Different memory, different transfer size
Each layer has its own natural **chunk**:

- **Registers / ALU:** fixed word (e.g. 32 or 64 bits) per operation.
- **Caches:** traffic in **cache lines** (often **64 bytes**), even for a 1-byte load.
- **DRAM:** the controller satisfies requests in patterns aligned to the channel; you still reason in **bytes** at the programming model.
- **Disk / SSD:** persistent storage uses **sectors / pages / blocks** (often **4 KiB** or more per OS page or flash erase/program unit).

So “how big is a read?” depends on **whether** you mean a C `char`, a cache miss fill, or a disk read.

### Instruction sets (ISA) — different CPUs, different languages
The **instruction set architecture** is the hardware’s **machine language**: which operations exist, how they are **encoded as bits**, and how they touch registers and memory. **x86-64** (most PCs), **AArch64** (many phones, Apple silicon), and **RISC-V** (teaching / open cores) are **different ISAs**:

- **Different bit encodings** for “add registers,” “load from memory,” branch, etc.
- **Different register files and rules** (counts, alignment, atomics).
- **Binaries are not interchangeable:** an x86-64 `.exe` will not run natively on AArch64; you need a **rebuild** for the target ISA, a **virtual machine** (JVM, WASM runtime), or **emulation** (slower).

**CISC vs RISC (cartoon level):** x86 historically has **many** instruction shapes and dense encoding; ARM/RISC-V favor **smaller regular** encodings — modern chips often decode everything to **micro-ops** anyway. For programming: **your compiler picks a target** (`x86_64-unknown-linux-gnu`, `aarch64-apple-darwin`, …); the CPU only executes what matches **its** ISA.

- **Why 8 bits per byte?** Convention today; networking and file formats often count bytes.
- **Still built from bytes underneath:** larger moves (cache lines, pages) are multiples of bytes.


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


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 132" role="img" aria-label="Different ISAs produce different machine code bit patterns">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Same intent, different ISA encodings</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">“add A to B” compiles to different bit patterns per target — only matching silicon runs it natively</text>
  <rect x="24" y="56" width="180" height="56" rx="8" fill="rgba(34,197,94,0.1)" stroke="#86efac"/>
  <text x="36" y="78" fill="#e4e4e7" font-size="10" font-weight="600">x86-64</text>
  <text x="36" y="96" fill="#a1a1aa" font-size="9" font-family="ui-monospace">…opcode / ModR/M…</text>
  <rect x="236" y="56" width="180" height="56" rx="8" fill="rgba(96,165,250,0.1)" stroke="#60a5fa"/>
  <text x="248" y="78" fill="#e4e4e7" font-size="10" font-weight="600">AArch64</text>
  <text x="248" y="96" fill="#a1a1aa" font-size="9" font-family="ui-monospace">…fixed 32-bit word…</text>
  <text x="12" y="124" fill="#71717a" font-size="9">toolchain emits ISA-specific object code; OS loader checks format + CPU type</text>
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


## 3. Queues on the memory path
RAM is **not** “one cycle away.” Loads and stores are **requests** that sit in **queues** while the CPU, cache, and DRAM subsystem catch up. That is why throughput can be high even when **latency** to the first byte of a new region is large: hardware **overlaps** many in-flight accesses.

**Inside the CPU (microarchitecture, simplified)**  
- **Load queue:** tracks pending **reads** (addresses waiting for data from the cache hierarchy or beyond). The core can keep executing other instructions while older loads finish.  
- **Store buffer / store queue:** holds pending **writes** (address + value) until they commit in program order to the cache (or merge with later stores to the same line). Stores often **retire** from the program’s point of view before the value is visible everywhere on the machine — that gap matters for **multithreaded** correctness and is why languages expose **atomics** and **memory ordering** rules.

**At the memory controller**  
Many cores and devices share one or more DRAM channels. The **memory controller** keeps **read and write request queues**, then **schedules** them against DRAM timing (banks, rows, refresh). Good scheduling improves bandwidth; bad patterns (random pointer chasing) leave queues full of one-off misses.

**Takeaway for CS101:** when you think “the CPU reads memory,” picture **FIFO-ish queues** of transactions between fast logic and slower DRAM — not a single synchronous read each instruction.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 200" role="img" aria-label="Load and store queues between CPU core and cache memory">
  <defs>
    <marker id="cc-mq-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Queues decouple the core from DRAM latency</text>
  <rect x="24" y="40" width="96" height="48" rx="8" fill="rgba(34,197,94,0.12)" stroke="#86efac" stroke-width="2"/>
  <text x="44" y="62" fill="#e4e4e7" font-size="11">CPU core</text>
  <text x="36" y="78" fill="#a1a1aa" font-size="9">issues loads/stores</text>
  <rect x="24" y="100" width="96" height="28" rx="4" fill="rgba(96,165,250,0.12)" stroke="#60a5fa"/>
  <text x="32" y="118" fill="#e4e4e7" font-size="9">load queue</text>
  <rect x="24" y="134" width="96" height="28" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="30" y="152" fill="#e4e4e7" font-size="9">store buffer</text>
  <path d="M124 114 H168" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-mq-mk)"/>
  <path d="M124 148 H168" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-mq-mk)"/>
  <rect x="172" y="88" width="112" height="72" rx="8" fill="rgba(39,39,42,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="188" y="112" fill="#e4e4e7" font-size="10">L1 / L2 / L3</text>
  <text x="184" y="130" fill="#a1a1aa" font-size="9">cache + coherency</text>
  <text x="184" y="148" fill="#71717a" font-size="8">parallel miss tracking</text>
  <path d="M288 124 H332" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-mq-mk)"/>
  <rect x="336" y="96" width="92" height="56" rx="6" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="348" y="118" fill="#e4e4e7" font-size="10">controller</text>
  <text x="344" y="136" fill="#a1a1aa" font-size="8">read/write Q</text>
  <path d="M382 156 L382 176" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-mq-mk)"/>
  <text x="340" y="192" fill="#71717a" font-size="9">DRAM</text>
  <text x="12" y="188" fill="#71717a" font-size="9">Many pending misses can overlap; ordering rules still constrain what other cores see.</text>
</svg></figure>


## 4. Memory layers (hierarchy)
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


## 5. Virtual memory (one paragraph)
Processes usually see **virtual addresses**; the **MMU** maps them to **physical** RAM frames. That gives isolation (process A cannot touch B’s memory by mistake) and allows **overcommit** (total virtual size can exceed RAM while only active pages sit in physical memory). A **page fault** means the needed page is not in RAM — the OS loads it from disk and resumes your instruction.

## 6. Remember & rehearse
- How many bits in a byte? How many distinct values can one byte represent?
- In one sentence: what is the difference between an **address** and the **contents** at that address?
- Order the layers from smallest/fastest to largest/slowest for a typical laptop.
- Why does the CPU use **queues** for loads and stores instead of blocking until DRAM answers each time?
- Name two different **ISAs** and explain why a binary built for one does not run on the other without recompilation or emulation.
