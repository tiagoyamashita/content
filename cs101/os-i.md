---
label: "I"
subtitle: "Machines & memory"
group: "Operating systems"
order: 1
---
Operating systems — Part I
Kernel role, memory layout, execution models, hardware landscape.

## 1. What operating systems do
- Manage hardware (CPU, RAM, disk, devices) on behalf of programs.
- Multiplex: many processes appear to run at once via scheduling.
- Isolate: fault or malicious code in one process must not wipe others.
- Abstract: files, sockets, threads — uniform APIs instead of raw hardware.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 156" role="img" aria-label="Programs sit above the OS, which manages hardware">
  <text x="118" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Where the OS sits</text>
  <rect x="110" y="30" width="200" height="32" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="132" y="50" fill="#e4e4e7" font-size="11">applications & libraries</text>
  <text x="202" y="74" fill="#71717a" font-size="15" aria-hidden="true">↓</text>
  <rect x="88" y="80" width="244" height="32" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="114" y="100" fill="#e4e4e7" font-size="11">operating system (kernel + services)</text>
  <text x="202" y="126" fill="#71717a" font-size="15" aria-hidden="true">↓</text>
  <rect x="48" y="132" width="324" height="14" rx="4" fill="rgba(63,63,70,0.95)" stroke="#71717a"/>
  <text x="96" y="143" fill="#a1a1aa" font-size="10">CPU · memory · storage · I/O devices</text>
</svg></figure>


## 2. Processes & virtual memory
- Process ≈ running program: code + data + kernel bookkeeping (PCB).
- Virtual memory: each process sees its own address space; OS maps to RAM/pages.
- Pages & page tables: translation from virtual → physical; TLB caches lookups.
- Demand paging & swapping when RAM pressure — slower but larger logical memory.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 118" role="img" aria-label="Each process has its own virtual address space mapped to physical frames">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Virtual memory per process</text>
  <rect x="16" y="32" width="132" height="56" rx="5" fill="rgba(34,197,94,0.08)" stroke="#86efac"/>
  <text x="44" y="50" fill="#86efac" font-size="10" font-weight="600">process A</text>
  <text x="28" y="68" fill="#a1a1aa" font-size="9">own virtual addresses</text>
  <rect x="172" y="32" width="132" height="56" rx="5" fill="rgba(96,165,250,0.08)" stroke="#60a5fa"/>
  <text x="200" y="50" fill="#93c5fd" font-size="10" font-weight="600">process B</text>
  <text x="184" y="68" fill="#a1a1aa" font-size="9">own virtual addresses</text>
  <text x="312" y="52" fill="#71717a" font-size="9">MMU + page tables map each</text>
  <text x="312" y="66" fill="#71717a" font-size="9">virtual page → physical frame.</text>
  <rect x="16" y="96" width="408" height="14" rx="3" fill="#27272a" stroke="#3f3f46"/>
  <text x="72" y="106" fill="#a1a1aa" font-size="9">physical RAM — frames shared under OS control; processes stay isolated</text>
</svg></figure>


## 3. Stack, heap & address space
- Typical layout: text (code), data/bss (globals), heap ↑, stack ↓, kernel reserved.
- Stack: automatic locals, call/return — LIFO, fixed policy; overflow = crash risk.
- Heap: malloc/new — explicit lifetime; allocator metadata + fragmentation concerns.
- Same words "stack/heap" as in CS101 — here tied to the OS loader & libc/runtime.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200" role="img" aria-label="Address space layout with stack and heap growing toward each other">
  <text x="100" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Typical user address space</text>
  <rect x="100" y="32" width="160" height="160" rx="4" fill="none" stroke="#52525b" stroke-width="2"/>
  <text x="112" y="50" fill="#a1a1aa" font-size="10">high addresses ↑</text>
  <rect x="108" y="56" width="144" height="28" rx="3" fill="rgba(244,63,94,0.12)" stroke="#f87171"/>
  <text x="130" y="74" fill="#fecaca" font-size="10">stack (grows down)</text>
  <text x="162" y="100" fill="#71717a" font-size="18" aria-hidden="true">↕</text>
  <text x="108" y="124" fill="#71717a" font-size="9">heap grows up · stack grows down</text>
  <rect x="108" y="134" width="144" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="130" y="152" fill="#bbf7d0" font-size="10">heap (grows up)</text>
  <text x="112" y="178" fill="#a1a1aa" font-size="10">low addresses</text>
  <text x="268" y="90" fill="#71717a" font-size="9">text (code) &</text>
  <text x="268" y="102" fill="#71717a" font-size="9">data/bss sit</text>
  <text x="268" y="114" fill="#71717a" font-size="9">between (not drawn)</text>
</svg></figure>


## 4. Machine code, bytecode & VMs
- Native: ISA machine instructions executed directly by CPU (x86-64, AArch64, …).
- Bytecode: portable IR for a VM (JVM .class, CIL/.NET, Python .pyc-style caches).
- JIT compiles hot bytecode to native at runtime (tiered optimization).
- OS still schedules the process/thread; the VM is user-space code using memory & syscalls.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 100" role="img" aria-label="Bytecode runs in a virtual machine, optionally JIT compiled to native code">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Native vs managed execution</text>
  <rect x="24" y="36" width="100" height="28" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="36" y="54" fill="#e4e4e7" font-size="10">.exe / ELF</text>
  <text x="136" y="52" fill="#a1a1aa" font-size="14">→</text>
  <rect x="160" y="36" width="100" height="28" rx="4" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="170" y="54" fill="#e4e4e7" font-size="10">CPU (native)</text>
  <rect x="24" y="68" width="100" height="28" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="40" y="86" fill="#e4e4e7" font-size="10">.class / IL</text>
  <text x="136" y="84" fill="#a1a1aa" font-size="14">→</text>
  <rect x="160" y="68" width="52" height="28" rx="4" fill="rgba(96,165,250,0.12)" stroke="#60a5fa"/>
  <text x="166" y="86" fill="#e4e4e7" font-size="9">VM</text>
  <text x="220" y="84" fill="#a1a1aa" font-size="14">→</text>
  <rect x="244" y="68" width="80" height="28" rx="4" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="252" y="86" fill="#e4e4e7" font-size="9">JIT → CPU</text>
  <text x="340" y="56" fill="#71717a" font-size="9">direct ISA</text>
  <text x="332" y="86" fill="#71717a" font-size="9">runtime + syscalls</text>
</svg></figure>


## 5. CPUs, ISAs & vendors
- ISA = instruction set architecture (what the software is allowed to assume).
- Microarchitecture = how a vendor implements that ISA (pipelines, caches, cores).
- x86-64: dominant on PCs — Intel & AMD as licensees/designers; backward compatibility legacy.
- Arm: phones, tablets, many servers; Apple M-series — Arm-compatible, custom Apple Silicon.
- RISC-V: open ISA — many vendors; growing in embedded & accelerators.
- Learn one ISA’s manual skim + one OS chapter on context switch — enough orientation.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 112" role="img" aria-label="Same ISA, different CPU vendors and microarchitectures">
  <text x="60" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">ISA vs chip designers</text>
  <rect x="140" y="32" width="140" height="36" rx="6" fill="rgba(34,197,94,0.1)" stroke="#86efac" stroke-width="2"/>
  <text x="166" y="54" fill="#e4e4e7" font-size="11">ISA (contract)</text>
  <text x="146" y="86" fill="#a1a1aa" font-size="10">x86-64 · AArch64 · RISC-V …</text>
  <path d="M100 50 L130 50 M290 50 L320 50" stroke="#71717a"/>
  <rect x="24" y="38" width="76" height="52" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="34" y="58" fill="#e4e4e7" font-size="9">vendor A</text>
  <text x="32" y="76" fill="#a1a1aa" font-size="8">µarch / cores</text>
  <rect x="320" y="38" width="76" height="52" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="330" y="58" fill="#e4e4e7" font-size="9">vendor B</text>
  <text x="328" y="76" fill="#a1a1aa" font-size="8">µarch / caches</text>
  <text x="88" y="104" fill="#71717a" font-size="9">many implementations of the same instruction set</text>
</svg></figure>


## 6. Kernel vs user & system calls
- User mode: cannot touch devices or page tables directly — traps on privilege violation.
- Kernel mode: full machine; handles interrupts, schedules, implements syscalls.
- System call: controlled gateway (read, write, mmap, fork, …) — parameter validation matters.
- Context switch: save registers + switch page tables + pick next runnable thread.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 124" role="img" aria-label="User mode calls into the kernel via a system call trap">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">User mode vs kernel mode</text>
  <rect x="40" y="36" width="160" height="44" rx="6" fill="rgba(96,165,250,0.1)" stroke="#60a5fa"/>
  <text x="72" y="58" fill="#e4e4e7" font-size="11">user mode</text>
  <text x="52" y="74" fill="#a1a1aa" font-size="9">apps · limited privileges</text>
  <rect x="220" y="36" width="160" height="44" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="242" y="58" fill="#e4e4e7" font-size="11">kernel mode</text>
  <text x="232" y="74" fill="#a1a1aa" font-size="9">devices · page tables · schedule</text>
  <path d="M200 58 H216" stroke="#fbbf24" stroke-width="3"/>
  <polygon points="216,52 228,58 216,64" fill="#fbbf24"/>
  <text x="96" y="100" fill="#fbbf24" font-size="10" font-weight="600">syscall / trap</text>
  <text x="180" y="100" fill="#71717a" font-size="9">controlled entry — validate args, then run kernel code</text>
  <text x="88" y="118" fill="#71717a" font-size="9">return to user when done</text>
</svg></figure>


## 7. Remember & rehearse
- Draw a process address space with stack/heap growth arrows.
- Explain one difference: bytecode on JVM vs native ELF on Linux.
- Name two CPU vendors and which ISA families they are known for (today).
