---
label: "I"
subtitle: "Basics & toolchain"
group: "Zig"
groupOrder: 1
order: 1
---
Zig — Part I
How Zig **organizes** code (**`struct`**, **`enum`**, **`union`**, **`fn`**), the **`zig`** CLI, **error unions** and **optionals**, **slices** and **strings**, and **`defer`** so later notes share a baseline.

## 1. Toolchain & the `zig` CLI

- **[ziglang.org/download](https://ziglang.org/download/)** — one archive per OS; no separate package manager required for the compiler itself.
- **`zig`** compiles, runs, tests, formats, and can act as a **C/C++ cross-compiler** (`zig cc`, `zig c++`).
- **`zig init`** scaffolds a project with **`build.zig`** and **`src/main.zig`** (see **Part II**).

```text
zig init
zig build run
zig build test
zig fmt src/
```

| Command | Role |
|---------|------|
| **`zig build`** | Compile via **`build.zig`** (default workflow) |
| **`zig build run`** | Build and run the default executable |
| **`zig build test`** | Run unit tests |
| **`zig run file.zig`** | Quick one-off script (no project) |
| **`zig test file.zig`** | Test a single file |
| **`zig fmt`** | Format source |
| **`zig version`** | Compiler version |

### Windows notes

Zig ships **LLVM**, **linker**, and **libc** integration — you do **not** need MSVC Build Tools for most Zig-only projects the way Rust often does. If you link against **native C libraries** built with MSVC, match ABIs and use **`zig build`** with the right **target** / **libc** options.

Open a **new terminal** after adding **`zig`** to **PATH**. **[Windows Terminal](https://aka.ms/terminal)** works well for long **`zig build`** output.

## 2. How Zig code is organized

Zig favors **explicit, readable control flow** — no hidden allocations, no exceptions, no preprocessor macros. Generics are **comptime** (compile-time), not a separate template language.

### Big picture: file → module

```text
my_project/
  build.zig           ← build script (Part II)
  build.zig.zon       ← optional package manifest
  src/
    main.zig          ← entry (or root for a library)
    parser.zig        ← another file in the same module
```

| Layer | What it is | Rough analogy |
|-------|------------|---------------|
| **Module** | One `.zig` file = one module; **`@import`** pulls in other files | Java **`package`** / Rust **`mod`** |
| **Struct** | Plain data + methods via namespaced functions | **`struct`** + free functions, or Rust **`struct`** + **`impl`** |
| **File scope** | Top-level **`const`**, **`var`**, **`fn`**, **`test`** | Same idea as most languages |

Unlike Rust’s crate graph, a small Zig app is often **one module** split across files with **`@import("parser.zig")`**.

### `struct` — fields and methods

```zig
const User = struct {
    id: u64,
    name: []const u8,
    active: bool,

    pub fn displayName(self: User) []const u8 {
        return self.name;
    }

    pub fn deactivate(self: *User) void {
        self.active = false;
    }
};
```

- Methods are **`pub fn`** inside the **`struct`** body — no separate **`impl`** block.
- **`self: User`** passes by value; **`self: *User`** is a mutable pointer (like **`&mut self`**).
- String data is usually **`[]const u8`** (UTF-8 bytes) — not a special **`String`** type.

### `enum` and `union` — tagged and untagged variants

**`enum`** — fixed set of named constants; can carry payloads:

```zig
const OrderStatus = enum {
    draft,
    paid,
    shipped,
    cancelled,
};

const Message = union(enum) {
    text: []const u8,
    count: u32,
    quit,
};
```

**`union(enum)`** is a **tagged union** (safe **`switch`** on the tag). Plain **`union`** requires you to track the active field yourself — rare in application code.

### Optionals — `?T`

**`?T`** means “maybe **`T`**” — like Rust **`Option<T>`** or Java **`Optional`**.

```zig
const std = @import("std");

fn findUser(id: u64) ?User {
    if (id == 1) return User{ .id = 1, .name = "Ada", .active = true };
    return null;
}

fn greet(name: ?[]const u8) void {
    if (name) |n| {
        std.debug.print("Hello, {s}\n", .{n});
    } else {
        std.debug.print("Hello, world\n");
    }
}
```

**`if (x) |bound|`** unwraps a non-null optional into **`bound`**.

### Error unions — `!T`

Zig errors are **typed error sets**, not exceptions. **`!T`** means “returns **`T`** or an error” — like Rust **`Result<T, E>`** but **`E`** is a compile-time **set of error names**.

```zig
const std = @import("std");

const ParseError = error{
    InvalidDigit,
    Empty,
};

fn parseU8(s: []const u8) ParseError!u8 {
    if (s.len == 0) return ParseError.Empty;
    const n = std.fmt.parseInt(u8, s, 10) catch return ParseError.InvalidDigit;
    return n;
}

fn demo() !void {
    const n = try parseU8("42"); // `try` propagates errors upward
    std.debug.print("{d}\n", .{n});
}
```

| Syntax | Meaning |
|--------|---------|
| **`error{Name}`** | One error value in a set |
| **`FooError!T`** | Return **`T`** or any error in set **`FooError`** |
| **`try expr`** | Propagate error to caller (caller must return **`!`** ) |
| **`catch`** | Handle or map errors |
| **`anyerror`** | Any error type (use sparingly at boundaries) |

**No stack unwinding** — errors are **return values** you must **`try`**, **`catch`**, or **`ignore`**.

### Slices and strings

| Type | Meaning |
|------|---------|
| **`[]T`** | Slice — pointer + length (like Rust **`&[T]`**) |
| **`[]const u8`** | Read-only UTF-8 string slice |
| **`*[N]T`** | Pointer to N elements |
| **`*T`** | Single-item pointer |

```zig
const label: []const u8 = "hello";
const nums = [_]i32{ 1, 2, 3 };
const slice: []const i32 = nums[0..];
```

Literals like **`"hi"`** are **`*const [2:0]u8`** (pointer to null-terminated array) — coerce to **`[]const u8`** as needed.

### `defer` — scoped cleanup

**`defer`** runs when the current scope exits (success, **`return`**, or **`err`** path).

```zig
const std = @import("std");

fn process(allocator: std.mem.Allocator) !void {
    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit();

    try list.append('x');
    // `list.deinit()` runs here automatically
}
```

Pair **`defer`** with explicit **allocators** (Part III).

## 3. Program shape

```zig
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}\n", .{"Zig"});
}

fn double(x: i32) i32 {
    return x * 2;
}
```

- **`pub fn main() !void`** — **`main`** may return errors (e.g. stdout failures).
- **`const`** — immutable binding; **`var`** — mutable.
- **`try`** in **`main`** only works if **`main`** returns **`!void`** (or you handle errors yourself).

## 4. `switch` — exhaustive control flow

**`switch`** on integers, enums, and error unions must cover **all** cases (or use **`else`** where allowed).

```zig
fn orderLabel(status: OrderStatus) []const u8 {
    return switch (status) {
        .draft => "draft",
        .paid => "paid",
        .shipped => "shipped",
        .cancelled => "cancelled",
    };
}
```

For **`?T`** and **`!T`**, **`if`** / **`try`** / **`catch`** are usually clearer than overusing **`switch`**.

## 5. Comptime preview

**`comptime`** runs at compile time — constants, type-level logic, and generics without a separate macro language.

```zig
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

const x = max(u32, 10, 20); // `20` computed at compile time if args are comptime-known
```

**Part IV** goes deeper on **comptime** and **C interop**.

## 6. Testing in the same file

```zig
const std = @import("std");

test "double works" {
    try std.testing.expectEqual(@as(i32, 42), double(21));
}
```

Run with **`zig test src/main.zig`** or **`zig build test`** in a project.

## 7. Mental map: Rust vs Zig (high level)

```text
Rust                          Zig
────                          ───
struct + impl                 struct { fn methods... }
Result<T, E>                  ErrorSet!T
Option<T>                     ?T
cargo / Cargo.toml            zig build / build.zig (+ build.zig.zon)
ownership + borrow checker    explicit allocators + pointers (no GC)
async/await + runtime         OS threads / I/O (no language async today)
```

## 8. Related

Next: **Part II** — **`build.zig`**, dependencies, workspaces [Build system & packages](ii-build-system-and-packages.md). **Part III** — hands-on **[Ziglings](https://github.com/ratfactor/ziglings)** [Learn with Ziglings](iii-learn-with-ziglings.md). **Part IV** — allocators, **comptime**, **C** [Memory, comptime & C interop](iv-memory-comptime-and-c-interop.md).
