---
label: "III"
subtitle: "Learn with Ziglings"
group: "Zig"
groupOrder: 1
order: 3
---
Zig — Part III: Learn with Ziglings
**[Ziglings](https://github.com/ratfactor/ziglings)** is a hands-on exercise track: small broken programs you fix until **`zig build`** and tests pass. Use it **alongside** these notes and the **[Zig Language Reference](https://ziglang.org/documentation/master/)** — typing fixes beats reading alone.

## 1. What Ziglings is

| | |
|---|---|
| **Format** | Many tiny exercises under **`exercises/`** grouped by topic |
| **Your job** | Fix compile errors, satisfy **`test`** blocks, read hints in comments |
| **Tool** | **`build.zig`** steps per exercise — **`zig build -Dn=n`** style workflow (see repo README) |
| **Goal** | Muscle memory for **optionals**, **error unions**, **slices**, **pointers**, **comptime**, and **`defer`** |

Ziglings does **not** replace Part I–II or the official docs — it **reinforces** them. After Part I (syntax + errors) and skimming Part II (**`zig build`**), you are ready to start.

## 2. Prerequisites

1. **Zig toolchain** — [ziglang.org/download](https://ziglang.org/download/) (match the version Ziglings expects — check their README).
2. **`zig build`** works in a fresh **`zig init`** project.
3. **Editor** — [Zig language support](https://ziglang.org/learn/getting-started/#editors) (Zig extension in VS Code, or **ZLS** in other editors) for inline errors.

```text
zig version
```

## 3. Clone and run

```text
git clone https://github.com/ratfactor/ziglings.git
cd ziglings
zig build
```

Follow the repository’s **README** for the exact step names — typically you run exercises in order and the build script tells you what to fix next.

If **`zig build`** fails immediately, your **Zig version** may not match the branch — switch Ziglings branch/tag or install the Zig version they document.

## 4. How a session works

1. Open the **current exercise** file under **`exercises/`**.
2. Run the suggested **`zig build`** step (or **`zig test`** on that file if the README says so).
3. Read the compiler message — Zig errors often include **notes** pointing at the fix.
4. Save and re-run until the step passes; move to the next exercise.

Tips:

- Read the **comment block** at the top of each exercise — Ziglings encodes the lesson there.
- When stuck for more than ~15 minutes, read the **next** exercise’s comments only as a last resort (or check **solutions** branch if the repo provides one).
- Keep **[Part I](i-basics-and-toolchain.md)** open for **`?T`**, **`!T`**, and slice syntax.

## 5. What you’ll practice (and where we covered it)

| Ziglings area (typical) | Reinforces |
|-------------------------|------------|
| Variables, types, **`const`/`var`** | Part I — program shape |
| **`if`**, **`while`**, **`for`** | Part I — control flow |
| **Optionals** **`?T`**, **`orelse`** | Part I — optionals |
| **Error unions** **`try`**, **`catch`** | Part I — errors |
| **Slices**, strings | Part I — slices |
| **Pointers**, **`struct`**, **`enum`** | Part I — organization |
| **Allocators**, **`ArrayList`** | Part III → **Part IV** |
| **Comptime** | Part IV — comptime |
| **`defer`**, errdefer | Part I + Part IV |

When an exercise touches **`build.zig`**, cross-check **Part II** [Build system & packages](ii-build-system-and-packages.md).

## 6. Suggested study order

```text
Part I (this track)     →  syntax, errors, optionals, defer
       ↓
Ziglings clone          →  short daily blocks, one exercise at a time
       ↓
Language Reference      →  same chapter as the exercise topic
       ↓
Part II (build.zig)     →  when exercises mention modules or steps
       ↓
Part IV (memory)        →  when allocators appear
       ↓
Your own `zig init`     →  tiny CLI or parser from scratch
```

Offline reference while practicing: save the **Language Reference** PDF or use **`zig ast-check`** / **`zig fmt`** locally.

## 7. When you’re stuck

1. Re-read the exercise header comments.
2. Compare your Zig version with Ziglings’ required version.
3. Search [Ziglings issues](https://github.com/ratfactor/ziglings/issues) and [Zig Community](https://ziglang.org/community/).
4. Read the matching section in the [Language Reference](https://ziglang.org/documentation/master/) — Ziglings tracks the language, not a separate dialect.

Do **not** skip exercises permanently because they feel hard — note the topic and return after **Part IV** if allocators or **comptime** were the blocker.

## 8. After Ziglings

- Build a small **`zig init`** project (CLI args parser, file filter, socket echo).
- Read **Part II** again when adding a **`build.zig.zon`** dependency.
- Read **Part IV** before writing libraries that allocate on behalf of callers.
- Explore **[zig.guide](https://zig.guide/)** for narrative tutorials that complement Ziglings.

## 9. Related

- [github.com/ratfactor/ziglings](https://github.com/ratfactor/ziglings) — source and instructions
- **Part I** — [Basics & toolchain](i-basics-and-toolchain.md)
- **Part II** — [Build system & packages](ii-build-system-and-packages.md)
- **Part IV** — [Memory, comptime & C interop](iv-memory-comptime-and-c-interop.md)
- [Zig Language Reference](https://ziglang.org/documentation/master/)
