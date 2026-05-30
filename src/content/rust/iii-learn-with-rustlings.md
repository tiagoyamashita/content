---
label: "III"
subtitle: "Learn with Rustlings"
group: "Rust"
groupOrder: 1
order: 3
---
Rust — Part III: Learn with Rustlings
**[Rustlings](https://rustlings.rust-lang.org/)** is the official hands-on exercise track: small broken programs you fix until they compile and tests pass. Use it **alongside** these notes and [The Rust Programming Language](https://doc.rust-lang.org/book/) book — reading alone is slower than typing and breaking things on purpose.

## 1. What Rustlings is

| | |
|---|---|
| **Format** | Dozens of tiny exercises under `exercises/` grouped by topic |
| **Your job** | Find **`TODO`** / **`todo!()`**, edit the file, make **`cargo`** happy |
| **Tool** | The **`rustlings`** CLI walks you through exercises in a sensible order |
| **Goal** | Muscle memory for **`struct`**, **`impl`**, **`match`**, ownership, iterators, and more |

Rustlings does **not** replace Part I–II or the Book — it **reinforces** them. After Part I (organization + ownership) and Part II (**`cargo`**), you are ready to start.

## 2. Prerequisites

1. **Rust toolchain** — [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install) (`rustup`, `cargo`, `rustc`).
2. **`cargo build` works** on your machine — on **Windows**, install **MSVC C++ Build Tools** first (see **Part I**, §1).
3. **Editor** — [rust-analyzer](https://rust-analyzer.github.io/) in VS Code (or any editor that supports it) so errors show inline.

Update before installing Rustlings:

```text
rustup update
```

## 3. Install and initialize

From any directory where you want the exercise folder:

```text
cargo install rustlings
rustlings init
cd rustlings
rustlings
```

If install fails, try:

```text
cargo install rustlings --locked
```

**`rustlings` not found?** Cargo puts binaries in **`~/.cargo/bin`** (Linux/macOS) or **`%USERPROFILE%\.cargo\bin`** (Windows). Add that directory to your **PATH**, then open a **new** terminal.

On **Windows**, use **[Windows Terminal](https://aka.ms/terminal)** for the best watch-mode experience (including **WSL** if you use it).

## 4. How a session works

1. **`rustlings`** starts **watch mode** — it runs the current exercise and re-runs when you save the file under **`exercises/`**.
2. Read the compiler error, edit the exercise file, save again.
3. When the exercise passes, Rustlings advances to the next one.

Useful keys in watch mode:

| Key | Action |
|-----|--------|
| **`h`** | Hint for the current exercise |
| **`l`** | Interactive **exercise list** (done vs pending, jump, reset) |
| **`r`** | Re-run current exercise (also used when **`--manual-run`** is set) |

If file watching fails (some VMs/containers), use:

```text
rustlings --manual-run
```

Then press **`r`** after each save.

Each topic folder has a **`README.md`** with links — skim it before diving into that section’s exercises.

## 5. What you’ll practice (and where we covered it)

| Rustlings area (typical) | Reinforces |
|--------------------------|------------|
| Variables, functions | Part I — program shape |
| **`struct`**, **`enum`**, **`match`** | Part I — organization |
| Ownership, borrowing, slices | Part I — ownership |
| **`struct`/`enum` methods**, modules | Part I — **`impl`**, modules |
| Collections, **`String`** | Book ch. 8 + exercises |
| Error handling **`Result`** | Part I — **`Result`**, Book ch. 9 |
| Generics, **`trait`**, lifetimes | Book ch. 10–11 (go deeper after basics) |
| Tests, **`clippy`**, **`macro`s** | Part II — **`cargo test`**, quality habits |

When an exercise mentions **crates** or **`Cargo.toml`**, cross-check **Part II** (`ii-cargo-and-shareable-crates.md`).

## 6. Suggested study order

```text
Part I (this track)     →  skim organization + ownership
       ↓
rustlings init          →  run `rustlings` daily in short blocks
       ↓
The Book (in parallel)  →  same chapters as the exercise topic
       ↓
Part II (Cargo)         →  when exercises touch modules / deps
       ↓
Your own `cargo new`    →  tiny bin + lib project from scratch
```

**Offline docs** while practicing:

```text
rustup doc --book
rustup doc --std
```

## 7. When you’re stuck

1. Press **`h`** in watch mode for a built-in hint.
2. Re-read the topic **`README.md`** inside that **`exercises/...`** folder.
3. Search [Rustlings Q&A discussions](https://github.com/rust-lang/rustlings/discussions/categories/q-a).
4. Compare with [Rust Book](https://doc.rust-lang.org/book/) chapter for that topic — Rustlings is designed to run **in parallel**, not instead of the Book.

Do **not** skip exercises permanently because they feel hard — use **`l`** to jump ahead and come back; use **`r`** in the list to reset an exercise if you want a clean file.

## 8. After Rustlings

- Build a small **`cargo new`** project (CLI tool, parser, game loop).
- Read **Part II** again when publishing or splitting a **workspace**.
- Contribute to an open-source Rust crate or add a [community exercise](https://rustlings.rust-lang.org/community-exercises/) if you want to teach others.

## 9. Related

- [rustlings.rust-lang.org](https://rustlings.rust-lang.org/) — setup, usage, demo
- [github.com/rust-lang/rustlings](https://github.com/rust-lang/rustlings) — source and issues
- **Part I** — `i-basics-and-toolchain.md`
- **Part II** — `ii-cargo-and-shareable-crates.md`
- **Part IV** — async, pitfalls, Tokio (`iv-async.md`)
- [The Rust Book](https://doc.rust-lang.org/book/)
