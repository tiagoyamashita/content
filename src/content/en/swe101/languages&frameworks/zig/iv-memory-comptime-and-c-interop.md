---
label: "IV"
subtitle: "Memory, comptime & C interop"
group: "Zig"
groupOrder: 1
order: 4
---
Zig — Part IV: Memory, comptime & C interop
**Explicit allocators**, **`comptime`** generics, and **C ABI** interop — the pieces that separate toy Zig from shippable systems code. Assumes **Part I** (pointers, slices, errors) and **`zig build`** (**Part II**).

## 1. Memory model (no hidden heap)

Zig has **no garbage collector** and **no global allocator** in the language. Any heap use goes through an **`std.mem.Allocator`** passed into functions that allocate.

| Idea | Zig approach |
|------|----------------|
| Who allocates? | Caller provides **`Allocator`** (or stack-only data) |
| Who frees? | Usually the same code path that allocated, often via **`defer`** |
| Stack | **`var x: T = ...`** — automatic |
| Heap | **`allocator.create`**, **`ArrayList`**, **`ArenaAllocator`**, etc. |

```zig
const std = @import("std");

pub fn duplicateGreeting(allocator: std.mem.Allocator, name: []const u8) ![]u8 {
    const msg = try std.fmt.allocPrint(allocator, "Hello, {s}!", .{name});
    return msg; // caller must `allocator.free(msg)` when done
}

pub fn useIt(allocator: std.mem.Allocator) !void {
    const msg = try duplicateGreeting(allocator, "Zig");
    defer allocator.free(msg);
    std.debug.print("{s}\n", .{msg});
}
```

**Library rule:** If your function returns allocated memory, **document** who frees it. Prefer **`defer`** in the caller right after **`try`**.

### `errdefer` — cleanup on error paths only

```zig
fn load(allocator: std.mem.Allocator) ![]u8 {
    const buf = try allocator.alloc(u8, 1024);
    errdefer allocator.free(buf);

    // if a later `try` fails, `buf` is freed; on success, caller owns `buf`
    try fill(buf);
    return buf;
}
```

### Common allocators

| Allocator | Use |
|-----------|-----|
| **`GeneralPurposeAllocator`** | Dev / general heap (detect leaks in **`.safety = true`** mode) |
| **`ArenaAllocator`** | Many allocs, one **`deinit`** frees all |
| **`FixedBufferAllocator`** | Stack buffer backing small temp allocs |
| **`page_allocator`** | Rare direct use; backing for GPA |

```zig
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
defer _ = gpa.deinit();
const allocator = gpa.allocator();
```

### `ArrayList` pattern

```zig
var list = std.ArrayList(u8).init(allocator);
defer list.deinit();

try list.appendSlice("hello");
try list.append('!');
const slice = try list.toOwnedSlice(); // transfers ownership — caller frees
defer allocator.free(slice);
```

## 2. Pointers — safety is your discipline

Zig does **not** have Rust’s borrow checker. **Optional pointers** **`?*T`**, alignment, and **sentinel-terminated** slices encode some invariants; everything else is on you.

| Type | Meaning |
|------|---------|
| **`*T`** | Single-item pointer — may be null only if **`?*T`** |
| **`[*]T`** | Many-item pointer (unknown length) |
| **`[]T`** | Slice (ptr + len) — preferred for buffers |
| **`align(n) *T`** | Aligned pointer for SIMD / FFI |

Avoid **use-after-free**: don’t return **`[]const u8`** pointing into memory you **`free`** in the same function unless you document a **caller-owned** buffer.

## 3. Comptime — generics without templates

**`comptime`** values and parameters run at **compile time**. Type parameters are **`comptime T: type`**.

### Generic function

```zig
const std = @import("std");

fn min(comptime T: type, a: T, b: T) T {
    return if (a < b) a else b;
}

test "min u32" {
    try std.testing.expectEqual(@as(u32, 3), min(u32, 3, 9));
}
```

### `comptime` blocks and reflection

```zig
const std = @import("std");

fn StructFields(comptime T: type) void {
    @setEvalBranchQuota(10_000);
    inline for (std.meta.fields(T)) |field| {
        @compileLog(field.name);
    }
}
```

**`@compileLog`** prints at compile time (shows in **`zig build`** output). **`inline for`** unrolls over **comptime-known** arrays (e.g. struct fields).

### Type-driven APIs

```zig
fn readInt(comptime T: type, bytes: []const u8) T {
    return std.mem.readInt(T, bytes[0..@sizeOf(T)], .little);
}
```

Use **comptime** for **zero-cost** abstractions — no runtime vtables unless you choose **`anytype`** / function pointers.

### `anytype` — defer type checking to call site

```zig
const std = @import("std");

fn printValue(value: anytype) void {
    const T = @TypeOf(value);
    if (T == []const u8) {
        std.debug.print("{s}\n", .{value});
    } else {
        std.debug.print("{any}\n", .{value});
    }
}
```

Prefer **`comptime T: type`** when you want **explicit** generics; **`anytype`** when duck-typing keeps call sites short.

## 4. C interop

Zig targets **C ABI** cleanly — call C from Zig and export Zig for C.

### Import C headers — `@cImport`

```zig
const c = @cImport({
    @cInclude("stdio.h");
});

pub fn main() void {
    _ = c.printf("from C\n");
}
```

Linking may require **`exe.linkLibC()`** in **`build.zig`** and correct include paths on the host.

### Export Zig for C

```zig
export fn zig_add(a: i32, b: i32) i32 {
    return a + b;
}
```

Build a **shared library** (**`addSharedLibrary`**) and declare **`export`** functions with C-compatible types (**`i32`**, **`*u8`**, etc.).

### `zig cc` — portable C compiler

```text
zig cc -o hello hello.c
```

Useful for building native deps with the **same target** as your Zig binary when cross-compiling.

## 5. Concurrency (today)

Zig **does not** ship **`async`/`await`** in the language (unlike Rust’s **`async fn`**). Concurrent I/O and CPU work use:

| Approach | When |
|----------|------|
| **OS threads** — **`std.Thread`** | Parallel CPU, blocking I/O in thread pool |
| **Blocking I/O** in threads | Simple servers and tools |
| **Event loops** (libraries) | Advanced networking — ecosystem evolves |

**Do not** assume Rust-style async runtimes — check current library docs (**`std.net`**, community servers) for your Zig version.

```zig
const std = @import("std");

const thread = try std.Thread.spawn(.{}, worker, .{value});
thread.join();
```

Keep **shared state** behind **mutexes** or **channels** (**`std.Thread.Mutex`**, **`std.Thread.Condition`**) — same discipline as C/C++.

## 6. Problems that arise (and fixes)

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Leak reported by GPA | Missing **`free`** / **`deinit`** | **`defer`** after every successful alloc |
| Double free | **`defer`** + transfer ownership | One owner — use **`toOwnedSlice`** semantics carefully |
| Slice points to stack | Returning local **`[]const u8`** | Allocate or require caller buffer |
| `error.OutOfMemory` | No heap left | Propagate with **`try`**; use arena for batch work |
| C link undefined symbol | Wrong lib / missing **`linkLibC`** | **`build.zig`** link lines, **`zig build`** summary |
| Comptime explosion | Huge **`inline for`** | Raise **`@setEvalBranchQuota`** or reduce metaprogramming |

## 7. When to choose Zig

**Good fit:**

- CLI tools, parsers, codecs, game engines, embedded-adjacent code
- Replacing C with **safer** errors and **`defer`**, keeping **C ABI**
- Cross-compiling one codebase to many targets from a single dev machine

**Consider something else:**

- Team needs mature **async web** ecosystem today → Rust, Go, or JVM may be faster to ship
- Heavy numeric / ML stacks → Python, Julia, or C++ libraries
- Maximum hiring pool for one language → Java, JavaScript, Python

## 8. Learning path

1. **Part I** + **Ziglings** — syntax and errors under your fingers.
2. **Part II** — real **`build.zig`** with a dependency.
3. **This part** — rewrite one function to take **`Allocator`**, add **`@cImport`** for a tiny C lib.
4. Read **[Zig guide — memory](https://zig.guide/)** and official **FFI** docs for your version.

## 9. Related

- **Part I** — [Basics & toolchain](i-basics-and-toolchain.md)
- **Part II** — [Build system & packages](ii-build-system-and-packages.md)
- **Part III** — [Learn with Ziglings](iii-learn-with-ziglings.md)
- **Part V** — full MVC layout, folder map, logging UML [Web MVC project layout](v-mvc.md)
- **Part VI** — TLS, reverse proxy, deployment [TLS & deployment](vi-tls-and-deployment.md)
- [Zig Language Reference — C](https://ziglang.org/documentation/master/#C)
- [zig.guide](https://zig.guide/) — community tutorials
